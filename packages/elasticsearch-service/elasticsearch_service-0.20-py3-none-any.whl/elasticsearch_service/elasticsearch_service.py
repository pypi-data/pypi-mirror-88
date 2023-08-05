from elasticsearch import Elasticsearch,RequestsHttpConnection
from elasticsearch import helpers
import ssl
from elasticsearch_dsl import Search, Index
import json
import logging
import pandas as pd

class ElasticsearchService:
    """
    Class designed to ease request to Elasticsearch (extract and import).
    """

    # Logging
    _FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    _logger = None



    def __init__(self, host='localhost', port=9200, **kwargs):
        """
        Constructor.
        :param host: elasticsearch host (eg localhost)
        :param port: elasticsearch port (eg 9200)
        :param kwargs:
        doc_type is different from '_doc' (default value)
        timefield (if needed for requests based on dates)
        """

        # Logging
        logging.basicConfig(format=self._FORMAT, level=logging.WARNING)
        self._logger = logging.getLogger(__name__)
        logging.getLogger(__name__).setLevel(logging.INFO)

        self.host=host
        self.port=port
        user=kwargs.get('http_auth_username')
        passwd=kwargs.get('http_auth_password')
        with_authent = (user!= None) and (passwd!= None)
        if kwargs.get('doc_type'):
            self.doc_type = kwargs.get('doc_type')
        else:
            self.doc_type = '_doc'
        if (with_authent): # ajout parametre extra (authent http basic)
            self._logger.info("log with auth")
            self.scheme=kwargs.get('scheme')
            if self.scheme=='https':
                self.es = Elasticsearch(hosts=[self.host], port=self.port
                                    ,http_auth = (user,
                                     passwd),
                                    verify_certs=False,
                                    connection_class=RequestsHttpConnection,
                                    scheme=self.scheme)
            else:
                self.es = Elasticsearch(hosts=[self.host], port=self.port
                                    ,http_auth = (user,
                                     passwd),
                                    scheme=self.scheme)
        else:
            self.es = Elasticsearch(hosts=[self.host], port=self.port)

        if kwargs.get('timefield'):
            self.timefield = kwargs.get('timefield')

    def getClient(self):
        return self.es
    
    def setDoc_type(self, doc_type):
        self.doc_type = doc_type

    def get_mapping(self, index):
        """
        Returns es index mapping
        :param index: es index
        :return: mapping as returned by elasticsearch-dsl package
        """
        dslIndex = Index(using=self.es, name=index)
        return dslIndex.get_mapping()

    def put_mapping(self, index, mapping_body):
        """
        Put es index mapping
        :param index: es index
        :param mapping_body: mapping body
        :param **kwargs: extra parameters (eg: timeout)
        """
        self.es.indices.put_mapping(index=index, body=mapping_body)
    

    def _build_search(self, index, **kwargs):
        """
        Internal method building the quering with respect to elasticsearch-dsl package.
        :param index: index for search
        :param kwargs: see getDocumentsCount and getDocuments
        :return:
        """
        timeRanged = False #is the query based on a time range ?
        filtered = False # is the query filtered ?
        ranged = False # has the query ranges?
        excluded=False # has must not
        field_to_include=False # has only specific field to include
        wildcard=False

        if kwargs.get('startdate'):
            timeRanged = True
            timefield = kwargs.get('timefield')
            startdate = kwargs.get('startdate')
            if kwargs.get('enddate'):
                enddate = kwargs.get('enddate')
            else:
                enddate = 'now'
        if kwargs.get('filters'):
            filtered = True
            filters = kwargs.get('filters')
        if kwargs.get('exclude'):
            excluded = True
            exclude = kwargs.get('exclude')
        if kwargs.get('ranges'):
            ranged = True
            ranges = kwargs.get('ranges')
        if kwargs.get('field_to_include'):
            field_to_include = True
            fields_to_include = kwargs.get('field_to_include')
        if kwargs.get('wildcard'):
            wildcard=True
            wildcards=kwargs.get('wildcard')

        search = Search(using=self.es, index=index, doc_type=self.doc_type).params(request_timeout=2000)

        if wildcard:
            for wild in wildcards:
                search = search.filter('wildcard', **{wild: wildcards[wild]})
        if excluded:
            for ex in exclude.keys():
                search=search.exclude('terms',**{ex: exclude[ex]})
        if timeRanged:
            if startdate != enddate:
                timeRange = {timefield:{'gte': startdate, 'lt': enddate}}
            else:
                timeRange = {timefield:{'gte': startdate, 'lte': enddate}}
            search = search.filter('range', **timeRange)
        if ranged:
            # ranges are expected in format : [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
            for range_filter in ranges:
                search = search.filter('range', **range_filter)
        if filtered:
            for key in filters.keys():
                search = search.filter('terms', **{key: filters[key]})
        if field_to_include:
            for field in fields_to_include.keys():
                search=search.source( **{field: fields_to_include[field]})

        self._logger.info(json.dumps(search.to_dict()))

        return search


    def get_documents_count(self, index, **kwargs):
        """
        Returns document count in the index according to options
        :param index: index for search
        :param kwargs:
        startdate, timefield, endate : for time ranges, only documents with a date greater than equal to startdate and strictly lower than enddate according to timefield will be requested.
         If startdate is equal to enddate, document from startdate will be requested. Date format is expected to be compliant with elasticsearch (eg 'YYYY-MM-dd')
        ranges : if there is a filter accoring to a numerical field value. Ranges are expected in format : [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        filters : disctionnary with all fields to use for filtering with their expected values in an array : {field:[value1, value2], field2:[value1]}.
        :return:
        number of document in index matching constraints.
        """
        return self._build_search(index, **kwargs).count()

    def get_documents(self, index, **kwargs):
        """
        Returns document  in the index according to options
        :param index: index for search
        :param kwargs:
        startdate, timefield, endate : for time ranges, only documents with a date greater than equal to startdate and strictly lower than enddate according to timefield will be requested.
         If startdate is equal to enddate, document from startdate will be requested. Date format is expected to be compliant with elasticsearch (eg 'YYYY-MM-dd')
        ranges : if there is a filter accoring to a numerical field value. Ranges are expected in format : [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        filters : disctionnary with all fields to use for filtering with their expected values in an array : {field:[value1, value2], field2:[value1]}.
        :return:
        document in index matching constraints as returned by elasticsearch-dsl package (Hits)
        """
        return self._build_search(index, **kwargs).params(request_timeout=2000).scan()

    def get_field_values(self, index, field, **kwargs):
        """
        Returns a dict with all possible values for field in ES and associated count
        :param index: es index
        :param field: field to consider
        :param kwargs:
        :return: dict key=field value, value: count
        """
        search = self._build_search(index, **kwargs)
        search.aggs.bucket('fieldCounts', 'terms', field=field, size=10000)
        fieldValues = {}
        for bucket in search.execute().aggregations.fieldCounts.buckets:
            fieldValues[bucket.key] =  bucket.doc_count
        return fieldValues

    def export_documents(self, index, filename, **kwargs):
        """
        Write documents  from the index according to options into a file
        :param index: index for search
        :param filename: file for data export (including path)
        :param kwargs:
        startdate, timefield, endate : for time ranges, only documents with a date greater than equal to startdate and strictly lower than enddate according to timefield will be requested.
         If startdate is equal to enddate, document from startdate will be requested. Date format is expected to be compliant with elasticsearch (eg 'YYYY-MM-dd')
        ranges : if there is a filter accoring to a numerical field value. Ranges are expected in format : [{field:{'gte':value, 'lte':value}}, {field:{'gte':value}}, {field:{'lte':value}}]
        filters : disctionnary with all fields to use for filtering with their expected values in an array : {field:[value1, value2], field2:[value1]}.
        :return: na
        """
        documentsGenerator = self.get_documents(index, **kwargs)
        documents = []
        format=kwargs.get('format','json')
        for doc in documentsGenerator:
            doc_with_id={**doc.to_dict(),'_id':doc.meta.id}
            documents.append(doc_with_id)
        self.__export_documents(documents,filename,exportformat=format)

    def __export_documents(self,documents,filename,exportformat):
        with open(filename, 'w') as f:
            if exportformat=='csv':
                df = pd.DataFrame(data=documents)
                df.to_csv(filename, encoding='utf-8', sep=';', index=False)
            else:
                f.write(json.dumps(documents))


    def import_documents(self, index, documents, **kwargs):
        """
        Import documents (array of dict) into elasticsearch index
        :param index: elasticsearch index (created if doesn't exist)
        :param documents: array of dict. For updates, each document (dict) must containg a value for key '_id'
        :return: response
        """
        self._logger.info('%s documents to index into %s', len(documents), index)
        response = None
        if 'pipeline' in kwargs:
            pipeline_name = kwargs.get("pipeline")
            response = helpers.bulk(self.es, documents, index=index, doc_type=self.doc_type, pipeline=pipeline_name)
        else:
            response = helpers.bulk(self.es, documents, index=index, doc_type=self.doc_type)
        
        # It returns a tuple with summary information - 
        # number of successfully executed actions and either list of errors or number of errors if stats_only is set to True.
        return response

    def import_documents_from_file(self, index, filename, delimiter=';'):
        """
        Load json data into elasticsearch
        :param index: elasticsearch index (created if doesn't exist)
        :param filename: json or csv file (For updates, each document (dict) must containg a value for key '_id')
        :param delimiter : define delimiter (only for csv files)
        :return: na
        """

        with open(filename, 'r') as f:
            if filename.endswith('.csv'):
                df=pd.read_csv(f, delimiter=delimiter,keep_default_na=False)
                documents=df.to_dict('records')
            elif filename.endswith('.json'):
                documents = json.load(f)
            else:
                raise Exception('File must be .csv or .json')
        helpers.bulk(self.es, documents, index=index, doc_type=self.doc_type)

    def get_allindex_accordingindexwithwildcard(self,indexwithwildcard):
        indexs=self.es.indices.get('*')
        indexwithoutwildcard=indexwithwildcard[:-1]
        return [x for x in indexs if x.startswith(indexwithoutwildcard)]

    def delete_index(self,index_to_delete):
        self.es.indices.delete(index=index_to_delete, ignore=[400, 404])






ElasticSearchService
---------------------


**First install with pip**

    `pip install elasticsearch-service`

To use , simply do::

     from elasticsearch_service import ElasticsearchService

Configure your elk Service with your parameters
###################################################

With no authentification define your host(default='localhost' and  port (default=9200)::

    elk_service=ElasticsearchService() # default localhost and port 9200
           OR (ONLY FOR URL DIFFERENT Of localhost AND PORT IS NOT 9200
    elk_service=ElasticsearchService('myurl',9201)

With HTTP basic authentification host, port and additional informations::

    elk_service=ElasticsearchService('localhost',9200,scheme = 'http',http_auth_username = 'myuser',http_auth_password='mypassword')


To import objects in ELK use :
##############################

elk_service.import_documents(<index_elk>,<list_of_dict>)

where <index_elk> is a string like 'myelk-index'
where <list_of_dict> is a list of dict like [{'id':'id1','field1':'value1,'field1','field2':'value2'},{'id':'id2','field1':'value3,'field2','field2':'value4'}]::

    list_of_values=[{'_id':'myid1','field1':'value1','field2':'value2','date':'2016-07-15T15:29:50+02:00'},{'_id':'myid2','field1':'value33','field2':'value4','date':'2016-07-15T15:29:50+02:00'}]
    elk_service.import_documents('myelk-index',list_of_values)

To search Objects in ELK use :
##############################

elk_service.get_documents(<index>,<parameter>)

        where <index> is a string like 'myelk-index'

        where <parameter> are :
            To Specify a dateField use
                timefield='my_date_field'

                If so, you must specified a start date GREATER OR EQUAL
                   startdate='2020-04-01'
                And a end date LESS than (and not EQUAL)
                   enddate='2020-04-02'

            To Specify your query in a dict format use
                filters={'field1':['value1','valuer2'],'field2:[value]}
            To specify your query you MUST NOT in a dict format use
                exclude={'field1':['value1','valuer2']}
            To specify query with wildcard use
                 {'field1.keyword': 'value*'}
            To get only somme fields use :
                field_to_include={'include':['field1','field2']}

examples ::

    hits=elk_service.get_documents('myelk-index')
    hits=elk_service.get_documents('myelk-index',timefield='date',startdate='2020-04-01',enddate='2020-04-02')
    hits=elk_service.get_documents('myelk-index',filters={'field1':['value1','value3'],'field2':['value4']})
    hits=elk_service.get_documents('myelk-index',filters={'field1':['value1','value3']},wildcard={'field1.keyword':'value3*'})

examples to get values from search (to have hits)::

     for hit in hits:
        # if you want to access to your value in dict format
        values_in_dictformat=hit.to_dict()
        # OR
        # if you want to access to a specific value
        field1=hit.field1


TO Export a document in json(default) or csv file use :
#######################################################

export_documents(<INDEX>,<FILENAME>,<FORMAT>,<PARAMETER>)

        where <INDEX> is the index to export (strings)
        where <FILENAME> is the file name (string)
        where <FORMAT> can be json (default) ou csv
        where <PARAMETER> is the same than method getDocument() see previous7

example::

    elk_service.export_documents('myelk-index','elkdata.json')
    elk_service.export_documents('myelk-index','elkdata.csv',format='csv')

TO Import a json or csv file use :
##################################

import_documents_from_file(<INDEX>,<FILENAME>)
Note that :
for csv file : default delimiter is ;
for json file: must be list of value like [{"id": "id1"},{"id": "id2"}] <br/>


        where <INDEX> is the index to export (strings)
        where <FILENAME> is the file name (string) : can
        where <FORMAT> is the type of file : json (default) or csv

example::

    elk_service.import_documents_from_file('myelk-index1','elkdata.json')
    elk_service.import_documents_from_file('myelk-index2','elkdata.csv') # if delimiter is ;
    elk_service.import_documents_from_file('myelk-index3','elkdata.csv',delimiter=',') # if delimiter is ,

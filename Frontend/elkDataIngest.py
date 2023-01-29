import pandas as pd 
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
from nlpModel import classify
import datetime
def ingestData(name, aspect, feedback):
    elasticUsername  = 'elastic'
    elasticPassword  = 'changeme'
    ## Setup Connection to Elasticsearch
    # es = Elasticsearch("http://localhost:9200", basic_auth=(elasticUsername, elasticPassword))
    es = connections.create_connection(hosts=["http://elastic:"+elasticPassword+"@localhost:9200"], basic_auth=(elasticUsername, elasticPassword))

    # validation
    if not name:
        name = "None"
    
    label = classify(feedback, aspect)

    data = {
        "time_stamp": datetime.datetime.now(),
        "name": name,
        "aspect": aspect,
        "feedback": feedback,
        "label": label
    }
    print(data)

    
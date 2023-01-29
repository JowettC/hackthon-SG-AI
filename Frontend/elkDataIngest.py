import pandas as pd 
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
from nlpModel import classify
import json
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
    if (label == 0):
        label = "negative"
    elif (label == 1):
        label = "positive"
    # timestamp = datetime.datetime.now()
    data = {
        "@timestamp": str(datetime.date.today()),
        "name": name,
        "aspect": aspect,
        "feedback": feedback,
        "label": label
    }
    es.index(index='customer_review_data', document=json.dumps(data))

if __name__ == "__main__":
    ingestData("may", "service", "The service was great")
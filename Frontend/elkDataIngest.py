import pandas as pd 
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
from nlpModel import classify
import json
import datetime

from firestore import db

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
    label = 1
    if (label < 0):
        label = "negative"
    elif (label == 1):
        label = "positive"
    else:
        label = "neutral"
    # timestamp = datetime.datetime.now()
    data = {
        "@timestamp": str(datetime.date.today()),
        "name": name,
        "aspect": aspect,
        "feedback": feedback,
        "label": label
    }

    es.index(index='customer_review_data', document=json.dumps(data))
    print("Data Ingested")

    try:
        ingestIntoFirestore(data)
        # print("Data Ingested into Firestore")
    except(Exception):
        print("Error Ingesting into Firestore")


def ingestIntoFirestore(data):
    coll_ref  = db.collection(u'customer_review_data')
    create_time, doc_ref = coll_ref.add(
        {
            '@timestamp': data['@timestamp'],
            'name': data['name'],
            'aspect': data['aspect'],
            'feedback': data['feedback'],
            'label': data['label']
        }
    )
    print(f"{doc_ref.id} is created at {create_time}")
if __name__ == "__main__":
    ingestData("may", "service", "The service was great")
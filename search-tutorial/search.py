import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch(os.environ['ELASTIC_URL'])  # <-- connection options need to be added here
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self, index):
        self.es.indices.delete(index=index, ignore_unavailable=True)
        self.es.indices.create(index=index)

    def insert_document(self, index, document):
        return self.es.index(index=index, body=document)
    
    def insert_documents(self, index, documents):
        operations = []
        for document in documents:
            operations.append({ 'index': {'_index': index}})
            operations.append(document)
        return self.es.bulk(operations=operations)
      
    def reindex(self, index, file_path):
        with open(file_path, 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(index=index, documents=documents)

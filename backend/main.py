import os
from json import dumps, loads
from src.api import app 
from flask.testing import FlaskClient 

file = open("README.md", "a")


class DOCS:
    def __init__(self, app):
        self.app = app 
        self.client = self.app.test_client()
    
    def get_endpoints(self):
        endpoints = []
        for rule in self.app.url_map.iter_rules():
            endpoint = {
                "endpoint": rule.endpoint,
                "methods": [method for method in rule.methods if method != "HEAD" and method != "OPTIONS"]
            }
            endpoints.append(endpoint)
        return endpoints

    def format(self):
        endpoints = self.get_endpoints() 
        for endp in endpoints:
            if "GET" in endp["methods"]:
                print(endp["endpoint"])
                req = self.client.get(f"/{endp['endpoint']}")
                print(req.data)

doc = DOCS(app)
print(doc.format())
    


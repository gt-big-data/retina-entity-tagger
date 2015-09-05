import json
#import pprint
import requests

def lookup(name):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
              "id": None,
              "query": "atlanta",
              "type": "/location/location",
              "/location/location/containedby": []
            }
    request = requests.get(service_url, params = params)
    response = json.loads(request.text)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(response['result'])
    return response['result']

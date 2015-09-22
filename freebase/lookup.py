import json
import pprint
import requests

def lookup(name):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
              "id": None,
              "query": name,
              "type": "/location/location",
              "/location/location/containedby": []
            }
    request = requests.get(service_url, params = params)
    response = json.loads(request.text)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(response['result'])
    return response['result']

def categorize(name):
  service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
  query = [{"id": None,
    "name": name,
    "type": []}]
  params = {
    'query': json.dumps(query)
  }
  request = requests.get(service_url, params = params)
  response = json.loads(request.text)
  pp = pprint.PrettyPrinter(indent=4)
  #pp.pprint(response['result'][0])
  # print "verify"
  # return response['result'][0]['type']
  # print response['result'][0]['type']
  return indexTypes(response['result'][0]['type'])


def indexTypes(results):
  dictionary = {}
  mostCommonKey = '';
  mostCommonValue = 0;
  for objectType in results:
    #print objectType
    element = objectType.split('/')[1]
    if element == 'base' or  element == 'user' or len(element) == 1:
      objectType = objectType.split('/')[2]
    else:
      objectType = objectType.split('/')[1]
    #print objectType
    if objectType in dictionary.keys():
      dictionary[objectType] += 1
      if mostCommonValue < dictionary[objectType]:
        mostCommonKey = objectType
        mostCommonValue = dictionary[objectType]
    else:
      dictionary[objectType] = 1
      if mostCommonValue < dictionary[objectType]:
        mostCommonKey = objectType
        mostCommonValue = dictionary[objectType]
  return mostCommonKey





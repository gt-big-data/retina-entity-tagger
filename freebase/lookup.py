import json
import pprint
import requests
def getId(name):
  service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
  query = [{"id": None,
    "name": name,
    "type": []}]
  params = {
    'query': json.dumps(query)
  }
  request = requests.get(service_url, params = params)
  response = json.loads(request.text)
  response['result'][0]['id']


def lookup(name):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = [{"id": None,
              "name": name,
              "type": "/location/location",
              "/location/location/containedby": []
            }]
    params = {
    'query': json.dumps(query)
    }
    request = requests.get(service_url, params = params)
    response = json.loads(request.text)
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(response['result'])
    return response['result'][0]["/location/location/containedby"]

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
  # pp.pprint(response['result'][0])
  # print response['result'][0]['type']
  try:
    category = indexTypes(response['result'][0]['type']), response['result'][0]['id']
  except Exception:
    category = None

  return category



def indexTypes(results):
  dictionary = {}
  mostCommonKey = '';
  mostCommonValue = 0;
  for objectType in results:
    # print str(objectType)
    element = objectType.split('/')[1]
    if element == 'base' or len(element) == 1:
      objectType = objectType.split('/')[2]
    elif element == 'user':
      objectType = objectType.split('/')[3]
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

print open("article.json").read()
json_data= json.loads(open("article.json").read())
for entity in json_data[0]['entities']:
  print entity
  print categorize(entity)


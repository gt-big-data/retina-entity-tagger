import json
import urllib

def lookup(name):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
            "id": None,
            "name": name,
            "type": "/location/location",
            "/location/location/contains": []
        }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    return response['result']
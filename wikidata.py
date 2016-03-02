import requests, json, time, multiprocessing
from pprint import pformat
from collections import Counter

global property_dict, _entity_id_cache
property_dict = {"contained": "P131", "wdType": "P31", "capitalOf": "P6", "legislative": "P1", "geolocation": "P625", "industry": "P452"}
inverse_dict = {value: key for key, value in property_dict.items()}
_entity_id_cache = {}

def ask_wikidata(params):
    response = requests.get('http://www.wikidata.org/w/api.php', params=params)
    return json.loads(unicode(response.text))

def findEntity(entityText):
    jsonResult = ask_wikidata({'action': 'wbsearchentities', 'language': 'en', 'format': 'json', 'search': entityText})
    return [item['id'] for item in jsonResult.get('search', []) if 'id' in item]

def populateEntity(wdid, goodProperties=[]):
    goodProperties = ["contained", "wdType", "geolocation", "industry"] if len(goodProperties) == 0 else goodProperties
    jsonResult = ask_wikidata({'action': 'wbgetentities', 'languages': 'en', 'format': 'json', 'ids': wdid})
    f = open(wdid+'.txt', 'w'); f.write(pformat(jsonResult)); f.close();
    entry = jsonResult.get('entities', {}).get(wdid, None)
    if entry == None:
        return None
    build = {'_id': wdid, 'title': getTitle(entry), 'aliases': getAliases(entry)}
    myProperties = getProperties(entry, goodProperties)
    build['type'] = insiderType(myProperties)
    build.update(myProperties)
    return build

def bulkFind(texts):
    global _entity_id_cache
    workers = multiprocessing.Pool(3*multiprocessing.cpu_count())

    unique_entities = set(texts)
    new_entities = unique_entities - set(_entity_id_cache.keys())
    start = time.time()
    print 'Fetching', len(new_entities), 'new entity ids of', len(unique_entities), 'requested'
    id_results = workers.map(findEntity, new_entities)
    workers.close()
    print 'Fetched in ', time.time() - start, 'seconds'
    for new_entity, ids in zip(new_entities, id_results):
        _entity_id_cache[new_entity] = ids[0] if ids else None
    return {text: _entity_id_cache[text] for text in unique_entities}

def bulkPopulate(wdids):
    workers = multiprocessing.Pool(3*multiprocessing.cpu_count())
    results = workers.map(populateEntity, wdids)
    workers.close()
    return results

def getAliases(entityInformation):
    try:
        return [a['value'] for a in entityInformation['aliases']['en']]
    except:
        return None

def getTitle(entityInformation):
    try:
        return entityInformation['labels']['en']['value']
    except:
        return None

def getProperties(jsonObj, props=[]):
    global property_dict
    return {prop: getProperty(jsonObj, property_dict[prop]) for prop in props if getProperty(jsonObj, property_dict[prop])}

def insiderType(properties):
    try:
        if properties['wdType'] == 'Q5':
            return 'human'
        elif properties.get('geolocation', None) is not None:
            return 'loc'
        if properties.get('industry', None) is not None:
            return 'company'
    except:
        return ''

def getProperty(jsonObj, propId):
    try:
        if inverse_dict[propId] == 'geolocation':
            obj = jsonObj['claims'][propId][0]['mainsnak']['datavalue']['value']
            return {'lat': obj['latitude'], 'lon': obj['longitude']}
        else:
            return 'Q'+str(jsonObj['claims'][propId][0]['mainsnak']['datavalue']['value']['numeric-id'])
    except KeyError:
        return None


def getEntityProperties(wdid):
    jsonResult = ask_wikidata({'action': 'wbgetentities', 'languages': 'en', 'format': 'json', 'ids': wdid})
    return jsonResult['entities'][wdid]['claims'].keys()

def getPropertyTitle(wdid):
    jsonResult = ask_wikidata({'action': 'wbgetentities', 'languages': 'en', 'format': 'json', 'ids': wdid})
    return jsonResult['entities'][wdid]['labels']['en']['value']

def propertiesCounts(number_of_entities):
    propList = []
    for i in range(number_of_entities):
        q = 'Q' + str(i)
        try:
            propList.extend(getEntityProperties(q))
        except:
            pass
    return list((x[0], getPropertyTitle(x[0]), x[1]) for x in Counter(propList).most_common())

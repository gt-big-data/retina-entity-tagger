import requests
import pprint
import json
import math
import multiprocessing
import time

# Properties
PROP_CONTAINEDBY = "Contained By"
PROP_INSTANCEOF  = "Instance of"
PROP_HEADOFSTATE = "Head of State"
PROP_LEGISLATIVEBODY = "Legislative Body"
PROP_GEOLOCATION = "GeoLocation"

ID_CONTAINEDBY = "P131"
ID_INSTANCEOF = "P31"
ID_HEADOFSTATE = "P6"
ID_LEGISLATIVEBODY = "P1"
ID_GEOLOCATION = "P625"

def get_with_retry(url, params, tries_remaining=5):
    if tries_remaining == 0:
        return None
    try:
        time.sleep(0.01) # sleep 10 millis to be nice
        return requests.get(url, params=params)
    except Exception, e:
        time.sleep(1.0)
        return get_with_retry(url, params, tries_remaining - 1)

def search_entity(entityText, maxTries=5):
    '''
    Search wikidata for entities described by the text entityText.

    Sample usage:
    TBD

    Parameters:
    - entityText Text to search for an entity match.

    Output:
    If there was a wikidata match, returns a list of potentials ids, where
    - 'id' is the wikidata id of the entity, where the ids are sorted by likelihood of match, descending.

    If there was no entity match, returns an empty list.
    '''
    params = {
        'action': 'wbsearchentities',
        'language': 'en',
        'format': 'json',
        'search': entityText
    }
    response = get_with_retry(WikidataEntityLookup.BASE_URL, params=params)

    searchResult = json.loads(response.text)
    if 'search' not in searchResult or not searchResult['search']:
        return None

    result = [search['id'] for search in searchResult['search'] if 'id' in search]
    return result        

class WikidataEntityLookup(object):
    BASE_URL = 'http://www.wikidata.org/w/api.php'

    COMMON_PROPERTIES = {
        PROP_CONTAINEDBY : ID_CONTAINEDBY,
        PROP_INSTANCEOF : ID_INSTANCEOF,
        PROP_HEADOFSTATE : ID_HEADOFSTATE,
        PROP_LEGISLATIVEBODY : ID_LEGISLATIVEBODY,
        PROP_GEOLOCATION : ID_GEOLOCATION
    }

    IDS_TO_PROPERTIES = {value: key for key, value in COMMON_PROPERTIES.iteritems()}

    def __init__(self):
        self._workers = multiprocessing.Pool(
            3 * multiprocessing.cpu_count())
        self._entity_id_cache = {}

    def bulk_search_entities(self, entity_texts, maxTries=5):
        unique_entities = sorted(set(entity_texts))
        new_entities = [text for text in unique_entities if text not in self._entity_id_cache]
        start = time.time()
        print 'Fetching', len(new_entities), 'new entity ids of', len(unique_entities), 'requested'
        possible_ids = self._workers.map(search_entity, new_entities)
        print 'Fetched', len(unique_entities), 'entity ids in', time.time() - start, 'seconds'
        for new_entity, ids in zip(new_entities, possible_ids):
            self._entity_id_cache[new_entity] = [ids[0]] if ids else None
        return {text: self._entity_id_cache[text] for text in unique_entities}

    def searchEntity(self, entityText, maxTries=5):
        return search_entity(entityText, maxTries)

    def getTitle(self, entityInformation):
        if 'labels' in entityInformation and 'en' in entityInformation['labels'] and 'value' in entityInformation['labels']['en']:
            return entityInformation['labels']['en']['value']
        return None


    def getAliases(self, entityInformation):
        return entityInformation['aliases'] if 'aliases' in entityInformation else None

    def lookupEntityById(self, entityId, properties):
        """
        entityId, the entityId to look up
        properties, a collection of human-readable properties to look for
        """
        params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId])
        }

        propertyIds = []

        for key in properties:
            if key in WikidataEntityLookup.COMMON_PROPERTIES:
                propertyIds.append(WikidataEntityLookup.COMMON_PROPERTIES[key])

        response = get_with_retry(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)
        # print json.dumps(entityResult['entities'][entityId], sort_keys=True, indent=4, separators=(',', ': '))
        if 'entities' not in entityResult:
            print 'Error fetching entity for ', entityId
            return None

        entities = entityResult['entities']
        if entityId not in entities:
            return None

        entity = {
            'id': entityId,
            'title': self.getTitle(entities[entityId]),
            'aliases': self.getAliases(entities[entityId]),
            'properties': self.getProperties(entities[entityId], properties),
        }

        return entity

    def getProperties(self, entityInformation, propertyNames):
        properties = {}
        for propName in propertyNames:
            propId = WikidataEntityLookup.COMMON_PROPERTIES[propName]
            value = self.get_property_value(entityInformation, propId)
            if value:
                properties[propName] = {
                    'value': value,
                    'wd_id': propId,
                }
        return properties
        


    def get_property_value(self, entityInformation, propertyId):
        try:            
            claims_for_entity_id = entityInformation['claims']
            values_for_property_id = claims_for_entity_id[propertyId][0]
            main_values_for_property_id = values_for_property_id['mainsnak']

            data_values = main_values_for_property_id['datavalue']
            if 'numeric-id' in data_values:
                return 'Q' + str(data_values['numeric-id'])
            elif 'value' in data_values:
                return data_values['value']
        except KeyError:
            return None

if __name__ == '__main__':
    wd = WikidataEntityLookup()
    entities = ['UK', 'EU', 'U.S', 'Ireland', 'The European Commission', 'Lucia Caudet', 'Fox', 'Paramount Pictures', 'Comcast Corp', 'Sony', 'Viacom', 'Warner Bros', 'Twentieth Century', 'NBCUniversal']
    print wd.bulk_search_entities(entities)

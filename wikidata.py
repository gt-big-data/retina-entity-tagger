import requests
import pprint
import json
import math

# Properties
PROP_CONTAINEDBY = "Contained By"
PROP_INSTANCEOF  = "Instance of"
PROP_HEADOFSTATE = "Head of State"
PROP_LEGISLATIVEBODY = "Legislative Body"
PROPER_GEOLOCATION = "GeoLocation"

class WikidataEntityLookup(object):
    BASE_URL = 'http://www.wikidata.org/w/api.php'

    COMMON_PROP = {
        PROP_CONTAINEDBY: "P131",
        PROP_INSTANCEOF : "P31",
        PROP_HEADOFSTATE : "P6",
        PROP_LEGISLATIVEBODY : "P1"
        PROPER_GEOLOCATION : "P625"
    }

    def searchEntities(self, entityText):
        '''
        Search wikidata for entities described by the text entityText.

        Sample usage:
        wd = WikidataEntityLookup()
        entity = wd.searchEntities('NYC') # or, use an alias, eg wd.searchEntities('the big apple')
        print entity # prints {'id': 'Q60', 'description': 'city in state of New York..'}

        Parameters:
        - entityText Text to search for an entity match.

        Output:
        If there was a wikidata match, returns a dictionary of 'id', 'description', where
        - 'id' is the wikidata id of the entity
        - 'description' is the description of the entity, if one exists.

        If there was no entity match, returns None
        '''
        params = {
            'action': 'wbsearchentities',
            'language': 'en',
            'format': 'json',
            'search': entityText
        }
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        searchResult = json.loads(response.text)
        if 'search' not in searchResult or not searchResult['search']:
            return None

        # pick first one, for now
        bestResult = searchResult['search'][0]
        if 'id' not in bestResult:
            return None

        return {
            'id': bestResult['id'],
            'description': bestResult['description'] if 'description' in bestResult else '',
        }

    def getTitle(self, QId):
        params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId]) # pipe separate for multiple ids
        }
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)
        print entityResult['entities'][QId]['labels']['en']['value']


    def getAliases(self, entityId):
        params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId]) # pipe separate for multiple ids
        }
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)
        synonyms = entityResult['entities'][entityId]['aliases']
        # FOR PLACES:
        # P131 = contained by
        # P625 = geo coordinates
        return synonyms

    def propertyLookup(self, entityId, properties):
        """usage for propertyLookup

        entityId, the entityId to look up
        properties, the human readable
        """

        params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId])
        }
        propertyId = []
        for key in properties:
            if key in WikidataEntityLookup.COMMON_PROP:
                propertyId.append(WikidataEntityLookup.COMMON_PROP[key])
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)
        # print json.dumps(entityResult['entities'][entityId], sort_keys=True, indent=4, separators=(',', ': '))
        returnIds = {}
        for pId in propertyId:
            if pId in entityResult['entities'][entityId]['claims'] \
               and "numeric-id" in entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']:
                returnIds[pId] = 'Q'+str(entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']['numeric-id'])
            elif pId in entityResult['entities'][entityId]['claims']:
                returnIds[pId] = entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']
            else:
                returnIds[pId] = None
        return returnIds


data = WikidataEntityLookup()
entityId = data
# print data.propertyLookup("Q23556", [WikidataEntityLookup.COMMON_PROP["Contained By"], WikidataEntityLookup.COMMON_PROP["Instance of"], "P194", "P625"]).keys()

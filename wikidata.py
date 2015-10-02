import requests
import pprint
import json

class WikidataEntityLookup(object):
    BASE_URL = 'http://www.wikidata.org/w/api.php'

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

    def getEntity(self, entityId):
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

    def propertyLookup(self, entityId, propertyId):
        params = params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId])
        }
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)
        # print json.dumps(entityResult['entities'][entityId], sort_keys=True, indent=4, separators=(',', ': '))
        returnIds = {}
        for pId in propertyId:
            if pId in entityResult['entities'][entityId]['claims'].keys():
                returnIds[pId] = 'Q'+str(entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']['numeric-id'])
            else:
                returnIds[pId] = None
        return returnIds


"""usage for categorize

data = WikidataEntityLookup()
entityId = data
print data.categorize("Q23556", ["P131", "P31", "P1231892731"])
will return the property in a dictionary with the P# as the keys
if there is no such property the key maps to None
"""


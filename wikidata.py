import requests
import pprint
import json

class WikidataEntityLookup(object):
    BASE_URL = 'http://www.wikidata.org/w/api.php'
    def __init__(self):
        self.cache = {}
        
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
        If there was a wikidata match, returns id of the text
        If there was no entity match, returns None
        '''
        if entityText not in self.cache:
            params = {
                'action': 'wbsearchentities',
                'language': 'en',
                'format': 'json',
                'search': entityText
            }
            response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
            searchResult = json.loads(response.text)
            id_ = None
            if 'search' in searchResult and searchResult['search'] and\
                'id' in searchResult['search'][0]:
                id_ = searchResult['search'][0]['id']
            
            self.cache[entityText] = id_;
        return self.cache[entityText]

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
        return entityResult

    def propertyLookup(self, entityId, propertyId):
        """usage for propertyLookup

        data = WikidataEntityLookup()
        entityId = data
        print data.categorize("Q23556", ["P131", "P31", "P1231892731"])
        will return the property in a dictionary with the P# as the keys
        if there is no such property the key maps to None
        """
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
            if pId in entityResult['entities'][entityId]['claims']:
                returnIds[pId] = 'Q'+str(entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']['numeric-id'])
            else:
                returnIds[pId] = None
        return returnIds

import requests
import pprint
import json
import math

class WikidataEntityLookup(object):
    BASE_URL = 'http://www.wikidata.org/w/api.php'
    COMMON_PROP = {
        "Contained By" : "P131",
        "Instance of" : "P31",
        "Head of State" : "P6",
        "Legislative Body" : "P1",
        "GeoLocation" : "P625"
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
        params = params = {
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


    def getData(self, entityId, properties):
        params = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json',
            'ids': '|'.join([entityId]) # pipe separate for multiple ids
        }
        """gets all the data for a single entity id"""
        response = requests.get(WikidataEntityLookup.BASE_URL, params=params)
        entityResult = json.loads(response.text)

        title = entityResult['entities'][entityId]['labels']['en']['value']
        alias = entityResult['entities'][entityId]['aliases']

        """converts property text to property keys"""
        propertyId = []
        for key in properties:
            if key in WikidataEntityLookup.COMMON_PROP:
                propertyId.append(WikidataEntityLookup.COMMON_PROP[key])
        returnIds = {}

        """lookup each property in the results"""
        for pId in propertyId:
            """if property exists and is has a numeric value"""
            if pId in entityResult['entities'][entityId]['claims'] \
               and "numeric-id" in entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']:
                returnIds[pId] = 'Q'+str(entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']['numeric-id'])
            """if property exists but has a data value"""
            elif pId in entityResult['entities'][entityId]['claims']:
                returnIds[pId] = entityResult['entities'][entityId]['claims'][pId][0]['mainsnak']['datavalue']['value']
        return (title, alias, returnIds)




    def locDistance(self, entityId1, entityId2):
        Radius = 3963.19
        Error = 1.15
        entityId1 = self.propertyLookup(entityId1, ["P625"])["P625"]
        entityId2 = self.propertyLookup(entityId2, ["P625"])["P625"]
        long1 = math.radians(float(entityId1["longitude"]))
        lat1 = math.radians(float(entityId1["latitude"]))
        long2 = math.radians(float(entityId2["longitude"]))
        lat2 = math.radians(float(entityId2["latitude"]))
        dLong = long2 - long1
        dLat = lat2 - lat1
        a = math.sin(dLat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLong/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return Error * Radius * c

data = WikidataEntityLookup()
entityId = data
# print data.propertyLookup("Q23556", [WikidataEntityLookup.COMMON_PROP["Contained By"], WikidataEntityLookup.COMMON_PROP["Instance of"], "P194", "P625"]).keys()
print data.getData("Q62", ["Contained By", "Instance Of", "P1231892731"])




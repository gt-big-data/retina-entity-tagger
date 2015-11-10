import requests
import pprint
import json
import math

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
        pass

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

    def find_properties(self, entityId, properties):
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

    def get_property_value(propertyId, entityResult):
        try:
            results_for_entity_id = entityResult[entityId]
            claims_for_entity_id = results_for_entity_id['claims']
            values_for_property_id = claims_for_entity_id[propertyId][0]
            main_values_for_property_id = values_for_property_id['mainsnak']

            data_values = main_values_for_property_id['datavalue']
                if 'numeric-id' in data_values.keys():
                    return 'Q' + str(data_values['numeric-id'])
                elif 'value' in data_values.keys():
                    return data_values['value']
            except KeyError:
                pass
            return None

        discovered_properties = []

        for propertyId in propertyIds:
            propvalue = get_property_value(propertyId, entityResult)

            if propvalue and propertyId == ID_GEOLOCATION:
                propvalue.pop("globe", None)
                propvalue.pop("precision", None)


            if propvalue:
                prop = {
                'propid': propertyId,
                'propname': self.IDS_TO_PROPERTIES[propertyId],
                'propvalue': propvalue
                }

                discovered_properties.append(prop)

        return discovered_properties

data = WikidataEntityLookup()
entityId = data

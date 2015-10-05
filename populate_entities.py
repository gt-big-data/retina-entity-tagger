from dbco import *
from collections import defaultdict

def find_qdocs_with_entities(limit=10):
	'''Returns a set with all the entities used in discovered articles'''
	
	# Find all articles that have an entities field
	articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } },
		"$orderby": { '_id' : -1 } },{ "entities": 1}).limit(limit)

	# Conventient lambda function to creat sets of entities from the articles
	getEntitySets = lambda article: set(article['entities'])

	# Given articles, returns a list of sets which hold the entities from a given article
	entitySets = map(getEntitySets, articles)

	# Union all the sets of entities togeter, get one set of all entities found
	entities = set().union(*entitySets)

	# Converts each entity from unicode to str
	cleaned_entities = {str(entity) for entity in entities}

	print cleaned_entities

	return cleaned_entities


def find_wikidata_entity_info(entities):

	# {
	#     $id: 'Q60',
	#     description: 'city in new york; most populous city; ...',
	#     properties:  [
	#         {propid: 'P131', propname: 'containedby', propvalue: 'Q1384'},
	#         {propid: 'P625', propname: 'geocoords', propvalue: {latitude: 50, longitude: -30}}
	#     ]
	# }

	entry = lambda: {'id': None, 'description': None, 'properties': []}
	prop = lambda: {'propid': None, 'propname': None, 'containedby': None, 'propvalue': None}



	entries = {}

	for entity in entities:
		pass




def main():
	find_qdocs_with_entities(1)

if __name__ == "__main__":
    main()

	
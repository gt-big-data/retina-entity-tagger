from dbco import *
from collections import defaultdict

def find_qdocs_with_entities(limit=10):
	'''Returns a set with all the entities used in discovered articles'''

	articles = db.qdoc.find(
		{ "$query": { "entities": { "$exists": True } },  # Find all articles that have an entities field
		"$orderby": { '_id' : -1 } },  # Sort by latest entries
		{ "entities": 1}  # Only want to get back the entities fields for these articles
		).limit(limit)

	# Map articles to sets of their entities
	entitySets = map(lambda article: set(article['entities']), articles)

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

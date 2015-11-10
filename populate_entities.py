from dbco import *
from collections import defaultdict
import wikidata as wd

def find_entity_ids_from_qdocs(limit=10):
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

	# Ensure no None values in our entities
	entities.discard(None)

	# Converts each entity from unicode to str
	cleaned_entity_ids = {str(entity) for entity in entities}

	return cleaned_entity_ids

def storeEntities(entities):
   db.entities.insert(entities)


def find_wikidata_entity_info(entityIds):

	desiredProperties = [
		wd.PROP_INSTANCEOF,
		wd.PROP_CONTAINEDBY,
		wd.PROP_GEOLOCATION,
		# wd.PROP_HEADOFSTATE,
		# wd.PROP_LEGISLATIVEBODY,
	]

	entries = {}

	wd_lookup = wd.WikidataEntityLookup()

	for entityId in entityIds:
		entity = wd_lookup.lookupEntityById(entityId, desiredProperties)
		if not entity:
			print 'No entity for', entityId
			continue
		entityDoc = {}
		entityDoc['_id'] = entity['id']
		entityDoc['aliases'] = entity['aliases']
		entityDoc['title'] = entity['title']
		entityDoc['properties'] = entity['properties']
		yield entityDoc


def entities_in_db():
	return set(str(doc['_id']) for doc in db.entities.find({}, {'_id': 1}))


def main():
	stored_entities = entities_in_db()
	entity_ids = find_entity_ids_from_qdocs(limit=10)
	buf = []
	for entity in find_wikidata_entity_info(entity_ids - stored_entities):
		buf.append(entity)
		if len(buf) >= 10:
			storeEntities(buf)
			buf = []

	if buf:
		storeEntities(buf)

if __name__ == "__main__":
    main()

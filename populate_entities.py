from dbco import *
from collections import defaultdict
import wikidata as wd

def find_entity_ids_from_qdocs(limit=10):
	'''Returns a set with all the entities used in discovered articles'''

	articles = db.qdoc.find(
		{ "$query": { "entities": { "$exists": True, "$elemMatch": {"$type": 2 }, "$not": {"$regex": "Q.*"} } },  # Find all articles that have an entities field
		"$orderby": { '_id' : -1 } },  # Sort by latest entries
		{ "entities": 1}  # Only want to get back the entities fields for these articles
		)
	if limit:
		articles = articles.limit(limit)

	# Map articles to sets of their entities
	entity_ids = set([])
	for article in articles:
		for entity in article['entities']:
			if type(entity) is dict:
				id_ = entity['id']
				if not id_.startswith('Q'):
					import ipdb;ipdb.set_trace()
				entity_ids.add(id_)
			else:
				if not entity.startswith('Q'):
					import ipdb;ipdb.set_trace()
				entity_ids.add(entity)

	# Ensure no None values in our entities
	entity_ids.discard(None)

	# Converts each entity from unicode to str
	try:
		cleaned_entity_ids = {unicode(entity_id) for entity_id in entity_ids}
	except:
		import ipdb;ipdb.set_trace()
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
		if not entityId.startswith('Q'):
			import ipdb;ipdb.set_trace()

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
	print 'Found', len(stored_entities), 'entities already fetched'
	entity_ids = find_entity_ids_from_qdocs(limit=None)
	print 'Found', len(entity_ids), 'to fetch'
	buf = []
	for i, entity in enumerate(find_wikidata_entity_info(entity_ids - stored_entities)):
		print 'Fetched entity', i
		buf.append(entity)
		if len(buf) >= 10:
			print 'Storing entities'
			storeEntities(buf)
			buf = []

	if buf:
		storeEntities(buf)

if __name__ == "__main__":
	main()

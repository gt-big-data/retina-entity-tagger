import wikidata as wd
from dbco import *

def all_qdoc_entities():
	match = {'$match': {'entities': {'$exists': True}}}
	unwind = {'$unwind': '$entities'}
	group = {'$group': {'_id': '$entities.wdid'}}
	match2 = {'$match': {'_id': {'$ne': None}}}
	limit = {'$limit': 2000}
	return set([d['_id'] for d in db.qdoc.aggregate([match, unwind, group, match2, limit])])

def main():
	stored_entities = set(str(doc['_id']) for doc in db.entities.find({}, {'_id': 1}))
	entity_ids = all_qdoc_entities()
	print 'Found', len(stored_entities), 'entities already fetched'
	print 'Found', len(entity_ids), 'to fetch'
	newEnts = entity_ids - stored_entities
	print len(newEnts)
	pops = wd.bulkPopulate(newEnts)
	bulk = db.entities.initialize_unordered_bulk_op()
	i = 0
	for i, entity, pop in zip(range(len(newEnts)), newEnts, pops):
		bulk.find({'_id': pop['_id']}).upsert().update({'$set': pop})
		if i%100 == 0:
			bulk.execute();
			bulk = db.entities.initialize_unordered_bulk_op() # Reset
			print "Stored 100 new entities"
	if i%100 != 0:
		bulk.execute()

if __name__ == "__main__":
	main()
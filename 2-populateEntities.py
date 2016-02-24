import wikidata as wd
from dbco import *

def unpopulatedEntities():
	match = {'$match': {'entities': {'$exists': True}}}
	unwind = {'$unwind': '$entities'}
	match2 = {'$match': {'entities.wdid': {'$ne': None}}}
	group = {'$group': {'_id': '$entities.wdid'}}
	lookup = {'$lookup': {'from': 'entities', 'localField': '_id', 'foreignField': '_id', 'as': 'pop'}}
	match3 = {'$match': {'pop': []}} # Find only the ones that do not exist in entities
	return db.qdoc.aggregate([match, unwind, group, match2, limit])

def main():
	newEnts = [e['_id'] for e in unpopulatedEntities()]
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
	# main()
	ents = ['Barack Obama', 'Michelle Obama', 'Marvin Minsky', 'France', 'U.S.A']
	dictio = wd.bulkFind(ents)
	pops = wd.bulkPopulate([dictio[e] if dictio[e] is not None else None for e in ents])
	for ent, pop in zip(ents, pops):
		print ent, " => ", pop
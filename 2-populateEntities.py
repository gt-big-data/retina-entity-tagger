import wikidata as wd
from dbco import *

def unpopulatedEntities():
	match = {'$match': {'entities': {'$exists': True}}}
	unwind = {'$unwind': '$entities'}
	match2 = {'$match': {'entities.wdid': {'$ne': None}}}
	group = {'$group': {'_id': '$entities.wdid'}}
	lookup = {'$lookup': {'from': 'entities', 'localField': '_id', 'foreignField': '_id', 'as': 'pop'}}
	match3 = {'$match': {'pop': []}} # Find only the ones that do not exist in entities
	return db.qdoc.aggregate([match, unwind, match2, group, lookup, match3])

def main():
	newEnts = [e['_id'] for e in unpopulatedEntities()]
	print len(newEnts), "entities to populate"
	for chunckStart in xrange(0, len(newEnts), 1000):
		chunk = newEnts[chunckStart:(chunckStart+1000)]
		pops = wd.bulkPopulate(chunk)
		bulk = db.entities.initialize_unordered_bulk_op()
		for entity, pop in zip(chunk, pops):
			bulk.find({'_id': pop['_id']}).upsert().update({'$set': pop})
		bulk.execute()
		print "Populated 1000 entities"

if __name__ == "__main__":
	main()
	# ents = ['Google']
	# dictio = wd.bulkFind(ents)
	# pops = wd.bulkPopulate([dictio[e] if dictio[e] is not None else None for e in ents])
	# for ent, pop in zip(ents, pops):
	# 	print ent, " => ", pop
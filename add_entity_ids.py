from dbco import *
from name_entity_extraction import lookupNamedEntities

def getArticlesWithoutEntities(limit=1000):
	return db.qdoc.find({ "$query": { "entities1": { "$exists": True }, "entities": {"$exists": False } }, "$orderby": { '_id' : -1 } }).limit(limit)

#add entity ids to entities already in the database
def addEntityIds():
	articles = getArticlesWithoutEntities()
	for a in articles:
		db.qdoc.update( { "_id": a['_id'] },{"$set": {"entities": lookupNamedEntities(a['entities1']) }})


#rename field entities to entities1
#def changeEntitytoEntity1():
#	db.qdoc.update( {}, { '$rename': { 'entities': 'entities1'} }, upsert=False, multi=True )

addEntityIds()

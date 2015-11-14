from dbco import *

def get_articles(limit=1000):
	articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, "$orderby": { '_id' : -1 } }).limit(limit)
	return articles

'''goes through every entity in every article,
   should be changed to use indexes'''
def id_to_articles(entityId):
	articlesContainingId = []

	for a in get_articles():
		entities = a['entities']
		for e in entities:
			if e == entityId:
				articlesContainingId.append(a['_id'])

	return articlesContainingId

def entitiy_index():
	db.qdoc.create_index([("entities", pymongo.ASCENDING), ("background", True)])

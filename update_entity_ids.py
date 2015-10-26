from dbco import *
from name_entity_extraction import *

#updates entities to wikidata ids
def updateEntities():
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, "$orderby": { '_id' : 1 } })
    for a in articles:
        entities = a['entities']
        updated = isUpdated(entities)
        if not updated:
            #print entities
            newEntities = lookupNamedEntities(entities)
            #print newEntities
            db.qdoc.update( { "_id": a['_id'] }, { "$set": {"entities": newEntities} } )
            #print "---------------------------"

#determines if entities need to be updated
def isUpdated(entities):
    numOfQs = 0
    for e in entities:
        if e is None:
            numOfQs += 1
        elif e[0:1] == 'Q':
            numOfQs += 1

    if len(entities) == numOfQs:
        return True
    else:
        #print numOfQs
        #print len(entities)
        return False

#delete entities1 field
def deleteEntities1():
    bulk = db.qdoc.initialize_unordered_bulk_op()
    bulk.find({"entities1": {"$exists" : True} }).update({ "$unset": {"entities1" : True} })
    result = bulk.execute()
    print(result)

updateEntities()
#print db.qdoc.count()
#print db.qdoc.find({"entities1": {"$exists":True}}).count()
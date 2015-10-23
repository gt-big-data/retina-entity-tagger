from dbco import *
from name_entity_extraction import *

#updates entities to wikidata ids
def updateEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, "$orderby": { '_id' : 1 } }).limit(limit)
    for a in articles:
        entities = a['entities']
        updated = isUpdated(entities)
        if not updated:
            newEntities = lookupNamedEntities(entities)
            db.qdoc.update( { "_id": a['_id'] }, { "$set": {"entities": newEntities} } )
            

#determines if entities need to be updated
def isUpdated(entities):
    
    numOfQs = 0
    for e in entities:
        if e is None:
            numOfQs += 1
        elif e[0:1] == 'Q':
            numOfQs += 1

    if len(entities) is numOfQs:
        return True
    else:
        return False

#delete entities1 field
def deleteEntities1():
    db.qdoc.update(
    { "entities1": {"$exists" : True} },
    { "$unset": {"entities1" : True} },
    False, True
    )

#updateEntities(100)
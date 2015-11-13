from dbco import *
from name_entity_extraction import *
import re

#updates entities to wikidata ids
def updateEntities():
    query = {
        "entities": {
            "$exists": True,
            "$elemMatch": {
                "$type": 2, # string
                "$not":  re.compile("^Q\d+"),
            }
        }
    }

    articles = db.qdoc.find({ "$query":  query, "$orderby": { '_id' : -1 } })
    for i, a in enumerate(articles):
        entities = a['entities']
        if not already_updated(entities):
            #print entities
            print a['_id'], entities, 'need updated...'
            newEntities = lookupNamedEntities(entities)
            #print newEntities
            db.qdoc.update( { "_id": a['_id'] }, { "$set": {"entities": newEntities} } )
        else:
            print 'Article', i, 'already_updated', entities[0] if entities else 'no entity'

            #print "---------------------------"

#determines if entities need to be updated
def already_updated(entities):
    return all([not e or e[0] == 'Q' for e in entities])

#delete entities1 field
def deleteEntities1():
    bulk = db.qdoc.initialize_unordered_bulk_op()
    bulk.find({"entities1": {"$exists" : True} }).update({ "$unset": {"entities1" : True} })
    result = bulk.execute()
    print(result)

updateEntities()
#print db.qdoc.count()
#print db.qdoc.find({"entities1": {"$exists":True}}).count()
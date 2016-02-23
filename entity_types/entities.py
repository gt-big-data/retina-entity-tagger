from dbco import *
import pprint

def testing():

    db.qdoc.find().count
    #print(db.entities.find_one())
    db.qdoc.find().limit(1).skip(1000)
    art = list(db.qdoc.find({'entities': {'$exists': True}}).limit(1).skip(10000))[0]
    print('artobject' + str(art))
    '''
    for entity in art['entities']:
        print entity
    '''
    #print(list(db.entities.find({'_id': 'Q1'})))
    #P31

#Adds the type field to all entities
def addHumanType():
    #numeric-id is "human" (Q5)
    #_id is what the entity actually is
    #wdid refers to "Instance of"
    humanCount = 0
    entityLookup = list(db.entities.find({'_id': {'$exists': True}}).limit(100))
    for entity in entityLookup:
        #print(entity)
        properties = entity['properties']
        if ('Instance of' in properties.keys()):
            if (properties['Instance of']['value']['numeric-id'] == 5):
                humanCount += 1
                #print(entity['_id'])
                print(entity)
                #Do the actual update
                #db.entities.update( { "_id": entity['_id'] },{"$set": {"type": 'human' }})
    print('found ' + str(humanCount) + ' humans')

def qdocEntityLookup():
    '''
    wdoc = db.qdoc
    article = wdoc.find_one()
    #pprint.pprint(article)
    for entity in article['entities']:
        print(entity['wdid'])
    '''
    import pymongo
    print(pymongo.__version__)

    unwind = {"$unwind": '$entities'}
    lookup = {
            "$lookup":
            {
                "from": "entities",
                "localField": "entities.wdid",
                "foreignField": "_id",
                "as": "entity_lookup"
            }
    }
    match = {"$match": {"entity_lookup.type" : "human"}}
    limit = {"$limit": 1000}
    result = db.qdoc.aggregate([limit, unwind, lookup, match])

    #Error found: _id can't be trusted in qdoc, text can probably
    for item in result:
        print(item)
    #match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
    #qdocLookup = list(db.qdoc.find({'_id': {'$exists': True}}).limit(100))

qdocEntityLookup()
#testing()
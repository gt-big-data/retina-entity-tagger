from dbco import *
from name_entity_extraction import *

def updateEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, "$orderby": { '_id' : 1 } }).limit(limit)
    for a in articles:
        entities = a['entities']
        numOfQs = 0
        print type(entities)
        for e in entities: 
            #if e is not None:
                #print e[0:1]
            if e is not None and e[0:1] == "Q":
                #print "Entity starts with a Q"
                numOfQs += 1
            elif e is None:
                #print "Entity is none"
                numOfQs += 1
            elif e == "-1":
                #print "Entity is not in wikidata."
                numOfQs += 1
        print "-------------------------------"
        print numOfQs
        print len(entities)
        #if numOfQs < len(entities):
        namedEntities = lookupNamedEntities(entities)
        print "numOfQs: ", numOfQs , "length of entities: ", len(entities), "Named entities: " , namedEntities
    return
updateEntities(100)
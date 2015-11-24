from dbco import *

def most_common_entities(limit=10):
    results = db.qdoc.aggregate( [
        { "$unwind": "$entities" },
        { "$group": { "_id": "$entities", "total": {"$sum": 1} } },
        { "$sort": {"total": -1} },
        { "$limit": limit}
        ] )
    for ent in results:
        print ent


most_common_entities()

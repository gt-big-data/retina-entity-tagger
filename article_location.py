from dbco import *
from bson import ObjectId

def article_location(article):
    entities = db.qdoc.find_one({"_id":article})
    locations = []
    for entity in entities["entities"]:
        location_id = db.entities.find_one({"_id": entity, "properties.GeoLocation":{"$exists":True}})
        if location_id != None:
            title = location_id["title"]
            latitude = location_id["properties"]["GeoLocation"]["value"]['latitude']
            longitude = location_id["properties"]["GeoLocation"]["value"]['longitude']
            locations.append((title, longitude, latitude ))
    return locations

# articles = list(db.qdoc.find({"entities": {"$exists":True}}, {"_id":1}).limit(10))
# for article in articles:
#     print article_location(article["_id"])
#     print "next Article"



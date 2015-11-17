from dbco import *
from wikidata import WikidataEntityLookup

wd = WikidataEntityLookup()

def getEntitiesNoLocations(limit = 1000):
    return db.qdoc.find( { "$query" : { "loc" : { "$exists" : False } } } ).limit(limit)

def getEntitiesWithGeoLocationData(limit = 1000):
    return db.qdoc.find( { "$query" : { "properties.GeoLocation" : { "$exists" : True } } } ).limit(limit)


# add location to articles in db
def addLocationId():
    # Entity ID -> Location type -> Location name -> wikidata -> GeoJSON -> qdoc.update
    bulk = db.qdoc.initialize_unordered_bulk_op()
    articles = getEntitiesWithGeoLocationData()
    for a in articles:
        lat = a["properties"]["GeoLocation"]["params"]["latitude"]
        long = a["properties"]["GeoLocation"]["params"]["longitude"]
        coords = coordsToJSON(lat, long)
        bulk.find( { a["loc"] : { "$exists" : False } } ).update( { "$set" :  { "loc" : coords } } )
    bulk.execute()

def coordsToJSON(lat, long):
    # TODO Use of coords is probably very wrong
    return { type: "Point", coordinates: [ lat, long ] }

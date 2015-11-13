from dbco import *
from wikidata import WikidataEntityLookup

# !!!
# TODO NOTE: A lot of this code may be reuse/redundant. Use at your own discresion/edit freely. :)

wd = WikidataEntityLookup()


# Do once: Make 2dsphere index in article collection.
def initGeotagging():
    db.qdoc.createIndex( { loc : "2dsphere" } )


def getEntitiesNoLocations(limit = 1000):
    return db.qdoc.find( { "$query" : { "loc" : { "$exists" : False } } } ).limit(limit)


# add location to articles in db
def addLocationId():
    # Entity ID -> Location type -> Location name -> wikidata -> GeoJSON -> qdoc.update
    articles = getEntitiesNoLocations()
    tempEntityId
    for a in articles:
        for ent in a["entities"]:
            tempEntityId = searchEntities(ent)
            if (getEntity(tempEntityId["id"], ["P625"]) is not None):
                coordsRaw = propertyLookup(tempEntityId["id"], ["P625"])
                coordsJSON = coordsToJSON(coordsRaw)
                # Convert to GeoJSON
                # Update db
                db.qdoc.update( { "_id" : a['_id'], { "$set": { "loc" : coordsJSON } } )

def coordsToJSON(coords):
    # TODO Use of coords is probably very wrong
    return { type: "Point", coordinates: [ coords ] }


# UPDATING ARTICLES
# Setting: Run once/when stored articles do not have locations and need them
# Get all articles from collection w/o locations
# Add loc field to articles
# Make geoJSON object with article's lat and long
# db.collection.insert( geoJSOn data )
# Bulk push articles back to collection

# FOR NEW ARTICLES
# Setting: Do this after tagging with entities, before pushing to collection
# Add loc field to articles
# Make geoJSON object with article's lat and long
# db.collection.insert( geoJSOn data )
# Push article to collection as normal

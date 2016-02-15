from dbco import *
db.qdoc.find().count
db.entities.find_one()
db.qdoc.find().limit(1).skip(1000)
art = list(db.qdoc.find({'entities': {'$exists': True}}).limit(1).skip(10000))[0]
for entity in art['entities']:
    print entity
list(db.entities.find({'_id': 'Q142'}))
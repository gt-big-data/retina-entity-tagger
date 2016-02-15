from pymongo import *
from pprint import *


server = MongoClient('mongodb://143.215.138.132:27017/') # mongodb://146.148.59.202:27017/ old GCE 
db = server.big_data
wdoc = db.qdoc
article = wdoc.find_one()
pprint(article)

#api.retinanews.net/
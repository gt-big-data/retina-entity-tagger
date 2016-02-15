from pymongo import MongoClient, errors

client = MongoClient('mongodb://143.215.138.132:27017/') # mongodb://146.148.59.202:27017/ old GCE 
db = client['big_data']
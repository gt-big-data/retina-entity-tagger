from spacy.en import English
from collections import Counter
import time, multiprocessing
from dbco import *
import nlpUtil

def bulkFind(contents):
    workers = multiprocessing.Pool(3*multiprocessing.cpu_count())
    results = workers.map(nlpUtil.extractEntities, contents)
    workers.close()
    return results

def bulkSave(arts, entitiesList):
    bulk = db.qdoc.initialize_unordered_bulk_op()
    for a, e in zip(arts, entitiesList):
        bulk.find({'_id': a['_id']}).update({'$set': {'entities': e}, '$unset': {'reEnt': False}});
    bulk.execute();

def tagEntities():
    articles = db.qdoc.find({"entities": { "$exists": False }}, no_cursor_timeout=True).sort('_id', -1)
    spacy_parse_start = time.time();
    
    bulk = db.qdoc.initialize_unordered_bulk_op()
    articleBuild = []
    for a in articles:
        articleBuild.append(a)
        if len(articleBuild) >= 1024:
            results = bulkFind([unicode(a.get('title', '')+'\n'+a.get('content', '')) for a in articleBuild])
            bulkSave(articleBuild, results)
            print 'Handled ', len(articleBuild), 'docs in', time.time() - spacy_parse_start, 'seconds'
            spacy_parse_start = time.time();
            articleBuild = [] # reset

    if len(articleBuild) > 0:
        results = bulkFind([unicode(a.get('title', '')+'\n'+a.get('content', '')) for a in articleBuild])
        bulkSave(articleBuild, results)
        print 'Handled ', len(articleBuild), 'docs in', time.time() - spacy_parse_start, 'seconds'

if __name__ == "__main__":
    tagEntities()
from spacy.en import English
from collections import Counter
import wikidata as wd, time
from dbco import *

def extractEntities(text):
    global nlp
    SUPPORTED_TYPES = {'ORG', 'PERSON', 'GPE'}
    doc = nlp(unicode(text))
    entities = [ent for ent in doc.ents if ent.label_ in SUPPORTED_TYPES]
    return [ent.text.replace("'s", '') if ent.label_ == 'PERSON' else ent.text for ent in entities]

def list2Count(entity_list, text2wdid):
    entities = []
    for txt, count in Counter(entity_list).most_common():
        entities.append({'wdid': text2wdid.get(txt, None), 'text': txt, 'count': count})
    return entities

def insert_batch(updates):
    all_texts = set([text for _, textList in updates for text in textList])
    text2wdid = wd.bulkFind(all_texts)
    
    bulk = db.qdoc.initialize_unordered_bulk_op()
    for id_, entity_texts in updates:
        bulk.find({'_id': id_}).update({'$set': {'entities': list2Count(entity_texts, text2wdid)}})
    bulk.execute()

def tagEntities():
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }, no_cursor_timeout=True).limit(102400)
    updates = []; spacy_parse_start = time.time()
    print 'Begin entity tagging..'
    for article in articles:
        updates.append((article['_id'], extractEntities(article.get('content', ''))))
        if len(updates) >= 128:
            print 'Spacy parsed', len(updates), 'docs in', time.time() - spacy_parse_start, 'seconds'
            insert_batch(updates)
            spacy_parse_start = time.time()
            updates = []

    if updates:
        print 'Spacy parsed', len(updates), 'docs in', time.time() - spacy_parse_start, 'seconds'
        insert_batch(updates)

if __name__ == "__main__":
    print 'Loading spacy..'
    global nlp
    nlp = English()
    print 'Spacy loaded.'
    tagEntities()
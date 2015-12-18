import name_entity_spacy as spcy
from wikidata import WikidataEntityLookup
from collections import Counter
from dbco import *
import time

wd = WikidataEntityLookup()
def text_to_entity(entity_texts, text_to_ids):
    counts = Counter(entity_texts)
    entity_name_to_id = {}
    for entity in counts:
        possible_ids = text_to_ids[entity]
        entity_name_to_id[entity] = possible_ids[0] if possible_ids else None

    entities = []
    for entity_text, count in counts.most_common():
        entities.append({
            'wdid': entity_name_to_id[entity_text],
            'text': entity_text,
            'count': count,
        })
    return entities


def getArticlesNoEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }, no_cursor_timeout=True).limit(limit)
    return articles

def insert_batch(updates):
    all_entities = set()
    for _, entity_texts in updates:
        all_entities.update(entity_texts)
    text_to_ids = wd.bulk_search_entities(all_entities)
    bulk = db.qdoc.initialize_unordered_bulk_op()
    for id_, entity_texts in updates:
        entities = text_to_entity(entity_texts, text_to_ids)
        bulk.find({'_id': id_}).update({'$set': {'entities': entities}})
    bulk.execute()

#Driver
def tagEntities():
    articles = getArticlesNoEntities(102400)
    updates = []
    spacy_parse_start = time.time()
    print 'Begin entity tagging..'
    for article in articles:
        if 'content' in article:
            entity_texts = spcy.parse_entities(article['content'])
            updates.append((article['_id'], entity_texts))
            if len(updates) >= 128:
                print 'Spacy parsed', len(updates), 'docs in', time.time() - spacy_parse_start, 'seconds'
                insert_batch(updates)
                spacy_parse_start = time.time()
                updates = []
        else:
            err_str = 'No content in article {id}. Deleting article.'.format(id = a['_id'])
            print(err_str)
            db.qdoc.remove(spec_or_id = a['_id'])

    if updates:
        print 'Spacy parsed', len(updates), 'docs in', time.time() - spacy_parse_start, 'seconds'
        insert_batch(updates)

    import IPython;IPython.embed()

if __name__ == "__main__":
    tagEntities()

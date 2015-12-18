import name_entity_spacy as spcy
from wikidata import WikidataEntityLookup
from collections import Counter
from dbco import *

wd = WikidataEntityLookup()
def lookup_entities(entity_texts):
    counts = Counter(entity_texts)
    entity_name_to_id = {}
    for entity in counts:
        possible_ids = wd.searchEntities(entity)
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
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }).limit(limit)
    return articles

#Driver
def tagEntities():
    articles = getArticlesNoEntities(10)
    updates = []
    for article in list(articles):
        if 'content' in article:
            entity_texts = spcy.parse_entities(article['content'])
            updates.append((article['_id'], lookup_entities(entity_texts)))
            if len(updates) > 1000:
                bulk = db.qdoc.initialize_unordered_bulk_op()
                for id_, entities in updates:
                    bulk.find({'_id': id_}).update({'$set': {'entities': entities}})
                bulk.execute()
                updates = []
        else:
            err_str = 'No content in article {id}. Deleting article.'.format(id = a['_id'])
            print(err_str)
            db.qdoc.remove(spec_or_id = a['_id'])

    if updates:
        bulk = db.qdoc.initialize_unordered_bulk_op()
        for id_, entities in updates:
            bulk.find({'_id': id_}).update({'$set': {'entities': entities}})
        bulk.execute()

if __name__ == "__main__":
    tagEntities()

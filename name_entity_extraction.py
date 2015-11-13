import name_entity_spacy as spcy
import nltk
from wikidata import WikidataEntityLookup
from dbco import *

wd = WikidataEntityLookup()
def lookupNamedEntities(namedEntityTexts):
    '''
    Given list of texts that correspond to named entities,
    return a list of ids that these entities resolve to.

    If text does not match a known entity, then it will
    be mapped to None.

    Example usage:
    lookupNamedEntities(['NYC', 'New York State', 'Does not exist'])
    should return [
       'Q60',
       'Q1380',
       None,
    ]
    '''
    returned_list = []
    
    for i in xrange(len(namedEntityTexts)):
        entity = namedEntityTexts[i]
        entityId = wd.searchEntities(entity)
        returned_list.append(entityId)
        
    return returned_list


def getArticlesNoEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }).limit(limit)
    return articles

#Driver
def tagEntities():
    articles = getArticlesNoEntities()
    for a in articles:
        try:
            parsed_text = spcy.nlp_parse(a['content'])
            entities = lookupNamedEntities(parsed_text['entities'])
            unique_entities = sorted(set([entity for entity in entities if entity]))
            db.qdoc.update( { "_id": a['_id'] },{"$set": {"entity_ids": unique_entities, "entities": entities, "nlp" : parsed_text } } )
        except:
            err_str = 'No content in article {id}. Deleting article.'.format(id = a['_id'])
            print(err_str)
            db.qdoc.remove(spec_or_id = a['_id'])

if __name__ == "__main__":
    tagEntities()

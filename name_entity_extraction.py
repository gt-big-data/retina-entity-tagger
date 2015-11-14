import name_entity_spacy as spcy
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
    returned_dict = {}
    
    namedEntitySet = set(namedEntityTexts)
    missingEntitySet = namedEntitySet
    
    # lookup namedEntitySet in local database
    # Save entities not in local database as missingEntitySet
    
    for entity in missingEntitySet:
        entityId = wd.searchEntities(entity)
        returned_dict[entity] = entityId[0] if entityId else None
        
    return returned_dict


def getArticlesNoEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }).limit(limit)
    return articles

#Driver
def tagEntities():
    articles = getArticlesNoEntities()
    for a in articles:
        if 'content' in a:
            parsed_text = spcy.nlp_parse(a['content'])
            unique_entities = lookupNamedEntities(parsed_text['entities'])
            entity_map = [unique_entities[entity] for entity in parsed_text['entities']]
            db.qdoc.update( { "_id": a['_id'] },{"$set": {"entity_ids": unique_entities, "entity_map": entity_map, "nlp" : parsed_text } } )
        else:
            err_str = 'No content in article {id}. Deleting article.'.format(id = a['_id'])
            print(err_str)
            db.qdoc.remove(spec_or_id = a['_id'])

if __name__ == "__main__":
    tagEntities()

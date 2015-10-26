import nltk
from wikidata import WikidataEntityLookup
from dbco import *

wd = WikidataEntityLookup()
def lookupNamedEntities(namedEntityTexts):
    '''
    Given list of texts that correspond to named entities,
    return a list of dictionaries, where each dict has
    the original text, entity id, and description.

    Example usage:
    lookupNamedEntities(['NYC', 'New York State', 'USA'])
    should return [
        {'text': 'NYC', 'id': 'Q60', 'description': 'city in state of New York...'},
        {'text': 'New York State', 'id': 'Q1380', 'description': 'state in us..'}, ..
    ]
    '''
    returned_list = []

    for i in xrange(len(namedEntityTexts)):
        entity = namedEntityTexts[i]
        entityId = wd.searchEntities(entity)
        returned_list.append(entityId)

    return returned_list

def getNameEntities(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    nameEntity = []
    for sentence in chunked_sentences:
        for part in sentence:
            if type(part) is nltk.Tree:
                entityTree = part.leaves()
                entity = ""
                for tuplePair in entityTree:
                    entity += " "
                    entity += tuplePair[0]
                entity = entity[1:]
                nameEntity.append(entity)
    nameEntity = list(set(nameEntity))
    entities = lookupNamedEntities(nameEntity)
    storeEntities(entities)
    return entities

# def entityTester():
#     with open("small_sample_articles.json") as f:
#         for line in f:
#             print(getNameEntities(json.loads(line)["content"]))

def getArticlesNoEntities(limit=1000):
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": False } }, "$orderby": { '_id' : -1 } }).limit(limit)
    return articles

#Driver
def tagEntities():
    articles = getArticlesNoEntities()
    for a in articles:
        db.qdoc.update( { "_id": a['_id'] },{"$set": {"entities": getNameEntities(a['content'] ) } } )

def storeEntities(entities):
    for a in entities:
        if db.entities.find({"_id":a}).count() == 0:
            properties = wd.propertyLookup(a, ["P31", "P131"])
            nonNullProperties = []
            for key, value in properties:
                if value is not None:
                    nonNullProperties[key] = value
            db.entities.insert_one({"_id": a, "Title":wd.getTitle(a), "Aliases": wd.getAliases(a), "Properties": nonNullProperties})

if __name__ == "__main__":
    tagEntities()

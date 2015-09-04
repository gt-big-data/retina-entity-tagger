import nltk
from dbco import *

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
    return nameEntity

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

tagEntities()
from collections import Counter
from spacy.en import English
import wikidata as wd
from dbco import *

global nlp, fullDict

def loadWdidDict():
    di = {}
    for d in db.entities.find():
        di[d['title']] = d['_id']
        if d.get('aliases', []) is not None:
            for a in d.get('aliases', []):
                di[a] = d['_id']
    return di

def extractEntities(text):
    global nlp
    doc = nlp(unicode(text))
    entDict = {}
    for e in doc.ents:
        if e.label_ in {'ORG', 'PERSON', 'GPE', 'WORK_OF_ART'}:
            clean = cleanText(e)
            if clean in entDict:
                entDict[clean]['count'] += 1
            else:
                entDict[clean] = {'count': 1, 'type': e.label_}
    for e in entDict.keys():
        if entDict[e]['type'] == 'PERSON' and ' ' not in e:
            for j in entDict.keys():
                if j != e and entDict[j]['type']=='PERSON' and e in j and ' ' in j:
                    entDict[j]['count'] += entDict[e]['count']
                    entDict[e]['remove'] = True

    for i in entDict.keys():
        if 'remove' in entDict[i]:
            del entDict[i]

    entities = []
    for k in entDict: # reformatting
        obj = {'text': k}; obj.update(entDict[k]); del obj['type']
        entities.append(obj)
    entities = sorted(entities, key=lambda x: x['count'], reverse=True)
    return addWdid(entities)

def cleanText(e):
    final = e.text
    if e.label_ == 'PERSON':
        final = final.replace("'s", '') # remove possessives for people
    if final[:4].lower() == 'the ':
        final = final[4:]
    return final

def addWdid(entDict):
    global fullDict
    for ent in entDict:
        if ent['text'] in fullDict:
            ent['wdid'] = fullDict[ent['text']]
        else:
            finder = wd.findEntity(ent['text'])
            if finder == None or len(finder) == 0:
                ent['wdid'] = None
            else:
                ent['wdid'] = finder[0]
    return entDict

nlp = English()
fullDict = loadWdidDict()

if __name__ == "__main__":
    import random
    art = list(db.qdoc.find().limit(1).skip(int(500*random.random())))[0]
    totalText = unicode(art['title']+'\n\n'+art['content'])
    entDict = extractEntities(totalText)
    for e in entDict:
        print e
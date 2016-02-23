from spacy.en import English
import re

print 'Loading spacy..'
nlp = English()
print 'Spacy loaded.'

SUPPORTED_TYPES = {'ORG', 'PERSON', 'GPE'}

def parse_entities(text):
    doc = nlp(unicode(text))
    entities = [ent for ent in doc.ents if ent.label_ in SUPPORTED_TYPES]

    entity_texts = []
    for ent in entities:
        if ent.label_ == 'PERSON':
            entity_texts.append(ent.text.replace('\'s', ''))
        else:
            entity_texts.append(ent.text)

    return entity_texts
from spacy.en import English
import re

nlp = English()

SUPPORTED_TYPES = {'ORG', 'PERSON', 'GPE'}

def nlp_parse(text):
    doc = nlp(unicode(text))
    entities = [ent for ent in doc.ents if ent.label_ in SUPPORTED_TYPES]

    entity_texts = []
    for ent in entities:
        if ent.label_ == 'PERSON':
            entity_texts.append(ent.text.replace('\'s', ''))
        else:
            entity_texts.append(ent.text)

    return {
        'tokens': [tok.text for tok in doc],
        'entities': entity_texts,
        'entity_spans': [(ent.start, ent.end) for ent in entities],
        'sentence_spans': [(sent.start, sent.end) for sent in doc.sents]
    }

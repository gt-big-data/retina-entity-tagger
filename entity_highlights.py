from dbco import *

limit = 10

def create_sentences(content):
	'''Divide content into sentences'''
	return []

def get_highlighted_sentences(sentences, entities):
	'''Takes in paragraphs of text and a list of entities, returns a list of the sentences in content in which any number of words in entitites shows'''

	return []


# Gets results where we have entities
results = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, "$orderby": { '_id' : -1 } },
	{ "content": 1, "entities": 1}).limit(limit)

for result in results:
	content = result['content']
	entities = result['entities']

	# Convert entities to python strings rather than unicode strings
	entities = [str(e) for e in entities]
	sentences = create_sentences(content)

	highlighted = get_highlighted_sentences(sentences, entities)

	# Do something with highligthed sentences


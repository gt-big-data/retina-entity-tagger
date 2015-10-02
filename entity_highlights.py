from dbco import *
from nltk.tokenize import sent_tokenize
import re

def create_sentences(content):
	'''Divide content into sentences'''
	sentences = sent_tokenize(content)
	valid = []
	for s in sentences:
		
		try:
			# Decodes sentences names so python can work with them, removes newline characters
			s = str(s).strip()
			valid.append(s)

		except UnicodeEncodeError:
			pass

	return valid

def get_highlighted_sentences(sentences, entities):
	'''Takes in paragraphs of text and a list of entities, returns a list of the sentences in content in which any number of words in entitites shows'''
	words_re = re.compile("|".join(entities))

	highlights = []

	for sentence in sentences:

		for e in entities:
			if e.lower() in sentence.lower():
				highlights.append(sentence)

	return highlights

def save_to_db(result, highlights):
	doc_id = result["_id"]
	db.qdoc.update( { "_id": doc_id },{"$set": {"highlights": highlights} } )


# Gets results where we have entities
def main():
	limit = 10
	results = db.qdoc.find({ "$query": { "entities": { "$exists": True }, "content": { "$exists": True } }, "$orderby": { '_id' : -1 } },
		{ "content": 1, "entities": 1}).limit(limit)

	for result in results:

		result = dict([(k.encode('utf-8'), v) for k, v in result.items()])
		content = result['content']
		entities = result['entities']
		# Decodes entity names so python can work with them
		entities = [e.decode('utf-8') for e in entities]

		sentences = create_sentences(content)
		highlights = get_highlighted_sentences(sentences, entities)

		save_to_db(result, highlights)


if __name__ == "__main__":
    main()













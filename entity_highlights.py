from dbco import *
from nltk.tokenize import sent_tokenize
import re

def create_sentences(content):
	'''Divide content into sentences'''
	sentences = sent_tokenize(content)
	# Remove newline character from sentences, along with preceding or trailing whitespaces
	sentences = [re.sub('\n', '', sentence).strip() for sentence in sentences]
	return sentences

def get_highlighted_sentences(sentences, entities):
	'''Takes in paragraphs of text and a list of entities, returns a list of the sentences in content in which any number of words in entitites shows'''

	highlights = []

	for sentence in sentences:
		matching_entities = []
		found_match = False

		for entity in entities:
			if entity.lower() in sentence.lower():
				matching_entities.append(entity)
				found_match = True

		if found_match:
			highlight = {
			'sentence': sentence,
			'entitites': matching_entities
			}
			highlights.append(highlight)

	return highlights

def save_to_db(article, highlights):
	'''Updates an article in the db to include the highlights'''
	doc_id = article["_id"]
	db.qdoc.update( { "_id": doc_id },{"$set": {"highlights": highlights} } )


def main(limit=10):
	'''Fetches some number of articles, and saves to the databases the sentences that have a match with one of our entitites for the given article'''

	# Gets articles where we have entities and content, sort by how recent article is
	articles = db.qdoc.find({ "$query": { "entities": { "$exists": True }, "content": { "$exists": True } },
		"$orderby": { '_id' : -1 } },
		{ "content": 1, "entities": 1}).limit(limit)

	# Processes each article one at a time
	for article in articles:

		# Converts key names to python strings so lookup is convenient
		article = dict([(k.encode('utf-8'), v) for k, v in article.iteritems()])
		content = article['content']
		entities = article['entities']

		sentences = create_sentences(content)
		highlights = get_highlighted_sentences(sentences, entities)

		save_to_db(article, highlights)


if __name__ == "__main__":
    main()













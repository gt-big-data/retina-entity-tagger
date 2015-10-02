from dbco import *
from nltk.tokenize import sent_tokenize

def create_sentences(content):
	'''Divide content into sentences'''
	sentences = sent_tokenize(content)
	valid = []
	for sentence in sentences:
		
		try:
			# Decodes sentences names so python can work with them, removes newline characters
			sentence = str(sentence).strip()
			valid.append(sentence)

			# If the sentence has some strange unicode character in it, we'll ignore it for now
		except UnicodeEncodeError:
			pass

	return valid

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
			print highlight
			highlights.append(highlights)

	return highlights

def save_to_db(result, highlights):
	doc_id = result["_id"]
	print doc_id
	# print highlights
	# db.qdoc.update( { "_id": doc_id },{"$set": {"highlights": highlights} } )


# Gets results where we have entities
def main():
	limit = 10
	results = db.qdoc.find({ "$query": { "entities": { "$exists": True }, "content": { "$exists": True } }, "$orderby": { '_id' : -1 } },
		{ "content": 1, "entities": 1}).limit(limit)

	for result in results:

		result = dict([(k.encode('utf-8'), v) for k, v in result.iteritems()])
		content = result['content']
		entities = result['entities']
		# Decodes entity names so python can work with them
		entities = [entity.decode('utf-8') for entity in entities]

		sentences = create_sentences(content)
		highlights = get_highlighted_sentences(sentences, entities)

		save_to_db(result, highlights)


if __name__ == "__main__":
    main()













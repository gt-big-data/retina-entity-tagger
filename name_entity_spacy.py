from spacy.en import English
nlp = English()

        
def get_entities_spacy(input_string):
    input_string = unicode(input_string)
    doc = nlp(input_string)
    
    output_list = []
    for span in list(doc.ents):
        ent_name = []
        for token in span:
            ent_name.append(token.orth_)
        ent_name = " ".join(ent_name)
        output_list.append(ent_name)
            
    return output_list

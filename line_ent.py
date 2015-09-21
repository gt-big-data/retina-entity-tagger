from spacy.en import English
nlp = English()

        
def list_ent(input_string):
    """inputs string; returns list of known entities"""
    doc = nlp(input_string)
    
    output_list = []
    for token in doc:
        if token.ent_type != "":
            output_list.append(token.orth_)
            
    return output_list
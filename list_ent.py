# -*- coding: utf-8 -*-
"""
v1.0 21 Sep 2015
v1.1 28 Sep 2015
    - Renamed to list_ent.py
    - Added unicode conversion.
    - Retooled output to handle multi-word entities.

@author: samyeager
"""

from spacy.en import English
nlp = English()

        
def list_ent(input_string):
    """inputs string; returns list of known entities"""
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
    
if __name__ == "__main__":
    string = """The United Nations (UN) is an intergovernmental organization to promote international co-operation. A replacement for the ineffective League of Nations, the organization was established on 24 October 1945 after World War II in order to prevent another such conflict. At its founding, the UN had 51 member states; there are now 193. The headquarters of the United Nations is in Manhattan, New York City, and experiences extraterritoriality. Further main offices are situated in Geneva, Nairobi and Vienna. The organization is financed by assessed and voluntary contributions from its member states. Its objectives include maintaining international peace and security, promoting human rights, fostering social and economic development, protecting the environment, and providing humanitarian aid in cases of famine, natural disaster, and armed conflict."""
    entities = list_ent(string)
    
    print(entities[:5])
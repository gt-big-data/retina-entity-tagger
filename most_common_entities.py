# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:51:25 2015

@author: samyeager
"""

from dbco import *
from collections import *

def get_articles_with_entities(limit=1000):
    """retrieves articles that have entities"""
    articles = db.qdoc.find({ "$query": { "entities": { "$exists": True } }, \
        "$orderby": { '_id' : -1 } }).limit(limit)
    return articles

def most_common_entities(limit=1000):
    """produces an OrderedDict with most common entities for articles on top"""
    articles = get_articles_with_entities(limit)
    output_dict = defaultdict(int)
    for item in articles:
        for entity in item['entities']:
            output_dict[entity] += 1
    
    output_dict = OrderedDict(sorted(output_dict.items(), key=lambda t: t[1], reverse = True))    
    
    return output_dict    

if __name__ == "__main__":
    a = most_common_entities()
    print(a.items()[:5])

Retina Entity Tagger
====================

#What you need to install?
- Git
- MongoDB
- Python/Pip (winpython for windows)
- Numpy
- Nltk
- Beautiful Soup
- Requests

# What is entity tagging? Why do it?
Imagine a user searches for news about "Georgia." If we implement this by searching for articles with 
the word "Georgia", we may miss many important articles about "Atlanta" or "Athens" that are relevant to
"Georgia," but do not mention the state explicitly.

If we knew that "Atlanta" was a city in "Georgia" then we could return these relevant search results.

Entity tagging is what powers this kind of search where we understand concepts expressed in news articles.
By doing this, we can deliver a better user experience and deliver more relevant content.

# High level overview
To power entity search, we need to do the following
- Extract every entity from news articles crawled, and index them by entity
- Build a database of known entities
- Build a database of entity relationships

These are the goals of this project. Here is an overview of how we can achieve each.

# Entity Extraction
We can use nltk to extract named entities. This is somewhat of a noisy process, so we can search for these entities and
in our entity database, trying to resolve them.

# Entity Database
We can build a database by leveraging wikipedia. Potentially we can crawl and extract all locations in wikipedia by
starting with the [List of Cities](https://en.wikipedia.org/wiki/Lists_of_cities) page.

Then, we can store the following:
- Entity: has id, name, and type. For example, "North America" would be represented as an entity with name "North America" 
and type of "Continent"
- Relationships: Has "from_id", "to_id", and "type". To represent that "Atlanta" is part of "Georgia", we can make
a relationship between Atlanta and Georgia that has type "contains" (representing that "Georgia" contains "Atlanta")

If processing raw wikipedia pages proves too difficult, we can use the [Wikidata entity API](https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities) to resolve our named entities.
For example, see [this gist](https://gist.github.com/edsu/4681747)

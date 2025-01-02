bio_extractor_prompt = """I have extracted the following key-value pairs from an Infobox in Wikipedia:

{info}

Please clean and organize the data:
Please clean and organize the data:
1. Parse nested templates and links (e.g., {{birth date and age|1958|7|8}} -> Date(year=1958, month=7, day=8).
2. Use the following options for relationship types: spouse, child, parent, sibling, cousin, grandparent, unknown.
3. Use the following options for occupations: actor, musician, director, writer, producer, other (other if unknown).
4. Ignore irrelevant keys like 'image'.
5. Return the cleaned data as JSON.
6. For relationships where the name is unknown, add a placeholder like "Unnamed Child" or "Unnamed Spouse".
7. For relationships where the occupation is unknown, add a placeholder like `None`.
8. Extract location data from links (e.g., [[Philadelphia]], Pennsylvania, U.S. -> Location(city"Philadelphia", state="Pennsylvania", country="U.S.")


Note: a relative can be a child, spouse (e.g., husband, wife), grandparent, cousin, brother, etc.

Return the result as JSON.
"""

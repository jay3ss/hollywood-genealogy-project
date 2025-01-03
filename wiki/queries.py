family_tree_query = """
SELECT (?relativeLabel as ?name) (?relationshipType AS ?relationship_type)
WHERE {{
  VALUES (?relationship ?property) {{
    ("father" wdt:P22)     # father
    ("mother" wdt:P25)     # mother
    ("sibling" wdt:P3373)  # sibling
    ("child" wdt:P40)      # child
    ("spouse" wdt:P26)     # spouse
    ("partner" wdt:P451)   # partner
    ("relative" wdt:P1038) # relative
  }}

  # Retrieve the direct relationships (e.g., father, mother, etc.)
  wd:{entity_id} ?property ?relative.

  # Fetch kinship only for relatives
  OPTIONAL {{
    wd:{entity_id} p:P1038 ?statement.
    ?statement ps:P1038 ?relative;
               pq:P1039 ?kinship.
    ?kinship rdfs:label ?kinshipLabel.
    FILTER(LANG(?kinshipLabel) = "en")
  }}

  # Fetch the relative's label (name)
  ?relative rdfs:label ?relativeLabel.
  FILTER(LANG(?relativeLabel) = "en")

  # Handle relationship type
  BIND(
    IF(STR(?relationship) = "relative" && BOUND(?kinshipLabel), ?kinshipLabel, ?relationship) AS ?relationshipType
  )

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE] en". }}
}}
"""


occupations_query = """
SELECT ?occupation
WHERE {{
  wd:{entity_id} wdt:P106 ?job.
  ?job rdfs:label ?occupation.

  FILTER(LANG(?occupation) = "en")

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE] en". }}
}}
"""


biographical_info_query = """
SELECT
  ?birth_date
  ?death_date
  ?gender
  ?birth_place
  ?biography
WHERE {{
  # Specify the person by their Wikidata entity ID
  OPTIONAL {{ wd:{entity_id} wdt:P569 ?birth_date_entity. }}  # Birth date (P569)
  OPTIONAL {{ wd:{entity_id} wdt:P570 ?death_date_entity. }}  # Death date (P570)
  OPTIONAL {{ wd:{entity_id} wdt:P21 ?gender_entity. }}  # Gender (P21)
  OPTIONAL {{ wd:{entity_id} wdt:P19 ?birth_place_entity. }}  # Hometown / place of birth (P19)
  OPTIONAL {{ wd:{entity_id} schema:description ?biography. FILTER(LANG(?biography) = "en") }}  # Biography in English only

  OPTIONAL {{
    ?gender_entity rdfs:label ?gender.
    FILTER(LANG(?gender) = "en")
  }}

  OPTIONAL {{
    ?birth_place_entity rdfs:label ?birth_place.
    FILTER(LANG(?birth_place) = "en")
  }}

  # Formatting birth and death dates as 'YYYY-MM-DD'
  BIND(
    IF(
      BOUND(?birth_date_entity),
      CONCAT(
        STR(YEAR(?birth_date_entity)),
        "-",
        STR(MONTH(?birth_date_entity)),
        "-",
        STR(DAY(?birth_date_entity))
      ),
      ?birth_date_entity
    ) AS ?birth_date
  )

  BIND(
    IF(
      BOUND(?death_date_entity),
      CONCAT(
        STR(YEAR(?death_date_entity)),
        "-",
        STR(MONTH(?death_date_entity)),
        "-",
        STR(DAY(?death_date_entity))
      ),
      ?death_date_entity
    ) AS ?death_date
  )
}}
"""

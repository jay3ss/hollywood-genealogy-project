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
}}
"""

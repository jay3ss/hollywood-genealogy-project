import requests

from config import config
from wiki.queries import family_tree_query
from wiki.schemas import Relationship
from wiki.utils import flatten_to_model

session = requests.Session()
session.headers.update(
    {
        "User-Agent": config.wikipedia_user_agent,
    }
)


def search_wiki(query: str) -> dict:
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": query,
    }

    response = session.get(config.wikipedia_api_url, params=params)
    response.raise_for_status()
    results = response.json()

    return results["query"]["search"]


@flatten_to_model(Relationship)
def fetch_relatives(entity_id: str) -> list:
    params = {
        "query": family_tree_query.format(entity_id=entity_id),
        "format": "json",
    }
    response = session.get(config.wikidata_api_url, params=params)

    response.raise_for_status()

    return response.json()["results"]["bindings"]
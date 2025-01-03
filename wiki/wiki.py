import requests

from config import config
from wiki.queries import (
    biographical_info_query,
    family_tree_query,
    occupations_query,
    schools_info_query,
)
from wiki.schemas import BiographicalInfo, Occupation, Relationship, School
from wiki.utils import flatten_to_schema

session = requests.Session()
session.headers.update(
    {
        "User-Agent": config.wikipedia_user_agent,
    }
)


def fetch_from_wikidata(query: str) -> list:
    params = {
        "query": query,
        "format": "json",
    }
    response = session.get(config.wikidata_api_url, params=params)

    response.raise_for_status()

    return response.json()["results"]["bindings"]


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


@flatten_to_schema(Relationship)
def fetch_relatives(entity_id: str) -> list:
    return fetch_from_wikidata(family_tree_query.format(entity_id=entity_id))


@flatten_to_schema(Occupation)
def fetch_occupations(entity_id: str) -> list:
    return fetch_from_wikidata(occupations_query.format(entity_id=entity_id))


@flatten_to_schema(BiographicalInfo)
def fetch_biographical_info(entity_id: str) -> list:
    return fetch_from_wikidata(biographical_info_query.format(entity_id=entity_id))


@flatten_to_schema(School)
def fetch_schools_info(entity_id: str) -> list:
    return fetch_from_wikidata(schools_info_query.format(entity_id=entity_id))

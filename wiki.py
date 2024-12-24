import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")

WIKIPEDIA_API_URL = os.environ.get("WIKIPEDIA_API_URL")
WIKIPEDIA_USER_AGENT = os.environ.get("WIKIPEDIA_USER_AGENT")


session = requests.Session()
session.headers.update(
    {
        "User-Agent": WIKIPEDIA_USER_AGENT,
    }
)


def search_wiki(query: str) -> dict:
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": query,
        # "User-Agent": WIKIPEDIA_USER_AGENT,
    }

    response = session.get(WIKIPEDIA_API_URL, params=params)
    response.raise_for_status()
    results = response.json()

    return results["query"]["search"]

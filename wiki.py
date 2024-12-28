import requests

from config import config


session = requests.Session()
session.headers.update(
    {
        # "User-Agent": WIKIPEDIA_USER_AGENT,
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
        # "User-Agent": WIKIPEDIA_USER_AGENT,
    }

    response = session.get(config.wikipedia_api_url, params=params)
    response.raise_for_status()
    results = response.json()

    return results["query"]["search"]

from datetime import datetime

import requests
import wikitextparser as wtp

from config import config


session = requests.Session()
session.headers.update(
    {
        "User-Agent": config.wikipedia_user_agent,
    }
)

replace_string_map = {
    "\n": "",
    "{": "",
    "}": "",
}


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


def parse_infobox(text: str) -> dict:
    parsed = wtp.parse(text)

    # find the infobox
    infobox_template = None
    for template in parsed.templates:
        if template.name.replace("\n", "").strip().lower() == "infobox person":
            infobox_template = template
            break

    if not infobox_template:
        return None

    infobox_data = {}
    for argument in infobox_template.arguments:
        param_name = argument.name.strip().lower()
        param_value = argument.value.strip()
        print(type(argument.value), argument.value)
        print(type(argument.name), argument.name)

        if param_name == "name":
            infobox_data["name"] = param_value
        elif param_name == "birth_date":
            if "{{birth date and age" in param_value:
                _, birth_year, birth_month, birth_day = param_value.maketrans(
                    replace_string_map
                ).split("|")
                birth_date_str = f"{birth_year}-{birth_month}-{birth_day}"
                infobox_data["birth_date"] = birth_date_str

                try:
                    infobox_data["birth_date_obj"] = datetime.strptime(
                        birth_date_str, "%Y-%m-%d"
                    )
                except ValueError as e:
                    print("Error converting birth date string to datetime object:", e)
                    infobox_data["birth_date_obj"] = None
        elif param_name == "occupation":
            infobox_data["occupation"] = param_value

    return infobox_data

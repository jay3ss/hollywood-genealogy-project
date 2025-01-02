import re
from typing import Optional


def extract_birth_date(text: str) -> Optional[dict]:
    """Extract the birth date from Infobox text"""
    match = re.search(r"{{birth date and age\|(\d+)\|(\d+)\|(\d+)}}", text)
    if match:
        return {
            "year": int(match.group(1)),
            "month": int(match.group(2)),
            "day": int(match.group(3)),
        }
    return None


def extract_birth_place(text: str) -> list[str]:
    """Extract the birth place from Infobox text"""
    birth_place = text.strip().translate(str.maketrans("", "", "[],")).split()
    return birth_place


extract_birth_date_tool = {
    "type": "function",
    "function": {
        "name": "extract_birth_date",
        "description": "Extracts the birth date from an Infobox text.",
        "parameters": {
            "type": "object",
            "required": ["text"],
            "properties": {
                "text": {"type": "string", "description": "Infobox text"},
            },
        },
    },
}

extract_birth_place_tool = {
    "type": "function",
    "function": {
        "name": "extract_birth_place",
        "description": "Extracts the birth place from an Infobox text.",
        "parameters": {
            "type": "object",
            "required": ["text"],
            "properties": {
                "text": {"type": "string", "description": "Infobox text"},
            },
        },
    },
}

# Tools dictionary to map the function names to actual function implementations
available_functions = {
    "extract_birth_date": extract_birth_date,
    "extract_birth_place": extract_birth_place,
}

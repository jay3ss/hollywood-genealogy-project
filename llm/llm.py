from enum import Enum
from typing import Optional

from ollama import chat
from pydantic import BaseModel, Field

from config import config
from llm.prompts import bio_extractor_prompt


class Occupation(str, Enum):
    actor = "actor"
    musician = "musician"
    director = "director"
    writer = "writer"
    producer = "producer"
    other = "other"

    def __repr__(self):
        return self.value


class RelationshipType(str, Enum):
    spouse = "spouse"
    child = "child"
    parent = "parent"
    sibling = "sibling"
    cousin = "cousin"
    nibling = "nibling"
    grandparent = "grandparent"
    unknown = "unknown"

    def __repr__(self):
        return self.value


class Relative(BaseModel):
    name: str
    occupation: Optional[Occupation] = Field(
        "other", description="The occupation of the relative (e.g., actor, musician)"
    )
    relationship_type: Optional[RelationshipType] = Field(
        "unknown", description="The type of relationship (e.g., spouse, child)"
    )


class Date(BaseModel):
    year: int
    month: int
    day: int

    def __repr__(self) -> str:
        return f"{self.year}-{self.month}-{self.day}"


class Location(BaseModel):
    """
    Pydantic model for a location that may include (but not limited to):
    - city
    - state/province/etc
    - country
    - zip code
    """

    city: str
    state: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    zipcode: Optional[str] = Field(default=None)


class BioDataExtraction(BaseModel):
    name: str = Field(description="The name of the person")
    birth_date: Optional[Date] = Field(
        description="The person's birthdate (e.g., July 8, 1958 -> 1958-7-8)",
        default=None,
    )
    birth_place: Optional[Location] = Field(
        description="The place where the person was born", default=None
    )
    spouse: Optional[Relative] = Field(
        description="The person's current spouse (name, occupation, and relationship type)"
    )
    children: Optional[list[Relative]] = Field(
        description="The list of the person's children and step-children (name, occupation, and relationship type)"
    )
    occupation: Optional[list[Occupation]] = Field(
        None, description="List of occupations of the person(e.g., actor, musician)"
    )
    relatives: Optional[list[Relative]] = Field(
        description="The list of the person's relatives", default=[]
    )


def parse_infobox(text: str, model: str = config.llm_model) -> dict:
    response = chat(
        messages=[{"role": "user", "content": bio_extractor_prompt.format(info=text)}],
        model=model,
        format=BioDataExtraction.model_json_schema(),
        options={"temperature": 0.0},
    )

    return BioDataExtraction.model_validate_json(response.message.content)

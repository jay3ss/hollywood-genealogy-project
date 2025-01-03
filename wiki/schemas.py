from typing import Optional

from pydantic import BaseModel


class Relationship(BaseModel):
    name: str
    relationship_type: str


class Occupation(BaseModel):
    occupation: str


class BiographicalInfo(BaseModel):
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    biography: Optional[str] = None

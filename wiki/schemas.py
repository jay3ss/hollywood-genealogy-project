from pydantic import BaseModel


class Relationship(BaseModel):
    name: str
    relationship_type: str


class Occupation(BaseModel):
    occupation: str

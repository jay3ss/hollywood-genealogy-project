from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Person(SQLModel, table=True):

    __tablename__ = "people"

    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: Optional[str]
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    gender: Optional[str] = None
    hometown: Optional[str] = None
    biography: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    schools: List["School"] = Relationship(back_populates="people")
    occupations: List["Occupation"] = Relationship(back_populates="people")
    relationships: List["PeopleRelationship"] = Relationship(back_populates="person")


class School(SQLModel, table=True):

    __tablename__ = "schools"

    id: int = Field(default=None, primary_key=True)
    name: str
    location: str
    type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    people: List[Person] = Relationship(back_populates="schools")


class Occupation(SQLModel, table=True):

    __tablename__ = "occupations"

    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    people: List[Person] = Relationship(back_populates="occupations")


class RelationshipType(SQLModel, table=True):

    __tablename__ = "relationship_types"

    id: int = Field(default=None, primary_key=True)
    type_name: str  # "spouse", "sibling", etc.
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PeopleSchools(SQLModel, table=True):
    person_id: int = Field(foreign_key="people.id", primary_key=True)
    school_id: int = Field(foreign_key="schools.id", primary_key=True)
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    degree: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PeopleOccupations(SQLModel, table=True):
    person_id: int = Field(foreign_key="people.id", primary_key=True)
    occupation_id: int = Field(foreign_key="occupations.id", primary_key=True)
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PeopleRelationship(SQLModel, table=True):

    __tablename__ = "people_relationships"

    person_1_id: int = Field(foreign_key="people.id", primary_key=True)
    person_2_id: int = Field(foreign_key="people.id", primary_key=True)
    relationship_type_id: int = Field(foreign_key="relationship_types.id")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

    relationship_type: Optional[RelationshipType] = Relationship()
    person: Person = Relationship(back_populates="relationships")
    related_person: Person = Relationship(back_populates="relationships")

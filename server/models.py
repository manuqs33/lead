from pydantic import EmailStr
from sqlmodel import SQLModel, Field,  Relationship
from typing import List, Optional
from datetime import datetime
from sqlalchemy import UniqueConstraint


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100, nullable=False)
    email: EmailStr = Field(max_length=100, nullable=False)
    address: Optional[str] = Field(max_length=100, nullable=True)
    phone: Optional[str] = Field(max_length=20, nullable=True)

    # Reverse one-to-many relationship
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="lead")
    lead_degrees: List["LeadDegree"] | None = Relationship(back_populates="lead")





class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    degree_id: int = Field(foreign_key="degree.id", nullable=False, index=True)
    duration_in_months: Optional[int] = Field(default=None, nullable=False)

    # Many-to-one relationship with Degree
    degree: "Degree" = Relationship(back_populates="subjects")
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="subject")

    # Only one subject with a given name can be associated with a degree
    __table_args__ = (
        UniqueConstraint('name', 'degree_id',
                        name='uq_subject_name_degree_id'),
    )


class Degree(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False, unique=True)

    # One-to-many relationship with Subject
    subjects: List["Subject"] = Relationship(back_populates="degree")

    # Reverse one-to-many relationship with LeadDegree
    lead_degrees: List["LeadDegree"] | None = Relationship(back_populates="degree")


class LeadDegree(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: int = Field(foreign_key="lead.id", nullable=False, index=True)
    degree_id: int = Field(foreign_key="degree.id", nullable=False, index=True)

    lead: "Lead" = Relationship(back_populates="lead_degrees")
    degree: "Degree" = Relationship(back_populates="lead_degrees")
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="lead_degree")

    __table_args__ = (UniqueConstraint(
        'lead_id', 'degree_id', name='uq_lead_degree'),)



class LeadSubject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    register_year: int = Field(nullable=False)
    times_taken: Optional[int] = Field(default=None, nullable=True)

    lead_id: int = Field(foreign_key="lead.id", nullable=False, index=True)
    subject_id: int = Field(foreign_key="subject.id", nullable=False, index=True)
    lead_degree_id: int = Field(foreign_key="leaddegree.id", nullable=False, index=True)

    lead: "Lead" = Relationship(back_populates="lead_subjects")
    subject: "Subject" = Relationship(back_populates="lead_subjects")
    lead_degree: "LeadDegree" = Relationship(back_populates="lead_subjects")

    __table_args__ = (UniqueConstraint(
        'lead_id', 'subject_id', name='uq_lead_subject'),)
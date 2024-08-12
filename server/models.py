from pydantic import EmailStr
from sqlmodel import SQLModel, Field,  Relationship
from typing import List, Optional
from sqlalchemy import UniqueConstraint


#Lead Models
class LeadBase(SQLModel):
    full_name: str = Field(max_length=100, nullable=False)
    email: EmailStr = Field(max_length=100, nullable=False)
    address: Optional[str] = Field(max_length=100, nullable=True, default=None)
    phone: Optional[str] = Field(max_length=20, nullable=True, default=None)

class Lead(LeadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="lead")
    lead_degrees: List["LeadDegree"] | None = Relationship(back_populates="lead")


class LeadPublic(LeadBase):
    id: int
    lead_degrees: List["LeadDegreePublic"] = []



# Subject Models
class BaseSubject(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    duration_in_months: Optional[int] = Field(nullable=True, default=None, gt=0, lt=13)

class Subject(BaseSubject, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    degree_id: Optional[int] = Field(foreign_key="degree.id", nullable=False, index=True)
    degree: "Degree" = Relationship(back_populates="subjects")
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="subject")

    # Only one subject with a given name can be associated with a degree
    __table_args__ = (
        UniqueConstraint('name', 'degree_id',
                        name='uq_subject_name_degree_id'),
    )

class SubjectPublic(BaseSubject):
    id: int



# Degree Models
class DegreeBase(SQLModel):
    name: str = Field(max_length=100, nullable=False, unique=True)

class Degree(DegreeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subjects: List["Subject"] = Relationship(back_populates="degree")
    lead_degrees: List["LeadDegree"] | None = Relationship(back_populates="degree")

class DegreePublic(DegreeBase):
    id: int



# LeadDegree Models
class LeadDegreeBase(SQLModel):
    lead_id: Optional[int]
    degree_id: Optional[int]

class LeadDegree(LeadDegreeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: Optional[int] = Field(foreign_key="lead.id", nullable=False, index=True)
    degree_id: Optional[int] = Field(foreign_key="degree.id", nullable=False, index=True)

    lead: "Lead" = Relationship(back_populates="lead_degrees")
    degree: "Degree" = Relationship(back_populates="lead_degrees")
    lead_subjects: List["LeadSubject"] | None = Relationship(back_populates="lead_degree")

    __table_args__ = (UniqueConstraint(
        'lead_id', 'degree_id', name='uq_lead_degree'),)


class LeadDegreePublic(LeadDegreeBase):
    id: int
    degree: "DegreePublic"
    lead_subjects: List["LeadSubjectPublic"] = []



# LeadSubject Models
class LeadSubjectBase(SQLModel):
    register_year: int = Field(nullable=False, gt=1990, lt=2026)
    times_taken: Optional[int] = Field(default=None, nullable=True)
    lead_id: Optional[int]
    subject_id: Optional[int]
    lead_degree_id: Optional[int]

class LeadSubject(LeadSubjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: Optional[int] = Field(foreign_key="lead.id", nullable=False, index=True)
    subject_id: Optional[int] = Field(foreign_key="subject.id", nullable=False, index=True)
    lead_degree_id: Optional[int] = Field(foreign_key="leaddegree.id", nullable=False, index=True)

    lead: "Lead" = Relationship(back_populates="lead_subjects")
    subject: "Subject" = Relationship(back_populates="lead_subjects")
    lead_degree: "LeadDegree" = Relationship(back_populates="lead_subjects")

    __table_args__ = (UniqueConstraint(
        'lead_id', 'subject_id', name='uq_lead_subject'),)


class LeadSubjectPublic(LeadSubjectBase):
    id: int
    subject: "SubjectPublic"


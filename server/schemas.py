from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional, List


class CreateLead(SQLModel):
    full_name: str = Field(max_length=100, nullable=False)
    email: EmailStr = Field(max_length=100, nullable=False)
    address: Optional[str] = Field(max_length=100, nullable=True)
    phone: Optional[str] = Field(max_length=20, nullable=True)
    degrees: List["CreateDegreeFromLead"] | None = None


class CreateDegreeFromLead(SQLModel):
    id: Optional[int] = None
    name: str = Field(max_length=100, nullable=False)
    subjects: List["CreateSubjectFromLead"] | None = None


class CreateSubjectFromLead(SQLModel):
    id: Optional[int]  = None
    name: str = Field(max_length=100, nullable=False)
    duration_in_months: Optional[int]  = None
    register_year: Optional[int]  = None
    times_taken: Optional[int]  = None



class CreateLeadResponse(SQLModel):
    id: int = Field()

class GetLeadWithRelationsModel(SQLModel):
    id: int
    full_name: str
    email: EmailStr
    address: Optional[str]  = None
    phone: Optional[str]  = None
    degrees: List["GetDegrees"] | None = None


class GetDegrees(SQLModel):
    id: int
    name: str
    subjects: List["GetSubjects"] | None = None


class GetSubjects(SQLModel):
    id: int
    name: str
    duration_in_months: Optional[int]
    register_year: Optional[int]
    times_taken: Optional[int]
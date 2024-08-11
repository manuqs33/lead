from pydantic import BaseModel, EmailStr
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


class CreateSubjectFromLead(BaseModel):
    id: Optional[int]  = None
    name: str = Field(max_length=100, nullable=False)
    duration_in_months: Optional[int]  = None
    register_year: Optional[int]  = None
    times_taken: Optional[int]  = None


class CreateLeadResponse(SQLModel):
    id: int
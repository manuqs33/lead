from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional, List


class CreateLead(SQLModel):
    full_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=100)
    address: Optional[str] = Field(max_length=100, nullable=True, default=None)
    phone: Optional[str] = Field(max_length=20, nullable=True, default=None)
    degrees: List["CreateDegreeFromLead"] | None = None


class CreateDegreeFromLead(SQLModel):
    id: Optional[int] = None
    name: str = Field(max_length=100, nullable=False)
    subjects: List["CreateSubjectFromLead"] | None = None


class CreateSubjectFromLead(BaseModel):
    id: Optional[int]  = None
    name: str = Field(max_length=100, nullable=False)
    duration_in_months: Optional[int] = Field(nullable=True, default=None, gt=0, lt=13)
    register_year: int = Field(nullable=False, gt=1990, lt=2026)
    times_taken: Optional[int]  = Field(nullable=True, default=None, gt=0, lt=10)


class CreateLeadResponse(SQLModel):
    id: int
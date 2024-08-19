from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class CreateLeadDto(BaseModel):
    full_name: str = Field(max_length=100)
    email: EmailStr
    address: Optional[str] = Field(max_length=100, default=None)
    phone: Optional[str] = Field(max_length=20, default=None)
    degrees: Optional[List["CreateDegreeFromLeadDto"]] = None


class CreateDegreeFromLeadDto(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=100)
    subjects: Optional[List["CreateSubjectFromLeadDto"]] = None


class CreateSubjectFromLeadDto(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=100)
    duration_in_months: Optional[int] = Field(gt=0, lt=13, default=None)
    register_year: int = Field(gt=1990, lt=2026)
    times_taken: Optional[int] = Field(gt=0, lt=11, default=None)

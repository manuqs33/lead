from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class LeadResponseDto(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    address: Optional[str]
    phone: Optional[str]
    lead_degrees: Optional[List["LeadDegreeResponseDto"]]


class LeadDegreeResponseDto(BaseModel):
    id: int
    degree: "DegreeResponseDto"
    lead_subjects: Optional[List["LeadSubjectResponseDto"]]


class DegreeResponseDto(BaseModel):
    id: int
    name: str


class LeadSubjectResponseDto(BaseModel):
    id: int
    subject: "SubjectResponseDto"
    times_taken: Optional[int]
    register_year: int


class SubjectResponseDto(BaseModel):
    id: int
    name: str
    duration_in_months: Optional[int]


class CreateLeadResponseDto(BaseModel):
    id: int

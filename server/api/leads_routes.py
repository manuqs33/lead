from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Degree, Lead, LeadDegree, LeadPublic
from schemas import CreateLead, CreateLeadResponse
from services import leads_service, degrees_service, subjects_service



router = APIRouter()


@router.post("/leads/", response_model=CreateLeadResponse)
def create_lead(lead: CreateLead, session: Session = Depends(get_session)):
    db_lead = leads_service.create_lead(lead, session)
    if lead.degrees is not None:
        degrees: List[Degree] = degrees_service.check_or_create_degrees(session, lead.degrees)
        lead_degrees: List[LeadDegree] = degrees_service.check_or_asign_lead_to_degrees(session, db_lead.id, degrees)
        degrees_with_subjects = [degree for degree in lead.degrees if degree.subjects]
        for degree in degrees_with_subjects:
            created_degree: Degree | None = next((created_degree for created_degree in degrees if created_degree.name == degree.name), None)
            assert degree.subjects is not None and created_degree and created_degree.id is not None
            lead_degree: LeadDegree | None = next((lead_degree for lead_degree in lead_degrees if lead_degree.degree_id == created_degree.id), None)
            subjects = subjects_service.check_or_create_subjects(session, degree.subjects, created_degree.id)
            assert lead_degree and lead_degree.id is not None
            subjects_service.assign_lead_to_subjects(session, db_lead.id, lead_degree.id, subjects, degree.subjects)
    return CreateLeadResponse(id=db_lead.id)


@router.get("/leads/{lead_id}/", response_model=LeadPublic)
def get_lead_with_relations(lead_id: int, session: Session = Depends(get_session)):
    lead = session.get(Lead, lead_id)
    print("lead", lead)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.get("/leads/", response_model=List[LeadPublic])
def get_leads(session: Session = Depends(get_session)):
    leads = session.exec(select(Lead)).all()
    return leads

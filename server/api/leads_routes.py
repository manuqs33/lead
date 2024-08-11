from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from schemas import CreateLead, CreateLeadResponse, GetLeadWithRelationsModel
from services import leads_service, degrees_service, subjects_service


router = APIRouter()


@router.post("/leads/", response_model=CreateLeadResponse)
def create_lead(lead: CreateLead, session: Session = Depends(get_session)):
    db_lead = leads_service.create_lead(lead, session)
    degrees = degrees_service.check_or_create_degrees(session, lead.degrees)
    """ lead_degrees = check_or_asign_lead_to_degrees(session, db_lead.id, degrees)
    for degree in lead.degrees:
        subjects = check_or_create_subjects(session, degree.subjects)
        lead_degree = next(lead_degree for lead_degree in lead_degrees if lead_degree.degree_id == degree.id)
        asign_lead_to_subjects(session, db_lead.id, lead_degree.id, subjects, degree.subjects) """
    return CreateLeadResponse(id=db_lead.id)


@router.get("/leads/{lead_id}/", response_model=GetLeadWithRelationsModel)
def get_lead_with_relations(lead_id: int, session: Session = Depends(get_session)):
    lead = leads_service.get_lead_with_relations(lead_id, session)
    return lead

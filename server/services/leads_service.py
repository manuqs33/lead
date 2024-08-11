from fastapi import HTTPException
from sqlmodel import Session, select
from models import Lead, LeadDegree, LeadSubject
from schemas import CreateLead, CreateLeadResponse, GetDegrees, GetLeadWithRelationsModel, GetSubjects


def create_lead(lead: CreateLead, session: Session) -> CreateLeadResponse:
    db_lead = Lead(full_name=lead.full_name, email=lead.email, address=lead.address, phone=lead.phone)
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)
    lead_response: CreateLeadResponse = CreateLeadResponse(id=db_lead.id)
    return lead_response


def get_lead_with_relations(lead_id: int, session: Session) -> Lead:
    lead = session.exec(select(Lead).where(Lead.id == lead_id)).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


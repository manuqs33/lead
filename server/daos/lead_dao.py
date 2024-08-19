from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from dtos import CreateLeadDto, CreateLeadResponseDto
from models import Lead
from database import get_session


class LeadDao:

    def create_lead(self, lead: CreateLeadDto, session: Session) -> CreateLeadResponseDto:
        db_lead = Lead(full_name=lead.full_name, email=lead.email,
                       address=lead.address, phone=lead.phone)
        session.add(db_lead)
        session.commit()
        session.refresh(db_lead)
        lead_response: CreateLeadResponseDto = CreateLeadResponseDto(
            id=db_lead.id)
        return lead_response

    def get_lead(self, lead_id: int, session: Session) -> Lead | None:
        statement = select(Lead).where(Lead.id == lead_id)
        lead = session.execute(statement).scalar_one_or_none()
        return lead

    def get_leads(self, session: Session, limit: int = 10, offset: int = 0) -> list[Lead]:
        leads_sequence = session.scalars(
            select(Lead).offset(offset).limit(limit)).all()
        leads = list(leads_sequence)
        return leads

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from dtos import CreateLeadDto, CreateLeadResponseDto
from models import LeadDegree, Degree
from database import get_session


class LeadDegreeDao:

    def find_existing_lead_degrees(self, degree_ids: list[int], lead_id: int, session: Session) -> list[LeadDegree]:
        existing_lead_degrees = session.scalars(
            select(LeadDegree).where(
                LeadDegree.lead_id == lead_id,
                LeadDegree.degree_id.in_(degree_ids)
            )
        ).all()
        return list(existing_lead_degrees)

    def create_lead_degrees(self, non_assigned: list[Degree], lead_id: int, session: Session) -> list[LeadDegree]:
        new_lead_degrees = [LeadDegree(lead_id=lead_id, degree_id=degree.id)
                            for degree in non_assigned]
        if new_lead_degrees:
            session.add_all(new_lead_degrees)
            session.commit()
            for lead_degree in new_lead_degrees:
                session.refresh(lead_degree)
        return new_lead_degrees

from typing import List
from models import Lead, Degree, LeadDegree
from dtos import CreateLeadDto, CreateLeadResponseDto
from daos import LeadDao
from services import DegreesService, SubjectsService
from sqlalchemy.orm import Session


class LeadsService:
    def __init__(self, degrees_service: DegreesService, subjects_service: SubjectsService):
        self.degrees_service = degrees_service
        self.subjects_service = subjects_service
        self.lead_dao = LeadDao()

    def create_leads_and_relations(self, lead: CreateLeadDto, session: Session) -> CreateLeadResponseDto:
        db_lead = self.create_lead(lead, session)
        if lead.degrees is not None:
            degrees: List[Degree] = self.degrees_service.check_or_create_degrees(
                lead.degrees, session)
            lead_degrees: List[LeadDegree] = self.degrees_service.check_or_asign_lead_to_degrees(
                db_lead.id, degrees, session)
            degrees_with_subjects = [
                degree for degree in lead.degrees if degree.subjects]
            for degree in degrees_with_subjects:
                created_degree: Degree | None = next(
                    (created_degree for created_degree in degrees if created_degree.name == degree.name), None)
                assert degree.subjects is not None and created_degree and created_degree.id is not None
                lead_degree: LeadDegree | None = next(
                    (lead_degree for lead_degree in lead_degrees if lead_degree.degree_id == created_degree.id), None)
                subjects = self.subjects_service.check_or_create_subjects(
                    degree.subjects, created_degree.id, session)
                assert lead_degree and lead_degree.id is not None
                self.subjects_service.assign_lead_to_subjects(
                    db_lead.id, lead_degree.id, subjects, degree.subjects, session)
        return CreateLeadResponseDto(id=db_lead.id)

    def create_lead(self, lead: CreateLeadDto, session: Session) -> CreateLeadResponseDto:
        lead_response: CreateLeadResponseDto = self.lead_dao.create_lead(lead, session)
        return lead_response

    def get_lead(self, lead_id: int, session: Session) -> Lead | None:
        lead = self.lead_dao.get_lead(lead_id, session)
        return lead

    def get_leads(self, session: Session, limit: int = 10, offset: int = 0) -> List[Lead]:
        leads = self.lead_dao.get_leads( session, limit, offset)
        return leads

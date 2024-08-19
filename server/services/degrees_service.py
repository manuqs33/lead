from typing import List
from dtos import CreateDegreeFromLeadDto
from models import Degree, LeadDegree
from daos import DegreeDao, LeadDegreeDao
from sqlalchemy.orm import Session


class DegreesService():
    def __init__(self):
        self.degree_dao = DegreeDao()
        self.lead_degree_dao = LeadDegreeDao()

    def check_or_create_degrees(self, degrees: List[CreateDegreeFromLeadDto], session: Session) -> List[Degree]:
        degree_names = [degree.name for degree in degrees]
        existing_degrees = self.degree_dao.find_existing_degrees(degree_names, session)
        existing_degree_names = [degree.name for degree in existing_degrees]
        non_existing_names = [
            degree.name for degree in degrees if degree.name not in existing_degree_names]
        new_degrees = self.degree_dao.create_degrees(non_existing_names, session)
        return existing_degrees + new_degrees

    def check_or_asign_lead_to_degrees(self, lead_id: int, degrees: List[Degree], session: Session) -> List[LeadDegree]:
        degree_ids = [degree.id for degree in degrees]
        existing_lead_degrees = self.lead_degree_dao.find_existing_lead_degrees(
            degree_ids, lead_id, session)
        existing_degree_ids = [
            lead_degree.degree_id for lead_degree in existing_lead_degrees]
        non_assigned = [
            degree for degree in degrees if degree.id not in existing_degree_ids]
        new_lead_degrees = self.lead_degree_dao.create_lead_degrees(
            non_assigned, lead_id, session)
        return existing_lead_degrees + new_lead_degrees
from typing import List
from dtos import CreateSubjectFromLeadDto
from models import LeadSubject, Subject
from daos import SubjectDao, LeadSubjectDao
from sqlalchemy.orm import Session


class SubjectsService:
    def __init__(self):
        self.subject_dao = SubjectDao()
        self.lead_subject_dao = LeadSubjectDao()

    def check_or_create_subjects(self, subjects: List[CreateSubjectFromLeadDto], degree_id: int, session: Session) -> List[Subject]:
        subject_names = [subject.name for subject in subjects]
        existing_subjects = self.subject_dao.find_existing_subjects(
            subject_names, degree_id, session)
        existing_subject_names = [
            subject.name for subject in existing_subjects]
        non_existing_subjects = [
            subject for subject in subjects if subject.name not in existing_subject_names]
        new_subjects = self.subject_dao.create_subjects(
            non_existing_subjects, degree_id, session)
        return existing_subjects + new_subjects
    
    def assign_lead_to_subjects(self, lead_id: int, lead_degree_id: int, subjects: List[Subject], metadata: List[CreateSubjectFromLeadDto], session: Session) -> List[LeadSubject]:
        metadata_dict = {item.name: item for item in metadata}
        new_lead_subjects = self.lead_subject_dao.create_lead_subjects(
            lead_id, lead_degree_id, subjects, metadata_dict, session)
        return new_lead_subjects

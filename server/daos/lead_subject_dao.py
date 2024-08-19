from fastapi import Depends
from typing import List
from dtos import CreateSubjectFromLeadDto
from models import Subject, LeadSubject
from database import get_session
from sqlalchemy.orm import Session


class LeadSubjectDao:

    def create_lead_subjects(self, lead_id: int, lead_degree_id: int, subjects: List[Subject], metadata_dict: dict[str, CreateSubjectFromLeadDto], session: Session) -> List[LeadSubject]:
        new_lead_subjects = [
            LeadSubject(
                lead_degree_id=lead_degree_id,
                lead_id=lead_id,
                subject_id=subject.id,
                times_taken=metadata_dict[subject.name].times_taken,
                register_year=metadata_dict[subject.name].register_year
            ) for subject in subjects
        ]
        if new_lead_subjects:
            session.add_all(new_lead_subjects)
            session.commit()
            for new_lead_subject in new_lead_subjects:
                session.refresh(new_lead_subject)
        return new_lead_subjects

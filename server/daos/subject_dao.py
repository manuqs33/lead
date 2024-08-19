from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_session
from models import Subject
from dtos import CreateSubjectFromLeadDto


class SubjectDao:

    def find_existing_subjects(self, subject_names: list[str], degree_id: int, session: Session) -> list[Subject]:
        subjects = session.query(Subject).filter(
            Subject.degree_id == degree_id).filter(Subject.name.in_(subject_names)).all()
        return subjects

    def create_subjects(self, subjects: List[CreateSubjectFromLeadDto], degree_id: int, session: Session):
        new_subjects = [Subject(name=subject.name, duration_in_months=subject.duration_in_months, degree_id=degree_id)
                        for subject in subjects]
        if new_subjects:
            session.add_all(new_subjects)
            session.commit()
            for subject in new_subjects:
                session.refresh(subject)
                assert subject.id is not None
        return new_subjects

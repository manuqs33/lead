

from typing import List
from sqlmodel import Session, select, col
from models import LeadSubject, Subject
from schemas import CreateSubjectFromLead


def check_or_create_subjects(session: Session, subjects: List[CreateSubjectFromLead], degree_id: int) -> List[Subject]:
    subject_names = [subject.name for subject in subjects]

    existing_subjects = session.exec(select(Subject).where(Subject.degree_id ==
                                      degree_id, col(Subject.name).in_(subject_names))).all()

    existing_subject_names = [subject.name for subject in existing_subjects]
    new_subjects = [Subject(name=subject.name, duration_in_months=subject.duration_in_months, degree_id=degree_id)
                    for subject in subjects if subject.name not in existing_subject_names]
    if new_subjects:
        session.add_all(new_subjects)
        session.commit()
        for subject in new_subjects:
            session.refresh(subject)
            assert subject.id is not None 

    all_subjects = list(existing_subjects) + new_subjects
    return all_subjects


def assign_lead_to_subjects(session: Session, lead_id: int, lead_degree_id: int, subjects: List[Subject], metadata: List[CreateSubjectFromLead]) -> List[LeadSubject]:
    response: List[LeadSubject] = []
    metadata_dict = {item.name: item for item in metadata}
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

    response.extend(new_lead_subjects)
    return response

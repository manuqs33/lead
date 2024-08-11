

from typing import List
from sqlalchemy import select
from sqlmodel import Session, col
from models import LeadSubject, Subject
from schemas import CreateSubjectFromLead


def check_or_create_subjects(session: Session, subjects: List[CreateSubjectFromLead]) -> List[Subject]:
    """ subject_names = [subject.name for subject in subjects]
    existing_subjects = session.exec(
        select(Subject).where(Subject.name in subject_names))
    .all()


    existing_subject_names = {subject.name for subject in existing_subjects}
    new_subjects = [Subject(name=subject.name, duration_in_months=subject.duration_in_months)
                    for subject in subjects if subject.name not in existing_subject_names]
    if new_subjects:
        session.bulk_save_objects(new_subjects)
        session.commit()
    session.refresh()
    all_subjects = existing_subjects + new_subjects
    return all_subjects """
    subject = Subject(name=subjects[0].name, duration_in_months=subjects[0].duration_in_months)
    list_subjects = [subject]
    return list_subjects


def asign_lead_to_subjects(session: Session, lead_id: int, lead_degree_id: int, subjects: List[Subject], metadata: List[CreateSubjectFromLead]) -> List[LeadSubject]:
    response: List[LeadSubject] = []
    metadata_dict = {item.name: item for item in metadata}
    new_lead_subjects = [
        LeadSubject(
            lead_degree_id=lead_degree_id,
            lead_id=lead_id,
            subject_id=subject.id,
            times_taken=metadata_dict.get(subject.name).times_taken,
            register_year=metadata_dict.get(subject.name).register_year
        ) for subject in subjects
    ]
    if new_lead_subjects:
        session.bulk_save_objects(new_lead_subjects)
        session.commit()
    session.refresh()
    response.extend(new_lead_subjects)
    return response

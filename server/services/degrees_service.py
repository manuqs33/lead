from datetime import datetime
from typing import List
from sqlmodel import Session, select, col
from models import Degree, LeadDegree #type: ignore
from schemas import CreateDegreeFromLead #type: ignore


def check_or_create_degrees(session: Session, degrees: List[CreateDegreeFromLead]) -> List[Degree]:
    degree_names = [degree.name for degree in degrees]
    existing_degrees = session.exec(select(Degree).where(
        col(Degree.name).in_(degree_names)
    )).all()
    existing_degree_names = [degree.name for degree in existing_degrees]
    new_degrees = [Degree(name=degree.name)
                   for degree in degrees if degree.name not in existing_degree_names]
    if new_degrees:
        session.add_all(new_degrees)
        session.commit()
        for degree in new_degrees:
            session.refresh(degree)

    all_degrees = list(existing_degrees) + list(new_degrees)
    return all_degrees


def check_or_asign_lead_to_degrees(session: Session, lead_id: int, degrees: List[Degree]) -> List[LeadDegree]:
    response: List[LeadDegree] = []
    degree_ids = [degree.id for degree in degrees]
    existing_lead_degrees = session.exec(
        select(LeadDegree).where(
                LeadDegree.lead_id == lead_id,
                col(LeadDegree.degree_id).in_(degree_ids))
    ).all()

    existing_lead_degree_ids = [degree.id for degree in existing_lead_degrees]
    new_lead_degrees = []
    for degree in degrees:
        if degree.id is not None and degree.id not in existing_lead_degree_ids:
            new_lead_degrees.append(
                LeadDegree(lead_id=lead_id, degree_id=degree.id)
            )
    if new_lead_degrees:
        session.add_all(new_lead_degrees)
        session.commit()
        for new_lead_degree in new_lead_degrees:
            session.refresh(new_lead_degree)


    response.extend(existing_lead_degrees)
    response.extend(new_lead_degrees)
    return response

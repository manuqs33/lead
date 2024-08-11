from datetime import datetime
from typing import List
from sqlmodel import Session, select, col
from models import Degree, LeadDegree
from schemas import CreateDegreeFromLead


def check_or_create_degrees(session: Session, degrees: List[CreateDegreeFromLead]) -> List[Degree] | None:
    if not degrees:
        return None
    degree_names = [degree.name for degree in degrees]
    print("degree names", degree_names)
    existing_degrees = session.exec(select(Degree).where(
        Degree.name.in_(degree_names)
    )).all()
    existing_degree_names = [degree.name for degree in existing_degrees]
    print("existing_degree_names", existing_degree_names)

    new_degrees = [Degree(name=degree.name)
                   for degree in degrees if degree.name not in existing_degree_names]
    print("new_degrees", new_degrees)
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
            col(LeadDegree.degree_id) in degree_ids)  # Use in_ on the column object
    ).all()

    existing_lead_degree_ids = {degree.id for degree in existing_lead_degrees}
    new_lead_degrees = []
    for degree in degrees:
        if (degree.id) not in existing_lead_degree_ids:
            new_lead_degrees.append(
                LeadDegree(lead_id=lead_id, degree_id=degree.id)
            )
    if new_lead_degrees:
        session.bulk_save_objects(new_lead_degrees)
        session.commit()

    session.refresh(new_lead_degrees)
    response.extend(existing_lead_degrees)
    response.extend(new_lead_degrees)
    return response

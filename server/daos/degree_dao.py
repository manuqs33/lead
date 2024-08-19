from fastapi import Depends
from sqlalchemy.orm import Session
from models import Degree
from database import get_session


class DegreeDao:

    def find_existing_degrees(self, degree_names: list[str], session: Session) -> list[Degree]:
        existing_degrees = session.query(Degree).filter(
            Degree.name.in_(degree_names)).all()
        return existing_degrees

    def create_degrees(self, degree_names: list[str], session: Session) -> list[Degree]:
        new_degrees = [Degree(name=name) for name in degree_names]
        session.add_all(new_degrees)
        session.commit()
        for degree in new_degrees:
            session.refresh(degree)
        return new_degrees

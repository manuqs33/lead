from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
if TYPE_CHECKING:
    from models import LeadDegree, Subject


class Degree(Base):
    __tablename__ = "degrees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="degree")
    lead_degrees: Mapped[list["LeadDegree"] | None] = relationship(
        "LeadDegree", back_populates="degree")

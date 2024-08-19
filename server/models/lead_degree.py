from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from models.base import Base
if TYPE_CHECKING:
    from models import Degree, LeadSubject, Lead


class LeadDegree(Base):
    __tablename__ = "lead_degrees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leads.id"), nullable=False, index=True)
    degree_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("degrees.id"), nullable=False, index=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="lead_degrees")
    degree: Mapped["Degree"] = relationship(
        "Degree", back_populates="lead_degrees")
    lead_subjects: Mapped[List["LeadSubject"] | None] = relationship(
        "LeadSubject", back_populates="lead_degree")

    __table_args__ = (
        UniqueConstraint('lead_id', 'degree_id', name='uq_lead_degree'),
    )

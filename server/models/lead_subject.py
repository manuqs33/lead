from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from models.base import Base
if TYPE_CHECKING:
    from models import Lead, Subject, LeadDegree


class LeadSubject(Base):
    __tablename__ = "lead_subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    register_year: Mapped[int] = mapped_column(Integer, CheckConstraint(
        "register_year BETWEEN 1990 AND 2025"), nullable=False)
    times_taken: Mapped[int | None] = mapped_column(Integer, CheckConstraint(
        "times_taken BETWEEN 0 AND 10"), nullable=True)
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leads.id"), nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    lead_degree_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lead_degrees.id"), nullable=False, index=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="lead_subjects")
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="lead_subjects")
    lead_degree: Mapped["LeadDegree"] = relationship(
        "LeadDegree", back_populates="lead_subjects")

    __table_args__ = (
        UniqueConstraint('lead_id', 'subject_id', name='uq_lead_subject'),
    )

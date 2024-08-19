from typing import List, TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from models.base import Base
if TYPE_CHECKING:
    from models import Degree, LeadSubject


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    degree_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("degrees.id"), nullable=False, index=True)
    degree: Mapped["Degree"] = relationship(
        "Degree", back_populates="subjects")
    lead_subjects: Mapped[List["LeadSubject"] | None] = relationship(
        "LeadSubject", back_populates="subject")
    duration_in_months: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("duration_in_months BETWEEN 1 AND 12"),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint('name', 'degree_id',
                         name='uq_subject_name_degree_id'),
    )

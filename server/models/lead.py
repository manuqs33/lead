from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
if TYPE_CHECKING:
    from models import LeadDegree, LeadSubject


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, default=None)

    lead_subjects: Mapped[list["LeadSubject"]
                          ] = relationship(back_populates="lead")
    lead_degrees: Mapped[list["LeadDegree"]
                         ] = relationship(back_populates="lead")

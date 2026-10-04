import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    WON = "won"
    LOST = "lost"


class SalesRepresentative(Base):
    __tablename__ = "sales_representatives"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    leads: Mapped[list["Lead"]] = relationship(back_populates="representative")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    meta_lead_id: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    campaign: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    ad_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    representative_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sales_representatives.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    representative: Mapped["SalesRepresentative"] = relationship(back_populates="leads")
    sale: Mapped["Sale | None"] = relationship(back_populates="lead", uselist=False)


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id"), unique=True, nullable=False, index=True
    )
    revenue: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    lead: Mapped["Lead"] = relationship(back_populates="sale")

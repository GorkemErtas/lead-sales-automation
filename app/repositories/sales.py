import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lead, Sale


class SaleRepository:
    def get_lead(self, db: Session, lead_id: uuid.UUID) -> Lead | None:
        return db.scalar(select(Lead).where(Lead.id == lead_id))

    def get_by_lead_id(self, db: Session, lead_id: uuid.UUID) -> Sale | None:
        return db.scalar(select(Sale).where(Sale.lead_id == lead_id))

    def create(self, db: Session, lead: Lead, revenue) -> Sale:
        sale = Sale(lead_id=lead.id, revenue=revenue)
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale

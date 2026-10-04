from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lead, SalesRepresentative
from app.schemas.lead import LeadCreate


class LeadRepository:
    def get_by_meta_id(self, db: Session, meta_lead_id: str) -> Lead | None:
        return db.scalar(select(Lead).where(Lead.meta_lead_id == meta_lead_id))

    def get_or_create_representative(self, db: Session, name: str) -> SalesRepresentative:
        representative = db.scalar(
            select(SalesRepresentative).where(SalesRepresentative.name == name)
        )
        if representative:
            return representative

        representative = SalesRepresentative(name=name)
        db.add(representative)
        db.flush()
        return representative

    def create(self, db: Session, payload: LeadCreate) -> Lead:
        representative = self.get_or_create_representative(db, payload.representative_name)
        lead = Lead(
            meta_lead_id=payload.meta_lead_id,
            campaign=payload.campaign,
            ad_cost=payload.ad_cost,
            representative_id=representative.id,
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead

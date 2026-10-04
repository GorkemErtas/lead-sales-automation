import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Lead, LeadStatus, Sale, SalesRepresentative


class AnalyticsRepository:
    def representative_totals(self, db: Session, representative_id: uuid.UUID):
        return db.execute(
            select(
                SalesRepresentative.name,
                func.count(Lead.id),
                func.count(Lead.id).filter(Lead.status == LeadStatus.WON),
                func.coalesce(func.sum(Lead.ad_cost), 0),
                func.coalesce(func.sum(Sale.revenue), 0),
            )
            .select_from(SalesRepresentative)
            .outerjoin(Lead, Lead.representative_id == SalesRepresentative.id)
            .outerjoin(Sale, Sale.lead_id == Lead.id)
            .where(SalesRepresentative.id == representative_id)
            .group_by(SalesRepresentative.id)
        ).one_or_none()

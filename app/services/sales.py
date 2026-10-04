import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Lead, LeadStatus, Sale
from app.repositories.sales import SaleRepository


class LeadNotFoundError(Exception):
    pass


class LeadAlreadyConvertedError(Exception):
    pass


class SaleService:
    def __init__(self, repository: SaleRepository | None = None) -> None:
        self.repository = repository or SaleRepository()

    def _convert_lead(self, db: Session, lead: Lead | None, revenue: Decimal) -> Sale:
        if lead is None:
            raise LeadNotFoundError

        if self.repository.get_by_lead_id(db, lead.id) is not None:
            raise LeadAlreadyConvertedError

        lead.status = LeadStatus.WON
        return self.repository.create(db, lead, revenue)

    def convert(self, db: Session, lead_id: uuid.UUID, revenue: Decimal) -> Sale:
        return self._convert_lead(db, self.repository.get_lead(db, lead_id), revenue)

    def convert_by_meta_id(self, db: Session, meta_lead_id: str, revenue: Decimal) -> Sale:
        return self._convert_lead(
            db,
            self.repository.get_lead_by_meta_id(db, meta_lead_id),
            revenue,
        )

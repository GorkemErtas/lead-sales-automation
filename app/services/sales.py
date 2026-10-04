import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import LeadStatus, Sale
from app.repositories.sales import SaleRepository


class LeadNotFoundError(Exception):
    pass


class LeadAlreadyConvertedError(Exception):
    pass


class SaleService:
    def __init__(self, repository: SaleRepository | None = None) -> None:
        self.repository = repository or SaleRepository()

    def convert(self, db: Session, lead_id: uuid.UUID, revenue: Decimal) -> Sale:
        lead = self.repository.get_lead(db, lead_id)
        if lead is None:
            raise LeadNotFoundError

        if self.repository.get_by_lead_id(db, lead_id) is not None:
            raise LeadAlreadyConvertedError

        lead.status = LeadStatus.WON
        return self.repository.create(db, lead, revenue)

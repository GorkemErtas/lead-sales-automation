from sqlalchemy.orm import Session

from app.models import Lead
from app.repositories.leads import LeadRepository
from app.schemas.lead import LeadCreate


class LeadService:
    def __init__(self, repository: LeadRepository | None = None) -> None:
        self.repository = repository or LeadRepository()

    def ingest(self, db: Session, payload: LeadCreate) -> tuple[Lead, bool]:
        existing = self.repository.get_by_meta_id(db, payload.meta_lead_id)
        if existing:
            return existing, False

        return self.repository.create(db, payload), True

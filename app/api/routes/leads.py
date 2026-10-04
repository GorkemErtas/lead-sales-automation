from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.leads import LeadService

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])
service = LeadService()


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    payload: LeadCreate,
    response: Response,
    db: Session = Depends(get_db),
) -> LeadResponse:
    lead, created = service.ingest(db, payload)
    if not created:
        response.status_code = status.HTTP_200_OK
    return LeadResponse.model_validate(lead)


@router.get("/recent")
def recent_leads(db: Session = Depends(get_db)):
    items = []
    for lead in service.list_recent(db):
        items.append({"id": str(lead.id), "meta_lead_id": lead.meta_lead_id, "campaign": lead.campaign, "ad_cost": str(lead.ad_cost), "status": lead.status.value, "representative_name": lead.representative.name, "created_at": lead.created_at.isoformat()})
    return items

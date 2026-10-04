import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sales import LeadAlreadyConvertedError, LeadNotFoundError, SaleService

router = APIRouter(prefix="/api/v1/leads", tags=["sales"])
service = SaleService()


@router.post("/{lead_id}/sale", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    lead_id: uuid.UUID,
    payload: SaleCreate,
    db: Session = Depends(get_db),
) -> SaleResponse:
    try:
        sale = service.convert(db, lead_id, payload.revenue)
    except LeadNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lead not found") from exc
    except LeadAlreadyConvertedError as exc:
        raise HTTPException(status_code=409, detail="Lead already converted") from exc

    return SaleResponse.model_validate(sale)

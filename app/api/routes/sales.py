import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sales import LeadAlreadyConvertedError, LeadNotFoundError, SaleService

router = APIRouter(prefix="/api/v1/leads", tags=["sales"])
service = SaleService()


def _to_response(sale) -> SaleResponse:
    return SaleResponse(
        id=sale.id,
        lead_id=sale.lead_id,
        representative_id=sale.lead.representative_id,
        revenue=sale.revenue,
        created_at=sale.created_at,
    )


def _convert_or_raise(convert):
    try:
        return _to_response(convert())
    except LeadNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Lead not found") from exc
    except LeadAlreadyConvertedError as exc:
        raise HTTPException(status_code=409, detail="Lead already converted") from exc


@router.post("/{lead_id}/sale", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    lead_id: uuid.UUID,
    payload: SaleCreate,
    db: Session = Depends(get_db),
) -> SaleResponse:
    return _convert_or_raise(lambda: service.convert(db, lead_id, payload.revenue))


@router.post(
    "/by-meta/{meta_lead_id}/sale",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sale_by_meta_id(
    meta_lead_id: str,
    payload: SaleCreate,
    db: Session = Depends(get_db),
) -> SaleResponse:
    return _convert_or_raise(
        lambda: service.convert_by_meta_id(db, meta_lead_id, payload.revenue)
    )

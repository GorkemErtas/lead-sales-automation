import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import RepresentativeMetrics
from app.services.analytics import AnalyticsService, RepresentativeNotFoundError

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
service = AnalyticsService()


@router.get("/representatives/{representative_id}", response_model=RepresentativeMetrics)
def representative_metrics(
    representative_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> RepresentativeMetrics:
    try:
        return service.representative_metrics(db, representative_id)
    except RepresentativeNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Representative not found") from exc

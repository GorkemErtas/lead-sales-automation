import uuid
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.repositories.analytics import AnalyticsRepository
from app.schemas.analytics import RepresentativeMetrics


TWO_PLACES = Decimal("0.01")


class RepresentativeNotFoundError(Exception):
    pass


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository | None = None) -> None:
        self.repository = repository or AnalyticsRepository()

    def representative_metrics(
        self, db: Session, representative_id: uuid.UUID
    ) -> RepresentativeMetrics:
        row = self.repository.representative_totals(db, representative_id)
        if row is None:
            raise RepresentativeNotFoundError

        name, total_leads, converted_leads, ad_cost, revenue = row
        ad_cost = Decimal(ad_cost)
        revenue = Decimal(revenue)
        profit = revenue - ad_cost

        conversion_rate = (
            Decimal(converted_leads) / Decimal(total_leads) * Decimal("100")
            if total_leads
            else Decimal("0")
        )
        roi = (
            profit / ad_cost * Decimal("100")
            if ad_cost > 0
            else None
        )

        return RepresentativeMetrics(
            representative_id=representative_id,
            representative_name=name,
            total_leads=total_leads,
            converted_leads=converted_leads,
            conversion_rate=conversion_rate.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
            ad_cost=ad_cost.quantize(TWO_PLACES),
            revenue=revenue.quantize(TWO_PLACES),
            profit=profit.quantize(TWO_PLACES),
            roi=roi.quantize(TWO_PLACES, rounding=ROUND_HALF_UP) if roi is not None else None,
        )

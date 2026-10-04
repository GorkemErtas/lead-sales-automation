import uuid
from decimal import Decimal
from pydantic import BaseModel

class RepresentativeMetrics(BaseModel):
    representative_id: uuid.UUID
    representative_name: str
    total_leads: int
    converted_leads: int
    conversion_rate: Decimal
    ad_cost: Decimal
    revenue: Decimal
    profit: Decimal
    roi: Decimal | None

class DashboardSummary(BaseModel):
    total_leads: int
    converted_leads: int
    conversion_rate: Decimal
    ad_cost: Decimal
    revenue: Decimal
    profit: Decimal
    roi: Decimal | None

class DashboardMetrics(BaseModel):
    summary: DashboardSummary
    representatives: list[RepresentativeMetrics]

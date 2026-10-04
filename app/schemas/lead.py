import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import LeadStatus


class LeadCreate(BaseModel):
    meta_lead_id: str = Field(min_length=1, max_length=120)
    campaign: str = Field(min_length=1, max_length=160)
    ad_cost: Decimal = Field(ge=0, decimal_places=2)
    representative_name: str = Field(min_length=1, max_length=120)


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    meta_lead_id: str
    campaign: str
    ad_cost: Decimal
    status: LeadStatus
    representative_id: uuid.UUID
    created_at: datetime

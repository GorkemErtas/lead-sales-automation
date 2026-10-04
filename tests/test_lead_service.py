from unittest.mock import Mock

from app.schemas.lead import LeadCreate
from app.services.leads import LeadService


def test_duplicate_meta_lead_is_idempotent() -> None:
    repository = Mock()
    existing = Mock()
    repository.get_by_meta_id.return_value = existing
    service = LeadService(repository)

    payload = LeadCreate(
        meta_lead_id="META-1042",
        campaign="pain-treatment-istanbul",
        ad_cost="120.00",
        representative_name="Ayse",
    )

    lead, created = service.ingest(Mock(), payload)

    assert lead is existing
    assert created is False
    repository.create.assert_not_called()

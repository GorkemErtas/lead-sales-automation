from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models import LeadStatus
from app.services.sales import LeadAlreadyConvertedError, SaleService


def test_conversion_marks_lead_as_won() -> None:
    repository = Mock()
    lead = SimpleNamespace(id=uuid4(), status=LeadStatus.NEW)
    sale = Mock()
    repository.get_lead.return_value = lead
    repository.get_by_lead_id.return_value = None
    repository.create.return_value = sale

    result = SaleService(repository).convert(Mock(), lead.id, Decimal("2500.00"))

    assert result is sale
    assert lead.status == LeadStatus.WON
    repository.create.assert_called_once()


def test_duplicate_conversion_is_rejected() -> None:
    repository = Mock()
    lead = SimpleNamespace(id=uuid4(), status=LeadStatus.WON)
    repository.get_lead.return_value = lead
    repository.get_by_lead_id.return_value = Mock()

    with pytest.raises(LeadAlreadyConvertedError):
        SaleService(repository).convert(Mock(), lead.id, Decimal("2500.00"))

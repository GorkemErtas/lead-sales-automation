from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

from app.services.analytics import AnalyticsService


def test_representative_profitability_metrics() -> None:
    representative_id = uuid4()
    repository = Mock()
    repository.representative_totals.return_value = (
        "Ayse",
        10,
        4,
        Decimal("1200.00"),
        Decimal("8500.00"),
    )

    metrics = AnalyticsService(repository).representative_metrics(Mock(), representative_id)

    assert metrics.total_leads == 10
    assert metrics.converted_leads == 4
    assert metrics.conversion_rate == Decimal("40.00")
    assert metrics.profit == Decimal("7300.00")
    assert metrics.roi == Decimal("608.33")

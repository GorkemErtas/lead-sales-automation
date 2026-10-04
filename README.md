# Lead Sales Automation

Focused PoC: track a simulated Meta Ads lead from acquisition to sale and calculate representative profitability in near real time.

```text
Meta Lead -> n8n Webhook -> FastAPI -> PostgreSQL -> Metrics -> Google Sheets
```

Metrics: lead count, conversions, conversion rate, ad cost, revenue, profit and ROI.

Stack: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, n8n, Google Sheets, Pytest.

Only synthetic data is used.

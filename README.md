# Lead Sales Automation

A focused proof of concept for a real RevOps question: **did a lead acquired through Meta Ads become a sale, and what is the assigned sales representative's cost/profitability?**

## Architecture

```text
Simulated Meta Lead
       |
       v
 n8n Webhook
       |
       v
 FastAPI / Python
       |
       v
   PostgreSQL
       |
       +----> Sale conversion
       |
       +----> Representative metrics
                    |
                    v
               Google Sheets
```

FastAPI owns the business rules and PostgreSQL is the source of truth. n8n is used as the integration/orchestration layer. Google Sheets is only a reporting destination.

## What is calculated?

For each sales representative:

- total leads
- converted leads
- conversion rate = converted leads / total leads
- advertising cost
- sales revenue
- profit = revenue - advertising cost
- ROI = profit / advertising cost x 100

## Run locally

Requirements: Docker and Docker Compose.

```bash
docker compose up --build
```

The API is available at `http://localhost:8000` and Swagger at `http://localhost:8000/docs`. n8n is available at `http://localhost:5678`.

The API container runs `alembic upgrade head` before startup, so the PostgreSQL schema is created automatically.

## Demo flow

Import both JSON files under `n8n/` into n8n.

A simulated Meta payload sent to the **Meta Lead Intake** webhook:

```json
{
  "lead_id": "META-1042",
  "campaign": "pain-treatment-istanbul",
  "ad_cost": 120.00,
  "representative": "Ayse"
}
```

is normalized by n8n and persisted through `POST /api/v1/leads`. The endpoint is idempotent by `meta_lead_id`, so webhook retries do not create duplicate leads.

When that lead converts, send the internal lead UUID and revenue to the **Sale Conversion and Profitability** webhook:

```json
{
  "lead_id": "00000000-0000-0000-0000-000000000000",
  "revenue": 2500.00
}
```

The workflow records the sale, marks the lead as won and requests the latest representative metrics.

## Google Sheets

After importing `n8n/sale-conversion-workflow.json`, add a Google Sheets node after **Get Representative Metrics**. Credentials and spreadsheet IDs are deliberately not committed.

Map these fields: `representative_name`, `total_leads`, `converted_leads`, `conversion_rate`, `ad_cost`, `revenue`, `profit`, `roi`.

Use an update/upsert keyed by `representative_id` so the sheet represents current metrics rather than duplicate snapshots.

## API

- `GET /health`
- `POST /api/v1/leads`
- `POST /api/v1/leads/{lead_id}/sale`
- `GET /api/v1/analytics/representatives/{representative_id}`

## Engineering decisions

- **Idempotent lead ingestion:** repeated Meta webhook delivery does not duplicate a lead.
- **One sale per lead:** duplicate conversion attempts are rejected.
- **Decimal money values:** financial calculations avoid binary floating-point arithmetic.
- **Separated layers:** API routes, services, repositories and persistence models have distinct responsibilities.
- **Synthetic data only:** the repository contains no real customer or patient information.
- **Secrets stay outside Git:** database and Google credentials are environment/configuration concerns.

## Tests

```bash
pytest -q
```

Tests cover API health, duplicate lead ingestion, conversion behavior and profitability calculations.

## Tech

Python 3.11, FastAPI, SQLAlchemy 2, PostgreSQL 16, Alembic, n8n, Google Sheets, Docker Compose and Pytest.

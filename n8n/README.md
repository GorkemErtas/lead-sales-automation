# n8n workflows

Two importable workflows are included.

## 1. Meta Lead Intake

`meta-lead-workflow.json`

Receives a simulated Meta lead and sends the normalized payload to FastAPI.

## 2. Sale Conversion and Profitability

`sale-conversion-workflow.json`

Receives a CRM-style sale event, records the conversion, then requests the latest profitability metrics for the assigned representative.

Example webhook body:

```json
{
  "lead_id": "<internal-lead-uuid>",
  "revenue": 2500.00
}
```

## Google Sheets

The final reporting node is intentionally configured in the n8n UI after import because Google credentials and the target spreadsheet ID must never be committed to Git.

Add a Google Sheets node after **Get Representative Metrics** and map:

- representative_name
- total_leads
- converted_leads
- conversion_rate
- ad_cost
- revenue
- profit
- roi

Use an upsert/update strategy keyed by representative ID so the sheet remains a current report instead of accumulating duplicate rows.

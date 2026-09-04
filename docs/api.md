# API Documentation

## `app.transaction_ingestion`

### `normalize_transaction(record: dict[str, Any]) -> dict[str, Any]`

Normalizes one input record into the stable transaction contract:

```json
{
  "date": "2026-01-05",
  "description": "Metro",
  "amount": 3.5,
  "currency": "USD",
  "merchant": "Metro",
  "category": "Transportation",
  "source": "csv"
}
```

Missing optional values use safe defaults. Invalid amounts become `0.0`.

### `parse_transactions(text: str, source: str = "csv") -> list[dict[str, Any]]`

Supported `source` values:

- `csv`: CSV with a header row.
- `json`: a JSON array or an object containing a `transactions` array.
- `plaid`: a Plaid-style JSON envelope containing `transactions`.

Empty input, invalid JSON, and non-object JSON records return an empty or filtered result without crashing the batch. Unsupported source values raise `ValueError` because they indicate a caller configuration error.

## Confluence publishing

Use `scripts/publish_confluence.py` to publish an HTML document:

```powershell
python scripts/publish_confluence.py docs/functional_page.html --title "AI-Expense-Advisor Functional Requirements"
```

## `app.budget_advisor`

### `calculate_budget_alerts(transactions, budgets, period, threshold=1) -> list[BudgetAlert]`

Calculates positive spending by category for a `YYYY-MM` period using `Decimal` arithmetic. Returns warning alerts at the configured threshold and critical alerts at or above the budget limit.

### `analyze_spending_trends(transactions) -> list[SpendingTrend]`

Aggregates positive spending by category and month and reports the percentage change from the prior observed period.

### `build_advisor_recommendation(alerts, sources) -> AdvisorRecommendation`

Builds an informational recommendation from alert data and approved `KnowledgeSource` citations. It returns an explicit no-guidance response when sources are absent; retrieval providers and persistence remain behind future interfaces.

Confluence credentials are loaded from environment variables and are never part of the request URL or page body.

To publish all seven approved SDLC pages, use:

```powershell
python scripts/publish_all_confluence.py
```

Preview the page and artifact mapping without contacting Confluence:

```powershell
python scripts/publish_all_confluence.py --dry-run
```

The batch command creates or updates this hierarchy in the configured space:

```text
CLAUDE Capstone Project
└── AI Expense Advisor
  ├── Requirements
  ├── Architecture
  ├── Design Review
  ├── Sprint Plans
  ├── Test Reports
  ├── Release Notes
  └── Audit Reports
```

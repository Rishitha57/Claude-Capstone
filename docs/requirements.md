# AI-Expense-Advisor Requirements

## US-001: Transaction Ingestion

**ID:** US-001  
**Title:** Transaction Ingestion

**As a** user, **I want** to upload transactions, **so that** my spending is tracked automatically.

### Acceptance criteria

- CSV upload is supported.
- JSON upload is supported.
- Input is validated and malformed records do not crash the ingestion batch.
- Transactions are automatically categorized.
- Validated transactions are stored for subsequent spending analysis. **Status:** pending storage-contract and authorization approval.

### Detailed behavior

- Empty input returns an empty list.
- JSON arrays, JSON envelopes, and Plaid-style JSON are supported.
- Each normalized transaction contains date, description, amount, currency, merchant, category, and source.
- Missing optional values receive safe defaults.
- Common merchants are categorized into Groceries, Entertainment, Food & Drink, Transportation, Housing, Health, or Other.

## US-002: Budget Alerts and AI Advisor

**ID:** US-002  
**Title:** Budget Alerts and AI Advisor

**As a** user, **I want** personalized budget insights, **so that** I can improve spending habits.

### Acceptance criteria

- Budget thresholds can be configured by spending category and period.
- Alerts are generated when spending reaches or exceeds a configured threshold.
- RAG recommendations use approved financial guidance and include source references.
- Spending trends are analyzed over defined periods and categories.

### Detailed behavior

- Budget arithmetic remains deterministic and independently testable.
- Personal transaction data is not sent to external providers without explicit configuration and consent.
- When no relevant guidance is found, the advisor says so and does not invent citations.
- Recommendations remain informational and are not presented as regulated financial advice.

## Non-functional requirements

- Secrets are read from environment variables and excluded from Git.
- Core financial calculations maintain at least 90% test coverage.
- Public Python functions use type hints and docstrings.
- Confluence publishing is opt-in and reports failures without logging credentials.

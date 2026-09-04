# AI-Expense-Advisor Architecture

## Components

1. **Ingestion** normalizes CSV, JSON, and Plaid-style records into a stable transaction schema.
2. **Budget service** aggregates transactions by category and period, then emits threshold alerts.
3. **Knowledge service** indexes approved financial guidance and retrieves relevant passages with citations.
4. **Advisor** combines budget status and retrieved passages into a bounded response; it does not provide regulated financial advice.
5. **Documentation publisher** uses Confluence Cloud REST API to upsert requirements, design artifacts, and workflow reports.

## Data flow

```text
Input files/API -> Ingestion -> normalized transactions -> Budget service -> alerts
                                      |                         |
                                      +-> Knowledge retrieval -> Advisor response

SDLC artifacts -> HTML templates -> Confluence publisher -> Confluence space
```

## Integration boundary

Confluence access is disabled until `CONFLUENCE_BASE_URL`, `CONFLUENCE_SPACE_KEY`, `CONFLUENCE_EMAIL`, and `CONFLUENCE_API_TOKEN` are configured. The API token is sent only in the Authorization header and is never included in logs or page content.

Pages are located by space key and title. Existing pages are updated with an incremented version; missing pages are created beneath `CONFLUENCE_PARENT_PAGE_ID` when supplied.

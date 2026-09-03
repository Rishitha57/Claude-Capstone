# AI Expense Advisor Agentic SDLC Capstone Project using GitHub Copilot

## Purpose

Automates:

- Transaction ingestion
- Budget monitoring
- Spending analysis
- Recommendation generation
- Confluence documentation publishing

## Project Structure

```text
app/
tests/
docs/
scripts/
```

## Run

```bash
pip install -r requirements.txt
pytest
python scripts/publish_all_confluence.py
```

## Agentic SDLC Artifacts

- `requirements.md`
- `architecture.md`
- `design-review.md`
- `review-report.md`
- `impl-plan.md`
- `test-report.md`
- `pr-description.md`
- `release-notes.md`

## Confluence Configuration

Publishing requires `CONFLUENCE_BASE_URL`, `CONFLUENCE_SPACE_KEY`,
`CONFLUENCE_EMAIL`, and `CONFLUENCE_API_TOKEN` in `.env`. Never commit `.env`
or include credentials in documentation.

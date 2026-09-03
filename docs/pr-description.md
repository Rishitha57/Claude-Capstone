# Pull Request: Add Agentic SDLC and Confluence Documentation Sync

## Summary

Adds the AI-Expense-Advisor Agentic SDLC documentation workflow and an optional Confluence Cloud publishing integration. The change delivers resilient US-001 transaction ingestion, structured requirements and architecture artifacts, Confluence-ready reports, and automated unit, integration, and end-to-end tests.

US-002 budget alerts and RAG implementation remains intentionally out of scope until the architecture-review gates are approved.

## Changes Made

- Added resilient CSV, JSON, and Plaid-style transaction normalization in `app/transaction_ingestion.py`.
- Added typed, environment-configured Confluence page create/update support in `app/confluence_publisher.py`.
- Added the publishing CLI at `scripts/publish_confluence.py`.
- Added unit tests for normalization, malformed input, missing fields, source preservation, and Confluence request behavior.
- Added integration coverage across CSV, JSON, and Plaid input formats.
- Added an E2E test that invokes the publishing CLI against a local HTTP Confluence stub.
- Added requirements, architecture, design review, implementation plan, API documentation, and HTML report templates under `docs/`.
- Updated the SDLC workflow command, workflow state context, README, environment example, and Git ignore rules.
- Added `pytest.ini` so the repository package is importable during test execution.

## Test Evidence

Command:

```text
pytest -q
```

Result:

```text
9 passed
```

Additional checks:

- Python compilation passed.
- Static diagnostics reported no errors.
- `git diff --check` passed.
- Coverage target: 90% for core financial calculations. A numeric coverage report is pending because `coverage` was not available in the original verification environment.

## Known Limitations

- US-002 budget alerts, vector retrieval, and advisor response generation are not implemented; they remain blocked by the approved design-review gates.
- Live Confluence publishing was not tested against an Atlassian tenant; the API contract is tested against a local HTTP stub.
- Confluence network failures beyond HTTP errors still need explicit handling.
- Input validation currently covers empty page titles and parser resilience, but not upload size limits or full schema validation.
- No production database, authentication, tenant isolation, retention workflow, or deployment pipeline is included in this PR.
- The vulnerability scanner could not run because `pip-audit` is not installed.

## Reviewer Checklist

- [ ] Requirements in `docs/requirements.md` are implemented or explicitly listed as blocked.
- [ ] Architecture and design-review decisions are reflected in the code.
- [ ] Secrets remain environment-based and `.env` is excluded from Git.
- [ ] Input validation and failure behavior are acceptable for the approved scope.
- [ ] Unit, integration, and E2E tests pass.
- [ ] Coverage is measured and reaches the 90% target for core financial calculations.
- [ ] Dependency vulnerability scanning is completed.
- [ ] Confluence page creation and update behavior is approved.
- [ ] Lens code review is complete before merge.

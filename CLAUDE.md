# CLAUDE.md - AI-Expense-Advisor Agentic SDLC Project

## Capstone Overview: Automated Documentation Sync & Confluence Integration

This project follows an 8-step Agentic SDLC pipeline driven by Claude agent personas, rules, and commands:

- **Step 1: Requirements**: `docs/requirements/requirements.md`
- **Step 2: Architecture**: `docs/architecture/architecture.md`
- **Step 3: Design Review**: `docs/design/design-review.md`
- **Step 4: Implementation Planning**: `docs/plans/impl-plan.md`
- **Step 5: Implementation**: US-001 Transaction Ingestion and US-002 Budget Alerts & RAG
- **Step 6: Review**: code quality and security review checklist
- **Step 7: Verify**: test suite and output verification
- **Step 8: PR & Confluence Sync**: PR generation and Confluence reporting

## Confluence Integration

- User stories are synchronized from and to Confluence when the integration is configured.
- Final workflow and verification reports are published to Confluence pages.
- Publishing uses `scripts/publish_all_confluence.py` and is disabled until the required environment variables are configured.
- Secrets must remain in `.env` and must never appear in source files, reports, logs, or commits.

## Project Scope

- **US-001**: Transaction ingestion from CSV, JSON, and Plaid-style data with validation and categorization.
- **US-002**: Deterministic budget alerts, spending trend analysis, and citation-backed advisor recommendations.

## SDLC Agent Workflow

All development follows the agent personas in `.claude/agents/`. Run the workflow instructions from `.claude/commands/run-sdlc-workflow.md`.

## Coding Standards

- Use strict Python typing and document public functions with docstrings.
- Keep budget arithmetic deterministic and independently testable.
- Handle malformed transaction input without unhandled batch exceptions.
- Maintain at least 90% coverage for core financial calculations.
- Run `.claude/hooks/check-secrets.sh` before committing staged changes.

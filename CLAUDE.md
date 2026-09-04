# CLAUDE.md - AI-Expense-Advisor Agentic SDLC Project

## Capstone Overview: Automated Documentation Sync & Confluence Integration

This project follows a 7-stage Agentic SDLC pipeline driven by agent personas and workflow commands:

- **Stage 1: Requirements**: `docs/requirements.md`
- **Stage 2: Architecture and Design Review**: `docs/architecture.md` and `docs/design-review.md`
- **Stage 3: Planning**: `docs/impl-plan.md`
- **Stage 4: Implementation**: US-001 Transaction Ingestion and US-002 Budget Alerts & RAG
- **Stage 5: Testing and Review**: `docs/test-report.md` and `docs/review-report.md`
- **Stage 6: Deployment and Audit**: `docs/workflow-report-WF-2026-001.html`
- **Stage 7: Confluence Sync**: `scripts/publish_all_confluence.py`

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

When using Claude Code, start it from the repository root with `claude`.
Claude loads this file and the project-local `.claude/` commands automatically.
Use `/run-project` to run the self-contained verification workflow. Use
`/run-sdlc-workflow` to advance the approval-gated SDLC stages.

## Coding Standards

- Use strict Python typing and document public functions with docstrings.
- Keep budget arithmetic deterministic and independently testable.
- Handle malformed transaction input without unhandled batch exceptions.
- Maintain at least 90% coverage for core financial calculations.
- Keep credentials in environment variables and never commit `.env`.

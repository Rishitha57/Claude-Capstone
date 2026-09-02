# CLAUDE.md - AI-Expense-Advisor Project Guidelines

## Project Overview
AI-Powered Personal Finance Tracker & Expense Advisor featuring:
- **US-001**: Transaction Ingestion (CSV/JSON/Plaid mock stream parsing & categorization).
- **US-002**: Budget Alerts & RAG (Context-aware spending analysis, RAG knowledge base for financial advice).

## SDLC Agent Workflow
All development follows the 9-agent persona pipeline located in `.claude/agents/`.
Run the workflow command via: `.claude/commands/run-sdlc-workflow.md`.

## Coding Standards
- Strict adherence to TypeScript / Python best practices.
- Zero unhandled exceptions in transaction parsing.
- Secure secret handling (No hardcoded API keys; verified via `.claude/hooks/check-secrets.sh`).

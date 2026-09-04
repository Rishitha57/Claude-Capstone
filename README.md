# AI Expense Advisor

GitHub Copilot Agentic SDLC Capstone Project.

## Business Objective

Provide automated spending analysis and budgeting recommendations using AI-assisted workflows.

---

## User Stories

### US-001

Transaction ingestion and categorization.

### US-002

Budget alerts and AI-powered spending recommendations.

---

## SDLC Deliverables

✅ Requirements

✅ Architecture

✅ Design Review

✅ Implementation Plan

✅ Development

✅ Testing

✅ Verification

✅ PR Preparation

✅ Confluence Publication

---

## Project Structure

```text
app/
tests/
docs/
scripts/
.claude/
```

---

## Run Tests

```bash
pytest -v
```

## Verify the workflow

Install the development tools and run every local verification gate:

```bash
python -m pip install -r requirements-dev.txt
python scripts/verify_workflow.py
```

The verifier runs tests, core budget coverage, `pip-audit`, and an offline
Confluence publication check. Live publication is optional and requires the
`CONFLUENCE_*` environment variables described in `docs/api.md`.

Approval gates are recorded locally in `.claude/context/workflow-context.json`:

```powershell
python scripts/workflow_approval.py submit implementation
python scripts/workflow_approval.py approve implementation --reviewer "Name"
```

To run the workflow interactively, with a pause requiring your approval before
each next stage:

```powershell
python scripts/run_workflow.py --reviewer "Your Name"
```

---

## Publish Documentation

```bash
python scripts/publish_all_confluence.py
```

## Run with Claude CLI

Install Claude Code using the official Anthropic installer, then open a new
PowerShell window and run Claude from this repository root:

```powershell
cd C:\SDLC-CLAUDE
claude
```

Claude Code automatically reads `CLAUDE.md`, the `.claude/agents/` personas,
the `.claude/commands/` slash commands, and the project MCP configuration.
Inside Claude, use `/run-project` for local verification or
`/run-sdlc-workflow` for the staged Agentic SDLC process. The MCP configuration
contains no database credentials; the application does not require a database
to run locally.

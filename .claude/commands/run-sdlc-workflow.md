# Command: /run-sdlc-workflow

Execute the end-to-end SDLC workflow for the AI-Expense-Advisor capstone project and synchronize its artifacts to Confluence when configured.

## Execution Steps:
1. **Requirements**: `sage-business-analyst` validates US-001 and US-002 in `docs/requirements.md`.
2. **Architecture**: `nexus-solution-architect` and `aria-solution-engineer` maintain `docs/architecture.md` and `docs/design-review.md`.
3. **Planning and Branching**: `branch-git-planner` records dependency order in `docs/impl-plan.md`.
4. **Implementation**: `forge-developer` implements ingestion, budgets, and approved-source RAG behavior.
5. **Testing and Review**: `shield-automation-tester` runs tests; `lens-code-reviewer` checks correctness, security, and coverage.
6. **Deployment and Audit**: `deploy-build-engineer` builds artifacts; `chronicle-auditor` updates `docs/workflow-report-WF-2026-001.html` and workflow state.
7. **Confluence Sync**: `confluence-publisher` runs `python scripts/publish_all_confluence.py` to publish Requirements, Architecture, Design Review, Implementation Plan, Test Report, Release Notes, and Workflow Audit Report. Use `--dry-run` when credentials are unavailable; live synchronization is skipped until Confluence environment variables are configured.

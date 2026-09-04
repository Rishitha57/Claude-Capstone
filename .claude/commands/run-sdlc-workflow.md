# Command: /run-sdlc-workflow

Execute the end-to-end SDLC workflow for the AI-Expense-Advisor capstone project and synchronize its artifacts to Confluence when configured.

Every stage is a human approval gate. After completing a stage, submit it for
review and wait for an explicit approval or rejection:

```powershell
python scripts/workflow_approval.py submit requirements
python scripts/workflow_approval.py approve requirements --reviewer "Name"
python scripts/workflow_approval.py reject requirements --reviewer "Name" --reason "Required revision"
```

Rejected stages must be corrected and submitted again. A stage cannot be
approved or rejected before it is submitted. Decisions and review history are
stored in `.claude/context/workflow-context.json`.

When the user asks to run this workflow, do not advance silently. Stop after
each stage, show the generated artifacts and current status, and ask exactly:
**"Approve this stage and continue?"** Wait for the user's response. On
approval, continue to the next stage. On rejection, record the reason and stop
until the stage is corrected and resubmitted. The local interactive runner is:

```powershell
python scripts/run_workflow.py --reviewer "Your Name"
```

## Execution Steps:
1. **Requirements**: `business-analyst` validates US-001 and US-002 in `docs/requirements.md`.
2. **Architecture**: `solution-architect` maintains `docs/architecture.md` and `docs/design-review.md`.
3. **Planning and Branching**: `developer` records dependency order in `docs/impl-plan.md`.
4. **Implementation**: `developer` implements ingestion, budgets, and approved-source RAG behavior.
5. **Testing and Review**: `tester` runs `python scripts/verify_workflow.py`, which checks tests, core coverage, dependency vulnerabilities, secret scanning, and offline publication.
6. **Deployment and Audit**: The workflow owner updates `docs/workflow-report-WF-2026-001.html` and workflow state.
7. **Confluence Sync**: `confluence-publisher` runs `python scripts/publish_all_confluence.py` to publish Requirements, Architecture, Design Review, Implementation Plan, Test Report, Release Notes, and Workflow Audit Report. Use `--dry-run` when credentials are unavailable; live synchronization is skipped until Confluence environment variables are configured.

The local runner is intentionally self-contained: Copilot personas perform
artifact edits, while the repository scripts enforce verification and persist
gate decisions. No external orchestrator or Confluence tenant is required for
the local workflow.

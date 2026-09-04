"""Human approval gates for the staged SDLC workflow."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APPROVAL_PENDING = "AWAITING_APPROVAL"
APPROVED = "APPROVED"
REJECTED = "REJECTED"
STAGE_ORDER = (
    "requirements",
    "architecture",
    "planning",
    "implementation",
    "testing-review",
    "deployment-audit",
    "confluence-sync",
)


class WorkflowApprovalError(ValueError):
    """Raised when a requested workflow transition is invalid."""


def load_context(context_path: Path) -> dict[str, Any]:
    """Load and validate a workflow context JSON document."""
    try:
        context = json.loads(context_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise WorkflowApprovalError(f"Unable to load workflow context: {error}") from error
    if not isinstance(context, dict) or not isinstance(context.get("stages"), list):
        raise WorkflowApprovalError("Workflow context must contain a stages list")
    return context


def save_context(context_path: Path, context: dict[str, Any]) -> None:
    """Persist workflow context as readable, deterministic JSON."""
    context_path.write_text(
        json.dumps(context, indent=2) + "\n",
        encoding="utf-8",
    )


def _stage(context: dict[str, Any], stage_name: str) -> dict[str, Any]:
    for stage in context["stages"]:
        if stage.get("name") == stage_name:
            return stage
    raise WorkflowApprovalError(f"Unknown workflow stage: {stage_name}")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def submit_stage(context: dict[str, Any], stage_name: str) -> dict[str, Any]:
    """Submit a completed stage for human approval."""
    stage = _stage(context, stage_name)
    if stage_name in STAGE_ORDER:
        stage_index = STAGE_ORDER.index(stage_name)
        incomplete = [
            previous
            for previous in context["stages"]
            if previous.get("name") in STAGE_ORDER[:stage_index]
            and previous.get("status") != APPROVED
        ]
        if incomplete:
            raise WorkflowApprovalError(
                f"Stage '{stage_name}' is blocked by: {', '.join(previous['name'] for previous in incomplete)}"
            )
    if stage.get("status") not in {"IN_PROGRESS", REJECTED}:
        raise WorkflowApprovalError(
            f"Stage '{stage_name}' must be IN_PROGRESS or REJECTED before submission"
        )
    stage["status"] = APPROVAL_PENDING
    stage["submitted_at"] = _timestamp()
    stage.pop("rejection_reason", None)
    return stage


def approve_stage(
    context: dict[str, Any], stage_name: str, reviewer: str
) -> dict[str, Any]:
    """Approve a stage awaiting human review and record the reviewer."""
    if not reviewer.strip():
        raise WorkflowApprovalError("A reviewer is required for approval")
    stage = _stage(context, stage_name)
    if stage.get("status") != APPROVAL_PENDING:
        raise WorkflowApprovalError(
            f"Stage '{stage_name}' must be awaiting approval before approval"
        )
    reviewed_at = _timestamp()
    stage.update(
        {
            "status": APPROVED,
            "approved_by": reviewer.strip(),
            "approved_at": reviewed_at,
        }
    )
    _record_review(stage, "approved", reviewer.strip(), reviewed_at)
    return stage


def reject_stage(
    context: dict[str, Any], stage_name: str, reviewer: str, reason: str
) -> dict[str, Any]:
    """Reject a stage awaiting human review and record an actionable reason."""
    if not reviewer.strip():
        raise WorkflowApprovalError("A reviewer is required for rejection")
    if not reason.strip():
        raise WorkflowApprovalError("A rejection reason is required")
    stage = _stage(context, stage_name)
    if stage.get("status") != APPROVAL_PENDING:
        raise WorkflowApprovalError(
            f"Stage '{stage_name}' must be awaiting approval before rejection"
        )
    reviewed_at = _timestamp()
    stage.update(
        {
            "status": REJECTED,
            "rejected_by": reviewer.strip(),
            "rejected_at": reviewed_at,
            "rejection_reason": reason.strip(),
        }
    )
    _record_review(stage, "rejected", reviewer.strip(), reviewed_at, reason.strip())
    return stage


def _record_review(
    stage: dict[str, Any],
    decision: str,
    reviewer: str,
    reviewed_at: str,
    reason: str | None = None,
) -> None:
    history = stage.setdefault("approval_history", [])
    event: dict[str, str] = {
        "decision": decision,
        "reviewer": reviewer,
        "timestamp": reviewed_at,
    }
    if reason is not None:
        event["reason"] = reason
    history.append(event)
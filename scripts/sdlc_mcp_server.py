"""MCP tools for the human-approved local SDLC workflow."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP

from app.workflow_approval import (
    APPROVAL_PENDING,
    APPROVED,
    WorkflowApprovalError,
    approve_stage,
    load_context,
    reject_stage,
    save_context,
    submit_stage,
)

CONTEXT_PATH = ROOT / ".claude" / "context" / "workflow-context.json"
mcp = FastMCP("sdlc-workflow-engine")


def _context() -> dict[str, Any]:
    """Load the repository workflow context."""
    return load_context(CONTEXT_PATH)


def _result(context: dict[str, Any], stage: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a compact, JSON-safe workflow response."""
    result: dict[str, Any] = {
        "workflow_id": context.get("workflow_id"),
        "status": context.get("status"),
        "current_stage": context.get("current_stage"),
        "stages": [
            {"name": item.get("name"), "status": item.get("status")}
            for item in context["stages"]
        ],
    }
    if stage is not None:
        result["stage"] = stage
    return result


@mcp.tool()
def workflow_status() -> dict[str, Any]:
    """Return the current status of every SDLC stage."""
    return _result(_context())


@mcp.tool()
def execute_sdlc_workflow() -> dict[str, Any]:
    """Start or resume the workflow and return the next human approval gate."""
    context = _context()
    try:
        next_stage = next(
            (
                stage
                for stage in context["stages"]
                if stage.get("status") not in {APPROVED, "OPTIONAL", "COMPLETED"}
            ),
            None,
        )
        if next_stage is None:
            return {
                **_result(context),
                "message": "Workflow is complete; no human approval is pending.",
            }

        if next_stage.get("status") in {"IN_PROGRESS", "REJECTED"}:
            submit_stage(context, str(next_stage["name"]))
            save_context(CONTEXT_PATH, context)
        return {
            **_result(context, next_stage),
            "message": "Review the stage artifacts, then approve or reject this stage.",
            "approval_required": True,
            "approval_status": APPROVAL_PENDING,
        }
    except (OSError, WorkflowApprovalError) as error:
        return {"ok": False, "error": str(error)}


@mcp.tool()
def submit_workflow_stage(stage_name: str) -> dict[str, Any]:
    """Submit a completed stage for human approval."""
    context = _context()
    try:
        stage = submit_stage(context, stage_name)
        save_context(CONTEXT_PATH, context)
        return _result(context, stage)
    except (OSError, WorkflowApprovalError) as error:
        return {"ok": False, "error": str(error)}


@mcp.tool()
def approve_workflow_stage(stage_name: str, reviewer: str) -> dict[str, Any]:
    """Approve a stage that is awaiting explicit human review."""
    context = _context()
    try:
        stage = approve_stage(context, stage_name, reviewer)
        save_context(CONTEXT_PATH, context)
        return _result(context, stage)
    except (OSError, WorkflowApprovalError) as error:
        return {"ok": False, "error": str(error)}


@mcp.tool()
def reject_workflow_stage(stage_name: str, reviewer: str, reason: str) -> dict[str, Any]:
    """Reject a stage and record the reviewer's actionable reason."""
    context = _context()
    try:
        stage = reject_stage(context, stage_name, reviewer, reason)
        save_context(CONTEXT_PATH, context)
        return _result(context, stage)
    except (OSError, WorkflowApprovalError) as error:
        return {"ok": False, "error": str(error)}


@mcp.tool()
def run_verification() -> dict[str, Any]:
    """Run the repository's complete offline verification workflow."""
    completed = subprocess.run(
        [sys.executable, "scripts/verify_workflow.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "output": completed.stdout + completed.stderr,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

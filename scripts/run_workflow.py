"""Run the local workflow with an explicit human decision at every gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.workflow_approval import (  # noqa: E402
    APPROVAL_PENDING,
    APPROVED,
    REJECTED,
    WorkflowApprovalError,
    approve_stage,
    load_context,
    reject_stage,
    save_context,
    submit_stage,
)


def _next_stage(context: dict[str, object]) -> dict[str, object] | None:
    """Return the first workflow stage that is not approved."""
    stages = context["stages"]
    assert isinstance(stages, list)
    for stage in stages:
        assert isinstance(stage, dict)
        if stage.get("status") != APPROVED and stage.get("status") != "OPTIONAL":
            return stage
    return None


def _ask(prompt: str) -> str:
    """Read one human decision from the interactive terminal."""
    return input(prompt).strip().lower()


def main(argv: list[str] | None = None) -> int:
    """Advance one stage at a time, requiring approval before continuation."""
    parser = argparse.ArgumentParser(description="Run the SDLC workflow with human gates")
    parser.add_argument(
        "--context",
        type=Path,
        default=Path(".claude/context/workflow-context.json"),
        help="Path to workflow context JSON",
    )
    parser.add_argument("--reviewer", required=True, help="Name recorded for approvals")
    args = parser.parse_args(argv)

    try:
        context = load_context(args.context)
        while True:
            stage = _next_stage(context)
            if stage is None:
                print("Workflow complete: all required stages are approved.")
                return 0

            name = str(stage["name"])
            print(f"\nStage: {name}")
            print(f"Current status: {stage.get('status')}")
            print("Artifacts:")
            for artifact in stage.get("artifacts", []):
                print(f"  - {artifact}")

            if stage.get("status") == REJECTED:
                print(f"Previous rejection: {stage.get('rejection_reason', 'none')}")
            elif stage.get("status") == "IN_PROGRESS":
                submit_stage(context, name)
                save_context(args.context, context)
                print("Stage submitted for approval.")

            decision = _ask("Approve this stage and continue? [approve/reject/quit]: ")
            if decision == "approve":
                if stage.get("status") != APPROVAL_PENDING:
                    submit_stage(context, name)
                approve_stage(context, name, args.reviewer)
                save_context(args.context, context)
                print(f"Approved: {name}")
            elif decision == "reject":
                reason = input("Rejection reason: ").strip()
                if stage.get("status") != APPROVAL_PENDING:
                    submit_stage(context, name)
                reject_stage(context, name, args.reviewer, reason)
                save_context(args.context, context)
                print(f"Rejected: {name}. The workflow will stop for correction.")
                return 1
            elif decision in {"quit", "q", "no", "n"}:
                print("Workflow paused. No later stage was started.")
                return 2
            else:
                print("Enter approve, reject, or quit.")
    except (EOFError, KeyboardInterrupt):
        print("\nWorkflow paused. No later stage was started.", file=sys.stderr)
        return 2
    except (OSError, WorkflowApprovalError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
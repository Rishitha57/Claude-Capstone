"""Command-line interface for human workflow stage approvals."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.workflow_approval import (
    WorkflowApprovalError,
    approve_stage,
    load_context,
    reject_stage,
    save_context,
    submit_stage,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the workflow approval command-line parser."""
    parser = argparse.ArgumentParser(description="Manage SDLC human approval gates")
    parser.add_argument(
        "--context",
        type=Path,
        default=Path(".claude/context/workflow-context.json"),
        help="Path to workflow context JSON",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("submit", "approve"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("stage")
        if command == "approve":
            command_parser.add_argument("--reviewer", required=True)

    reject_parser = subparsers.add_parser("reject")
    reject_parser.add_argument("stage")
    reject_parser.add_argument("--reviewer", required=True)
    reject_parser.add_argument("--reason", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run a submit, approve, or reject workflow transition."""
    args = build_parser().parse_args(argv)
    try:
        context = load_context(args.context)
        if args.command == "submit":
            stage = submit_stage(context, args.stage)
        elif args.command == "approve":
            stage = approve_stage(context, args.stage, args.reviewer)
        else:
            stage = reject_stage(context, args.stage, args.reviewer, args.reason)
        save_context(args.context, context)
    except (OSError, WorkflowApprovalError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"{args.command}: {stage['name']} -> {stage['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
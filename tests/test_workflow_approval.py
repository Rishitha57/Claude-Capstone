import json

import pytest

from scripts.run_workflow import main as run_workflow
from app.workflow_approval import (
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


def make_context():
    return {"stages": [{"name": "requirements", "status": "IN_PROGRESS"}]}


def test_submit_then_approve_records_reviewer_and_history():
    context = make_context()

    submit_stage(context, "requirements")
    stage = approve_stage(context, "requirements", "reviewer@example.com")

    assert stage["status"] == APPROVED
    assert stage["approved_by"] == "reviewer@example.com"
    assert stage["approval_history"][0]["decision"] == "approved"


def test_rejection_requires_reason_and_can_be_resubmitted():
    context = make_context()
    submit_stage(context, "requirements")

    with pytest.raises(WorkflowApprovalError, match="reason"):
        reject_stage(context, "requirements", "reviewer", " ")

    stage = reject_stage(context, "requirements", "reviewer", "Add acceptance criteria")
    assert stage["status"] == REJECTED
    submit_stage(context, "requirements")
    assert context["stages"][0]["status"] == APPROVAL_PENDING


def test_approval_is_blocked_until_submission():
    with pytest.raises(WorkflowApprovalError, match="awaiting approval"):
        approve_stage(make_context(), "requirements", "reviewer")


def test_unknown_stage_is_rejected():
    with pytest.raises(WorkflowApprovalError, match="Unknown workflow stage"):
        submit_stage(make_context(), "missing")


def test_submission_requires_previous_stage_approval():
    context = {
        "stages": [
            {"name": "requirements", "status": "IN_PROGRESS"},
            {"name": "architecture", "status": "IN_PROGRESS"},
        ]
    }

    with pytest.raises(WorkflowApprovalError, match="requirements"):
        submit_stage(context, "architecture")


def test_context_round_trip(tmp_path):
    path = tmp_path / "workflow.json"
    context = make_context()
    save_context(path, context)

    assert load_context(path) == json.loads(path.read_text(encoding="utf-8"))


def test_interactive_runner_requires_approval_before_next_stage(tmp_path, monkeypatch, capsys):
    path = tmp_path / "workflow.json"
    save_context(
        path,
        {
            "stages": [
                {"name": "requirements", "status": "IN_PROGRESS", "artifacts": []},
                {"name": "architecture", "status": "IN_PROGRESS", "artifacts": []},
            ]
        },
    )
    answers = iter(["approve", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert run_workflow(["--context", str(path), "--reviewer", "reviewer"]) == 2
    output = capsys.readouterr().out
    assert "Approved: requirements" in output
    assert "Workflow paused" in output
    assert load_context(path)["stages"][0]["status"] == APPROVED
    assert load_context(path)["stages"][1]["status"] == APPROVAL_PENDING


def test_interactive_runner_records_rejection_reason(tmp_path, monkeypatch):
    path = tmp_path / "workflow.json"
    save_context(path, {"stages": [{"name": "requirements", "status": "IN_PROGRESS"}]})
    answers = iter(["reject", "Missing acceptance criteria"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert run_workflow(["--context", str(path), "--reviewer", "reviewer"]) == 1
    stage = load_context(path)["stages"][0]
    assert stage["status"] == REJECTED
    assert stage["rejection_reason"] == "Missing acceptance criteria"
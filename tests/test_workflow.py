"""Automated tests for the mock LangGraph workflow."""

from __future__ import annotations

import os

os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from app.workflow import build_workflow, demo_input, qc_is_current


def config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def test_happy_path_pauses_for_owner_and_resumes_after_reopening_db(tmp_path):
    db = tmp_path / "checkpoints.sqlite"
    thread_id = "test-happy-path"

    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["PASS"]), config(thread_id))
        snapshot = graph.get_state(config(thread_id))
        assert snapshot.next == ("owner_approval",)
        assert snapshot.values["qc_status"] == "PASS"
        assert snapshot.values["workflow_status"] == "RUNNING"

    # Reopen the same database to prove the interrupt/checkpoint survives process lifetime.
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(Command(resume={"decision": "approved"}), config(thread_id))
        final = graph.get_state(config(thread_id)).values
        assert final["workflow_status"] == "SIMULATED_COMPLETE"
        assert final["approval"]["decision"] == "approved"
        assert final["publication"]["status"] == "SIMULATED_ONLY_NOT_PUBLISHED"


def test_revision_creates_new_render_and_requires_new_qc(tmp_path):
    db = tmp_path / "revision.sqlite"
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["REVISE", "PASS"]), config("test-revision"))
        state = graph.get_state(config("test-revision")).values
        assert state["revision_attempts"] == 1
        assert state["video_version"] == 2
        assert state["qc_status"] == "PASS"
        assert state["qc_report"]["video_version"] == 2
        assert qc_is_current(state)
        assert graph.get_state(config("test-revision")).next == ("owner_approval",)


def test_three_automatic_revisions_then_escalation(tmp_path):
    db = tmp_path / "max-revisions.sqlite"
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["REVISE", "REVISE", "REVISE", "REVISE"]), config("test-max-revisions"))
        state = graph.get_state(config("test-max-revisions")).values
        assert state["revision_attempts"] == 3
        assert state["video_version"] == 4
        assert state["workflow_status"] == "NEEDS_HUMAN_REVIEW"
        assert "approval" not in state
        assert "publication" not in state


def test_qc_fail_never_reaches_owner_approval_or_publish(tmp_path):
    db = tmp_path / "qc-fail.sqlite"
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["FAIL"]), config("test-qc-fail"))
        state = graph.get_state(config("test-qc-fail")).values
        assert state["workflow_status"] == "NEEDS_HUMAN_REVIEW"
        assert "approval" not in state
        assert "publication" not in state


def test_owner_rejection_never_publishes(tmp_path):
    db = tmp_path / "reject.sqlite"
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["PASS"]), config("test-reject"))
        graph.invoke(Command(resume={"decision": "rejected"}), config("test-reject"))
        state = graph.get_state(config("test-reject")).values
        assert state["workflow_status"] == "REJECTED"
        assert "publication" not in state


def test_invalid_approval_payload_is_rejected(tmp_path):
    db = tmp_path / "invalid-approval.sqlite"
    with SqliteSaver.from_conn_string(str(db)) as saver:
        graph = build_workflow(saver)
        graph.invoke(demo_input(["PASS"]), config("test-invalid-approval"))
        try:
            graph.invoke(Command(resume={"decision": "maybe"}), config("test-invalid-approval"))
        except ValueError as exc:
            assert "decision" in str(exc)
        else:
            raise AssertionError("Invalid approval payload must be rejected.")


def test_qc_report_for_old_version_is_not_current():
    state = {
        "video_id": "video-1",
        "video_version": 2,
        "render_sha256": "new-checksum",
        "render_artifact": {"sha256": "new-checksum"},
        "qc_report": {
            "video_id": "video-1",
            "video_version": 1,
            "artifact_sha256": "old-checksum",
        },
    }
    assert not qc_is_current(state)

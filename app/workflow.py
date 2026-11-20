"""Deterministic LangGraph proof of concept.

All agents and publishing operations in this module are mocks. No real AI provider,
media renderer, social account, or external publishing API is called.
"""

from __future__ import annotations

import hashlib
from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.state import WorkflowState, event

MAX_AUTOMATIC_REVISIONS = 3
VALID_QC_OUTCOMES = {"PASS", "REVISE", "FAIL", "QC_INCOMPLETE", "NEEDS_HUMAN_REVIEW"}


def _render_digest(video_id: str, version: int) -> str:
    payload = f"{video_id}:v{version}:mock-render".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def qc_is_current(state: WorkflowState) -> bool:
    """A QC PASS is valid only for the exact current render version and checksum."""
    report = state.get("qc_report") or {}
    artifact = state.get("render_artifact") or {}
    return bool(
        report.get("video_id") == state.get("video_id")
        and report.get("video_version") == state.get("video_version")
        and report.get("artifact_sha256") == state.get("render_sha256")
        and artifact.get("sha256") == state.get("render_sha256")
    )


def qc_release_eligible(state: WorkflowState) -> bool:
    """Enforce the release score, critical-finding, and inspection-completeness gates."""
    report = state.get("qc_report") or {}
    return bool(
        state.get("qc_status") == "PASS"
        and qc_is_current(state)
        and report.get("score", 0) >= 90
        and not report.get("critical_findings")
        and report.get("inspection_complete") is True
    )


def product_researcher(state: WorkflowState) -> dict[str, Any]:
    name = state.get("product_name", "Unspecified sample product")
    return {
        "product_research": {
            "product_name": name,
            "evidence_status": "MOCK_ONLY",
            "claims": [],
            "note": "Replace with source-backed research before real campaigns.",
        },
        "event_log": [event("agent_completed", agent="product-researcher")],
    }


def trend_scout(state: WorkflowState) -> dict[str, Any]:
    return {
        "trend_report": {
            "trend_status": "MOCK_ONLY",
            "opportunities": [],
            "note": "No live trend source was queried.",
        },
        "event_log": [event("agent_completed", agent="trend-scout")],
    }


def content_strategist(state: WorkflowState) -> dict[str, Any]:
    return {
        "content_strategy": {
            "objective": "Demonstrate the workflow using mock data.",
            "platforms": ["tiktok", "youtube_shorts", "instagram_reels"],
        },
        "event_log": [event("agent_completed", agent="content-strategist")],
    }


def hook_copywriter(state: WorkflowState) -> dict[str, Any]:
    return {
        "script_package": {
            "hooks": ["Mock hook for workflow testing"],
            "script": "This is placeholder copy, not a verified product claim.",
            "disclosure_required": True,
        },
        "event_log": [event("agent_completed", agent="hook-copywriter")],
    }


def creative_director(state: WorkflowState) -> dict[str, Any]:
    return {
        "creative_plan": {
            "scenes": [{"scene": 1, "purpose": "Placeholder storyboard scene"}],
        },
        "event_log": [event("agent_completed", agent="creative-director")],
    }


def voice_talent(state: WorkflowState) -> dict[str, Any]:
    return {
        "voice_package": {
            "audio_artifact": None,
            "status": "MOCK_ONLY_NOT_RENDERED",
        },
        "event_log": [event("agent_completed", agent="voice-talent")],
    }


def video_editor(state: WorkflowState) -> dict[str, Any]:
    version = 1
    digest = _render_digest(state["video_id"], version)
    artifact = {
        "artifact_id": f"mock-render-{state['video_id']}-v{version}",
        "artifact_type": "video_render_mock",
        "version": version,
        "sha256": digest,
        "uri": None,
    }
    return {
        "video_version": version,
        "render_sha256": digest,
        "render_artifact": artifact,
        "event_log": [event("mock_render_created", video_version=version, sha256=digest)],
    }


def quality_control(state: WorkflowState) -> dict[str, Any]:
    outcomes = state.get("qc_outcomes") or ["PASS"]
    cursor = state.get("qc_cursor", 0)
    requested = outcomes[cursor] if cursor < len(outcomes) else "NEEDS_HUMAN_REVIEW"
    outcome = requested.upper()
    if outcome not in VALID_QC_OUTCOMES:
        outcome = "QC_INCOMPLETE"
    version = state["video_version"]
    report = {
        "qc_report_id": f"qc-{state['video_id']}-v{version}-n{cursor + 1}",
        "video_id": state["video_id"],
        "video_version": version,
        "artifact_sha256": state["render_sha256"],
        "status": outcome,
        "score": 100 if outcome == "PASS" else 60,
        "critical_findings": [],
        "inspection_type": "MOCK_WORKFLOW_TEST_ONLY",
        "inspection_complete": outcome == "PASS",
    }
    return {
        "qc_cursor": cursor + 1,
        "qc_status": outcome,
        "qc_report": report,
        "event_log": [event("mock_qc_completed", status=outcome, video_version=version)],
    }


def route_after_qc(state: WorkflowState) -> str:
    status = state.get("qc_status")
    if status == "PASS" and qc_release_eligible(state):
        return "owner_approval"
    if status == "REVISE" and state.get("revision_attempts", 0) < MAX_AUTOMATIC_REVISIONS:
        return "revise_video"
    return "human_review"


def revise_video(state: WorkflowState) -> dict[str, Any]:
    attempt = state.get("revision_attempts", 0) + 1
    return {
        "revision_attempts": attempt,
        "workflow_status": "REVISION_IN_PROGRESS",
        "event_log": [event("revision_started", attempt=attempt, max_attempts=MAX_AUTOMATIC_REVISIONS)],
    }


def rerender_video(state: WorkflowState) -> dict[str, Any]:
    version = state["video_version"] + 1
    digest = _render_digest(state["video_id"], version)
    artifact = {
        "artifact_id": f"mock-render-{state['video_id']}-v{version}",
        "artifact_type": "video_render_mock",
        "version": version,
        "sha256": digest,
        "uri": None,
    }
    return {
        "video_version": version,
        "render_sha256": digest,
        "render_artifact": artifact,
        "event_log": [event("mock_rerender_created", video_version=version, sha256=digest)],
    }


def human_review(state: WorkflowState) -> dict[str, Any]:
    return {
        "workflow_status": "NEEDS_HUMAN_REVIEW",
        "event_log": [
            event(
                "escalated_to_human",
                qc_status=state.get("qc_status"),
                revision_attempts=state.get("revision_attempts", 0),
            )
        ],
    }


def owner_approval(state: WorkflowState) -> dict[str, Any]:
    # Deterministic ID: the node restarts from its beginning after an interrupt.
    approval_id = (
        f"approval:{state['campaign_id']}:{state['video_id']}:"
        f"v{state['video_version']}:{state['render_sha256'][:12]}"
    )
    if not qc_release_eligible(state):
        raise ValueError("Owner approval is locked: latest render does not meet all QC release gates.")

    decision = interrupt(
        {
            "kind": "owner_publication_approval",
            "approval_id": approval_id,
            "campaign_id": state["campaign_id"],
            "video_id": state["video_id"],
            "video_version": state["video_version"],
            "artifact_sha256": state["render_sha256"],
            "qc_report_id": state["qc_report"]["qc_report_id"],
            "message": "Approve or reject this exact mock video version for the simulated publishing step.",
        }
    )
    if not isinstance(decision, dict) or decision.get("decision") not in {"approved", "rejected"}:
        raise ValueError("Approval response must contain decision='approved' or decision='rejected'.")

    approval = {
        "approval_id": approval_id,
        "decision": decision["decision"],
        "video_id": state["video_id"],
        "video_version": state["video_version"],
        "artifact_sha256": state["render_sha256"],
        "qc_report_id": state["qc_report"]["qc_report_id"],
        "actor": "owner_mock",
    }
    return {
        "approval": approval,
        "workflow_status": "APPROVED" if decision["decision"] == "approved" else "REJECTED",
        "event_log": [event("owner_decision_recorded", decision=decision["decision"], approval_id=approval_id)],
    }


def route_after_approval(state: WorkflowState) -> str:
    approval = state.get("approval") or {}
    is_bound_to_current = (
        approval.get("video_id") == state.get("video_id")
        and approval.get("video_version") == state.get("video_version")
        and approval.get("artifact_sha256") == state.get("render_sha256")
        and approval.get("qc_report_id") == (state.get("qc_report") or {}).get("qc_report_id")
    )
    if approval.get("decision") == "approved" and is_bound_to_current and qc_is_current(state):
        return "mock_publish"
    return "stop"


def mock_publish(state: WorkflowState) -> dict[str, Any]:
    """Simulate a publish record; never calls a platform or account."""
    if route_after_approval(state) != "mock_publish":
        raise ValueError("Publishing is blocked without a valid approval for the latest QC-passed render.")
    publication_id = f"mock-publication:{state['video_id']}:v{state['video_version']}"
    return {
        "publication": {
            "publication_id": publication_id,
            "status": "SIMULATED_ONLY_NOT_PUBLISHED",
            "platform": "mock-platform",
        },
        "workflow_status": "SIMULATED_COMPLETE",
        "event_log": [event("mock_publish_simulated", publication_id=publication_id)],
    }


def build_workflow(checkpointer: Any):
    """Compile the deterministic workflow with the supplied persistent checkpointer."""
    builder = StateGraph(WorkflowState)
    builder.add_node("product_researcher", product_researcher)
    builder.add_node("trend_scout", trend_scout)
    builder.add_node("content_strategist", content_strategist)
    builder.add_node("hook_copywriter", hook_copywriter)
    builder.add_node("creative_director", creative_director)
    builder.add_node("voice_talent", voice_talent)
    builder.add_node("video_editor", video_editor)
    builder.add_node("quality_control", quality_control)
    builder.add_node("revise_video", revise_video)
    builder.add_node("rerender_video", rerender_video)
    builder.add_node("human_review", human_review)
    builder.add_node("owner_approval", owner_approval)
    builder.add_node("mock_publish", mock_publish)

    builder.add_edge(START, "product_researcher")
    builder.add_edge("product_researcher", "trend_scout")
    builder.add_edge("trend_scout", "content_strategist")
    builder.add_edge("content_strategist", "hook_copywriter")
    builder.add_edge("hook_copywriter", "creative_director")
    builder.add_edge("creative_director", "voice_talent")
    builder.add_edge("voice_talent", "video_editor")
    builder.add_edge("video_editor", "quality_control")
    builder.add_conditional_edges(
        "quality_control",
        route_after_qc,
        {
            "revise_video": "revise_video",
            "human_review": "human_review",
            "owner_approval": "owner_approval",
        },
    )
    builder.add_edge("revise_video", "rerender_video")
    builder.add_edge("rerender_video", "quality_control")
    builder.add_edge("human_review", END)
    builder.add_conditional_edges(
        "owner_approval",
        route_after_approval,
        {"mock_publish": "mock_publish", "stop": END},
    )
    builder.add_edge("mock_publish", END)
    return builder.compile(checkpointer=checkpointer)


def demo_input(qc_outcomes: list[str] | None = None) -> WorkflowState:
    """Create a safe mock campaign input for local tests and demonstrations."""
    return {
        "campaign_id": "campaign-demo-001",
        "product_id": "product-demo-001",
        "content_id": "content-demo-001",
        "video_id": "video-demo-001",
        "product_name": "Sample product (mock only)",
        "qc_outcomes": [value.upper() for value in (qc_outcomes or ["PASS"])],
        "qc_cursor": 0,
        "revision_attempts": 0,
        "event_log": [],
        "workflow_status": "RUNNING",
    }

"""Shared, JSON-serializable state for the prototype workflow."""

from __future__ import annotations

from operator import add
from typing import Annotated, Any, TypedDict


class WorkflowState(TypedDict, total=False):
    campaign_id: str
    product_id: str
    content_id: str
    video_id: str
    product_name: str
    product_research: dict[str, Any]
    trend_report: dict[str, Any]
    content_strategy: dict[str, Any]
    script_package: dict[str, Any]
    creative_plan: dict[str, Any]
    voice_package: dict[str, Any]
    video_version: int
    render_artifact: dict[str, Any]
    render_sha256: str
    qc_outcomes: list[str]
    qc_cursor: int
    qc_status: str
    qc_report: dict[str, Any]
    revision_attempts: int
    workflow_status: str
    approval: dict[str, Any]
    publication: dict[str, Any]
    event_log: Annotated[list[dict[str, Any]], add]


def event(name: str, **details: Any) -> dict[str, Any]:
    """Return a small serializable audit event."""
    return {"event": name, **details}

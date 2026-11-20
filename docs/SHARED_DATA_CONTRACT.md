# Shared Data Contract — Agent Handoffs

## 1. Purpose

This document defines the common identifiers, handoff envelope, status vocabulary, artifact references, and validation rules shared by the AI Manager and all specialist agents.

Agent-specific README files define domain responsibilities. This document defines how their work is identified, transferred, versioned, and audited.

## 2. Canonical Identifiers

Use stable opaque IDs. UUIDv4 or UUIDv7 are acceptable implementation choices; do not encode personal data or business secrets in IDs.

| Identifier | Meaning | Lifecycle |
|---|---|---|
| `campaign_id` | A coordinated marketing campaign | Across all campaign tasks |
| `product_id` | A researched product or variant | Reused when product identity is unchanged |
| `content_id` | A content idea or creative unit | Across script and creative iterations |
| `video_id` | A video deliverable | Across its production versions |
| `task_id` | One assigned unit of agent work | Unique per task attempt group |
| `run_id` | One execution of a task | Unique per execution |
| `artifact_id` | One immutable stored file or report | Unique per artifact |
| `approval_id` | One human decision | Unique per decision |
| `qc_report_id` | One inspection report | Unique per inspection |
| `publication_id` | One platform publication record | Unique per platform publication |

Never use a filename as the sole identifier.

## 3. Versioning Rules

- Every mutable deliverable must have an explicit integer `version`, starting at 1.
- Published or inspected files must be immutable artifacts.
- A new render creates a new video production version.
- QC approval is bound to the exact `video_id`, `version`, and `artifact_id`.
- A new render invalidates the previous release approval for the new version.
- Revisions must reference the previous version and the findings they address.
- Never overwrite an artifact that has been used for approval, QC, or publication.

## 4. Common Handoff Envelope

Every agent-to-agent handoff must be wrapped in a common envelope. The following is an illustrative JSON shape; implementation validation must use a formal schema.

```json
{
  "contract_version": "1.0",
  "campaign_id": "uuid",
  "product_id": "uuid",
  "content_id": "uuid",
  "video_id": "uuid",
  "task_id": "uuid",
  "run_id": "uuid",
  "producer_agent": "product-researcher",
  "consumer_agent": "trend-scout",
  "deliverable_type": "product_research_report",
  "deliverable_version": 1,
  "status": "completed",
  "created_at": "2026-01-01T00:00:00Z",
  "input_artifacts": [],
  "output_artifacts": [
    {
      "artifact_id": "uuid",
      "artifact_type": "report",
      "uri": "provider://bucket/object",
      "media_type": "application/json",
      "sha256": "hex-digest",
      "size_bytes": 12345
    }
  ],
  "summary": "Evidence-backed product research completed.",
  "warnings": [],
  "unresolved_questions": [],
  "next_action": "validate_and_assign_trend_research"
}
```

Values above are examples, not actual IDs or deployed storage URIs. The implementation must validate required fields and permitted values for each deliverable type.

## 5. Required Envelope Fields

- `contract_version`: schema version.
- `campaign_id`: required for campaign work.
- `task_id` and `run_id`: traceability.
- `producer_agent` and `consumer_agent`: accountable handoff parties.
- `deliverable_type` and `deliverable_version`: typed output and version.
- `status`: task result status.
- `created_at`: UTC timestamp in ISO 8601 format.
- `input_artifacts` and `output_artifacts`: explicit artifact references.
- `summary`: concise result.
- `warnings` and `unresolved_questions`: explicit limitations.
- `next_action`: proposed next workflow action; orchestrator validates it.

Where a field is not applicable, represent it according to the schema's nullable/optional rule. Do not invent placeholder values.

## 6. Artifact Reference Contract

Each artifact record should include:
- `artifact_id`
- `artifact_type`
- `uri` or managed storage key
- `media_type`
- `sha256` checksum
- `size_bytes`
- `created_at`
- `created_by`
- `version`
- `access_classification`
- `retention_policy`, when defined

Artifact URIs must not expose long-lived credentials. Use authenticated access or short-lived signed URLs.

## 7. Status Vocabulary

### Task execution statuses
- `pending`
- `queued`
- `running`
- `completed`
- `blocked`
- `failed`
- `cancelled`
- `needs_human_review`

### QC statuses
- `pass`
- `revise`
- `fail`
- `qc_incomplete`
- `needs_human_review`

### Owner decision statuses
- `pending`
- `approved`
- `rejected`
- `expired`
- `revoked`

### Publication statuses
- `not_ready`
- `awaiting_owner_approval`
- `approved_to_publish`
- `publishing`
- `published`
- `publication_failed`
- `manual_action_required`
- `cancelled`

Do not conflate a completed agent task with an approved QC result or an Owner approval.

## 8. Approval Record

An Owner approval must be an immutable record containing:
- `approval_id`
- `campaign_id`
- `video_id`
- Exact video version and artifact checksum.
- Exact platform and publication metadata package version.
- Decision: approved or rejected.
- Owner identity reference.
- Decision timestamp.
- Optional comment.
- Expiration or revocation metadata, if supported.

Any change to the approved video or material publication metadata requires a new approval.

## 9. QC Binding

A QC report must bind to:
- `qc_report_id`
- `campaign_id`
- `video_id`
- Exact render version and artifact checksum.
- Script and storyboard versions.
- Inspection timestamp.
- Category scores and weighted total.
- Findings with severity and evidence references.
- One QC status.

Only `pass` on the exact latest render may unlock the Owner approval request. The orchestrator enforces this rule; the Manager cannot override it.

## 10. Revision Contract

Every revision task must include:
- Previous video or deliverable version.
- Revision attempt number.
- Maximum attempt count: 3 automatic attempts.
- Finding IDs being addressed.
- Responsible agent.
- Explicit acceptance criteria.
- New output version and artifact reference.

The attempt counter is stored centrally and cannot be reset by an agent. After the third unsuccessful automatic attempt, the workflow escalates to a human.

## 11. Evidence and Data Quality

Research and analytics outputs must distinguish:
- Verified facts.
- Source-backed observations.
- Estimates.
- Hypotheses.
- Recommendations.
- Unknown or unavailable data.

Every material factual claim should include a source reference, retrieval timestamp, and confidence where applicable.

Missing metrics are null/unknown, not zero. Conflicting sources must be recorded and resolved or escalated.

## 12. Validation Rules

The orchestrator must reject or quarantine a handoff when:
- Required identifiers are missing or inconsistent.
- Contract version is unsupported.
- Required artifact references are absent.
- Artifact checksum does not match.
- Deliverable type is not allowed for the producer agent.
- Version regresses or duplicates an immutable version.
- Status is invalid for the workflow stage.
- A required approval or QC gate is missing.
- A handoff attempts to bypass the defined workflow.

Validation errors must be structured, actionable, and traceable.

## 13. Compatibility and Change Management

- Use semantic schema versioning.
- Backward-compatible optional fields may be added in a minor version.
- Breaking changes require a new major contract version and migration plan.
- Agents must declare the contract version they support.
- Keep example payloads and automated schema tests in sync with this document.

## 14. Implementation Note

This is the canonical design contract. Before production use, convert it into machine-validated JSON Schema or equivalent typed models and add positive and negative tests. Documentation alone does not enforce the contract.

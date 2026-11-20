# System Architecture — AI Affiliate Agency Cloud

## 1. Purpose

This document defines the logical architecture for the AI Affiliate Agency Cloud. It is a design contract, not a claim that the system has already been deployed.

The system must run AI inference, orchestration, storage, and video rendering in cloud services. The Owner's Windows PC is primarily a control and monitoring client.

## 2. Architecture Principles

- Cloud-first: local hardware must not be required for model inference or rendering.
- Modular: providers and agents must be replaceable through stable interfaces.
- API-first: every workflow capability must be callable through a documented interface.
- Evidence-first: factual product claims and performance metrics must carry source references.
- Human-governed: publishing and paid actions require explicit authorization.
- Observable: every task, artifact, retry, cost, and state transition must be traceable.
- Resilient: transient provider failures must be retried safely; permanent failures must be escalated.
- Cost-aware: record estimated and actual cost per task and campaign.
- Secure by default: credentials remain server-side and are never committed to Git.

## 3. Logical Components

### 3.1 Owner Control Interface

A web dashboard or lightweight client used to:
- Create and configure campaigns.
- Submit product links and approved assets.
- Review research, scripts, storyboards, and generated outputs.
- Approve or reject publication packages.
- View workflow status, QC reports, cost, and performance.

The interface is not responsible for executing AI workloads locally.

### 3.2 API / Application Backend

The backend is the trusted entry point for:
- Authentication and authorization.
- Campaign and task creation.
- Input validation.
- Workflow commands.
- Artifact metadata.
- Approval records.
- Audit events.
- Dashboard queries.

### 3.3 Workflow Orchestrator

The orchestrator:
- Executes the approved workflow graph.
- Assigns tasks to specialist agents.
- Validates shared handoff envelopes.
- Persists state before and after each task.
- Handles retries, timeouts, cancellation, and escalation.
- Enforces QC and Owner approval gates.

The orchestrator, not an LLM prompt, is the final authority for state transitions and gates.

### 3.4 Agent Runtime

Each specialist agent is a bounded worker with:
- A documented role and input contract.
- A documented output contract.
- Explicit tool permissions.
- Time and cost limits.
- Structured results and errors.
- No authority beyond its assigned responsibility.

The AI Manager coordinates work but does not replace deterministic workflow enforcement.

### 3.5 Provider Adapters

Adapters normalize external services for:
- LLM and reasoning models.
- Product and trend research.
- Text-to-speech and voice generation.
- Image and video generation.
- Video rendering and transcoding.
- Object storage.
- Platform publishing.
- Platform analytics.

Each adapter must declare supported operations, authentication requirements, pricing model, rate limits, data retention, and known limitations.

### 3.6 Data and Artifact Storage

Use a database for structured records and object storage for large files.

Structured records include campaigns, products, tasks, versions, approvals, QC reports, publication records, metrics, and audit events.

Artifacts include source images, generated assets, voice tracks, subtitles, project files, renders, thumbnails, and reports.

Store artifact metadata and immutable references in the database. Do not store large media blobs directly in ordinary relational rows.

## 4. High-Level Workflow

1. Owner creates a campaign and supplies a product URL or product evidence.
2. Product Researcher creates an evidence-backed Product Research Report.
3. Trend Scout evaluates relevant trends and formats.
4. Content Strategist prepares a campaign brief and content ideas.
5. Hook & Copywriter creates versioned script options.
6. Creative Director prepares a storyboard and asset plan.
7. Voice Talent generates approved narration.
8. Video Editor assembles and renders a version.
9. Independent QC Inspector evaluates the exact rendered version.
10. REVISE returns actionable findings to the responsible production stage; each new render receives full QC.
11. A QC PASS on the latest version unlocks the publication approval request.
12. Owner explicitly approves or rejects the exact publication package.
13. Publishing Specialist publishes only through authorized, supported methods, or provides a manual publishing package.
14. Performance Analyst collects available analytics and returns evidence-based insights.

## 5. State and Gate Enforcement

The backend must enforce these invariants:

- No publishing without a recorded Owner approval for the exact video version and platform package.
- No publication-ready state without QC PASS for the exact latest render.
- A new render invalidates the prior render's QC approval.
- The AI Manager cannot modify a QC result.
- Automatic revision attempts are counted centrally and capped at three.
- A workflow cannot silently skip a required stage.
- Missing data is not treated as a successful check or a zero metric.
- External side effects must be idempotent or protected by duplicate-action controls.

## 6. Execution and Reliability

Every task should support:
- Unique task ID and idempotency key.
- Input artifact references and version identifiers.
- Execution timeout.
- Bounded retry policy for transient failures.
- Explicit permanent failure and blocked states.
- Cancellation where safe.
- Structured logs and error codes.
- Cost and usage metadata.
- Start, completion, and last-updated timestamps.

A retry must not duplicate a publication, purchase, or other external side effect.

## 7. Security Boundaries

- Store API keys and OAuth tokens only in an approved secret manager or protected server environment.
- Never commit secrets, cookies, tokens, or private customer data.
- Use least-privilege permissions per agent and provider adapter.
- Validate and scan uploaded files before processing.
- Restrict outbound network access where practical.
- Keep private signed artifact URLs short-lived.
- Record who approved a publication and what exact version was approved.
- Define retention and deletion policies before storing personal data.

## 8. Deployment Shape

The initial deployment may use managed services to reduce operational burden:
- Managed application hosting.
- Managed database.
- Managed object storage.
- Managed queue or workflow service, if needed.
- External AI/media providers through adapters.

Do not select a permanent vendor stack until the tool evaluation and proof-of-concept stages compare cost, API access, reliability, data policy, and portability.

## 9. Observability

Track at minimum:
- Workflow success and failure rates.
- Per-agent latency and error rate.
- Provider rate limits and outages.
- Cost per task, video, and campaign.
- Revision count and reasons.
- QC score distribution and critical failures.
- Approval wait time.
- Publishing success and duplicate prevention.
- Analytics freshness and completeness.

## 10. Current Implementation Status

This repository currently contains project and agent specifications. The architecture described here is a target design. No deployed backend, orchestrator, dashboard, database, cloud renderer, or production provider integration is implied by this document.

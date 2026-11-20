# Development Roadmap

## 1. Delivery Goal

Build a reliable cloud-first AI affiliate content agency that can research products, create short-form content, render videos, inspect quality independently, request revisions, and prepare publishing packages for explicit Owner approval.

The repository currently contains specifications and planning documents. The roadmap below separates design work from working software.

## 2. Delivery Principles

- Build and test in small, reversible increments.
- Reuse maintained open-source projects where their license and capabilities fit.
- Prefer managed cloud services when they reduce operational burden without creating unacceptable lock-in.
- Do not assume a free web interface means free API access.
- Record current pricing, API availability, rate limits, terms, and data policies before selection.
- Never store secrets in Git.
- Never enable automatic publishing before approval enforcement and audit logging are tested.
- Measure actual cost and quality before scaling.

## 3. Phases and Exit Criteria

### Phase 0 — Requirements and Repository Foundation

Deliverables:
- Project Charter.
- System Architecture.
- Shared Data Contract.
- Agent specifications.
- Development roadmap.
- Tool evaluation policy and decision records.

Exit criteria:
- All 10 specialist agents and AI Manager have defined roles.
- Handoffs and canonical IDs are documented.
- QC, revision, and Owner approval gates are unambiguous.
- No contradictory workflow rules remain.

### Phase 1 — Tool and Provider Evaluation

Evaluate candidate services for:
- LLM and agent execution.
- Product research and web retrieval.
- Trend research data access.
- TTS and voice consistency.
- Image/video generation.
- Video rendering and transcoding.
- Workflow orchestration.
- Database and object storage.
- Publishing and analytics.

For each candidate record:
- Project/provider and official URL.
- License and commercial-use rights.
- API availability and restrictions.
- Pricing, free tier, and usage limits.
- Hosting requirements.
- Data retention and privacy.
- Reliability and support.
- Portability and lock-in.
- Proof-of-concept result.

Exit criteria:
- Shortlisted stack has evidence-backed decisions.
- Critical providers have working API proofs of concept.
- Expected unit costs have been estimated.
- No critical legal, licensing, or API-access blocker remains.

### Phase 2 — Core Backend and Workflow Skeleton

Deliverables:
- Repository code structure and development environment.
- Authentication and Owner roles.
- Campaign, task, artifact, and event data models.
- Shared contract validation.
- Workflow state machine.
- Audit logging and idempotency.
- Basic dashboard for campaign status.

Exit criteria:
- A sample campaign can move through mocked agent tasks.
- Invalid transitions and missing identifiers are rejected.
- State survives service restart.
- Secrets are not exposed in logs or client code.

### Phase 3 — Research and Planning Agents

Implement:
- Product Researcher.
- Trend Scout.
- Content Strategist.
- Hook & Copywriter.
- Creative Director.

Exit criteria:
- Each agent consumes and emits validated contracts.
- Source references and uncertainty are preserved.
- Script and creative versions are traceable.
- A campaign can produce a complete approved production brief.

### Phase 4 — Voice and Video Production

Implement:
- Voice Talent.
- Video Editor.
- Cloud rendering and artifact storage.

Exit criteria:
- Voice and render artifacts are stored immutably.
- Output formats and media metadata are validated.
- Render failures are observable and recoverable.
- Cost and latency are recorded per render.

### Phase 5 — Independent QC and Revision Loop

Implement:
- Independent QC runtime.
- Technical media checks.
- Human-review escalation.
- Revision routing and centralized attempt counter.
- Release-level reinspection.

Exit criteria:
- QC evaluates the exact artifact checksum and version.
- Critical defects block release regardless of score.
- A new render requires complete QC.
- The Manager cannot override QC.
- Three failed automatic attempts trigger escalation.

### Phase 6 — Approval and Publishing Preparation

Implement:
- Publication package generation.
- Owner approval UI and immutable approval record.
- Platform adapters only where official APIs and terms allow.
- Manual publishing fallback.

Exit criteria:
- Publishing is impossible without valid Owner approval for the exact version and platform package.
- Duplicate publishing is prevented or safely detected.
- Failed or unsupported publishing becomes a clear manual action.
- Publication IDs and URLs are verified before being recorded.

### Phase 7 — Analytics and Optimization

Implement:
- Authorized analytics ingestion.
- Data quality and freshness checks.
- Performance reports.
- Experiment tracking and feedback into future strategy.

Exit criteria:
- Missing metrics remain unknown, not zero.
- Recommendations cite observed data and limitations.
- Platform metrics are not compared as if definitions were identical.
- Campaign outcomes can be traced to the exact published video version.

### Phase 8 — Reliability, Security, and Cost Optimization

Deliverables:
- Load and failure testing.
- Backups and recovery.
- Monitoring and alerts.
- Permission reviews.
- Data retention and deletion controls.
- Cost dashboards and provider fallback strategy.

Exit criteria:
- Recovery procedures are tested.
- Sensitive data access is least-privilege.
- Cost thresholds and usage alerts work.
- No unresolved critical security or release blocker remains.

## 4. Initial Non-Goals

Until explicitly approved, the project will not:
- Publish automatically without Owner approval.
- Purchase products, subscriptions, credits, or ads.
- Use unofficial scraping or account automation that violates platform terms.
- Clone a real person's voice without appropriate authorization.
- Guarantee virality, sales, or conversion outcomes.
- Run heavy AI inference or video rendering on the Owner's local PC.

## 5. Definition of Production Readiness

The system is not production-ready merely because agents can generate text or videos. Production readiness requires validated contracts, durable state, secure credentials, reliable artifact storage, complete QC, enforceable approval gates, audit trails, cost visibility, and tested recovery behavior.

## 6. Current Status

Current repository state: specification and planning stage. No production application, cloud infrastructure, agent runtime, database, dashboard, or platform integration is confirmed as implemented.

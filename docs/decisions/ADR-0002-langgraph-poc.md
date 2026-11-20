# ADR-0002: LangGraph Workflow Proof of Concept

- **Status:** Implemented as a mock-only prototype; automated CI verification pending
- **Date:** 2026-11-20
- **Related:** ADR-0001, Shared Data Contract, Development Roadmap

## Decision

Implement the first workflow prototype with LangGraph and SQLite checkpointing.

The prototype is intentionally deterministic and uses mock agents. It does not call paid AI APIs, render media, access social accounts, or publish real content.

## Included Capabilities

- Sequential mock Product Research, Trend Scout, Content Strategy, Copywriting, Creative Direction, Voice Talent, and Video Editor steps.
- Mock render versioning with deterministic SHA-256 artifact checksums.
- Mock QC decisions and conditional revision routing.
- Maximum of three automatic creative revision attempts.
- Escalation after the third unsuccessful revision.
- QC PASS binding to exact video ID, version, and render checksum.
- LangGraph interrupt for explicit Owner approval.
- Approval binding to exact video version, checksum, and QC report.
- Mock publishing node that refuses to run without current QC PASS and matching approval.
- SQLite-backed LangGraph checkpoints for local development and tests.
- CLI commands to start a demo, inspect a thread, and approve/reject a paused demo.
- Pytest suite and GitHub Actions CI workflow.

## Local Development Only

SQLite checkpointing is intended for local development, tests, and lightweight single-process experimentation. It is not the production multi-worker storage decision. The project should evaluate a managed PostgreSQL-backed checkpoint store and application database before cloud deployment.

The SQLite checkpoint file is local state and must not be committed. Set `LANGGRAPH_STRICT_MSGPACK=true` when using the SQLite checkpointer.

## Acceptance Tests

The automated suite covers:
1. Owner approval pause and resume after reopening the SQLite database.
2. Revision creates a new render and requires a new QC report.
3. Three automatic revisions then escalation.
4. QC FAIL blocks approval and publishing.
5. Owner rejection blocks publishing.
6. Invalid approval payload rejection.
7. Stale QC report cannot authorize the current render.

CI is configured for Python 3.11, 3.12, and 3.13. A successful code commit is not evidence that tests passed; inspect the GitHub Actions run result before declaring the prototype verified.

## Known Limitations

- Agent outputs and QC outcomes are fixtures, not actual AI analysis.
- The QC score is mock data and is not a release-quality inspection.
- The approval actor is a test placeholder, not authenticated Owner identity.
- The mock publication record does not represent a platform upload.
- The prototype does not yet implement API authentication, production database models, object storage, job queues, secrets management, or cloud deployment.
- The shared data contract is represented by typed workflow state but is not yet enforced with a formal JSON Schema validator.

## Exit Criteria for This POC

The POC is considered technically validated only when CI passes on the supported Python matrix and the tests demonstrate checkpoint persistence, revision limits, stale-QC rejection, approval binding, and publishing lockout.

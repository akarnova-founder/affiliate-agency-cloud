# ADR-0001: Initial Workflow and Agent Runtime Shortlist

- **Status:** Proposed — proof of concept required
- **Date:** 2026-11-20
- **Scope:** Agent orchestration and workflow execution for the AI Affiliate Agency Cloud

## Context

The system coordinates 10 specialist agents and an AI Manager. Its workflow includes long-running media generation, revision loops, QC gates, human approval pauses, external APIs, and potentially expensive side effects such as publishing.

The Owner's Windows PC is a control client only. Runtime execution, orchestration, storage, and rendering are intended to run in cloud infrastructure.

The system therefore needs:
- Explicit workflow state and validated transitions.
- Durable persistence and recovery after worker/provider failures.
- Human-in-the-loop pause and resume.
- Bounded retries and idempotent side effects.
- Clear integration boundaries for agents and external services.
- Cost and usage visibility.
- A manageable operational footprint.

## Candidates Reviewed

### LangGraph — preferred first proof-of-concept candidate

LangGraph is a low-level orchestration framework/runtime for long-running, stateful agents. It models workflows as shared state, nodes, and edges, and supports persistence/checkpointing, streaming, and human-in-the-loop flows. It can combine deterministic functions with LLM-driven steps and does not require LangChain for the orchestration layer.

Official documentation:
- https://langchain-ai.github.io/langgraph/
- https://langchain-ai.github.io/langgraph/how-tos/multi-agent-network/

Why it fits:
- The project already defines a known workflow and explicit specialist roles.
- Conditional transitions can implement QC PASS/REVISE/FAIL paths.
- Human approval can pause and resume a workflow.
- Checkpoints can preserve workflow state.
- Deterministic validation can remain ordinary application code.

Risks and items to test:
- Checkpointer and database setup.
- Recovery behavior around long-running provider calls.
- Idempotency of external side effects when nodes retry or resume.
- Cloud hosting and worker scaling model.
- Operational monitoring and migration strategy.

### Temporal — alternative for durable business workflow execution

Temporal provides durable workflow execution that records workflow history and can resume after worker crashes or transient failures. Activities have retry policies, and workflows can wait for external intervention.

Official documentation:
- https://docs.temporal.io/durable-execution

Why it fits:
- Strong durable execution model for workflows that may run for a long time.
- Clear separation between workflow logic and activities.
- Useful if the project grows into a high-reliability workflow platform with complex external side effects.

Risks and items to test:
- Additional concepts and operational infrastructure.
- Whether its durability model is needed for the initial scale.
- Integration pattern with agent runtime and checkpointed LLM work.
- Hosting and operational cost.

### n8n — optional integration automation, not the initial source of truth

n8n supports queue mode with a main instance and worker instances. Its documentation notes that queue mode uses external storage such as S3 for binary data; filesystem binary storage is not supported in queue mode.

Official documentation:
- https://docs.n8n.io/hosting/scaling/queue-mode/

Potential uses:
- Notifications.
- Approval reminders.
- Simple integrations and scheduled reporting.
- Connecting third-party systems where a visual workflow is useful.

Why it should not initially own the core production state:
- The project's QC, version binding, revision counter, and approval invariants need strongly validated application-level state transitions.
- The core workflow should have one authoritative state machine and audit trail.

### LiteLLM — candidate model gateway, not an agent orchestrator

LiteLLM provides a common interface to many model providers and a self-hosted gateway with virtual keys, spend tracking, budgets, and rate limits. Its documentation notes that database configuration is required for budget enforcement.

Official documentation:
- https://docs.litellm.ai/
- https://docs.litellm.ai/docs/proxy/users

Potential uses:
- Centralizing model provider access.
- Keeping provider credentials server-side.
- Tracking usage and cost.
- Applying key/team budgets and rate limits.

Risks and items to test:
- Actual provider compatibility and pricing metadata.
- Database and Redis requirements for the desired enforcement behavior.
- Security hardening and operational maintenance.
- Budget enforcement behavior under failures.

### Remotion — candidate programmable video rendering tool

Remotion supports rendering through its CLI and server-side rendering API, and documents cloud deployment options including AWS Lambda.

Official documentation:
- https://www.remotion.dev/docs/render

Potential uses:
- Template-driven short-form video assembly.
- Programmatic subtitles, overlays, product shots, and motion graphics.
- Reproducible render pipelines.

Risks and items to test:
- License and commercial usage terms for the intended business.
- Cloud rendering cost and concurrency.
- Rendering time, memory, and media compatibility.
- Whether it fits alongside or instead of other open-source media tools.

## Proposed Initial Stack Shape

For a low-complexity first proof of concept:

1. **LangGraph** for agent workflow orchestration.
2. **PostgreSQL** for campaign records, task metadata, approvals, QC reports, and durable checkpoints where supported.
3. **Object storage** for immutable media and report artifacts.
4. **LiteLLM** as an optional model gateway after a security and cost proof of concept.
5. **Remotion** as one video-rendering candidate, subject to license and performance checks.
6. **n8n** only for peripheral integrations and notifications if it provides a clear benefit.

Do not combine LangGraph and Temporal in the first implementation unless a concrete requirement proves that one runtime cannot meet. Running two workflow engines initially would add operational complexity and duplicate state ownership.

## Decision

Select LangGraph as the first orchestration proof-of-concept candidate, not yet as a final production commitment.

Keep Temporal as the alternative if testing shows that the workflow needs stronger or simpler durable business-process execution than the LangGraph-based design can provide.

Do not use n8n as the authoritative state machine for production, QC, revision, or approval invariants.

Evaluate LiteLLM and Remotion independently as provider gateway and media rendering candidates.

## Proof-of-Concept Acceptance Tests

Build a small, non-production workflow with mock agents and no paid provider calls. It must demonstrate:

1. Create a campaign with canonical IDs from the shared data contract.
2. Execute three mock agent steps in sequence.
3. Persist state and resume after a simulated worker/process interruption.
4. Pause for a simulated Owner approval and resume only after an explicit approval event.
5. Route mock QC PASS to approval and mock QC REVISE to a revision task.
6. Enforce a centrally stored maximum of three automatic revision attempts.
7. Reject stale QC reports when the render version or checksum changes.
8. Prevent publishing when approval is absent or bound to a different artifact.
9. Record task events, errors, and estimated cost metadata.
10. Prove retries do not duplicate external side effects.

## Open Questions Before Final Selection

- Which cloud platform and deployment model offers the best cost/operational balance?
- Which PostgreSQL and object storage provider should be used?
- Which model providers offer suitable API access, commercial rights, quality, and cost?
- Which video rendering approach provides the required output quality and unit economics?
- What retention and deletion rules apply to generated media and campaign data?

## Consequences

This shortlist narrows the next engineering experiment while avoiding premature commitment to a production vendor stack. The final selection must be based on reproducible tests, current official pricing, licenses, terms, API access, and operational evidence.

No tool listed in this ADR is currently installed, deployed, or integrated into the application by virtue of this document.

# AI Affiliate Agency Cloud

A cloud-first, multi-agent system for researching affiliate products, planning short-form content, generating voice and video assets, independently inspecting quality, preparing publishing packages, and learning from performance.

**Project status:** specification and planning stage. This repository does not yet represent a deployed or operational production system.

## Project principles

- Cloud processing; the Owner's local PC is a control and review client.
- Reuse suitable open-source tools and legitimate APIs before building custom components.
- Keep providers replaceable and costs visible.
- Ground product claims and analytics in evidence.
- Inspect every latest render independently.
- Never publish without explicit Owner approval for the exact content version.

## Agent team

**AI Manager** coordinates 10 specialist agents:

1. Product Researcher
2. Trend Scout
3. Content Strategist
4. Hook & Copywriter
5. Creative Director
6. Voice Talent
7. Video Editor
8. Independent Quality Control Inspector
9. Publishing Specialist
10. Performance Analyst

## Workflow

Product input → product research → trend research → content strategy → script and hooks → creative plan and storyboard → voice generation → video production → independent QC → revisions when needed → publishing preparation → Owner approval → publication → performance analysis.

QC uses a 100-point score with a target of at least 90. Critical defects block PASS regardless of score. Every new render requires complete release-level QC. Automatic revisions are limited to three attempts before human escalation.

## Repository map

- `docs/PROJECT_CHARTER.md` — project goals, principles, and non-negotiable rules.
- `docs/ARCHITECTURE.md` — target cloud-first system architecture.
- `docs/SHARED_DATA_CONTRACT.md` — canonical IDs, handoff envelope, statuses, versioning, and approval binding.
- `docs/DEVELOPMENT_ROADMAP.md` — phased implementation and acceptance criteria.
- `docs/TOOL_EVALUATION.md` — open-source, API, provider, license, and cost evaluation policy.
- `agents/` — role specifications for the Manager and specialist agents.

## Workflow prototype

A deterministic LangGraph proof of concept is available in `app/`. It uses mock agents, SQLite checkpoints, revision/QC gates, and a simulated Owner approval pause. It does not call paid AI APIs, render media, or publish to social platforms.

See [POC Quickstart](docs/POC_QUICKSTART.md) to run it locally. See [ADR-0002](docs/decisions/ADR-0002-langgraph-poc.md) for scope, limitations, and acceptance tests.

## Development approach

Build in verified increments:
1. Complete and reconcile specifications.
2. Evaluate tools, licenses, API access, costs, and data policies.
3. Prove critical providers with small experiments.
4. Implement shared contracts and workflow state enforcement.
5. Add research, content, voice, video, QC, publishing, and analytics capabilities.
6. Test security, reliability, recovery, and cost controls.

## Important safety gates

- No secrets in Git.
- No unsupported product claims, fabricated testimonials, or invented metrics.
- No publishing without explicit Owner approval.
- A QC PASS applies only to the exact inspected artifact and version.
- The orchestrator enforces gates; prompts and agent claims are not sufficient enforcement.

## Current limitations

The current repository contains specifications and planning documents only. No cloud infrastructure, backend, dashboard, database, agent runtime, rendering pipeline, or platform integration is confirmed as implemented.

See [Development Roadmap](docs/DEVELOPMENT_ROADMAP.md) for the staged delivery plan.

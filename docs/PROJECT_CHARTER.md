# Project Charter — AI Affiliate Agency Cloud

## 1. Project Vision

Build a cloud-based AI Affiliate Content Agency capable of researching products, identifying trends, developing content strategies, creating scripts, producing voiceovers and videos, performing independent quality inspections, preparing content for publication, and learning from campaign performance.

The system operates as an orchestrated team of AI agents with a human Owner supervising business decisions and approving publication.

This charter defines project-level policy. The target architecture, shared handoff contract, roadmap, and provider evaluation rules are documented separately in the linked documents below.

## 2. Core Principles

- Reuse and adapt suitable open-source tools whenever practical.
- Build custom components only when existing tools are insufficient.
- Cloud-first processing; the local PC acts primarily as a controller and review interface.
- Cost-efficient infrastructure with free tiers prioritized only when API access, terms, limits, and total cost are verified.
- Modular architecture that allows agents and providers to be replaced.
- Quality takes priority over production quantity.
- No content may be published without explicit human approval for the exact content version and platform package.
- Never assume a service's web interface is free to use through its API.
- Protect credentials, personal information, intellectual property, and business data.
- Never fabricate product facts, testimonials, sources, or performance metrics.
- Treat documentation as design intent until working software has been implemented and tested.

## 3. AI Agent Team

The system consists of 10 specialized agents:

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

An AI Manager coordinates the agents, tracks workflow status, assigns tasks, validates handoffs, and manages revision cycles. Deterministic workflow services must enforce critical state transitions and approval gates.

## 4. Content Production Workflow

Product Input
→ Product Research
→ Trend Research
→ Content Strategy
→ Script and Hook
→ Creative Planning and Storyboard
→ Voice Generation
→ Video Production
→ Independent Quality Control
→ Revision if Required
→ Publishing Preparation
→ Human Approval
→ Publication
→ Performance Analysis

Stages may be parallelized only when dependencies and validation requirements remain satisfied. Every handoff must follow `docs/SHARED_DATA_CONTRACT.md`.

## 5. Mandatory Quality Control

Every generated video must pass independent Quality Control before it can be submitted for Owner publication approval.

QC must inspect:
- Technical integrity.
- Visual quality and product identity.
- Audio quality and synchronization.
- Content accuracy and script alignment.
- Creative quality and pacing.
- Subtitle placement and readability.
- Hook and CTA execution.
- Required disclosures and platform compliance risks.

QC must issue exactly one status:
- PASS
- REVISE
- FAIL
- QC_INCOMPLETE
- NEEDS_HUMAN_REVIEW

A critical defect blocks PASS regardless of numeric score. The AI Manager cannot change the QC score or override the inspector's decision. QC PASS applies only to the exact inspected video version and artifact checksum.

## 6. Quality Scoring

Total score: 100 points.

- Technical Integrity: 25 points.
- Visual Quality: 25 points.
- Audio Quality: 20 points.
- Content Accuracy: 20 points.
- Creative Quality: 10 points.

Target score: 90 or higher. A score of 90 or higher does not guarantee PASS if a critical defect exists or required checks are incomplete.

## 7. Revision Policy

- Automatically revise correctable content when QC returns REVISE.
- Each revision must include documented findings and acceptance criteria.
- Maximum of three automatic revision attempts per tracked revision cycle.
- Every new render must undergo complete release-level QC.
- After three unsuccessful attempts, escalate to NEEDS_HUMAN_REVIEW.
- Preserve previous renders, reports, and revision history.
- Infrastructure retries are separate from creative revision attempts and must not duplicate external side effects.

## 8. Human Authority

The human Owner retains authority over:
- Product selection and campaign priorities.
- Budget and provider selection.
- Final content and publication approval.
- Publication authorization.
- Business strategy and exceptions.

Publishing remains locked until explicit approval is recorded for the exact video version and platform package. Material changes require a new approval.

## 9. Cloud-First Infrastructure

The local computer is used for:
- Browser-based control.
- Project administration.
- Monitoring and review.
- Approving or rejecting outputs.

AI inference, orchestration, rendering, storage, and heavy processing should run on cloud services wherever feasible. The system must not depend on the Owner's local PC for production workloads.

## 10. Development Strategy

Development proceeds incrementally:
1. Requirements and repository foundation.
2. Tool and provider evaluation.
3. Architecture and shared data contracts.
4. Core backend and workflow state enforcement.
5. Research and planning agents.
6. Voice and video production.
7. Independent QC and revision loop.
8. Owner approval and publishing preparation.
9. Analytics and optimization.
10. Security, reliability, and cost optimization.

Each phase has explicit acceptance criteria in `docs/DEVELOPMENT_ROADMAP.md`.

## 11. Security

Never commit:
- API keys, access tokens, passwords, or cookies.
- Private credentials or affiliate account secrets.
- Personal information or sensitive analytics.
- Private media or customer data without an approved handling policy.

Use protected server-side secret storage, least-privilege permissions, input validation, audit logging, and defined retention controls. Do not expose long-lived credentials in client code, logs, or artifact URLs.

## 12. Project Definition of Success

The system should eventually run repeatable content production workflows, generate content variations, inspect output independently, manage revisions, maintain production records, and deliver publication-ready content for human approval.

Success requires reliable execution, validated data contracts, secure credentials, durable state, observable costs, independent QC, enforceable human approval, and tested recovery behavior—not merely the ability to generate text or videos.

## 13. Supporting Project Documents

- [System Architecture](ARCHITECTURE.md)
- [Shared Data Contract](SHARED_DATA_CONTRACT.md)
- [Development Roadmap](DEVELOPMENT_ROADMAP.md)
- [Tool Evaluation Policy](TOOL_EVALUATION.md)
- [AI Manager Specification](../agents/manager/README.md)

These documents supplement this charter. If a conflict is found, project-level safety and human approval principles in this charter take precedence until the Owner approves a documented change.

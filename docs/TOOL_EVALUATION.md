# Tool and Provider Evaluation Policy

## 1. Purpose

This policy governs selection of open-source projects, hosted APIs, and cloud services for the AI Affiliate Agency Cloud.

The goal is to reuse proven tools without confusing a free user interface with free or unrestricted API access.

## 2. Required Evaluation Record

For every shortlisted tool, document:

- Name and official repository or product URL.
- Intended capability and agent/workflow stage.
- Open-source license and commercial-use compatibility.
- Last meaningful maintenance activity and release health.
- API availability, authentication, quotas, and rate limits.
- Pricing, free tier, credit expiry, and overage costs.
- Hosting and infrastructure requirements.
- Input/output formats and integration effort.
- Data processing, retention, training, and privacy terms.
- Reliability, observability, and support options.
- Security posture and known vulnerabilities.
- Vendor lock-in and migration path.
- Proof-of-concept result and unresolved risks.

Do not rely on search snippets or unofficial pricing summaries when a current official source is available.

## 3. Evaluation Categories

### A. Open-Source Software
Check the actual license file and dependencies. Confirm whether commercial use, modification, redistribution, and hosted deployment are permitted. A public GitHub repository is not automatically open source.

### B. Hosted Web Applications
A free browser interface does not imply an API, automation permission, commercial-use permission, or unlimited use. Verify each separately.

### C. APIs
Confirm the endpoint is publicly documented, credentials can be obtained legitimately, usage is permitted for the intended workload, and costs can be bounded.

### D. AI and Media Providers
Evaluate output quality, consistency, controllability, latency, throughput, usage-based cost, content restrictions, data retention, and commercial rights.

### E. Publishing and Analytics Integrations
Prefer official APIs and approved platform integrations. Verify account eligibility, permissions, review requirements, supported media types, rate limits, and current platform terms. Provide a manual workflow when an official integration is unavailable.

## 4. Scoring Framework

Score each candidate from 1 (poor) to 5 (excellent):

| Criterion | Weight |
|---|---:|
| Functional fit and output quality | 20% |
| API access and integration feasibility | 15% |
| Total cost at expected volume | 15% |
| License, terms, and commercial rights | 15% |
| Reliability and maintenance | 10% |
| Security and privacy | 10% |
| Portability and lock-in | 10% |
| Operational simplicity | 5% |

Weighted score = sum of (criterion score / 5 × criterion weight).

A high score does not override a hard blocker. Reject a candidate with incompatible licensing, prohibited usage, unacceptable data handling, no legitimate required API, or unbounded critical cost.

## 5. Cost Model

Estimate unit costs for:
- Research task.
- Script and creative package.
- Voice generation per minute.
- Image generation per asset.
- Video generation per second or clip.
- Video rendering per minute.
- Storage per GB-month and transfer.
- Orchestration and database usage.
- Publishing and analytics operations.

Model low, expected, and high usage. Include retries, failed generations, storage, egress, taxes where relevant, and provider minimums.

Never describe a service as free without recording the applicable limits and date checked.

## 6. Reuse Before Build

Before writing a custom component:
1. Search for maintained open-source projects with a compatible license.
2. Check if the project solves the actual required capability.
3. Verify API or automation interfaces.
4. Run a small proof of concept.
5. Compare maintenance, security, cost, and portability.
6. Adopt, adapt, or reject with a written decision.

Do not add a dependency solely because it is popular or has an attractive demo.

## 7. Provider Adapter Requirement

External services must be accessed through a replaceable adapter wherever practical. Agent specifications should depend on capability contracts, not hard-coded vendor names.

Each adapter must normalize:
- Request and response types.
- Authentication and secret references.
- Timeout and retry behavior.
- Rate limits and provider errors.
- Usage and cost metadata.
- Provider model/version.
- Data retention and processing notes.

## 8. Decision Records

For each major stack decision, create a short Architecture Decision Record in `docs/decisions/` containing:
- Context and requirements.
- Options considered.
- Evidence and date checked.
- Decision and rationale.
- Consequences and risks.
- Revisit trigger.

## 9. Review Cadence

Recheck pricing, API terms, model availability, licensing, and platform rules before production launch and whenever a provider changes its terms or service. Store the date and official source for each check.

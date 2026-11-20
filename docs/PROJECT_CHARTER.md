# Project Charter — AI Affiliate Agency Cloud

## 1. Project Vision

Build a cloud-based AI Affiliate Content Agency capable of researching products, identifying trends, developing content strategies, creating scripts, producing voiceovers and videos, performing independent quality inspections, and preparing content for publication.

The system is designed to operate as an orchestrated team of AI agents with a human owner supervising the business and approving publishing decisions.

## 2. Core Principles

- Reuse and adapt existing open-source tools whenever practical.
- Build custom components only when existing tools are insufficient.
- Cloud-first processing. The local PC acts primarily as a controller.
- Cost-efficient infrastructure with free-tier services prioritized.
- Modular architecture that allows individual agents and tools to be replaced.
- Quality must take priority over production quantity.
- No content may be published without human approval.
- Never assume a service's web interface is free to use through its API.
- Protect credentials, personal information, and business data.

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

An AI Manager coordinates the agents, tracks workflow status, assigns tasks, handles handoffs, and manages revision cycles.

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

## 5. Mandatory Quality Control

Every generated video must pass independent Quality Control before it can be approved for publication.

QC must inspect:

- Technical integrity
- Visual quality
- Audio quality
- Content accuracy
- Creative quality
- Product visibility
- Subtitle placement
- Hook effectiveness
- Scene and narration alignment
- CTA and compliance

QC must issue a status:

- PASS
- REVISE
- FAIL
- QC_INCOMPLETE
- NEEDS_HUMAN_REVIEW

A critical defect automatically blocks publication.

The AI Manager cannot override the QC Inspector's decision.

## 6. Quality Scoring

Total score: 100 points.

- Technical: 25 points
- Visual: 25 points
- Audio: 20 points
- Content: 20 points
- Creative: 10 points

Target score: 90 or higher.

A score of 90 or higher does not guarantee PASS if a critical defect exists.

## 7. Revision Policy

- Automatically revise content when QC returns REVISE.
- Each revision must include a documented issue and required correction.
- Maximum of 3 automatic revision attempts.
- Every new render must undergo QC again.
- After 3 unsuccessful attempts, escalate to NEEDS_HUMAN_REVIEW.
- The latest video must undergo final release-level QC.

## 8. Human Authority

The human owner retains authority over:

- Product selection
- Campaign priorities
- Budget and service selection
- Final content approval
- Publication authorization
- Business strategy

Publishing must remain locked until human approval is explicitly provided.

## 9. Cloud-First Infrastructure

The local computer is used for:

- Browser-based control
- Project administration
- Monitoring
- Reviewing generated content
- Approving or rejecting outputs

AI inference, orchestration, rendering, storage, and heavy processing should run on cloud services wherever feasible.

## 10. Development Strategy

Development will follow incremental stages:

1. Repository and documentation foundation
2. Tool and infrastructure audit
3. Architecture design
4. Agent specifications
5. Workflow orchestration
6. Production pipeline
7. QC automation
8. Dashboard and control interface
9. Publishing preparation
10. Performance feedback and optimization

Each stage must be reviewed before moving to the next.

## 11. Security

Never commit:

- API keys
- Access tokens
- Passwords
- Cookies
- Private credentials
- Personal information
- Affiliate account secrets
- Sensitive analytics

Use environment variables or secure secret storage.

## 12. Project Definition of Success

The system should eventually be capable of running repeatable content production workflows, generating multiple content variations, independently inspecting output quality, automatically handling revisions, maintaining production records, and delivering publication-ready content for human approval.

The goal is a reliable AI-powered content agency, not simply an automated video generator.

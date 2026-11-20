# LangGraph Workflow POC — Quickstart

## Purpose

Run the deterministic workflow prototype locally. It uses mock agent outputs and a local SQLite checkpoint database. It does not use AI API keys, render a video, or publish to any social platform.

## Requirements

- Python 3.11 or newer.
- Git.
- Windows 10, macOS, or Linux.

The Owner's PC only runs this lightweight orchestration demo; no GPU is required.

## Setup on Windows 10

Open PowerShell in the repository folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
$env:LANGGRAPH_STRICT_MSGPACK = "true"
```

If PowerShell blocks activation, use the Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Run the tests

```powershell
python -m pytest
```

## Start a mock campaign

```powershell
python -m app.cli start-demo --thread-id demo-001
```

The workflow should stop at the Owner approval gate after a mock QC PASS. It prints the exact video version and checksum that are awaiting a decision.

## Test a revision cycle

```powershell
python -m app.cli start-demo --thread-id demo-revision-001 --qc-outcomes REVISE,PASS
```

The first QC result is REVISE, a new mock render is created, and the second QC result is PASS. The workflow then pauses for Owner approval.

## Approve or reject the exact mock version

```powershell
python -m app.cli approve --thread-id demo-001
```

Or reject:

```powershell
python -m app.cli reject --thread-id demo-001
```

A simulated publication record is created only after approval. It is explicitly marked `SIMULATED_ONLY_NOT_PUBLISHED`; no external platform is contacted.

## Inspect a workflow

```powershell
python -m app.cli status --thread-id demo-001
```

## Checkpoint storage

By default, local checkpoints are stored in `data/dev_checkpoints.sqlite`. Do not commit this file. It is development-only storage, not a production database or multi-worker checkpoint solution.

## Troubleshooting

- Use the same `--thread-id` to inspect or resume a paused workflow.
- Use a new thread ID for each new demo campaign.
- If a demo thread is already completed, start a new thread rather than trying to approve it again.
- Ensure `LANGGRAPH_STRICT_MSGPACK=true` is set before running the CLI.
- If dependency installation fails, capture the full error and Python version before changing package pins.

## Current Status

The source code and CI workflow are committed separately from test results. Check the GitHub Actions workflow for the actual pass/fail result before treating this POC as verified.

"""Command-line interface for the local workflow proof of concept."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from app.workflow import build_workflow, demo_input

DEFAULT_DB = "data/dev_checkpoints.sqlite"


def _config(thread_id: str) -> dict[str, Any]:
    return {"configurable": {"thread_id": thread_id}}


def _print_state(graph: Any, thread_id: str) -> None:
    snapshot = graph.get_state(_config(thread_id))
    print(json.dumps({
        "thread_id": thread_id,
        "next_nodes": list(snapshot.next),
        "state": snapshot.values,
    }, indent=2, ensure_ascii=False, default=str))


def main() -> None:
    parser = argparse.ArgumentParser(description="Affiliate Agency Cloud workflow POC (mock only)")
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite checkpoint database path")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start-demo", help="Start a new mock campaign")
    start.add_argument("--thread-id", required=True)
    start.add_argument("--qc-outcomes", default="PASS", help="Comma-separated QC outcomes, e.g. REVISE,PASS")

    for name in ("approve", "reject", "status"):
        command = sub.add_parser(name, help=f"{name.title()} or inspect a paused workflow")
        command.add_argument("--thread-id", required=True)

    args = parser.parse_args()
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # LangGraph recommends strict msgpack deserialization for SQLite checkpoints.
    os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

    with SqliteSaver.from_conn_string(str(db_path)) as checkpointer:
        graph = build_workflow(checkpointer)
        config = _config(args.thread_id)

        if args.command == "start-demo":
            outcomes = [item.strip().upper() for item in args.qc_outcomes.split(",") if item.strip()]
            result = graph.invoke(demo_input(outcomes), config)
            _print_state(graph, args.thread_id)
            if graph.get_state(config).next:
                print("\nWorkflow paused. Review the exact version and use approve or reject.")
            else:
                print("\nWorkflow ended without real publishing. This is a mock-only prototype.")
            return

        if args.command == "status":
            _print_state(graph, args.thread_id)
            return

        decision = "approved" if args.command == "approve" else "rejected"
        graph.invoke(Command(resume={"decision": decision}), config)
        _print_state(graph, args.thread_id)
        print("\nDecision processed. Any publication record is simulated only; no platform was contacted.")


if __name__ == "__main__":
    main()

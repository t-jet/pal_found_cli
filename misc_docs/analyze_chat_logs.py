#!/usr/bin/env python3
"""Analyze VS Code Copilot chat session logs.

The logs in ``chat_logs`` are JSONL state snapshots/deltas. This script extracts
request-level token usage and counts direct agent requests plus subagent
invocations found inside serialized tool-call responses.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


LOG_DIR = Path(__file__).with_name("chat_logs")


@dataclass
class RequestStats:
    request_id: str
    session_file: str
    agent_name: str = "unknown"
    agent_id: str = ""
    mode_name: str = ""
    model_id: str = ""
    completion_tokens: int = 0
    elapsed_ms: int = 0
    timestamp: int = 0


@dataclass
class SubagentStats:
    agent_name: str
    model_name: str = ""
    invocation_ids: set[str] = field(default_factory=set)
    tool_call_ids: set[str] = field(default_factory=set)
    descriptions: Counter[str] = field(default_factory=Counter)
    parent_requests: set[str] = field(default_factory=set)
    parent_invocations: Counter[str] = field(default_factory=Counter)
    parent_descriptions: dict[str, Counter[str]] = field(default_factory=dict)
    parent_models: dict[str, Counter[str]] = field(default_factory=dict)
    session_files: set[str] = field(default_factory=set)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate token and request statistics from Copilot chat logs."
    )
    parser.add_argument(
        "log_dir",
        nargs="?",
        type=Path,
        default=LOG_DIR,
        help=f"Directory containing *.jsonl chat logs (default: {LOG_DIR})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of text tables.",
    )
    return parser.parse_args()


def iter_jsonl(path: Path) -> tuple[list[dict[str, Any]], int]:
    records: list[dict[str, Any]] = []
    bad_lines = 0
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                bad_lines += 1
                continue
            if isinstance(value, dict):
                records.append(value)
    return records, bad_lines


def apply_path(root: Any, path: list[Any], value: Any) -> Any:
    """Apply a simple VS Code state delta into a Python object tree."""
    if not path:
        return value

    current = root
    for key in path[:-1]:
        if isinstance(current, list) and isinstance(key, int):
            while len(current) <= key:
                current.append({})
            current = current[key]
        elif isinstance(current, dict):
            current = current.setdefault(key, [] if isinstance(path[-1], int) else {})
        else:
            return root

    last = path[-1]
    if isinstance(current, list) and isinstance(last, int):
        while len(current) <= last:
            current.append({})
        current[last] = value
    elif isinstance(current, dict):
        current[last] = value
    return root


def build_final_state(records: list[dict[str, Any]]) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for record in records:
        kind = record.get("kind")
        if kind == 0 and isinstance(record.get("v"), dict):
            state = record["v"]
        elif kind in {1, 2} and isinstance(record.get("k"), list):
            path = record["k"]
            value = record.get("v")
            if kind == 2 and path == ["requests"] and isinstance(value, list):
                state.setdefault("requests", [])
                if isinstance(state["requests"], list):
                    state["requests"].extend(value)
                continue
            state = apply_path(state, path, value)
    return state


def coerce_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return 0


def agent_label(request: dict[str, Any]) -> tuple[str, str, str]:
    mode_info = request.get("modeInfo") if isinstance(request.get("modeInfo"), dict) else {}
    mode_instructions = (
        mode_info.get("modeInstructions")
        if isinstance(mode_info.get("modeInstructions"), dict)
        else {}
    )
    agent = request.get("agent") if isinstance(request.get("agent"), dict) else {}

    mode_name = str(mode_info.get("modeName") or mode_info.get("name") or "")
    agent_name = str(
        mode_instructions.get("name")
        or mode_info.get("name")
        or mode_name
        or agent.get("fullName")
        or agent.get("name")
        or agent.get("id")
        or "unknown"
    )
    agent_id = str(agent.get("id") or "")
    return agent_name, agent_id, mode_name


def collect_tool_calls(value: Any) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if value.get("kind") == "toolInvocationSerialized":
            calls.append(value)
        for child in value.values():
            calls.extend(collect_tool_calls(child))
    elif isinstance(value, list):
        for child in value:
            calls.extend(collect_tool_calls(child))
    return calls


def analyze_file(
    path: Path,
    requests: dict[str, RequestStats],
    subagents: dict[str, SubagentStats],
) -> tuple[int, int]:
    records, bad_lines = iter_jsonl(path)
    state = build_final_state(records)
    seen_requests = 0

    index_to_request_id: dict[int, str] = {}
    seen_tool_calls: set[str] = set()
    final_requests = state.get("requests", [])

    def ingest_subagent_call(call: dict[str, Any], request_id: str) -> None:
        tool_data = call.get("toolSpecificData")
        if not isinstance(tool_data, dict) or tool_data.get("kind") != "subagent":
            return

        invocation_id = str(call.get("subAgentInvocationId") or "")
        tool_call_id = str(call.get("toolCallId") or "")
        dedupe_key = invocation_id or tool_call_id or json.dumps(call, sort_keys=True, default=str)
        if dedupe_key in seen_tool_calls:
            return
        seen_tool_calls.add(dedupe_key)

        subagent_name = str(tool_data.get("agentName") or "unknown")
        subagent = subagents.setdefault(subagent_name, SubagentStats(subagent_name))
        model_name = str(tool_data.get("modelName") or "")
        subagent.model_name = model_name or subagent.model_name
        if invocation_id:
            subagent.invocation_ids.add(invocation_id)
        if tool_call_id:
            subagent.tool_call_ids.add(tool_call_id)
        if request_id and model_name:
            subagent.parent_models.setdefault(request_id, Counter())[model_name] += 1
        if tool_data.get("description"):
            description = str(tool_data["description"])
            subagent.descriptions[description] += 1
            if request_id:
                subagent.parent_descriptions.setdefault(request_id, Counter())[description] += 1
        if request_id:
            subagent.parent_requests.add(request_id)
            subagent.parent_invocations[request_id] += 1
        subagent.session_files.add(path.name)

    for index, request in enumerate(final_requests):
        if not isinstance(request, dict):
            continue

        request_id = str(request.get("requestId") or f"{path.stem}#{index}")
        index_to_request_id[index] = request_id
        agent_name, agent_id, mode_name = agent_label(request)
        stats = requests.setdefault(
            request_id,
            RequestStats(request_id=request_id, session_file=path.name),
        )
        stats.session_file = path.name
        stats.agent_name = agent_name
        stats.agent_id = agent_id
        stats.mode_name = mode_name
        stats.model_id = str(request.get("modelId") or stats.model_id)
        stats.completion_tokens = max(
            stats.completion_tokens,
            coerce_int(request.get("completionTokens")),
        )
        stats.elapsed_ms = max(stats.elapsed_ms, coerce_int(request.get("elapsedMs")))
        stats.timestamp = max(stats.timestamp, coerce_int(request.get("timestamp")))
        seen_requests += 1

        for call in collect_tool_calls(request.get("response")):
            ingest_subagent_call(call, request_id)

    for record in records:
        path_keys = record.get("k") if isinstance(record.get("k"), list) else []
        parent_request_id = ""

        if len(path_keys) >= 2 and path_keys[0] == "requests" and isinstance(path_keys[1], int):
            parent_request_id = index_to_request_id.get(path_keys[1], "")

        value = record.get("v")
        if path_keys == ["requests"] and isinstance(value, list):
            request_values = value
        else:
            request_values = [value]

        for request_value in request_values:
            inferred_request_id = parent_request_id
            if isinstance(request_value, dict) and request_value.get("requestId"):
                inferred_request_id = str(request_value["requestId"])

            for call in collect_tool_calls(request_value):
                ingest_subagent_call(call, inferred_request_id)

    return seen_requests, bad_lines


def summarize(log_dir: Path) -> dict[str, Any]:
    requests: dict[str, RequestStats] = {}
    subagents: dict[str, SubagentStats] = {}
    files = sorted(log_dir.glob("*.jsonl"))
    bad_lines = 0
    parsed_request_rows = 0

    for path in files:
        file_requests, file_bad_lines = analyze_file(path, requests, subagents)
        parsed_request_rows += file_requests
        bad_lines += file_bad_lines

    by_agent: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "requests": 0,
            "completion_tokens": 0,
            "models": Counter(),
            "session_files": set(),
        }
    )
    for request in requests.values():
        row = by_agent[request.agent_name]
        row["requests"] += 1
        row["completion_tokens"] += request.completion_tokens
        row["session_files"].add(request.session_file)
        if request.model_id:
            row["models"][request.model_id] += 1

    subagent_invocations_by_request: Counter[str] = Counter()
    for subagent in subagents.values():
        subagent_invocations_by_request.update(subagent.parent_invocations)

    def subagent_completion_stats(row: SubagentStats) -> tuple[int, int]:
        parent_tokens = sum(
            requests[request_id].completion_tokens
            for request_id in row.parent_requests
            if request_id in requests
        )
        allocated_tokens = round(
            sum(
                requests[request_id].completion_tokens
                * invocation_count
                / subagent_invocations_by_request[request_id]
                for request_id, invocation_count in row.parent_invocations.items()
                if request_id in requests and subagent_invocations_by_request[request_id]
            )
        )
        return parent_tokens, allocated_tokens

    by_subagent_caller: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "invocations": 0,
            "parent_requests": set(),
            "parent_invocations": Counter(),
            "models": Counter(),
            "descriptions": Counter(),
            "session_files": set(),
        }
    )
    for subagent_name, subagent in subagents.items():
        for request_id, invocation_count in subagent.parent_invocations.items():
            request = requests.get(request_id)
            caller_agent = request.agent_name if request else "unknown"
            row = by_subagent_caller[(caller_agent, subagent_name)]
            row["invocations"] += invocation_count
            row["parent_requests"].add(request_id)
            row["parent_invocations"][request_id] += invocation_count
            row["descriptions"].update(subagent.parent_descriptions.get(request_id, Counter()))
            row["models"].update(subagent.parent_models.get(request_id, Counter()))
            row["session_files"].update(subagent.session_files)

    return {
        "log_dir": str(log_dir),
        "files": len(files),
        "bad_lines": bad_lines,
        "parsed_request_rows": parsed_request_rows,
        "unique_requests": len(requests),
        "total_completion_tokens": sum(r.completion_tokens for r in requests.values()),
        "subagent_token_note": (
            "Subagent call payloads do not contain direct token counters. "
            "parent_completion_tokens sums each parent request once when the "
            "subagent appeared; allocated_completion_tokens splits parent "
            "completionTokens across subagent invocations in that request."
        ),
        "by_agent": {
            name: {
                "requests": row["requests"],
                "completion_tokens": row["completion_tokens"],
                "models": dict(row["models"]),
                "session_files": sorted(row["session_files"]),
            }
            for name, row in sorted(
                by_agent.items(),
                key=lambda item: (-item[1]["completion_tokens"], item[0].lower()),
            )
        },
        "by_subagent": {
            name: {
                "invocations": len(row.invocation_ids) or len(row.tool_call_ids),
                "parent_requests": len(row.parent_requests),
                "parent_completion_tokens": subagent_completion_stats(row)[0],
                "allocated_completion_tokens": subagent_completion_stats(row)[1],
                "model": row.model_name,
                "top_descriptions": row.descriptions.most_common(10),
                "session_files": sorted(row.session_files),
            }
            for name, row in sorted(
                subagents.items(),
                key=lambda item: (
                    -sum(
                        requests[request_id].completion_tokens
                        for request_id in item[1].parent_requests
                        if request_id in requests
                    ),
                    item[0].lower(),
                ),
            )
        },
        "by_subagent_caller": {
            f"{caller_agent} -> {subagent_name}": {
                "caller_agent": caller_agent,
                "subagent": subagent_name,
                "invocations": row["invocations"],
                "parent_requests": len(row["parent_requests"]),
                "parent_completion_tokens": sum(
                    requests[request_id].completion_tokens
                    for request_id in row["parent_requests"]
                    if request_id in requests
                ),
                "allocated_completion_tokens": round(
                    sum(
                        requests[request_id].completion_tokens
                        * invocation_count
                        / subagent_invocations_by_request[request_id]
                        for request_id, invocation_count in row["parent_invocations"].items()
                        if request_id in requests and subagent_invocations_by_request[request_id]
                    )
                ),
                "models": dict(row["models"]),
                "top_descriptions": row["descriptions"].most_common(10),
                "session_files": sorted(row["session_files"]),
            }
            for (caller_agent, subagent_name), row in sorted(
                by_subagent_caller.items(),
                key=lambda item: (
                    -sum(
                        requests[request_id].completion_tokens
                        for request_id in item[1]["parent_requests"]
                        if request_id in requests
                    ),
                    item[0][0].lower(),
                    item[0][1].lower(),
                ),
            )
        },
    }


def print_table(title: str, headers: list[str], rows: list[list[Any]]) -> None:
    print(f"\n{title}")
    if not rows:
        print("  (none)")
        return
    widths = [
        max(len(str(value)) for value in [header] + [row[index] for row in rows])
        for index, header in enumerate(headers)
    ]
    print("  " + "  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  " + "  ".join("-" * width for width in widths))
    for row in rows:
        print("  " + "  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def print_text(summary: dict[str, Any]) -> None:
    print(f"Chat log directory: {summary['log_dir']}")
    print(f"Files analyzed: {summary['files']}")
    print(f"Unique requests: {summary['unique_requests']}")
    print(f"Total completion tokens: {summary['total_completion_tokens']:,}")
    if summary["bad_lines"]:
        print(f"Malformed JSONL lines skipped: {summary['bad_lines']}")
    print("Token note: these logs expose completionTokens; prompt/input token fields were not present.")
    print(summary["subagent_token_note"])

    agent_rows = [
        [
            name,
            data["requests"],
            f"{data['completion_tokens']:,}",
            ", ".join(data["models"].keys()) or "-",
        ]
        for name, data in summary["by_agent"].items()
    ]
    print_table("Requests and Tokens by Invoked Agent", ["agent", "requests", "completion tokens", "models"], agent_rows)

    subagent_rows = [
        [
            name,
            data["invocations"],
            data["parent_requests"],
            f"{data['parent_completion_tokens']:,}",
            f"{data['allocated_completion_tokens']:,}",
            data["model"] or "-",
            "; ".join(f"{desc} ({count})" for desc, count in data["top_descriptions"][:3]) or "-",
        ]
        for name, data in summary["by_subagent"].items()
    ]
    print_table(
        "Subagent Invocations",
        [
            "subagent",
            "invocations",
            "parent requests",
            "parent tokens",
            "allocated tokens",
            "model",
            "top descriptions",
        ],
        subagent_rows,
    )

    subagent_caller_rows = [
        [
            data["caller_agent"],
            data["subagent"],
            data["invocations"],
            data["parent_requests"],
            f"{data['parent_completion_tokens']:,}",
            f"{data['allocated_completion_tokens']:,}",
            ", ".join(data["models"].keys()) or "-",
            "; ".join(f"{desc} ({count})" for desc, count in data["top_descriptions"][:3]) or "-",
        ]
        for data in summary["by_subagent_caller"].values()
    ]
    print_table(
        "Subagent Invocations by Caller Agent",
        [
            "caller",
            "subagent",
            "invocations",
            "parent requests",
            "parent tokens",
            "allocated tokens",
            "models",
            "top descriptions",
        ],
        subagent_caller_rows,
    )


def main() -> None:
    args = parse_args()
    summary = summarize(args.log_dir)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_text(summary)


if __name__ == "__main__":
    main()

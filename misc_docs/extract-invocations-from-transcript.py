#!/usr/bin/env python3
"""Extract subagent invocations from VS Code/Copilot transcript JSONL files.

The default output is tailored to the ticket-helper investigation:

- locate each `runSubagent` invocation for `ticket-helper`
- preserve the exact full prompt used to invoke the subagent
- collect `reasoningText` from assistant thinking turns inside the subagent
- collect tool invocations and their success/failure status, including
  `run_in_terminal` commands with explanation and goal

The transcript event tree can keep parent-agent follow-up messages under a
completed subagent's ancestry, so completed invocations are bounded by their own
`runSubagent` completion line.

Parallel sibling `runSubagent` starts can also be serialized as descendants of
one another. The extractor treats every target-agent `runSubagent` start as an
invocation boundary so wrapper/sibling calls do not appear as ordinary tools
inside another invocation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_TRANSCRIPT_DIR = Path(__file__).with_name("transcripts")
DEFAULT_CHAT_LOG_DIR = Path(__file__).with_name("chat_logs")
DEFAULT_OUTPUT = Path(__file__).with_name("ticket-helper-failures.md")


@dataclass
class TranscriptEvent:
    raw: dict[str, Any]
    line: int

    @property
    def event_id(self) -> str:
        return str(self.raw.get("id") or "")

    @property
    def parent_id(self) -> str:
        return str(self.raw.get("parentId") or "")

    @property
    def event_type(self) -> str:
        return str(self.raw.get("type") or "")

    @property
    def timestamp(self) -> str:
        return str(self.raw.get("timestamp") or "")

    @property
    def data(self) -> dict[str, Any]:
        data = self.raw.get("data")
        return data if isinstance(data, dict) else {}


@dataclass
class SubagentInvocation:
    file: str
    request_line: int | None
    request_timestamp: str
    request_message_id: str
    line: int
    event_id: str
    parent_id: str
    tool_call_id: str
    timestamp: str
    description: str
    prompt: str
    events: list[TranscriptEvent] = field(default_factory=list)
    success: bool | None = None
    complete_line: int | None = None
    complete_timestamp: str = ""
    nested_invocation_ids: list[str] = field(default_factory=list)
    nested_tool_call_ids: list[str] = field(default_factory=list)
    wrapper_invocation: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract subagent prompts, thinking turns, and tool invocations from transcript JSONL files."
    )
    parser.add_argument(
        "transcript_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_TRANSCRIPT_DIR,
        help=f"Directory containing transcript *.jsonl files (default: {DEFAULT_TRANSCRIPT_DIR})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown output path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--chat-log-dir",
        type=Path,
        default=DEFAULT_CHAT_LOG_DIR,
        help=f"Directory containing matching chat log *.jsonl files (default: {DEFAULT_CHAT_LOG_DIR})",
    )
    parser.add_argument(
        "--agent",
        default="ticket-helper",
        help="Subagent name to extract from runSubagent calls (default: ticket-helper)",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[TranscriptEvent]:
    events: list[TranscriptEvent] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                events.append(TranscriptEvent(value, line_no))
    return events


def parse_tool_arguments(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return value if isinstance(value, dict) else {}
    return {}


def markdown_fence(text: Any) -> str:
    value = "" if text is None else str(text)
    run = 0
    max_run = 0
    for char in value:
        if char == "`":
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    ticks = "`" * max(3, max_run + 1)
    return f"{ticks}\n{value}\n{ticks}"


def one_line(text: str) -> str:
    return str(text or "").replace("\n", " ").strip()


def completion_events_by_tool_call(events: list[TranscriptEvent]) -> dict[str, list[TranscriptEvent]]:
    completions: dict[str, list[TranscriptEvent]] = {}
    for event in events:
        data = event.data
        tool_call_id = data.get("toolCallId")
        if event.event_type == "tool.execution_complete" and tool_call_id:
            completions.setdefault(str(tool_call_id), []).append(event)
    return completions


def iter_dicts(value: Any) -> Any:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def index_chat_log_tools(chat_log_dir: Path) -> dict[str, dict[str, dict[str, Any]]]:
    by_file: dict[str, dict[str, dict[str, Any]]] = {}
    if not chat_log_dir.exists():
        return by_file

    for path in sorted(chat_log_dir.glob("*.jsonl")):
        by_tool_call: dict[str, dict[str, Any]] = {}
        with path.open("r", encoding="utf-8-sig") as handle:
            for line_no, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    root = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for item in iter_dicts(root):
                    if item.get("kind") != "toolInvocationSerialized":
                        continue
                    tool_call_id = item.get("toolCallId")
                    if not tool_call_id:
                        continue
                    by_tool_call[str(tool_call_id)] = {
                        "line": line_no,
                        "tool_id": str(item.get("toolId") or ""),
                        "subagent_invocation_id": str(item.get("subAgentInvocationId") or ""),
                        "is_complete": item.get("isComplete"),
                        "result_is_error": (item.get("resultDetails") or {}).get("isError")
                        if isinstance(item.get("resultDetails"), dict)
                        else None,
                        "result_details": item.get("resultDetails"),
                        "tool_specific_data": item.get("toolSpecificData"),
                    }
        if by_tool_call:
            by_file[path.name] = by_tool_call

    return by_file


def terminal_log_summary(log_entry: dict[str, Any] | None) -> dict[str, Any]:
    if not log_entry:
        return {}
    data = log_entry.get("tool_specific_data")
    if not isinstance(data, dict) or data.get("kind") != "terminal":
        return {}
    state = data.get("terminalCommandState") if isinstance(data.get("terminalCommandState"), dict) else {}
    command_line = data.get("commandLine") if isinstance(data.get("commandLine"), dict) else {}
    output = data.get("terminalCommandOutput") if isinstance(data.get("terminalCommandOutput"), dict) else {}
    cwd = data.get("cwd") if isinstance(data.get("cwd"), dict) else {}
    return {
        "exit_code": state.get("exitCode"),
        "duration": state.get("duration"),
        "timestamp": state.get("timestamp"),
        "command": command_line.get("original") or command_line.get("forDisplay"),
        "cwd": cwd.get("path"),
        "output_line_count": output.get("lineCount"),
        "output_text": output.get("text"),
    }


def extract_file(path: Path, agent_name: str) -> list[SubagentInvocation]:
    events = load_jsonl(path)
    parent_by_id = {event.event_id: event.parent_id for event in events if event.event_id}
    completions = completion_events_by_tool_call(events)
    invocations_by_start_id: dict[str, SubagentInvocation] = {}
    requests_by_tool_call: dict[str, dict[str, Any]] = {}

    for event in events:
        if event.event_type != "assistant.message":
            continue
        for request in event.data.get("toolRequests") or []:
            if request.get("name") != "runSubagent":
                continue
            arguments = parse_tool_arguments(request.get("arguments"))
            if arguments.get("agentName") != agent_name:
                continue
            requests_by_tool_call[str(request.get("toolCallId") or "")] = {
                "line": event.line,
                "timestamp": event.timestamp,
                "message_id": event.event_id,
            }

    for event in events:
        data = event.data
        if event.event_type != "tool.execution_start":
            continue
        if data.get("toolName") != "runSubagent":
            continue

        arguments = parse_tool_arguments(data.get("arguments"))
        if arguments.get("agentName") != agent_name:
            continue

        tool_call_id = str(data.get("toolCallId") or "")
        request_event = requests_by_tool_call.get(tool_call_id, {})
        invocation = SubagentInvocation(
            file=path.name,
            request_line=request_event.get("line"),
            request_timestamp=str(request_event.get("timestamp") or ""),
            request_message_id=str(request_event.get("message_id") or ""),
            line=event.line,
            event_id=event.event_id,
            parent_id=event.parent_id,
            tool_call_id=tool_call_id,
            timestamp=event.timestamp,
            description=str(arguments.get("description") or ""),
            prompt=str(arguments.get("prompt") or ""),
        )

        completion = next(iter(completions.get(tool_call_id, [])), None)
        if completion:
            invocation.success = bool(completion.data.get("success"))
            invocation.complete_line = completion.line
            invocation.complete_timestamp = completion.timestamp

        invocations_by_start_id[event.event_id] = invocation

    run_start_ids = set(invocations_by_start_id)
    run_tool_call_by_start_id = {
        start_id: invocation.tool_call_id for start_id, invocation in invocations_by_start_id.items()
    }

    def nearest_run_start(event: TranscriptEvent) -> str | None:
        current = event.parent_id
        seen: set[str] = set()
        while current and current not in seen:
            seen.add(current)
            if current in run_start_ids:
                return current
            current = parent_by_id.get(current, "")
        return None

    for event in events:
        start_id = nearest_run_start(event)
        if not start_id:
            continue

        invocation = invocations_by_start_id[start_id]
        if event.line <= invocation.line:
            continue
        if invocation.complete_line is not None and event.line > invocation.complete_line:
            continue

        # A target-agent runSubagent start nested under another target-agent
        # start is a separate invocation boundary, not a normal child tool.
        # VS Code/Copilot transcripts can serialize parallel sibling subagent
        # calls this way, which previously inflated tool counts and produced
        # confusing `runSubagent - unknown` entries inside the parent.
        if event.event_id in run_start_ids:
            nested = invocations_by_start_id[event.event_id]
            invocation.nested_invocation_ids.append(nested.event_id)
            invocation.nested_tool_call_ids.append(nested.tool_call_id)
            continue

        invocation.events.append(event)

    for invocation in invocations_by_start_id.values():
        tools = collect_tool_invocations(invocation)
        non_wrapper_tools = [tool for tool in tools if not is_target_subagent_tool(tool, agent_name)]
        thinking = collect_thinking(invocation)
        # If an older transcript shape still leaves a nested target-agent
        # runSubagent request in the event stream, capture it as nested metadata.
        for tool in tools:
            if (tool.get("name") or "") != "runSubagent":
                continue
            arguments = tool.get("arguments") or {}
            if arguments.get("agentName") != agent_name:
                continue
            tool_call_id = str(tool.get("tool_call_id") or "")
            if tool_call_id and tool_call_id not in invocation.nested_tool_call_ids:
                invocation.nested_tool_call_ids.append(tool_call_id)
            for nested_start_id, nested_tool_call_id in run_tool_call_by_start_id.items():
                if nested_tool_call_id != tool_call_id:
                    continue
                if nested_start_id != invocation.event_id and nested_start_id not in invocation.nested_invocation_ids:
                    invocation.nested_invocation_ids.append(nested_start_id)
        invocation.wrapper_invocation = (
            not non_wrapper_tools
            and not thinking
            and (bool(tools) or bool(invocation.nested_tool_call_ids))
        )

    return sorted(invocations_by_start_id.values(), key=lambda item: item.line)


def extract_invocations(transcript_dir: Path, agent_name: str) -> list[SubagentInvocation]:
    invocations: list[SubagentInvocation] = []
    for path in sorted(transcript_dir.glob("*.jsonl")):
        invocations.extend(extract_file(path, agent_name))
    return sorted(invocations, key=lambda item: (item.file, item.line))


def collect_thinking(invocation: SubagentInvocation) -> list[tuple[int, str, str]]:
    thinking: list[tuple[int, str, str]] = []
    for event in invocation.events:
        if event.event_type != "assistant.message":
            continue
        reasoning = event.data.get("reasoningText")
        if reasoning:
            thinking.append((event.line, event.timestamp, str(reasoning)))
    return thinking


def collect_tool_invocations(
    invocation: SubagentInvocation,
    log_tools: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    tool_requests: list[dict[str, Any]] = []
    tool_starts: dict[str, dict[str, Any]] = {}
    completions: dict[str, dict[str, Any]] = {}

    for event in invocation.events:
        data = event.data
        if event.event_type == "assistant.message":
            for request in data.get("toolRequests") or []:
                arguments = parse_tool_arguments(request.get("arguments"))
                tool_requests.append(
                    {
                        "request_line": event.line,
                        "request_timestamp": event.timestamp,
                        "tool_call_id": str(request.get("toolCallId") or ""),
                        "name": str(request.get("name") or ""),
                        "arguments": arguments,
                        "command": str(arguments.get("command") or ""),
                        "explanation": str(arguments.get("explanation") or ""),
                        "goal": str(arguments.get("goal") or ""),
                    }
                )

        if event.event_type == "tool.execution_start" and data.get("toolName"):
            arguments = parse_tool_arguments(data.get("arguments"))
            tool_starts[str(data.get("toolCallId") or "")] = {
                "start_line": event.line,
                "timestamp": event.timestamp,
                "name": str(data.get("toolName") or ""),
                "arguments": arguments,
                "command": str(arguments.get("command") or ""),
                "explanation": str(arguments.get("explanation") or ""),
                "goal": str(arguments.get("goal") or ""),
            }

        if event.event_type == "tool.execution_complete" and data.get("toolCallId"):
            completions[str(data.get("toolCallId"))] = {
                "line": event.line,
                "timestamp": event.timestamp,
                "success": data.get("success"),
            }

    seen = {request["tool_call_id"] for request in tool_requests}
    for tool_call_id, start in tool_starts.items():
        if tool_call_id in seen:
            continue
        tool_requests.append(
            {
                "request_line": None,
                "request_timestamp": "",
                "tool_call_id": tool_call_id,
                "name": start["name"],
                "arguments": start["arguments"],
                "command": start["command"],
                "explanation": start["explanation"],
                "goal": start["goal"],
            }
        )

    for request in tool_requests:
        start = tool_starts.get(request["tool_call_id"])
        if start:
            request["start"] = start
            request.setdefault("name", start["name"])
            if not request.get("command"):
                request["command"] = start["command"]
            if not request.get("explanation"):
                request["explanation"] = start["explanation"]
            if not request.get("goal"):
                request["goal"] = start["goal"]
        request["completion"] = completions.get(request["tool_call_id"])
        log_entry = (log_tools or {}).get(invocation.file, {}).get(request["tool_call_id"])
        request["log"] = log_entry
        request["terminal_log"] = terminal_log_summary(log_entry)

    return sorted(
        tool_requests,
        key=lambda item: (
            item.get("request_line") or (item.get("start") or {}).get("start_line") or 0,
            item["tool_call_id"],
        ),
    )


def collect_ordered_events(
    invocation: SubagentInvocation,
    log_tools: dict[str, dict[str, dict[str, Any]]] | None = None,
    target_agent_name: str = "",
) -> list[dict[str, Any]]:
    ordered: list[dict[str, Any]] = []
    tool_invocations = collect_tool_invocations(invocation, log_tools)

    visible_tools = [
        tool for tool in tool_invocations if not is_target_subagent_tool(tool, target_agent_name)
    ]
    for index, tool in enumerate(visible_tools, 1):
        start = tool.get("start") or {}
        ordered.append(
            {
                "kind": "tool",
                "line": start.get("start_line") or tool.get("request_line") or 0,
                "index": index,
                "tool": tool,
            }
        )

    thinking_index = 0
    for event in invocation.events:
        if event.event_type != "assistant.message":
            continue
        reasoning = event.data.get("reasoningText")
        if not reasoning:
            continue
        thinking_index += 1
        ordered.append(
            {
                "kind": "thinking",
                "line": event.line,
                "index": thinking_index,
                "timestamp": event.timestamp,
                "text": str(reasoning),
            }
        )

    return sorted(ordered, key=lambda item: (item["line"], 0 if item["kind"] == "thinking" else 1, item["index"]))


def status_label(success: Any) -> str:
    if success is None:
        return "unknown"
    return "success" if bool(success) else "failure"


def effective_tool_status(tool: dict[str, Any]) -> str:
    terminal = tool.get("terminal_log") or {}
    exit_code = terminal.get("exit_code")
    if isinstance(exit_code, int):
        return "success" if exit_code == 0 else "failure"
    log_entry = tool.get("log") or {}
    if log_entry.get("result_is_error") is True:
        return "failure"
    completion = tool.get("completion")
    if completion:
        return status_label(completion.get("success"))
    return "unknown"


def is_target_subagent_tool(tool: dict[str, Any], agent_name: str) -> bool:
    if not agent_name:
        return False
    if (tool.get("name") or "") != "runSubagent":
        return False
    arguments = tool.get("arguments") or {}
    return arguments.get("agentName") == agent_name


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def unique_ordered(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def render_markdown(
    invocations: list[SubagentInvocation],
    transcript_dir: Path,
    agent_name: str,
    log_tools: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> str:
    transcript_display = display_path(transcript_dir)
    lines: list[str] = []
    lines.append(f"# {agent_name} Subagent Invocations")
    lines.append("")
    lines.append(
        f"Generated from `{transcript_display}` on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
    )
    lines.append("")
    lines.append(f"Total {agent_name} invocations: {len(invocations)}.")
    lines.append("")
    wrapper_count = sum(1 for invocation in invocations if invocation.wrapper_invocation)
    nested_reference_count = sum(1 for invocation in invocations if invocation.nested_tool_call_ids)
    lines.append(f"Wrapper-only invocations: {wrapper_count}.")
    lines.append(f"Invocations with nested/wrapper subagent references: {nested_reference_count}.")
    lines.append("")
    lines.append(
        "For each invocation, the top-level status is the `runSubagent` tool completion status. "
        "Tool statuses use terminal exit codes from matching chat logs when available; non-zero terminal exit codes are reported as failures. "
        "Nested target-agent `runSubagent` starts are reported as wrapper metadata instead of ordinary tool failures."
    )
    lines.append("")

    for number, invocation in enumerate(invocations, 1):
        title = invocation.description or one_line(invocation.prompt)[:80] or invocation.tool_call_id
        lines.append(f"## {number}. {title}")
        lines.append("")
        lines.append(f"- File: `{transcript_display}/{invocation.file}`")
        if invocation.request_line:
            lines.append(f"- Invocation request line: `{invocation.request_line}`")
        if invocation.request_timestamp:
            lines.append(f"- Invocation request timestamp: `{invocation.request_timestamp}`")
        if invocation.request_message_id:
            lines.append(f"- Invocation request message id: `{invocation.request_message_id}`")
        lines.append(f"- Execution start line: `{invocation.line}`")
        lines.append(f"- Execution start id: `{invocation.event_id}`")
        lines.append(f"- Tool call id: `{invocation.tool_call_id}`")
        lines.append(f"- Execution start timestamp: `{invocation.timestamp}`")
        if invocation.complete_line:
            lines.append(f"- Completion line: `{invocation.complete_line}`")
        if invocation.complete_timestamp:
            lines.append(f"- Completion timestamp: `{invocation.complete_timestamp}`")
        lines.append(f"- Invocation status: `{status_label(invocation.success)}`")
        lines.append(f"- Wrapper-only invocation: `{'yes' if invocation.wrapper_invocation else 'no'}`")
        nested_tool_call_ids = unique_ordered(invocation.nested_tool_call_ids)
        nested_invocation_ids = unique_ordered(invocation.nested_invocation_ids)
        if nested_tool_call_ids:
            lines.append(
                "- Nested/wrapper subagent tool call ids: "
                + ", ".join(f"`{tool_call_id}`" for tool_call_id in nested_tool_call_ids)
            )
        if nested_invocation_ids:
            lines.append(
                "- Nested/wrapper subagent execution start ids: "
                + ", ".join(f"`{event_id}`" for event_id in nested_invocation_ids)
            )
        lines.append("")
        lines.append("### Full Prompt")
        lines.append("")
        lines.append(markdown_fence(invocation.prompt))
        lines.append("")

        lines.append("### Events In Order")
        lines.append("")
        ordered_events = collect_ordered_events(invocation, log_tools, agent_name)
        if ordered_events:
            for event in ordered_events:
                if event["kind"] == "thinking":
                    lines.append(
                        f"#### Thinking {event['index']} "
                        f"(line {event['line']}, timestamp `{event['timestamp']}`)"
                    )
                    lines.append("")
                    lines.append(markdown_fence(event["text"]))
                    lines.append("")
                    continue

                tool = event["tool"]
                completion = tool.get("completion")
                start = tool.get("start") or {}
                transcript_success = completion.get("success") if completion else None
                tool_name = tool.get("name") or start.get("name") or "unknown"
                lines.append(f"#### Tool {event['index']}: `{tool_name}` - `{effective_tool_status(tool)}`")
                lines.append("")
                if tool.get("request_line"):
                    lines.append(f"- Request line: `{tool['request_line']}`")
                if tool.get("request_timestamp"):
                    lines.append(f"- Request timestamp: `{tool['request_timestamp']}`")
                if start:
                    lines.append(f"- Execution start line: `{start['start_line']}`")
                    if start.get("timestamp"):
                        lines.append(f"- Execution start timestamp: `{start['timestamp']}`")
                lines.append(f"- Tool call id: `{tool['tool_call_id']}`")
                if completion:
                    lines.append(f"- Completion line: `{completion['line']}`")
                    if completion.get("timestamp"):
                        lines.append(f"- Completion timestamp: `{completion['timestamp']}`")
                    lines.append(f"- Transcript completion status: `{status_label(transcript_success)}`")
                log_entry = tool.get("log")
                terminal = tool.get("terminal_log") or {}
                if log_entry:
                    lines.append(f"- Chat log line: `{log_entry['line']}`")
                    if log_entry.get("result_is_error") is not None:
                        lines.append(f"- Chat log result error: `{bool(log_entry['result_is_error'])}`")
                if terminal:
                    lines.append(f"- Terminal exit code: `{terminal.get('exit_code')}`")
                    lines.append(
                        f"- Terminal exit status: `{'success' if terminal.get('exit_code') == 0 else 'failure'}`"
                    )
                    if terminal.get("duration") is not None:
                        lines.append(f"- Terminal duration ms: `{terminal['duration']}`")
                    if terminal.get("cwd"):
                        lines.append(f"- Terminal cwd: `{terminal['cwd']}`")
                    if terminal.get("output_line_count") is not None:
                        lines.append(f"- Terminal output line count: `{terminal['output_line_count']}`")
                lines.append(f"- Explanation: {tool.get('explanation') or ''}")
                lines.append(f"- Goal: {tool.get('goal') or ''}")
                lines.append("")
                if terminal and terminal.get("exit_code") not in (None, 0) and terminal.get("output_text"):
                    lines.append("Terminal Output:")
                    lines.append("")
                    lines.append(markdown_fence(terminal["output_text"]))
                    lines.append("")
                if tool.get("command"):
                    lines.append("Command:")
                    lines.append("")
                    lines.append(markdown_fence(tool["command"]))
                    lines.append("")
                lines.append("Arguments:")
                lines.append("")
                lines.append(markdown_fence(json.dumps(tool.get("arguments") or {}, indent=2, ensure_ascii=False)))
                lines.append("")
        else:
            lines.append("_No thinking turns or tool invocations recorded inside this subagent invocation._")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    log_tools = index_chat_log_tools(args.chat_log_dir)
    invocations = extract_invocations(args.transcript_dir, args.agent)
    markdown = render_markdown(invocations, args.transcript_dir, args.agent, log_tools)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.output} with {len(invocations)} {args.agent} invocations.")


if __name__ == "__main__":
    main()

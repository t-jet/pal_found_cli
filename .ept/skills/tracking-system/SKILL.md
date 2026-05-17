---
name: tracking-system
description: >-
  Manages a ticket tracking system for AI agent collaboration.
  Use this skill to retrieve workflow documentation, inspect ticket type
  definitions and allowed status transitions, and perform all ticket,
  comment, and link operations. Activate when an agent needs to create,
  read, update, or search tickets; update ticket fields or description
  after creation; filter tickets by parent, reporter, assignee, status,
  type, or priority; add, read, or update comments; create, list, or
  remove inter-ticket links; inspect the workflow configuration
  (ticket types, statuses, stage goals, responsible roles, transitions,
  definitions of done, or automatic transition rules); or generate a
  prioritized build queue with blocking relationships and priority
  reconciliation. Keywords: tracker, ticket, issue, task, bug, feature,
  epic, dev story, question, workitem, comment, link, workflow, status,
  transition, assignee, priority, stage, DoD, create ticket, update ticket,
  update field, update description, list tickets, filter by parent, filter
  by reporter, search tickets, get ticket, comment create, comment get,
  comment update, comment list, link create, link list, link remove,
  workflow status, workflow transitions, workflow types, type-info,
  automatic transitions, build queue, build-queue, priority reconciliation,
  blocking relationships, work queue, queue tickets.
compatibility: Requires Python with PyYAML; run from the project where `.ept/tracker/` exists.
metadata:
  author: t-jet
  version: "0.1.0"
---

## Overview

This skill operates the tracking system using CLI interface.
All operations MUST go through the CLI.

Read full [references/REFERENCE.md](references/REFERENCE.md) for full command syntax, field descriptions, and exit codes.

## Operational Rules

### CLI-only tracker access

All tracker work MUST be performed through the CLI documented in [references/REFERENCE.md](references/REFERENCE.md).

Do not read, write, search, or infer from internal tracker storage under `.ept/tracker/` directly. This includes ticket markdown files, indexes, workflow configuration files, and cache/state files. The internal storage layout is not part of the agent contract.

Allowed direct file reads for this skill are limited to this `SKILL.md` and the public reference documentation under `references/`.

### Preflight every command

Before running any tracker CLI command, validate the intended command against [references/REFERENCE.md](references/REFERENCE.md):

- Use only documented commands, subcommands, positional arguments, and options.
- Check required arguments and flags before execution, especially `--author` and `--subject` where applicable.
- Do not invent convenience commands or aliases such as `ticket`, `tickets`, `comments`, `links`, or `comment add`.
- Do not use unsupported options such as `--body`, `--value`, `--include-comments`, `--include-linked`, `--resolution`, `--reporter` on commands where the reference does not list them.
- For ticket creation, use `type-info <type>` or prior CLI YAML output to identify required fields before calling `create`.
- For status changes, run or reuse `workflow transitions <type> <current-status>` before `update --status`.
- For link creation, use only link types accepted by the CLI.

If preflight fails, correct the command before executing it.

### Terminal exit code is authoritative

After every terminal command, use the terminal process exit code as the source of truth:

- Exit code `0` means success.
- Non-zero exit code means failure, even if the surrounding tool invocation is marked complete or successful.
- On failure, read the error output, correct the command only if the fix is specific and justified by the error plus the reference, and retry at most once.
- Stop dependent operations after a non-zero exit code until the failed command is corrected and succeeds.
- For configuration or unexpected errors, report the exact command, exit code, and error output. Do not inspect `.ept/tracker/` internals to diagnose them.

### Reuse CLI YAML status-context output

The CLI is designed to return YAML status-context blocks that contain the
information needed for follow-up ticket processing. Parse and reuse this YAML
before making additional calls.

In particular:

- After `get`, use the returned status context, metadata, and content body as the current ticket state.
- After `create`, use `ticket_id`, `current_status`, `allowed_transitions`, `definitions_of_done`, `instructions`, and other returned YAML fields for the next step.
- After `update --status`, use the returned YAML status context to decide whether another transition is allowed or whether work should stop.
- After `type-info`, reuse required fields, optional fields, terminal statuses, ticket instructions, status catalogue, and transition information.
- After `workflow status` or `workflow transitions`, reuse those results during the current request instead of repeating the same command.

Make additional CLI calls only when the needed information is absent, stale due to a successful mutation, or explicitly requested.

### Cross-platform command construction

Commands must work across Windows, macOS, and Linux:

- Prefer direct invocation of the Python CLI: `python .ept/skills/tracking-system/tracker/tracker_cli.py ...`
- Avoid shell-specific constructs in tracker commands unless the environment has been explicitly detected and the construct is necessary.
- Avoid command chaining for tracker operations. Execute one documented CLI command at a time and consume its output.
- Do not rely on PowerShell-only syntax such as here-strings, `Remove-Item`, `$env:...`, or `;` chaining in generic tracker workflows.
- Do not rely on POSIX-only syntax such as heredocs, `rm`, `export`, or `&&` chaining in generic tracker workflows.
- For repeated work, plan a pipeline of documented CLI commands and feed each command's YAML/status output into the next command.

### Multiline text handling

Use only multiline mechanisms documented in [references/REFERENCE.md](references/REFERENCE.md):

- `create --description <text>` decodes `\n`, `\r\n`, and `\t`.
- `create --description-file <path>` reads the ticket description from a file.
- `update --description <text>` decodes `\n`, `\r\n`, and `\t`.
- `update --description-file <path>` replaces the ticket body from a file.
- `comment create --text <body>` supports `\n` escape sequences.
- `comment update --text <body>` supports the documented comment update path.

Do not use undocumented options such as `comment create --text-file` unless the reference is updated to include them.

Avoid passing large Markdown bodies through shell-sensitive inline strings. For long ticket descriptions, prefer `--description-file`. For comments, keep text concise and use escaped newlines with `--text`.

## Build queue generation rules

If you're asked to generate work queue in different forms like in the examples below, always use the `build-queue all` command to generate the full build queue with all available information and return results.

Examples:
- "Build a prioritized work queue of all non-terminal tickets. Execute build-queue all. Return the complete queue with all ticket metadata, statuses, priorities, assignees, and blocking relationships arranged in implementation order."
- "Get ready tickets for workflow"
- "Generate a prioritized build queue with blocking relationships and priority reconciliation"

## Operational notes

Always refer to the [references/REFERENCE.md](references/REFERENCE.md) for detailed operational guidance, including command syntax, field descriptions, and exit codes.



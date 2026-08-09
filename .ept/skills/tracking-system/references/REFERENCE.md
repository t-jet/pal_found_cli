# Tracking System — Technical Reference

Full command syntax, field descriptions, and exit codes for the tracking system.
All workflow parameters (ticket types, statuses, link types, priorities, transitions) are
configuration-driven — retrieve them at runtime using the workflow CLI commands.

---

## CLI Entry Points

| Entry point | Location | Notes |
|---|---|---|
| Unified CLI | `.ept/skills/tracking-system/tracker/tracker_cli.py` | All commands via one script |
| Wrapper module | `.ept/skills/tracking-system/tracker/tracker_wrapper.py` | Shared helpers for wrapper scripts |

```bash
# Unified CLI
python .ept/skills/tracking-system/tracker/tracker_cli.py <command> [subcommand] [args]
```

---

## Ticket Commands

### `create`

```
python .ept/skills/tracking-system/tracker/tracker_cli.py create <type> [title] --author <role> [options]
```

| Argument / Option | Required | Description |
|---|---|---|
| `<type>` | Yes | Ticket type key — run `workflow types` to list valid values |
| `<title>` | Yes† | Ticket title (positional or `--title`) |
| `--title <text>` | Yes† | Keyword form (avoids shell quoting issues) |
| `--priority <level>` | No | Priority level (default: Medium) — run `workflow types` to see valid values |
| `--assignee <role>` | No | Assignee role identifier |
| `--parent <id>` | No | Parent ticket ID (alias: `--child-of`) |
| `--child-of <id>` | No | Alias for `--parent` |
| `--addressed-to <role>` | No | Target role (used with `question` type) |
| `--description <text>` | No | Inline description; `\n`, `\r\n`, `\t` decoded |
| `--description-file <path>` | No | Path to file whose contents become description |
| `--field key=value` | No | Extra structured field (repeatable) |
| `--author <role>` | **Yes** | Author / actor identifier |

†  Either positional `<title>` or `--title` must be supplied; not both.

**Repeatable options**: `--field` can be specified multiple times to set multiple optional fields in a single command.

Example:

```bash
# Create with multiple fields
python .ept/skills/tracking-system/tracker/tracker_cli.py create question \
    --title "How should we handle errors?" \
    --addressed-to architect \
    --field component=error-handling \
    --field labels=discussion \
    --author developer
```

**Output on success** — YAML status-context block:

```yaml
ticket_id: TASK-001
current_status: New
status_description: "Ticket created and awaiting triage."
status_goal: "Prepare the ticket for execution."
status_responsible_roles: [Requester]
allowed_transitions: [Open, Canceled]
definitions_of_done:
  - target_statuses: [Open]
    dod_criteria:
      - Acceptance criteria defined
      - Assignee set
instructions:
  - Set assignee to ticket creator.
  - Move to Open when DoD is met.
```

---

### `get`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py get <ticket-id> [--author <role>]
```

Returns the YAML status-context block **plus** full ticket metadata and content body.

---

### `list`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py list [--status <status>] [--assignee <role>]
    [--type <type>] [--priority <level>] [--parent <ticket-id>] [--reporter <role>]
    [--non-terminal-only] [--author <role>]
```

All filters are optional and combinable. Returns a tabular summary (ID, status, priority, assignee, title).

| Option | Description |
|---|---|
| `--status <status>` | Filter by current status (repeatable; multiple values use OR logic) |
| `--assignee <role>` | Filter by assignee |
| `--type <type>` | Filter by ticket type (repeatable; multiple values use OR logic) |
| `--priority <level>` | Filter by priority (repeatable; multiple values use OR logic) |
| `--parent <ticket-id>` | Return only direct children of the given ticket. The parent ticket must exist. |
| `--reporter <role>` | Filter by the author who created the ticket |
| `--non-terminal-only` | Exclude tickets in terminal statuses (flag; no value required) |

**Multiple values format**: For repeatable options (`--status`, `--type`, `--priority`), specify the parameter multiple times. Tickets matching ANY of the provided values will be returned (OR logic).

Examples:

```bash
# List tickets with status "New" OR "Open" OR "In Progress"
python .ept/skills/tracking-system/tracker/tracker_cli.py list --status New --status Open --status "In Progress"

# List "feature" OR "task" tickets with "High" OR "Critical" priority
python .ept/skills/tracking-system/tracker/tracker_cli.py list --type feature --type task --priority High --priority Critical

# List all non-terminal tickets (excludes Done, Canceled, etc.)
python .ept/skills/tracking-system/tracker/tracker_cli.py list --non-terminal-only

# Combine filters: non-terminal tasks assigned to a specific role
python .ept/skills/tracking-system/tracker/tracker_cli.py list --non-terminal-only --type task --assignee developer
```

---

### `update`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py update <ticket-id> --author <role>
    [--status <status>] [--assignee <role>] [--priority <level>]
    [--field key=value] [--description <text>] [--description-file <path>]
```

At least one of `--status`, `--assignee`, `--priority`, `--field`, `--description`, or `--description-file` must be provided.

| Option | Description |
|---|---|
| `--status <status>` | Transition to a new status (validated against `allowed_transitions`) |
| `--assignee <role>` | Change the assignee |
| `--priority <level>` | Change the priority |
| `--field key=value` | Update an optional ticket field by name (repeatable). The field must be in the ticket type's allowed field list. Supplying an unknown or disallowed field name raises a validation error naming the offending field and listing allowed values. |
| `--description <text>` | Replace the ticket body text; `\n`, `\r\n`, `\t` are decoded |
| `--description-file <path>` | Replace the ticket body with the contents of a file |

- `--status` transitions are validated against `allowed_transitions` in the workflow.
- When `--status` is supplied, output is the YAML status-context block.
- Other field-only updates print a brief confirmation line.
- Every write produces an auto-generated comment listing which fields were modified.

Always run `workflow transitions <type> <current-status>` before updating status.

**Repeatable options**: `--field` can be specified multiple times to update multiple optional fields in a single command.

Example:

```bash
# Update multiple fields
python .ept/skills/tracking-system/tracker/tracker_cli.py update TASK-001 \
    --field component=ui \
    --field labels=refactoring \
    --author developer
```

---

### `search`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py search <query> [--in-title] [--in-content] [--author <role>]
```

`--in-title` is on by default. Combine with `--in-content` to search both fields.

---

## Comment Commands

### `comment create`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py comment create <ticket-id>
    --subject <text> [--text <body>] --author <role>
```

`--text` supports `\n` escape sequences for multi-line content.
All execution plans, summaries, and decisions **must** be stored as comments (not separate files).

---

### `comment list`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py comment list <ticket-id> [--author <role>]
```

Returns tabular summary: comment-id, author, created, updated, subject. No body text — use `comment get` for full text.

---

### `comment get`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py comment get <ticket-id> <comment-id> [--author <role>]
```

Returns metadata + full body. `<comment-id>` is the timestamp–author composite key from `comment create` / `comment list`.

---

### `comment update`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py comment update <ticket-id> <comment-id>
    [--subject <text>] [--text <body>] --author <role>
```

At least one of `--subject` or `--text` must be supplied. Updated timestamp is refreshed automatically.

---

## Link Commands

### `link create`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py link create <source-id> <target-id> <link-type>
    --author <role> [--comment <text>]
```

Both ticket IDs must exist. Valid link types are configuration-driven — run `python .ept/skills/tracking-system/tracker/tracker_cli.py --help-toon` to see currently registered values.
Returns the assigned link ID (`LINK-NNNNN`) on success.

---

### `link list`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py link list <ticket-id>
    [--direction in|out|all] [--author <role>]
```

`--direction` default: `all`. Output columns: link-id, source, target, link-type, role-of-queried-ticket.

---

### `link remove`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py link remove <link-id> --author <role>
```

`<link-id>` format: `LINK-NNNNN`. Both forward and reverse records are removed atomically. Irreversible.

---

## Workflow Commands (read-only)

### `type-info`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py type-info <type> [--author <role>]
```

Prints the full YAML information for a single ticket type. Useful for inspecting the full type
definition that the workflow is built from.

| Top-level key | Description |
|---|---|
| `type` | Ticket type key (e.g. `feature`, `task`) |
| `id_prefix` | Ticket ID prefix used when generating IDs (e.g. `FEATURE`, `TASK`) |
| `description` | Human-readable summary of the ticket type's purpose |
| `required_fields` | Fields that must be set on every ticket of this type |
| `optional_fields` | Fields that may be set but are not mandatory |
| `initial_status` | Status assigned automatically when the ticket is created |
| `terminal_statuses` | Statuses from which no further transitions are allowed |
| `statuses` | Full status catalogue — each entry carries `description`, `stage_goal`, and `responsible_roles` |
| `allowed_transitions` | Explicit per-status transition map: `status → [allowed next statuses]` |
| `automatic_transitions` | Optional list of structured rules that transition the ticket automatically when conditions are met. Rules are evaluated after every `create` and `update` operation. Each rule carries a `rule` key identifying its type (e.g. `all_children_reach_status`, `first_child_reaches_status`, `linked_ticket_reaches_status`, `child_blocker_created`, `all_blockers_cleared`, `this_ticket_reaches_status`). Transitions are performed by the system and do not require a manual `update` call. |
| `ticket_instructions` | Per-status instructions for agents acting on tickets of this type |

Valid type keys are configuration-driven — run `workflow types` to list all registered values.

---

### `workflow types`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py workflow types [--author <role>]
```

Lists all registered ticket types: key, ID prefix, status count, initial status, terminal statuses.

---

### `workflow status`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py workflow status [<type> [<status-name>]] [--author <role>]
```

| Invocation | Output |
|---|---|
| `workflow status` | Cross-type summary of all types and their statuses |
| `workflow status <type>` | All statuses for `<type>` with stage goals and terminal markers |
| `workflow status <type> <status-name>` | Full detail: description, stage goal, responsible roles, allowed transitions |

---

### `workflow transitions`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py workflow transitions <type> [<status-name>] [--author <role>]
```

| Invocation | Output |
|---|---|
| `workflow transitions <type>` | Complete transition table (from-status → allowed to-statuses) |
| `workflow transitions <type> <status-name>` | Exits from `<status-name>` only |

Use this **before every** `update --status` call to verify the move is allowed.

---

## Build Queue Commands (read-only)

The `build-queue` command generates a prioritized work queue of non-terminal tickets,
automatically reconciling priorities based on parent-child and blocking relationships.

### `build-queue all`

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py build-queue all
```

**Run all stages**

Executes stages 1-4 in sequence: filter, reconcile, sort, and output. This is the recommended
command for generating a complete build queue.



---

## Index reconciliation

```bash
python .ept/skills/tracking-system/tracker/tracker_cli.py reconcile-index --author <role> [--apply]
```

Without `--apply`, this command reports status differences between ticket
frontmatter and the CSV index without changing files. With `--apply`, it copies
canonical frontmatter statuses into the index. Ticket content, timestamps,
comments, and links remain unchanged.

---

## Fields

### Core fields (all ticket types)

| Field | Type | Notes |
|---|---|---|
| `id` | string | Immutable. Format `<PREFIX>-<NNN>` |
| `type` | string | Ticket type key — valid values from `workflow types` |
| `title` | string | Immutable after creation |
| `status` | string | Current lifecycle status — valid values from `workflow status <type>` |
| `priority` | string | Priority level — valid values from `workflow types` |
| `assignee` | string | Role or agent identifier |
| `reporter` | string | Creator role or agent identifier |
| `created` | datetime | ISO 8601 timestamp set on creation |
| `updated` | datetime | ISO 8601 timestamp; refreshed on every mutation |

### Optional fields

| Field | Type | Notes |
|---|---|---|
| `parent` | string | Parent ticket ID (physical folder; persisted in index only) |
| `addressed_to` | string | Target role for `question` tickets |
| `epic` | string | Epic ticket ID (logical grouping via Epic Link) |
| `feature_request` | string | Feature Request ID |
| `component` | string | Functional module this ticket relates to |
| `labels` | list | Free-form classification tags |
| `sprint` | string | Sprint name or identifier |
| `prior_status` | string | Status saved automatically before a ticket is moved to `Blocked` by an automatic transition rule. Restored when all blockers are cleared. Cleared after the restore. Managed by the system; do not set manually. |

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `2` | Validation error (invalid type, status, transition, missing required arg) |
| `3` | Configuration error (bad config structure or missing configuration) |
| `4` | File operation error (ticket not found, IO failure) |
| `5` | Unexpected / unhandled error |

---

## Pre-Action Checklist for Agents

Before ANY write operation:

1. **Search for existing tickets** using `tracker_cli.py search` or `tracker_cli.py list`.
2. **Read workflow docs** — `workflow status <type>` + `workflow transitions <type> <status>`.
3. **Search open question tickets** before creating a new `question` type ticket (avoid duplicates).
4. **Verify allowed transition** via `workflow transitions` before every `update --status`.
5. **Record decisions and plans** as ticket comments, not as separate files.

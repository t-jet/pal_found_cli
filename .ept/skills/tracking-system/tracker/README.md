# Tracking System CLI Utility

A file-based ticket management CLI, organized as the `tracker` Python package.
Use this CLI instead of direct edits to files under `.ept/tracker/`.

## Project Structure

```
tracker/                    # Python package
├── __init__.py             # Public exports (exception classes)
├── __main__.py             # python -m tracker entry point
├── cli.py                  # Argparse setup, main(), TOON help builder
├── config.py               # TrackerPaths dataclass, workflow loading, runtime config
├── constants.py            # Exit codes, templates, field-name lists
├── comments.py             # Comment CRUD operations
├── exceptions.py           # TrackerError, ValidationError, etc.
├── formatters.py           # Display formatting + TOON encoder
├── index.py                # CSV index read/write, ID counter management
├── links.py                # Inter-ticket link CRUD
├── tickets.py              # Ticket CRUD, frontmatter parsing, search
├── utils.py                # Sanitization, escapes, timestamps, frontmatter builder
└── validators.py           # Type, status, link, direction validation
tests/                      # Pytest test suite
├── conftest.py             # Shared fixtures (tracker_env, helpers, YAML scaffolds)
├── test_cli.py             # CLI integration tests via main()
├── test_comments.py
├── test_config.py
├── test_e2e.py             # Subprocess E2E tests
├── test_formatters.py
├── test_links.py
├── test_tickets.py
├── test_utils.py
└── test_validators.py
tracker_cli.py              # Thin backward-compatible entry point
pyproject.toml              # Project metadata, dependencies, pytest config
```

## Setup

```bash
# With uv
uv venv .venv
uv pip install --python .venv/Scripts/python.exe pyyaml

# Or with pip
pip install pyyaml
pip install pytest pytest-cov   # dev only
```

## Running

```bash
# Via the wrapper (backward compatible)
python tracker_cli.py <command> --author <role>

# Via the package
python -m tracker <command> --author <role>
```

## Testing

```bash
# Run all tests
pytest

# Verbose with coverage
pytest -v --cov=tracker --cov-report=term-missing

# Run a single test file
pytest tests/test_tickets.py -v
```

`--author` is **required** for write commands (`create`, `update`, `link create`, `link remove`, `comment create`, `comment update`) and **optional** for read-only commands (`get`, `list`, `search`, `link list`, `comment list`, `comment get`, `workflow status`, `workflow transitions`, `build-queue`).

## Commands

### Tickets

- `create <type> <title>`
  - options: `--priority`, `--assignee`, `--parent|--child-of`, `--addressed-to`, `--description`, `--description-file`, `--field key=value`
  - **Output:** YAML block with status context (see [Create / status-update output](#create--status-update-output))
- `get <ticket-id>`
  - **Output:** YAML status-context block (same fields as `create`) followed by full ticket metadata and content body
- `list [--status ...] [--assignee ...] [--type ...] [--priority ...]`
- `update <ticket-id> [--status ...] [--assignee ...] [--priority ...]`
  - status changes are validated against `allowed_transitions` in `.workflow.yaml`
  - **When `--status` is supplied:** YAML status-context output (see below). Other field-only updates print a plain summary line.
- `search <query> [--in-title] [--in-content]`

### Create / status-update output

Both `create` and `update --status` return a YAML block on success:

```yaml
ticket_id: TASK-001
current_status: New
status_description: Ticket created and awaiting triage.
status_goal: Prepare the ticket for execution.
status_responsible_roles:
- Requester
allowed_transitions:
- Open
- Canceled
definitions_of_done:
- target_statuses:
  - Open
  dod_criteria:
  - Acceptance criteria defined
instructions:
- Set assignee to ticket creator.
- Move to Open when DoD is met.
```

| Field | Description |
|---|---|
| `ticket_id` | ID of the created / updated ticket |
| `current_status` | Status after the operation |
| `status_description` | Human-readable description of the status from the type YAML |
| `status_goal` | Stage goal of the status from `stage_goal` in the type YAML |
| `status_responsible_roles` | List of roles responsible for handling this status |
| `allowed_transitions` | List of reachable statuses from `allowed_transitions` in the type YAML |
| `instructions` | Step-by-step instructions for the current status from `ticket_instructions[status].instructions` |
| `definitions_of_done` | DoD list from `ticket_instructions[status].transition_dods` |

### Links

- `link create <source-id> <target-id> <link-type> [--comment ...]`
- `link list <ticket-id> [--direction in|out|all]`
- `link remove <link-id>`

### Comments

- `comment create <ticket-id> --subject <text> [--text <body>]`
- `comment list <ticket-id>`
- `comment get <ticket-id> <comment-id>`
- `comment update <ticket-id> <comment-id> [--subject ...] [--text ...]`

Comment files use this fixed header format:

1. `Subject: ...`
2. `Created: ...`
3. `Updated: ...`
4. `---`

### Workflow

Inspect status definitions and allowed transitions sourced from `.workflow.yaml`.

- `workflow status <type>` — list all statuses for a ticket type with stage goals and terminal markers
- `workflow status <type> <status-name>` — show full detail for one status: description, stage goal, responsible roles (array), and allowed transitions
- `workflow transitions <type> <status-name>` — list allowed target statuses from the given status, with terminal markers

### Build Queue

Generate a prioritized build queue of non-terminal tickets with blocking relationships and priority reconciliation.

- `build-queue stage1` — filter to non-terminal tickets only
- `build-queue stage2` — perform recursive priority reconciliation (ensures child priority >= parent, blocker priority >= blocked)
- `build-queue stage3` — sort tickets by priority and blocking relationships
- `build-queue stage4` — format and display the queue with position, blocking info, and ticket details
- `build-queue all` — run all stages (filter, reconcile, sort, output)

All subcommands accept optional `--author` for attribution of priority changes made during stage2.

## Exit Codes

- `0` success
- `2` validation error
- `3` configuration error
- `4` file operation error
- `5` unexpected error

## Notes

- Types, link types, statuses, and fields are validated against `.ept/tracker/.workflow.yaml`.
- Status changes in `update` are validated against `allowed_transitions`; invalid transitions are rejected with a clear error.
- Each status entry in `.workflow.yaml` carries `description`, `stage_goal`, and `responsible_roles` (YAML array).
- Per-type YAML files may include a `ticket_instructions` map keyed by status name. Each status entry supports two sub-keys used in the YAML output: `instructions` (list of strings) and `transition_dods` (list of DoD objects).
- Ticket updates synchronize `.index.csv` and ticket frontmatter metadata.
- Filtering in `list` is single-pass.

## Configuration File Structure

The workflow configuration is split across multiple files for maintainability:

```
.ept/tracker/.config/
├── .workflow.yaml          # Top-level config: fields, link_types, type_registry
│                           # ticket_types section holds $ref entries (see below)
├── .id-counters.yaml       # Auto-incremented ID counters per type
├── .index.csv              # Fast-lookup index of all tickets
├── .link-index.csv         # Index of all inter-ticket links
└── tickets/                # One YAML file per ticket type
    ├── task.yaml
    ├── feature.yaml
    ├── epic.yaml
    ├── dev_story.yaml
    ├── bug.yaml
    ├── resource_req.yaml
    ├── workitem.yaml
    ├── ba_subtask_analysis.yaml
    ├── ba_subtask_design.yaml
    ├── sa_subtask_analysis.yaml
    ├── sa_subtask_design.yaml
    ├── ux_subtask_analysis.yaml
    ├── ux_subtask_design.yaml
    ├── design.yaml
    ├── development.yaml
    ├── unittest.yaml
    ├── codereview.yaml
    ├── testcase.yaml
    ├── testexec.yaml
    ├── devops.yaml
    ├── bug_subtask.yaml
    └── question.yaml
```

### $ref References

The `ticket_types` list in `.workflow.yaml` uses `$ref` entries to point at the individual files:

```yaml
ticket_types:
  - $ref: tickets/task.yaml
  - $ref: tickets/feature.yaml
  # ...
```

Each file under `tickets/` is a plain YAML mapping containing a single ticket type definition:

```yaml
type: task
id_prefix: TASK
description: >
  General-purpose catch-all ticket ...
required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]
optional_fields: [parent, component, labels, due_date]
initial_status: New
terminal_statuses: [Closed, Canceled, Rejected, Duplicated]
statuses:
  New:
    description: "..."
    stage_goal: "..."
    responsible_roles:
      - Requester
allowed_transitions:
  New: [Open, Canceled, Rejected, Duplicated]
  # ...
automatic_transitions: []
ticket_instructions:
  New:
    instructions:
      - Set assignee to ticket creator.
      - Move to Open when DoD is met.
    transition_dods:
      - target_statuses: [Open]
        dod_criteria:
          - Acceptance criteria defined
          - Assignee set
  Open:
    instructions:
      - Execute the work.
    transition_dods: []
```

The `ticket_instructions` map is optional. Missing entries produce empty `instructions` and `definitions_of_done` lists in the YAML output.

**Backward compatibility:** Inline ticket-type entries (without `$ref`) continue to work. Test scaffolds that write `.workflow.yaml` directly do not need to use `$ref`.

**Adding a new ticket type:**
1. Create `tickets/<new_type>.yaml` with the full type definition.
2. Add `- $ref: tickets/<new_type>.yaml` to the `ticket_types` list in `.workflow.yaml`.
3. Add the corresponding entry to the `type_registry` section of `.workflow.yaml`.
4. Add the type key to the `fields.type.values` list in `.workflow.yaml`.


# CLI Gap Requirements — Ad-hoc Modification 01

## Context

This document defines requirements for functionality that the workflow skill (`SKILL.md`) mandates
but is not currently covered by the `tracker_cli.py` command set. Each gap is traceable to a
specific workflow rule or phase requirement. Implementation must follow the existing patterns in
`tracker/tickets.py`, `tracker/links.py`, and `tracker/cli.py`.

---

## GAP-01 — `update` command: arbitrary field update via `--field`

### Problem

`update_ticket()` in `tickets.py` accepts only `status`, `assignee`, and `priority`.
The `update` CLI sub-command exposes the same three options only.
There is no way to set or modify other ticket fields (e.g. `release_notes`, `addressed_to`,
`description`, or any type-specific optional field) after a ticket has been created.

Workflow Rule 6 states: *"Dev Story must have `release_notes` before Grooming."*
Because `create` writes `release_notes` only when it is passed via `--field`, and
`update` cannot modify it afterward, an agent that creates the ticket first and
adds release notes in a follow-up step is blocked.

### Requirements

1. **`update_ticket()` function** (`tracker/tickets.py`): accept an optional
   `extra_fields: dict[str, str] | None` parameter.
   - Validate each key against `cfg["valid_field_names"]` and the ticket type's
     `optional_fields` list, using the same rules already applied in `create_ticket()`.
   - Write changed fields to both the index (for columns that exist in `INDEX_FIELDNAMES`)
     and the ticket frontmatter file, using the existing `write_ticket_file()` helper.
   - Include updated fields in the auto-generated "Ticket updated" comment body.

2. **`update` CLI sub-command** (`tracker/cli.py`): add `--field key=value` (repeatable,
   identical signature to the existing `--field` on `create`) and pass the parsed result
   to `update_ticket()` as `extra_fields`.

3. **Help data** (`_build_help_data()`): add `--field` entry under the `update` command
   block, marked `repeatable: True`.

4. **Validation error message**: when an unknown or disallowed field is supplied, the error
   must name the offending field(s) and list allowed fields for the ticket type — matching
   the style used by `create_ticket()`.

5. **Tests**: add cases in `tests/test_tickets.py` and `tests/test_cli.py` that verify:
   - A known optional field (e.g. `release_notes`) can be updated after creation.
   - The change is persisted in the frontmatter file and reflected by `get`.
   - An unknown field name raises `ValidationError`.
   - A field not in the ticket type's `optional_fields` raises `ValidationError`.

---

## GAP-02 — `list` command: filter by parent ticket (`--parent`)

### Problem (GAP-02)

`list_tickets()` in `tickets.py` filters by `status`, `assignee`, `type`, and `priority`
only, even though the index CSV already stores a `parent` column (set at creation time via
`create_ticket`).

To find all sub-tasks of a DEV-STORY (e.g. to check whether all DESIGN sub-tasks are closed
before starting Phase 3), an agent must call `link list` and then `get` each linked ticket —
an indirect multi-step chain that is slow and error-prone.

### Requirements (GAP-02)

1. **`list_tickets()` function** (`tracker/tickets.py`): add an optional
   `parent: str | None = None` parameter.
   - When supplied, include only tickets whose `parent` column equals the given ID.
   - Apply the filter in the same single-pass loop alongside the existing filters.

2. **`list` CLI sub-command** (`tracker/cli.py`): add `--parent TICKET_ID` option and
   pass it to `list_tickets()`.

3. **Validation**: if `--parent` is provided, verify the referenced ticket exists using
   `ticket_exists()` and raise `ValidationError` with a clear message if it does not.

4. **Help data** (`_build_help_data()`): add `--parent` entry under the `list` command block.

5. **Tests**: add cases in `tests/test_tickets.py` and `tests/test_cli.py` that verify:
   - Filtering by parent returns only direct children of that ticket.
   - A non-existent parent ID results in a validation error.
   - Combining `--parent` with `--status` or `--type` filters correctly.

---

## GAP-03 — `update` command: `--field` for ticket body/description update

### Problem (GAP-03)

Ticket body text (the Markdown content below the frontmatter separator) cannot be modified
after creation. There is no CLI option to update the description or any other free-text body
section of an existing ticket.

This blocks agents that need to append progress notes, refined acceptance criteria, or design
decisions to an existing ticket without creating a comment.

### Requirements (GAP-03)

1. **`update_ticket()` function** (`tracker/tickets.py`): add an optional
   `description: str | None = None` parameter.
   - When supplied, replace the body section of the ticket file (the text after the closing
     `---` of the frontmatter) with the new value.
   - Use the existing `write_ticket_file()` helper to persist the change.
   - Decode escape sequences using `decode_escape_sequences()` (same as `create`).

2. **`update` CLI sub-command** (`tracker/cli.py`): add `--description TEXT` and
   `--description-file FILE` options, mirroring the same options on `create`.
   - `--description-file` must validate file existence before reading, with the same error
     message pattern used in the `create` handler.

3. **Help data** (`_build_help_data()`): add `--description` and `--description-file`
   entries under the `update` command block.

4. **Tests**: add cases that verify:
   - Description text is replaced and readable via `get`.
   - `--description-file` reads content from a file.
   - Neither `--description` nor `--description-file` being supplied leaves body unchanged.

---

## GAP-04 — `list` command: filter by `--reporter`

### Problem (GAP-04)

The index CSV stores a `reporter` column (the `--author` value at creation time).
There is no CLI filter for it. Agents that need to list all tickets opened by a specific
role (e.g. all tickets reported by `business-analyst`) must fetch the full list and
filter manually in post-processing.

### Requirements (GAP-04)

1. **`list_tickets()` function** (`tracker/tickets.py`): add an optional
   `reporter: str | None = None` parameter and apply it in the single-pass filter loop.

2. **`list` CLI sub-command** (`tracker/cli.py`): add `--reporter IDENTIFIER` option.

3. **Help data** (`_build_help_data()`): add `--reporter` entry under the `list` command block.

4. **Tests**: add cases that verify filtering by reporter returns correct results.

---

## Implementation Notes

- All new parameters must be keyword-only and default to `None` / the appropriate no-op
  value so existing callers are unaffected.
- All new CLI options must be wired into `_build_help_data()` so that `--help-toon` output
  stays accurate.
- Follow the existing comment-on-change pattern: every write operation in `update_ticket()`
  must produce an auto-generated comment via `create_comment()` that lists which fields
  were modified.
- No new modules are required; all changes are confined to `tracker/tickets.py` and
  `tracker/cli.py` (plus corresponding test files).
- **Unit test coverage**: the combined line coverage of `tracker/tickets.py` and
  `tracker/cli.py` must not drop below **80 %** after the changes are merged. Coverage is
  measured with `pytest --cov=tracker --cov-report=term-missing` and enforced via
  `--cov-fail-under=80`. New test cases added for each GAP must cover both the happy path
  and the primary error path (invalid input) for every new parameter or option.

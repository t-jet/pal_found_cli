# Design Requirements: Automatic Transition Rules for the Tracker CLI

## 1. Overview

This document specifies the implementation requirements to add machine-processable automatic transition rules to the tracker CLI utility, as defined in `adhoc_modification_02.md`. The feature replaces free-text `automatic_transitions` in ticket-type YAML files with a structured, evaluable rule vocabulary. The implementation must maintain backward compatibility with the existing test suite and all existing CLI commands.

---

## 2. Scope

### In scope
- Parsing `automatic_transitions` rules from ticket-type YAML files into the runtime configuration.
- A rule-evaluation engine that executes the six rule types defined in `adhoc_modification_02.md`.
- Triggering rule evaluation after `create_ticket` and `update_ticket` operations.
- Persisting `prior_status` in ticket frontmatter to support `Blocked` → restore transitions.
- Unit test coverage of **≥ 80%** for all new and modified modules.

### Out of scope
- Modifying the ticket-type YAML files themselves (that is a separate migration task).
- Adding new CLI commands or changing existing CLI argument signatures.
- Background/scheduled execution of rules (evaluation is synchronous, triggered by write operations).

---

## 3. Configuration Layer (`tracker/config.py`)

### REQ-CFG-01 — Parse `automatic_transitions` from ticket-type entries
`get_runtime_config()` must read the `automatic_transitions` list from each ticket-type entry (loaded via `$ref` or inline) and store it verbatim under `ticket_specs[<type>]["automatic_transitions"]`. If the field is absent or `null` the stored value must be an empty list `[]`.

### REQ-CFG-02 — No schema enforcement at load time
The config layer must not validate rule structure during loading. Structural validation is the responsibility of the rule-evaluation engine. Unknown keys in a rule dict must be silently ignored so that future rule types do not break existing deployments.

### REQ-CFG-03 — Backward compatibility
Existing ticket-type definitions that declare `automatic_transitions: []` or omit the field entirely must continue to load without error or warning.

---

## 4. New Module: `tracker/automations.py`

Create a new module `tracker/automations.py` that contains the complete rule-evaluation engine. No automatic-transition logic may be placed in `tickets.py`, `links.py`, or `cli.py`.

### 4.1 Rule Dispatcher

#### REQ-AUTO-01 — `evaluate_automatic_transitions(ticket_id, event)`
Public entry point. Signature:
```python
def evaluate_automatic_transitions(ticket_id: str, event: str) -> list[str]:
    ...
```
- `event` is one of `"ticket_created"` or `"ticket_updated"`.
- Reads the ticket's current state from the index and its `automatic_transitions` rules from the runtime config.
- Iterates over all rules for the ticket type and evaluates each in declaration order.
- For each rule whose pre-conditions are satisfied, calls `update_ticket` to perform the transition with `author="system"`.
- After each system-performed transition, recursively calls `evaluate_automatic_transitions` on the same ticket to allow chained transitions (max recursion depth: **5** to prevent infinite loops).
- Returns a list of transition descriptions performed (e.g., `["TASK-001: Open → In Progress"]`).
- Must **not** raise; exceptions from individual rule evaluators are caught, logged to stderr, and the remaining rules continue.

#### REQ-AUTO-02 — Rule type dispatch table
The dispatcher must look up each rule's `rule` key and route it to the corresponding evaluator function. Unrecognised rule keys must be silently skipped (no error).

### 4.2 Rule Evaluators

Each evaluator function has the signature:
```python
def _eval_<rulename>(ticket: dict, rule: dict, links: list[dict]) -> bool:
    ...
```
Returns `True` if the transition should fire; `False` otherwise. The dispatcher reads `source_status` from the rule (if present) and short-circuits to `False` before calling the evaluator when the ticket's current status does not match.

#### REQ-AUTO-03 — `AT-1: all_children_reach_status`
- Collect all child tickets: tickets whose `parent` field in the index equals `ticket_id`, **and** tickets linked via `link_types` entries in `child_filter` (if specified).
- Optionally filter by `child_filter.types`.
- Return `True` when **every** child in the filtered set has a status in `child_statuses`.
- Return `False` if no children match the filter (empty set does not satisfy "all").

#### REQ-AUTO-04 — `AT-2: first_child_reaches_status`
- Collect children the same way as AT-1.
- Return `True` when **any** child in the filtered set has a status in `child_statuses`.
- Return `False` if no children match the filter.

#### REQ-AUTO-05 — `AT-3: linked_ticket_reaches_status`
- Find links where `link_type` matches and this ticket plays the role specified by `link_role` (`"source"` → ticket is `source_ticket`; `"target"` → ticket is `target_ticket`).
- Optionally filter by `linked_ticket_types`.
- Return `True` when **any** such linked ticket has a status in `linked_statuses`.

#### REQ-AUTO-06 — `AT-4: child_blocker_created`
- Triggered only for `event == "ticket_created"` on the **child** ticket; the affected ticket is the parent.
- The evaluator is invoked on the **parent** ticket when a new child ticket (matching `child_filter.types`) with a link of type `child_filter.link_type` targeting the parent is created.
- When the pre-condition is met, save the parent's current status as `prior_status` in the parent ticket's frontmatter before transitioning to `target_status`.
- Implementation note: `evaluate_automatic_transitions` must also be called on the **parent** of every newly created ticket (if a parent exists) with `event="child_created"` so AT-4 can fire correctly.

#### REQ-AUTO-07 — `AT-5: all_blockers_cleared`
- Find all tickets linked to this ticket where the link indicates this ticket is blocked (i.e., this ticket is the `target_ticket` in a `Blocks` link, or any equivalent role from the link configuration).
- Return `True` when **all** such blocking tickets have a status in `blocker_terminal_statuses`.
- When `target_status == "prior_status"`, read the `prior_status` field from the ticket's frontmatter and use that as the actual target. If `prior_status` is absent or empty, skip the rule silently.

#### REQ-AUTO-08 — `AT-6: this_ticket_reaches_status`
- The trigger is that **this** ticket has just reached one of `source_statuses`.
- Find linked tickets matching `link_type`, `link_role`, and optionally `linked_ticket_types`.
- For each matching linked ticket whose current status equals `linked_ticket_source_status`, call `update_ticket` with `status = linked_ticket_target_status` (substituting `prior_status` from frontmatter if the value is the keyword `"prior_status"`).
- The evaluator must return `True` only if at least one linked ticket was actually updated.

### 4.3 `prior_status` Persistence

#### REQ-AUTO-09 — `prior_status` storage
`prior_status` is stored as an optional field in the ticket's YAML frontmatter (not in the CSV index). Its key is `prior_status`. The field is written when AT-4 fires and cleared (set to empty string) when AT-5 or AT-6 restores the prior status.

#### REQ-AUTO-10 — `prior_status` in field allowlist
`prior_status` must be added to the `valid_field_names` set in `config.py` (or declared as an optional field in every ticket type that has a `Blocked` status) so that `update_ticket` does not reject it as an unknown field.

---

## 5. Integration in `tracker/tickets.py`

### REQ-INT-01 — Post-create trigger
At the end of `create_ticket`, after writing the ticket file and updating the index:
1. Call `evaluate_automatic_transitions(ticket_id, "ticket_created")` on the new ticket.
2. If the new ticket has a parent, call `evaluate_automatic_transitions(parent_id, "child_created")` on the parent.

### REQ-INT-02 — Post-update trigger
At the end of `update_ticket`, after writing the ticket file and updating the index (only when `updated == True` and a status change occurred):
1. Call `evaluate_automatic_transitions(ticket_id, "ticket_updated")` on the updated ticket.
2. Read the updated ticket's parent from the index. If a parent exists, call `evaluate_automatic_transitions(parent_id, "child_status_changed")` on it.

### REQ-INT-03 — Prevent infinite loops via the update path
The `automations` module must pass `_system=True` (or an equivalent private flag) when calling `update_ticket` to suppress re-evaluation from within a system-triggered update. The `update_ticket` function must accept this flag and skip the post-update trigger when it is set.

### REQ-INT-04 — No breaking change to `update_ticket` signature
The `_system` flag must be keyword-only and default to `False`. All existing callers (tests, CLI) that omit the flag must continue to function without modification.

---

## 6. Validators (`tracker/validators.py`)

### REQ-VAL-01 — No new public validators required
Automatic transitions bypass user-facing validation (they are system-generated). The dispatcher may call `validate_status_transition` internally only as a safeguard; on failure it must log a warning and skip the transition rather than raise.

---

## 7. Unit Tests

### REQ-TEST-01 — Coverage threshold
All new and modified modules must achieve **≥ 80% line coverage** as measured by `pytest --cov`. The threshold applies to the following modules individually:
- `tracker/automations.py` (new)
- `tracker/config.py` (modified)
- `tracker/tickets.py` (modified)

### REQ-TEST-02 — New test file: `tests/test_automations.py`
Create `tests/test_automations.py` covering at minimum:

| Test class | Scenarios |
|---|---|
| `TestAllChildrenReachStatus` | All children terminal → fires; one child non-terminal → does not fire; no children → does not fire; type filter respected |
| `TestFirstChildReachesStatus` | One child in target status → fires; no children in target status → does not fire |
| `TestLinkedTicketReachesStatus` | Matching linked ticket in status → fires; link_role filter respected; no matching → does not fire |
| `TestChildBlockerCreated` | New question child with Blocks link → parent transitions to Blocked and prior_status saved; non-question child → does not fire |
| `TestAllBlockersCleared` | All blockers terminal → restores prior_status; one blocker active → does not fire; missing prior_status → rule skipped |
| `TestThisTicketReachesStatus` | Reaches source_status with matching linked ticket → linked ticket updated; linked ticket in wrong status → no update |
| `TestEvaluateAutomaticTransitions` | Chained transitions (AT-1 then AT-2 in sequence); max recursion depth respected; exception in evaluator does not prevent subsequent rules; empty rules list → no-op |

### REQ-TEST-03 — Extended `conftest.py` fixture
Add a `auto_tracker_env` fixture to `tests/conftest.py` that provides a tracker environment with:
- Ticket types that include `automatic_transitions` rules covering AT-1 through AT-6.
- Pre-populated tickets in various statuses for use in automations tests.
- The fixture must be isolated (tmp_path-based) and must not affect other fixtures.

### REQ-TEST-04 — Regression coverage for existing tests
All pre-existing tests (`test_tickets.py`, `test_validators.py`, `test_links.py`, etc.) must continue to pass without modification. The integration hooks (REQ-INT-01/02) must be transparent when no `automatic_transitions` rules are configured (empty list).

### REQ-TEST-05 — `prior_status` persistence tests
In `tests/test_tickets.py` (or `test_automations.py`), add tests verifying:
- After AT-4 fires, the parent ticket's frontmatter contains a non-empty `prior_status` key.
- After AT-5 fires, the parent ticket's status matches the saved `prior_status` and the field is cleared.

---

## 8. Module Dependency Rules

The new `automations.py` module may import from:
- `tracker.config` (`get_runtime_config`, `get_paths`)
- `tracker.index` (`get_ticket`, `read_index`, `read_link_index`, `ticket_exists`)
- `tracker.tickets` (`update_ticket`, `parse_ticket_file`, `write_ticket_file`)
- `tracker.exceptions` (`ValidationError`, `TrackerError`)
- Python standard library

`automations.py` must **not** be imported by `config.py`, `index.py`, `validators.py`, `links.py`, `comments.py`, or `formatters.py` (to keep the dependency graph acyclic). `tickets.py` imports `automations.py` only for the post-write trigger calls.

---

## 9. Error Handling

### REQ-ERR-01 — Rule evaluation failures must not propagate to callers
Any `TrackerError` or unexpected exception raised inside `evaluate_automatic_transitions` or any evaluator must be caught at the `evaluate_automatic_transitions` level, printed to stderr with the prefix `[automations warning]`, and suppressed so the originating `create_ticket` or `update_ticket` call completes normally.

### REQ-ERR-02 — Maximum recursion depth
When the recursion depth reaches 5 without stabilising, log a warning to stderr and return the transitions collected so far without further recursion.

---

## 10. Ticket-Type YAML Migration

This section specifies the exact changes to apply to every file in `.ept/tracker/.config/tickets/`. Each file must be updated in the order stated in the migration plan (Section 7 of `adhoc_modification_02.md`) so that rules referencing other ticket types can be validated against already-migrated definitions.

All changes are **limited to the `automatic_transitions` key** in each YAML file. No other keys (`statuses`, `allowed_transitions`, `ticket_instructions`, `transition_dods`, etc.) may be modified as part of this migration.

---

### 10.1 `question.yaml`

**Current value:** free-text trigger/action pairs (3 entries).

**Replace with:**

```yaml
automatic_transitions:
  # AT-4: block parent when this Question is created with a Blocks link
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore parent's prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status

  # AT-6: when this Question resolves/cancels/closes, unblock the parent
  - rule: this_ticket_reaches_status
    source_statuses: [Resolved, Canceled, Closed]
    link_type: Blocks
    link_role: source
    linked_ticket_types: []
    linked_ticket_source_status: Blocked
    linked_ticket_target_status: prior_status
```

---

### 10.2 `codereview.yaml`

**Current value:** free-text trigger/action pair (1 entry).

**Replace with:**

```yaml
automatic_transitions:
  # AT-3: activate this CodeReview when its linked Development sub-task resolves
  - rule: linked_ticket_reaches_status
    link_type: RelatesTo
    link_role: source
    linked_ticket_types: [development]
    linked_statuses: [Resolved]
    source_status: New
    target_status: Open

  # AT-4: block when a Question sub-task with a Blocks link is created
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status
```

---

### 10.3 `epic.yaml`

**Current value:** free-text trigger/action pairs (3 entries).

**Replace with:**

```yaml
automatic_transitions:
  # AT-2: first Developer Story enters active work → Epic moves to In Progress
  - rule: first_child_reaches_status
    child_filter:
      types: [dev_story]
    child_statuses: [Development, QA, Deployment, Resolved]
    source_status: Open
    target_status: In Progress

  # AT-1: all Developer Stories terminal (incl. Resolved) → Epic Resolved
  - rule: all_children_reach_status
    child_filter:
      types: [dev_story]
    child_statuses: [Resolved, Closed, Canceled, Rejected, Duplicated]
    source_status: In Progress
    target_status: Resolved

  # AT-1: all Developer Stories fully closed → Epic Done
  - rule: all_children_reach_status
    child_filter:
      types: [dev_story]
    child_statuses: [Closed, Canceled, Rejected, Duplicated]
    source_status: Resolved
    target_status: Done

  # AT-4: block when a Question sub-task with a Blocks link is created
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status
```

---

### 10.4 `feature.yaml`

**Current value:** `automatic_transitions: []`

**Replace with:**

```yaml
automatic_transitions:
  # AT-1: all Developer Stories closed → Feature advances to Resolved
  - rule: all_children_reach_status
    child_filter:
      types: [dev_story]
    child_statuses: [Closed, Canceled, Rejected, Duplicated]
    source_status: Waiting for Implementation
    target_status: Resolved

  # AT-4: block when a Question sub-task with a Blocks link is created
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status
```

---

### 10.5 `dev_story.yaml`

**Current value:** `automatic_transitions: []`

**Replace with:**

```yaml
automatic_transitions:
  # AT-1: all Development/Unittest/CodeReview sub-tasks closed → move to QA
  - rule: all_children_reach_status
    child_filter:
      types: [development, unittest, codereview]
    child_statuses: [Closed, Canceled, Rejected, Duplicated]
    source_status: Development
    target_status: QA

  # AT-1: all TestCase/TestExec/BugSubtask sub-tasks closed → move to Deployment
  - rule: all_children_reach_status
    child_filter:
      types: [testcase, testexec, bug_subtask]
    child_statuses: [Closed, Canceled, Rejected, Duplicated]
    source_status: QA
    target_status: Deployment

  # AT-1: DevOps sub-task closed → move to Resolved
  - rule: all_children_reach_status
    child_filter:
      types: [devops]
    child_statuses: [Closed, Canceled, Rejected, Duplicated]
    source_status: Deployment
    target_status: Resolved

  # AT-4: block when a Question sub-task with a Blocks link is created
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status
```

---

### 10.6 Files receiving AT-4 + AT-5 only (boilerplate block)

The following 16 files currently declare `automatic_transitions: []` and have a `Blocked` status. Each must have its `automatic_transitions: []` replaced with the two-rule boilerplate below. No other changes are made.

**Affected files:**

| File | Notes |
|---|---|
| `development.yaml` | CodeReview activation is owned by `codereview.yaml` AT-3 |
| `devops.yaml` | No type-specific auto-transitions |
| `design.yaml` | No type-specific auto-transitions |
| `unittest.yaml` | No type-specific auto-transitions |
| `testcase.yaml` | No type-specific auto-transitions |
| `testexec.yaml` | No type-specific auto-transitions |
| `bug_subtask.yaml` | No type-specific auto-transitions |
| `workitem.yaml` | No type-specific auto-transitions |
| `task.yaml` | No type-specific auto-transitions |
| `resource_req.yaml` | No type-specific auto-transitions |
| `ba_subtask_analysis.yaml` | No type-specific auto-transitions |
| `ba_subtask_design.yaml` | No type-specific auto-transitions |
| `sa_subtask_analysis.yaml` | No type-specific auto-transitions |
| `sa_subtask_design.yaml` | No type-specific auto-transitions |
| `ux_subtask_analysis.yaml` | No type-specific auto-transitions |
| `ux_subtask_design.yaml` | No type-specific auto-transitions |

**Replacement block (identical for all 16 files):**

```yaml
automatic_transitions:
  # AT-4: block when a Question sub-task with a Blocks link is created
  - rule: child_blocker_created
    child_filter:
      types: [question]
      link_type: Blocks
    save_prior_status: true
    target_status: Blocked

  # AT-5: restore prior status when all blockers are cleared
  - rule: all_blockers_cleared
    blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
    source_status: Blocked
    target_status: prior_status
```

---

### 10.7 `bug.yaml` — no change

`bug.yaml` does not expose a `Blocked` status in its `allowed_transitions` or `statuses` map. Its current `automatic_transitions: []` must remain unchanged.

---

### 10.8 `allowed_transitions` validation requirement

After all YAML files are updated, verify that every `target_status` referenced by any rule is reachable from the stated `source_status` according to that file's `allowed_transitions` map. Specifically:

| File | Rule | source_status | target_status | Must exist in `allowed_transitions[source_status]` |
|---|---|---|---|---|
| `question.yaml` | AT-6 | Blocked (linked parent) | prior_status (runtime) | Prior status must be a valid allowed target from Blocked in the parent's type |
| `codereview.yaml` | AT-3 | New | Open | `allowed_transitions.New` must include `Open` |
| `epic.yaml` | AT-2 | Open | In Progress | `allowed_transitions.Open` must include `In Progress` |
| `epic.yaml` | AT-1 | In Progress | Resolved | `allowed_transitions["In Progress"]` must include `Resolved` |
| `epic.yaml` | AT-1 | Resolved | Done | `allowed_transitions.Resolved` must include `Done` |
| `feature.yaml` | AT-1 | Waiting for Implementation | Resolved | `allowed_transitions["Waiting for Implementation"]` must include `Resolved` |
| `dev_story.yaml` | AT-1 | Development | QA | `allowed_transitions.Development` must include `QA` |
| `dev_story.yaml` | AT-1 | QA | Deployment | `allowed_transitions.QA` must include `Deployment` |
| `dev_story.yaml` | AT-1 | Deployment | Resolved | `allowed_transitions.Deployment` must include `Resolved` |
| All with Blocked | AT-5 | Blocked | prior_status | Prior status at runtime must be in `allowed_transitions.Blocked` |

Any missing transition must be added to `allowed_transitions` in the corresponding YAML file as part of this migration.

---

### 10.9 Migration unit-test requirement

Add a parametrised test `tests/test_yaml_migration.py` that:

1. Loads each of the 22 ticket-type YAML files directly.
2. Asserts that `automatic_transitions` is a list (not `null` and not a string).
3. For each rule in the list, asserts that the `rule` key is present and its value is one of the six known rule types.
4. For files listed in Section 10.6 plus `question.yaml`, asserts that an `all_blockers_cleared` (AT-5) rule exists.
5. For files listed in Section 10.6 plus `question.yaml`, `codereview.yaml`, `epic.yaml`, `feature.yaml`, `dev_story.yaml`, asserts that a `child_blocker_created` (AT-4) rule exists.
6. For `codereview.yaml`, asserts that a `linked_ticket_reaches_status` rule with `linked_ticket_types: [development]` exists.
7. For `epic.yaml`, asserts that exactly one `first_child_reaches_status` rule and exactly two `all_children_reach_status` rules exist.
8. For `dev_story.yaml`, asserts that exactly three `all_children_reach_status` rules exist with source statuses `Development`, `QA`, and `Deployment`.
9. For `bug.yaml`, asserts that `automatic_transitions` equals `[]`.

This test file operates purely on YAML parsing and must not initialise the tracker runtime config.

---

## 11. Acceptance Criteria

1. `pytest` passes on the full test suite with zero failures.
2. `pytest --cov=tracker --cov-report=term-missing` reports ≥ 80% line coverage for `automations.py`, `config.py`, and `tickets.py`.
3. Running `tracker update <id> --status Blocked --author test` on a ticket that has AT-5 rules and all blockers in terminal states triggers an automatic status restoration within the same CLI invocation.
4. Creating a `question` ticket as a child of a parent ticket (with a `Blocks` link) automatically transitions the parent to `Blocked` and saves `prior_status` in its frontmatter.
5. All existing `tracker` CLI commands produce identical output to the current baseline when no `automatic_transitions` rules are defined for the ticket types in use.

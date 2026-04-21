# Generic Automatic Transition Rules for the Ticketing System

## 1. Problem Statement

The `automatic_transitions` field exists in every ticket-type YAML file, but its usage is inconsistent:

- **18 of 22 files** declare `automatic_transitions: []` — the field is empty even though the `ticket_instructions` and `transition_dods` sections describe transitions that are clearly automatic (e.g., *"Move to Resolved when all Developer Stories are Closed"*, *"Parent ticket returns to its prior status"*).
- **3 files** contain free-text descriptions (codereview, epic, question) with no enforced structure, making machine-processing impossible.
- The same behavioral patterns recur across dozens of ticket types, duplicated each time as prose in `ticket_instructions`.

This document defines a **generic, machine-processable rule vocabulary** that replaces all current free-text automatic transition descriptions and provides a unified schema for expressing them.

---

## 2. Inventory of Current Automatic Transitions

### 2.1 Explicit (structured free-text, 3 files)

| File | Trigger text | Action text |
| --- | --- | --- |
| `codereview.yaml` | Linked Development sub-task transitions to Resolved | CodeReview: New → Open |
| `epic.yaml` | First linked Developer Story transitions to Development | Epic: Open → In Progress |
| `epic.yaml` | All linked Developer Stories are Resolved | Epic: In Progress → Resolved |
| `epic.yaml` | All linked Developer Stories are Closed | Epic: Resolved → Done |
| `question.yaml` | Question ticket created under a parent ticket | Parent ticket status → Blocked |
| `question.yaml` | Question ticket transitions to Resolved or Canceled | Parent ticket: Blocked → previous status (restored) |
| `question.yaml` | Question ticket transitions to Closed | Parent ticket: Blocked → previous status (restored) |

### 2.2 Implicit (described in instructions prose, 18 files)

The following transition behaviors are currently embedded as text instructions but are inherently automatic:

| Pattern | Where described | Affected files |
| --- | --- | --- |
| All blocking links cleared → restore to prior status | `Blocked` instructions (all files with Blocked status) | All 18 files with `Blocked` state |
| All child DEV Stories Closed → Feature: Waiting for Implementation → Resolved | `feature.yaml` Resolved instructions ("Automatically entered…") | `feature.yaml` |
| DEV sub-task Resolved → CODEREVIEW activates (New → Open) | `development.yaml` Resolved instructions | `development.yaml` |
| DESIGN sub-task Closed → DEV sub-tasks may start | `dev_story.yaml` Development instructions | `dev_story.yaml` |
| All DEV+UNITTEST+CODEREVIEW Closed → Story: Development → QA | `dev_story.yaml` Development instructions | `dev_story.yaml` |
| All TESTCASE+TESTEXEC+BUG-SUB Closed → Story: QA → Deployment | `dev_story.yaml` QA instructions | `dev_story.yaml` |
| DEVOPS Closed → Story: Deployment → Resolved | `dev_story.yaml` Deployment instructions | `dev_story.yaml` |

---

## 3. Generic Rule Types

Six generic rule types cover all observed patterns. Rules are composable and reusable across ticket types.

---

### Rule Type AT-1: `all_children_reach_status`

**Semantics:** When **all** child tickets matching given filters have reached one of the specified statuses, and this ticket is in the specified source status, transition to the target status.

**Proposed YAML schema:**

```yaml
- rule: all_children_reach_status
  child_filter:
    types: [<ticket_type>, ...]      # optional; omit to match any child type
    link_types: [Contains, ...]      # optional; match by link relationship
  child_statuses: [<status>, ...]    # statuses that count as "reached"
  source_status: <status>            # this ticket must be in this status
  target_status: <status>            # transition to this status
```

**Mapped instances:**

```yaml
# epic.yaml
- rule: all_children_reach_status
  child_filter:
    types: [dev_story]
  child_statuses: [Resolved, Closed, Canceled, Rejected, Duplicated]
  source_status: In Progress
  target_status: Resolved

- rule: all_children_reach_status
  child_filter:
    types: [dev_story]
  child_statuses: [Closed, Canceled, Rejected, Duplicated]
  source_status: Resolved
  target_status: Done

# feature.yaml
- rule: all_children_reach_status
  child_filter:
    types: [dev_story]
  child_statuses: [Closed, Canceled, Rejected, Duplicated]
  source_status: Waiting for Implementation
  target_status: Resolved

# dev_story.yaml — Development phase complete → QA
- rule: all_children_reach_status
  child_filter:
    types: [development, unittest, codereview]
  child_statuses: [Closed, Canceled, Rejected, Duplicated]
  source_status: Development
  target_status: QA

# dev_story.yaml — QA phase complete → Deployment
- rule: all_children_reach_status
  child_filter:
    types: [testcase, testexec, bug_subtask]
  child_statuses: [Closed, Canceled, Rejected, Duplicated]
  source_status: QA
  target_status: Deployment

# dev_story.yaml — Deployment phase complete → Resolved
- rule: all_children_reach_status
  child_filter:
    types: [devops]
  child_statuses: [Closed, Canceled, Rejected, Duplicated]
  source_status: Deployment
  target_status: Resolved
```

---

### Rule Type AT-2: `first_child_reaches_status`

**Semantics:** When the **first** child ticket matching given filters reaches one of the specified statuses, and this ticket is in the specified source status, transition to the target status.

**Proposed YAML schema:**

```yaml
- rule: first_child_reaches_status
  child_filter:
    types: [<ticket_type>, ...]
    link_types: [<link_type>, ...]   # optional
  child_statuses: [<status>, ...]
  source_status: <status>
  target_status: <status>
```

**Mapped instances:**

```yaml
# epic.yaml
- rule: first_child_reaches_status
  child_filter:
    types: [dev_story]
  child_statuses: [Development, QA, Deployment, Resolved]
  source_status: Open
  target_status: In Progress
```

---

### Rule Type AT-3: `linked_ticket_reaches_status`

**Semantics:** When a ticket linked to this ticket by a specific link type reaches one of the specified statuses, and this ticket is in the specified source status, transition to the target status.

**Proposed YAML schema:**

```yaml
- rule: linked_ticket_reaches_status
  link_type: <link_type>             # e.g. RelatesTo, Blocks, Contains
  link_role: <source|target>         # role this ticket plays in the link
  linked_ticket_types: [<type>, ...] # optional filter on the other ticket type
  linked_statuses: [<status>, ...]   # statuses of the linked ticket that fire the trigger
  source_status: <status>
  target_status: <status>
```

**Mapped instances:**

```yaml
# codereview.yaml
- rule: linked_ticket_reaches_status
  link_type: RelatesTo
  link_role: source
  linked_ticket_types: [development]
  linked_statuses: [Resolved]
  source_status: New
  target_status: Open

# development.yaml — implicitly triggers CodeReview activation (mirror of the above)
# (No rule needed on development.yaml itself; the rule lives on codereview.yaml)
```

---

### Rule Type AT-4: `child_blocker_created`

**Semantics:** When a child ticket that bears a `Blocks` link targeting this ticket is created (or becomes active), save the current status as `prior_status` and transition to `Blocked`.

This rule captures the automatic blocking of a parent when a QUESTION sub-task is created under it.

**Proposed YAML schema:**

```yaml
- rule: child_blocker_created
  child_filter:
    types: [<ticket_type>, ...]      # optional; typically [question]
    link_type: Blocks                # link from child to this ticket
  save_prior_status: true            # saves current status for restoration
  target_status: Blocked
```

**Mapped instances:**

```yaml
# Every ticket type that has a Blocked status — declared individually in each file.
- rule: child_blocker_created
  child_filter:
    types: [question]
    link_type: Blocks
  save_prior_status: true
  target_status: Blocked
```

---

### Rule Type AT-5: `all_blockers_cleared`

**Semantics:** When all active `is-blocked-by` links on this ticket are resolved (every blocking ticket is in a terminal status), transition from `Blocked` to `prior_status` (the status saved when the block was entered).

**Proposed YAML schema:**

```yaml
- rule: all_blockers_cleared
  blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
  source_status: Blocked
  target_status: prior_status        # special keyword: restore the saved status
```

**Mapped instances:**

```yaml
# Every ticket type that has a Blocked status — declared individually in each file.
- rule: all_blockers_cleared
  blocker_terminal_statuses: [Closed, Done, Canceled, Rejected, Duplicated]
  source_status: Blocked
  target_status: prior_status
```

---

### Rule Type AT-6: `this_ticket_reaches_status`  *(outbound side-effect)*

**Semantics:** When **this** ticket transitions to one of the specified statuses, trigger a status transition on a linked ticket. This is the mirror/outbound complement of AT-3 and handles cases where the action belongs to the source ticket, not the target.

**Proposed YAML schema:**

```yaml
- rule: this_ticket_reaches_status
  source_statuses: [<status>, ...]   # statuses this ticket reaches that fire the rule
  link_type: <link_type>
  link_role: <source|target>
  linked_ticket_types: [<type>, ...]
  linked_ticket_source_status: <status>   # linked ticket must be in this status
  linked_ticket_target_status: <status>  # linked ticket transitions to this status
```

**Mapped instances:**

```yaml
# question.yaml — when question resolves/cancels, unblock parent
- rule: this_ticket_reaches_status
  source_statuses: [Resolved, Canceled, Closed]
  link_type: Blocks
  link_role: source                   # this question blocks the parent
  linked_ticket_types: []             # any parent type
  linked_ticket_source_status: Blocked
  linked_ticket_target_status: prior_status
```

---

## 4. Rule Placement Convention

Rules AT-4 and AT-5 apply identically to every ticket type that has a `Blocked` status. Each ticket type file declares its own copy of these rules. This keeps every file self-contained and avoids implicit cross-file dependencies.

The two rules are boilerplate and can be copy-pasted verbatim into any ticket type that exposes a `Blocked` status:

```yaml
automatic_transitions:
  # AT-4: block this ticket when a Question sub-task with a Blocks link is created
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

## 5. Refactored `automatic_transitions` per Ticket Type

After applying the generic rules:

| Ticket type | Rule types used | Notes |
| --- | --- | --- |
| `question` | AT-4, AT-5, AT-6 | AT-6 restores parent on resolution |
| `codereview` | AT-3, AT-4, AT-5 | AT-3: DEV Resolved → CODEREVIEW Open |
| `epic` | AT-1 (×2), AT-2, AT-4, AT-5 | Phase progression via child aggregation |
| `feature` | AT-1, AT-4, AT-5 | All DEV Stories Closed → Resolved |
| `dev_story` | AT-1 (×3), AT-4, AT-5 | One AT-1 rule per Development/QA/Deployment phase |
| `development` | AT-4, AT-5 | CodeReview activation is owned by codereview's AT-3 rule |
| All other subtask types | AT-4, AT-5 | No type-specific auto-transitions |
| `bug`, `workitem`, `task`, `resource_req` | AT-4, AT-5 | No type-specific auto-transitions |

---

## 6. Schema Summary

```yaml
automatic_transitions:
  - rule: all_children_reach_status | first_child_reaches_status |
            linked_ticket_reaches_status | child_blocker_created |
            all_blockers_cleared | this_ticket_reaches_status

    # Common optional fields:
    source_status: <status>                    # pre-condition on this ticket's status
    target_status: <status> | prior_status     # transition destination

    # Rule-specific fields (see Section 3 for each rule type)
    child_filter:
      types: [...]
      link_types: [...]
      link_type: ...
    child_statuses: [...]
    linked_ticket_types: [...]
    linked_statuses: [...]
    link_type: ...
    link_role: source | target
    linked_ticket_source_status: ...
    linked_ticket_target_status: ...
    blocker_terminal_statuses: [...]
    save_prior_status: true | false
```

---

## 7. Migration Plan

1. **Update** `question.yaml`: Replace free-text `automatic_transitions` with AT-4, AT-5, and AT-6.
2. **Update** `codereview.yaml`: Replace free-text `automatic_transitions` with AT-3, AT-4, and AT-5.
3. **Update** `epic.yaml`: Replace free-text `automatic_transitions` with AT-1 (×2), AT-2, AT-4, and AT-5.
4. **Update** `feature.yaml`: Replace `automatic_transitions: []` with AT-1, AT-4, and AT-5.
5. **Update** `dev_story.yaml`: Replace `automatic_transitions: []` with AT-1 (×3), AT-4, and AT-5.
6. **Update** all remaining files with `automatic_transitions: []` that have a `Blocked` status: add AT-4 and AT-5 to each (`development`, `devops`, `design`, `unittest`, `testcase`, `testexec`, `bug_subtask`, `bug`, `workitem`, `task`, `resource_req`, `ba_subtask_analysis`, `ba_subtask_design`, `sa_subtask_analysis`, `sa_subtask_design`, `ux_subtask_analysis`, `ux_subtask_design`).
7. **Remove** all prose instructions that describe automatic transitions (they become redundant once rules are machine-enforced). Update `ticket_instructions` to reference rule behavior rather than re-describe it.
8. **Validate** each ticket type's `allowed_transitions` includes every `target_status` and `linked_ticket_target_status` referenced by its rules.

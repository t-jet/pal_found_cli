---
name: workflow
description: Guides AI agents on organizing development work, moving features through project stages, selecting and linking the correct ticket types, and respecting role responsibilities at each stage.
license: Apache-2.0
metadata:
  author: t-jet
  version: "0.1.0"
---

# Workflow Skill — Project Development Process

## Purpose

This skill guides AI agents on how to organize development work, move features through project stages, select and link the correct ticket types, and respect role responsibilities at each stage.

---

## Development Phases and Stages

The project lifecycle has four phases. Each phase produces specific ticket states and artifacts.
Below definition is the only high-level reference for the workflow. Agents must follow exact requirements provided for each status provided for each ticket type, which is accessible with help of the `ticket-helper` subagent.

### Phase 1 — Discovery and project Backlog Filling

| Stage | Action | Ticket states |
|---|---|---|
| 0 | Register Feature request | `FEATURE` → New |
| 1 | Match DoD for the new feature's New status | `FEATURE` → Open |


### Phase 2 — Requirements & Scope Refinement

| Stage | Action | Ticket states |
|---|---|---|
| 2 | Plan analysis sprint | `FEATURE` → Analysis; create `BA-ANA` + `SA-ANA` sub-tasks (Open) |
| 3 | Run analysis; create Epics and Dev Stories | `BA-ANA`/`SA-ANA` → In Progress; `EPIC` → New; `DEV-STORY` → Analysis |
| 4 | Analysis complete | `BA-ANA`/`SA-ANA` → Closed; `FEATURE` → In Development; `DEV-STORY` → New |

### Phase 3 — Design

| Stage | Action | Ticket states |
|---|---|---|
| 5 | Plan design sprint | `FEATURE` → In Development; create `BA-DES` + `SA-DES` sub-tasks (Open) |
| 6 | Design in progress | `BA-DES`/`SA-DES` → In Progress |
| 7 | Design done | `BA-DES`/`SA-DES` → Closed; `FEATURE` → Waiting for Implementation; `DEV-STORY` → Grooming |

### Phase 4 — Implementation

| Stage | Action | Ticket states |
|---|---|---|
| 8 | Grooming & planning | Create implementation sub-tasks under `DEV-STORY` (all Open); `DEV-STORY` → Grooming |
| 9 | Story estimated and ready | `DESIGN` sub-task → Closed; `DEV-STORY` → Open |
| 10 | Development starts | `DEV-STORY` → Development; `EPIC` → In Progress; `DEV`/`UNITTEST`/`CODEREVIEW`/`TESTCASE`/`DEVOPS` → In Progress |
| 11 | Testing & bug fixing | `TESTEXEC` → In Progress; `BUG-SUB` created if defects found |
| 12 | Ready for deployment | All implementation sub-tasks → Closed; `DEV-STORY` → Deployment |
| 13 | Deployed to UAT | `DEVOPS` manages UAT deployment |
| 14 | Deployed to Production | `DEV-STORY` → Resolved |
| 15 | All Dev Stories deployed | `EPIC` → Resolved → Done |
| 16 | All Epics deployed | `FEATURE` → Resolved → Closed |

---

## Ticket Type Reference

### Top-level Tickets

| Type | ID prefix | Purpose | Key roles |
|---|---|---|---|
| `feature` | FEATURE | Business requirement or initiative. Root of the hierarchy. Tracks the full lifecycle from idea to production. | Project Owner, Business Analyst |
| `epic` | EPIC | End-to-end use case grouping related Dev Stories under a Feature Request. | Business Analyst, Architect |
| `dev_story` | DEV-STORY | Single implementable unit of work, always nested under a Feature and linked to an Epic. Must fit in one sprint. | Tech Lead, Developers |
| `bug` | BUG | Production or UAT defect. Can trigger a new Feature Request if systemic. | QA Engineer, Developer |
| `task` | TASK | Ad-hoc general work not tied to a Feature or Epic. | Assignee |
| `resource_req` | RESOURCE-REQ | Request to provision a new agent role or resource for the project. | Reporter, Manager |

### Analysis Phase Sub-Tasks (children of `feature`)

| Type | ID prefix | Purpose |
|---|---|---|
| `ba_subtask_analysis` | BA-ANA | BA gathers and documents business requirements, impact, and acceptance criteria. |
| `sa_subtask_analysis` | SA-ANA | SA reviews affected services, defines architecture approach and technology stack. |

### Design Phase Sub-Tasks (children of `feature`)

| Type | ID prefix | Purpose |
|---|---|---|
| `ba_subtask_design` | BA-DES | BA produces detailed business design specifications and UI/UX artifacts. |
| `sa_subtask_design` | SA-DES | SA produces detailed technical architecture, API, and infrastructure specifications. |

### Implementation Sub-Tasks (children of `dev_story`)

| Type | ID prefix | Purpose |
|---|---|---|
| `design` | DESIGN | Grooming, estimation, and technical design for the story. Created first; closed before development starts. |
| `development` | DEV | Code implementation. Requires a paired `codereview` sub-task. |
| `unittest` | UNITTEST | Unit test implementation alongside development. |
| `codereview` | CODEREVIEW | Code review of the development sub-task result. |
| `testcase` | TESTCASE | Test case design by QA. Runs in parallel with development. |
| `testexec` | TESTEXEC | Test execution after development completes. |
| `devops` | DEVOPS | Pipeline, infrastructure, and deployment tasks. |
| `bug_subtask` | BUG-SUB | Defect sub-task created under a Dev Story when bugs are found during testing. |

### Cross-Cutting Sub-Tasks (children of any ticket)

| Type | ID prefix | Purpose |
|---|---|---|
| `question` | QUESTION | Clarification request to another team member. Automatically blocks the parent ticket until resolved. |
| `workitem` | WORK | Generic unclassified sub-task for ad-hoc work not fitting other types. |

### Analysis/Design UX Sub-Tasks

| Type | ID prefix | Purpose |
|---|---|---|
| `ux_subtask_analysis` | UX-ANA | UX analysis of user flows and interface requirements at the Analysis stage. |
| `ux_subtask_design` | UX-DES | UX detailed design (wireframes, prototypes) at the Design stage. |

---

## Ticket Hierarchy

```
FEATURE
├── BA-ANA  (Analysis stage)
├── SA-ANA  (Analysis stage)
├── BA-DES  (Design stage)
├── SA-DES  (Design stage)
├── UX-ANA  (Analysis stage, optional)
├── UX-DES  (Design stage, optional)
├── QUESTION  (any stage, blocks parent)
└── DEV-STORY  (one per use-case/implementation unit)
    ├── DESIGN
    ├── DEV
    ├── UNITTEST
    ├── CODEREVIEW
    ├── TESTCASE
    ├── TESTEXEC
    ├── DEVOPS
    ├── BUG-SUB  (created during testing if defects found)
    └── QUESTION  (any stage)

EPIC  ←→  FEATURE  (FeatureContains / Is Contained In Feature)
EPIC  ←→  DEV-STORY  (EpicLink field)
```

---

## Link Types

| Link type | Meaning | Typical usage |
|---|---|---|
| `Contains` / `Contained In` | Parent → child ownership | Feature → Dev Story; Dev Story → sub-task |
| `EpicLink` | Story belongs to Epic | DEV-STORY ↔ EPIC |
| `FeatureContains` / `Is Contained In Feature` | Feature ↔ Epic grouping | FEATURE ↔ EPIC |
| `Blocks` / `Is Blocked By` | One ticket prevents another | Question blocks parent; Bug blocks story |
| `DependsOn` / `Is Dependency For` | Ordering dependency | Story requires another to finish first |
| `BugFeature` (Comes From / Goes To) | Bug leads to Feature Request | BUG → FEATURE |
| `RelatesTo` | Loose contextual relationship | Any two related tickets |

---

## Workflow Rules for Agents

1. **Always check the workflow config** before creating or transitioning a ticket. Valid statuses, transitions and required fields should be retrieved by answering the `ticket-helper` subagent.

2. **Ticket creation sequence per phase:**
   - Phase 2 start → create `BA-ANA` + `SA-ANA` under the Feature; move Feature to Analysis.
   - Phase 3 start → create `BA-DES` + `SA-DES` under the Feature; move Feature to In Development.
   - Phase 4 start → create `DESIGN`, `DEV`, `UNITTEST`, `CODEREVIEW`, `TESTCASE`, `TESTEXEC`, `DEVOPS` under the Dev Story; move Dev Story to Grooming.

3. **Epic auto-transitions:** Epic moves to In Progress when its first Dev Story enters Development, and to Resolved/Done when all Dev Stories are Resolved/Closed.

4. **Question sub-tasks block the parent.** When created, set parent to Blocked. When closed, restore parent to its prior status and archive Q&A in `project_qa.md`.

5. **Dev Story must have `release_notes` before Grooming** and an `assignee` before Development.

6. **Development sub-task requires a paired CodeReview sub-task.** Do not close a Development sub-task without a corresponding CodeReview.

7. **Terminal statuses** (`Closed`, `Canceled`, `Rejected`, `Duplicated`, `Done`) are irreversible. Any non-terminal status can transition to a terminal status.

8. **Time reporting:** Allowed only on sub-tasks, never on Feature, Epic, or Dev Story directly.

9. **Use `task`** for ad-hoc work that does not belong to any Feature or Epic. Use `workitem` for unclassified sub-tasks within an existing ticket.

10. **Use `resource_req`** when a new agent role or team resource needs to be provisioned for the project.

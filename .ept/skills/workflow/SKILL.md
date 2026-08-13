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

## Mandatory ticket handling instructions

- Tickets should not be transitioned from one status to another if the transition has a Definition of Done (DoD) and that DoD is not met.
- DoD compliance must be documented in ticket comments by the responsible role with supporting evidence and verified by the manager.
- DoD criteria should be taken from the `ticket-helper` subagent output from the `definitions_of_done` section which defines the DoD for the current status. It includes the QUESTION sub-tasks that need to be resolved for the DoD to be considered met.
- Strictly follow instructions from the `instructions` section of the ticket-helper output while working on the ticket. This section contains specific instructions for the current status of the ticket and must be followed to ensure proper handling and progression of the ticket through its lifecycle.
- Evidence should be materialized: a link to the existing durable artifacts or chain-of-thought for the critical thinking in the ticket comment.
- All questions should be asked exclusively through the QUESTION sub-task type.
- When creating a ticket, read the DoD criteria for advancing it to the Open status and follow those instructions immediately after creation. Every new ticket must be promoted by its author to the Open status right away.

## Development Phases and Stages

The project lifecycle has four phases. Each phase produces specific ticket states and artifacts.
Below definition is the only high-level reference for the workflow. Agents must follow exact requirements provided for each status provided for each ticket type, which is accessible with help of the `ticket-helper` subagent.

### Phase 1 — Discovery and project planning

Analyze the project requirements and create FEATURE tickets representing the business requirements and initiatives, arranged by priority approved by the Project Owner. Each FEATURE should be linked to an EPIC that represents the end-to-end scenario it belongs to. The EPIC serves as a logical grouping for all features that required to achieve a specific business goal.
Features can belong to multiple Epics if they contribute to multiple end-to-end scenarios.
During this phase, the focus is on understanding the business needs, defining the high-level requirements, and organizing the work into manageable units that can be further analyzed and designed in subsequent phases.
At the end of the discovery phase, the set of well-defined prioritized FEATURE tickets in the Open status,linked to their respective EPIC tickets.

### Phase 2 — Requirements & Scope Refinement
This phase corresponds to the Analysis status of the FEATURE tickets.
The BA-ANA and SA-ANA sub-tasks are opened under each FEATURE to capture the analysis work by the Business Analyst and Solution Architect. The BA focuses on gathering and documenting business requirements, impact analysis, and acceptance criteria, while the SA reviews affected services, defines the architecture approach, and identifies the technology stack. If UX work is needed, a UX-ANA sub-task can also be created to analyze user flows and interface requirements at this stage. The goal of this phase is to refine the requirements and scope of the feature with Project Owner, ensuring that all necessary information is gathered to proceed with design.

### Phase 3 — Design
This phase starts once all analysis sub-tasks of the feature are closed and corresponds to the **`In Design`** status of the FEATURE tickets.
The BA-DES and SA-DES sub-tasks are opened under each FEATURE to capture the design work by the Business Analyst and Solution Architect. The BA produces detailed business design specifications and UI/UX artifacts, while the SA produces detailed technical architecture, API, and infrastructure specifications. If UX work is needed, a UX-DES sub-task can also be created to produce detailed design artifacts such as wireframes and prototypes. This phase focuses on producing the detailed design specifications needed for implementation, ensuring that all design work is completed and approved before moving to the implementation phase.
As part of BA-DES work, Developer Stories (DEV-STORY) are created and linked to the Feature. DEV-STORYs are created while the Feature is still `In Design`, before the design sub-tasks are closed. At the end of the design phase, all design sub-tasks are closed, the FEATURE ticket is moved to `Waiting for Implementation`, and all created DEV-STORY tickets begin progressing through their own lifecycle.

### Phase 4 — Implementation

This phase starts once DEV-STORY tickets are created (during Phase 3 BA-DES work) and moved to the `Open` status and holds until all related DEV-STORYs are deployed to production and closed.
The DEV-STORY lifecycle proceeds through the following stages: **Analysis** → **Grooming** → **Development** → **QA** → **Deployment** → **Resolved** → **Closed**.

- **Analysis:** Technical scope, constraints, and dependencies of the story are clarified. The `release_notes` field must be populated before the story can advance to Grooming.
- **Grooming:** All necessary sub-tasks are created during this stage: DESIGN (grooming, estimation, and technical planning), DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, and DEVOPS (as applicable). The DESIGN sub-task must be **completed and closed** as part of the Grooming stage before the story can transition to Development.
- **Development:** DEV, UNITTEST, and CODEREVIEW sub-tasks are executed. When all are closed, the story advances to QA.
- **QA:** TESTCASE and TESTEXEC sub-tasks are executed. If defects are found, BUG-SUB sub-tasks are created. When all QA sub-tasks and BUG-SUBs are closed, the story advances to Deployment.
- **Deployment:** DEVOPS sub-tasks are executed. When deployment is verified, the story advances to Resolved.

The workflow ensures that all necessary steps are followed for each story, including code review and testing, before deployment to production. The EPIC ticket is automatically transitioned to `In Progress` when the first DEV-STORY linked to it via the `EpicLink` relationship enters the Development stage, and to `Resolved`/`Done` when all linked DEV-STORYs are in a terminal status.

---

## Ticket Type Reference

### Top-level Tickets

The EPIC tickets are used to group related features and dev stories into end-to-end scenarios that represent real business scenarios, such as user registration, payment processing, or order fulfillment. They provide a way to organize and track the work at a higher level of abstraction than individual features or stories, ensuring that all related work is connected and aligned with the overall business goals. EPICs do not have implementation sub-tasks, but QUESTION sub-tasks can be created under an EPIC for clarification purposes. EPICs are linked to Features and Dev Stories through the `EpicLink` and `FeatureContains` relationships.

| Type | ID prefix | Purpose | Key roles |
|---|---|---|---|
| `feature` | FEATURE | Business requirement or initiative. Tracks the full lifecycle from idea to production. | Project Owner, Business Analyst |
| `epic` | EPIC | End-to-end scenario grouping related Dev Stories. Represents a path from stimulus to outcome like in architecture quality scenarios, but focused on real business needs. E.g. user registration, payment processing. | Business Analyst, Architect |
| `bug` | BUG | Production or UAT defect. Can trigger a new Feature Request if systemic or produce one or more BUG-SUB for the specific FEATURE if the root cause is identified as a defect. | QA Engineer, Developer |
| `task` | TASK | Ad-hoc general work not tied to a Feature or Epic. | Assignee |
| `resource_req` | RESOURCE-REQ | Request to provision a new agent role or resource for the project. | Reporter, Manager |

### Analysis Phase Sub-Tasks (children of `feature`)

First sub-tasks created under a Feature to capture analysis work by BA, SA and UX.
Focused on requirements gathering, impact analysis, and solution approach definition.
The UX-ANA is optional depending on the nature of the feature; if UX work is needed, UX-ANA should be created alongside BA-ANA and SA-ANA.

| Type | ID prefix | Purpose |
|---|---|---|
| `ba_subtask_analysis` | BA-ANA | BA gathers and documents business requirements, impact, and acceptance criteria. |
| `sa_subtask_analysis` | SA-ANA | SA reviews affected services, defines architecture approach and technology stack. |
| `ux_subtask_analysis` | UX-ANA | UX analysis of user flows and interface requirements at the Analysis stage. |

### Design Phase Sub-Tasks (children of `feature`)

Created after all analysis sub-tasks of the feature are closed at the start of Phase 3 to capture design work by BA, SA and UX.
Focused on producing detailed design specifications, technical architecture, and UI/UX artifacts needed for implementation.

| Type | ID prefix | Purpose |
|---|---|---|
| `ba_subtask_design` | BA-DES | BA produces detailed business design specifications and UI/UX artifacts. |
| `sa_subtask_design` | SA-DES | SA produces detailed technical architecture, API, and infrastructure specifications. |
| `ux_subtask_design` | UX-DES | UX detailed design (wireframes, prototypes) at the Design stage. |

### Feature Implementation Planning Sub-Tasks (children of `feature`)

Created after all design sub-tasks of the feature are closed to plan and prepare for implementation.
Focused on breaking down the work into implementable units (Dev Stories), defining acceptance criteria, and preparing for development.

| Type | ID prefix | Purpose |
|---|---|---|
| `dev_story` | DEV-STORY | Single implementable unit of work with business value, always nested under a Feature and linked to an Epic. Must fit in one sprint. | Tech Lead, Developers |


### Grooming and Implementation Planning Sub-Task (children of `dev_story`)

Created once the Dev Story is defined to capture the grooming, estimation, and technical design work needed to prepare the story for development. Focused on finalizing the implementation approach, breaking down the story into development and testing tasks, and ensuring all necessary information is available for the development team to start work. This sub-task is created first during the grooming phase and must be **closed before the story transitions to Development**. It serves as a prerequisite for all subsequent implementation work.

| Type | ID prefix | Purpose |
|---|---|---|
| `design` | DESIGN | Grooming, estimation, and technical design for the story. Created first; closed before development starts. |

### Implementation Sub-Tasks (children of `dev_story`)

All implementation sub-tasks are created **together during the Grooming stage** alongside the DESIGN sub-task. They capture the actual implementation work and become active only after DESIGN is closed. Focused on coding, testing, and deploying the DEV-STORY.

| Type | ID prefix | Purpose |
|---|---|---|
| `development` | DEV | Code implementation. Requires a paired `codereview` sub-task. |
| `unittest` | UNITTEST | Unit test implementation alongside development. |
| `codereview` | CODEREVIEW | Code review of the development sub-task result. |
| `testcase` | TESTCASE | Test case design by QA. Runs in parallel with development. |
| `testexec` | TESTEXEC | Test execution after development completes. |
| `devops` | DEVOPS | Pipeline, infrastructure, and deployment tasks. |
| `bug_subtask` | BUG-SUB | Defect sub-task created under a Dev Story when bugs are found during testing. |

### Cross-Cutting Sub-Tasks

The QUESTION type can be created under **any ticket type** at any stage when clarification or additional information is needed from another team member. It automatically blocks the parent ticket until the question is resolved, ensuring that work does not proceed without necessary clarifications. The WORK type is a generic unclassified sub-task for ad-hoc work that does not fit into any of the other defined types; it is only intended for use under `TASK` and `FEATURE` tickets.

| Type | ID prefix | Purpose |
|---|---|---|
| `question` | QUESTION | Clarification request to another team member. Automatically blocks the parent ticket until resolved. |
| `workitem` | WORK | Generic unclassified sub-task for ad-hoc work not fitting other types. |


---

## Ticket Hierarchy

The ticket hierarchy defines parent-child relationships between different ticket types in the workflow. It ensures that work is organized in a structured manner, with clear ownership and dependencies.

Structure:
```
root-level
|
├── FEATURE
|   ├── BA-ANA  (Analysis stage)
|   ├── SA-ANA  (Analysis stage)
|   ├── BA-DES  (Design stage)
|   ├── SA-DES  (Design stage)
|   ├── UX-ANA  (Analysis stage, optional)
|   ├── UX-DES  (Design stage, optional)
|   ├── QUESTION  (any stage, blocks ticket for which created)
|   |── DEV-STORY  (one per use-case/implementation unit)
|   |   ├── DESIGN (created during grooming, closed before development starts)
|   |   ├── DEV (development implementation)
|   |   ├── UNITTEST (unit test implementation, one per DEV sub-task)
|   |   ├── CODEREVIEW (code review of the development sub-task result)
|   |   ├── TESTCASE (test case design by QA, one per DEV sub-task, runs in parallel with development)
|   |   ├── TESTEXEC (test execution after development completes, can create BUG-SUB if defects found)
|   |   ├── DEVOPS (environment, pipeline, infrastructure, and deployment tasks)
|   |   ├── BUG-SUB  (created during testing if defects found)
|   |   └── QUESTION  (any stage, blocks ticket for which created)
|   └── WORK (unclassified sub-task for ad-hoc work not fitting other types)
├── EPIC  (end-to-end scenarios grouping for related DEV-STORYs and FEATUREs)
|       └── QUESTION  (any stage, blocks ticket for which created)
├── TASK (ad-hoc work)
|       ├── WORK (unclassified sub-task for ad-hoc work not fitting other types)
|       └── QUESTION  (any stage, blocks ticket for which created)
├── BUG (production or UAT defect)
|       └── QUESTION  (any stage, blocks ticket for which created)
└── RESOURCE-REQ (request to provision a new agent role or resource for the project)

```

In addition to the parent-child relationships defined in the hierarchy, there are also specific link types that define relationships between tickets across different branches of the hierarchy. These links provide additional context and connections between related work items.

Structure relationships:
```
EPIC  ←→  FEATURE  (FeatureContains / Is Contained In Feature)
EPIC  ←→  DEV-STORY  (EpicLink field)
```

---

## Link Types

| Type | Source Role | Target Role | Description | Usage |
|---|---|---|---|---|
| `Blocks` | Blocks | Is Blocked By | Blocking relationship. Source ticket prevents progress on target ticket. | Any ticket can block any other ticket. |
| `DependsOn` | Depends On | Is Dependency For | Dependency relationship. Source must wait for target to complete first. | Ticket requires another ticket to be completed before it can proceed. |
| `RelatesTo` | Relates To | Relates To | General symmetric relationship with no ordering implication. | Any loosely related tickets that share context. |
| `Contains` | Contains | Contained In | Containment/parent-child relationship mirroring virtual folder structure. | Feature Request → Developer Story; Developer Story → Sub-Task. |
| `EpicLink` | Epic Link | Epic Link | Symmetric association between an Epic and a Developer Story. | Links a Developer Story to its organizing Epic (logical grouping). |
| `FeatureContains` | Feature Contains | Is Contained In Feature | Feature-to-Epic organizational relationship. | Feature Request ↔ Epic (many-to-many, bidirectional). |
| `BugFeature` | Comes From | Goes To | A bug that requires a new Feature Request to address it properly. | Bug → Feature Request when bug resolution requires a feature. |
| `Question` | Asks About | Has Question | Links a Question sub-task to the ticket it asks about. Auto-created. | Automatically created when a Question sub-task is created under a parent. |
| `ParentChild` | Is Parent Of | Is Child Of | Explicit parent-child relationship, mirrors virtual folder nesting. | Any parent ticket → child ticket (supplements virtual folder structure). |

---

## Workflow Rules for Agents

0. **All ticketing system interactions MUST go through the `ticket-helper` subagent.** This includes — but is not limited to — creating, updating, and transitioning tickets; reading ticket content and comments; managing links; and retrieving any workflow information such as ticket type definitions, valid statuses, transition maps, instructions, or definitions of done. Never access the ticketing system directly by any other means. The `ticket-helper` is the single interface to the tracking system regardless of its underlying implementation.

1. **Always check the workflow config** before creating or transitioning a ticket. Valid statuses, transitions and required fields should be retrieved by asking the `ticket-helper` subagent.

2. Strictly follow the ticket hierarchy and link types defined in this workflow. Do not create tickets without the correct parent-child relationships or required links. For example, a `DEV-STORY` must always be linked to a parent `FEATURE` and an `EPIC` via the appropriate link types.

3. When creating a new ticket, ensure all required fields are populated according to the workflow rules for that ticket type and status. Tickets are always created in the NEW status. After creation, immediately check DoD of this status and perform all actions required to meet the DoD. Only then transition the ticket to the next status.

4. **Epic auto-transitions:** Epic should be moved to `In Progress` when the first Dev Story **linked to it via `EpicLink`** enters Development, and to `Resolved`/`Done` when all linked Dev Stories reach a terminal status.

5. **Question sub-tasks block the parent.** When created, set parent to Blocked. When closed, restore parent to its prior status.

6. **Dev Story must have `release_notes` before Grooming** and an `assignee` before Development.

7. **Development sub-task requires a paired CodeReview sub-task.** Do not close a Development sub-task without a corresponding CodeReview.

8. **Terminal statuses** (`Closed`, `Canceled`, `Rejected`, `Duplicated`, `Done`) are irreversible. Any non-terminal status can transition to a terminal status.

9. **Time reporting:** Allowed only on sub-tasks, never on Feature, Epic, or Dev Story directly.

10. **Use `task`** for ad-hoc work that does not belong to any Feature or Epic. Use `workitem` for unclassified sub-tasks within an existing ticket.

11. **Use `resource_req`** when a new agent role or team resource needs to be provisioned for the project.

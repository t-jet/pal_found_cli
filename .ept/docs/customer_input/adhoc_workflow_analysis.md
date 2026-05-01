# Workflow Analysis — Inconsistencies, Gaps, and Ambiguities

**Date:** 2026-04-30  
**Sources analyzed:**
- `.ept/skills/workflow/SKILL.md` — workflow narrative and agent rules
- `.ept/tracker/.config/.workflow.yaml` — top-level workflow config and type registry
- `.ept/tracker/.config/tickets/*.yaml` — individual ticket type definitions

---

## Summary

This document records findings from a systematic walkthrough of the project workflow from Phase 1 (Discovery) through Phase 4 (Implementation). Each finding includes a description with source references, a proposed resolution, and an empty resolution section for tracking decisions.

---

## Finding #1 — BUG ticket has no `Blocked` status or blocking auto-transitions

**Category:** Gap  
**Severity:** High

**Description:**  
`bug.yaml` does not define a `Blocked` status, does not include `Blocked` in `allowed_transitions`, and has `automatic_transitions: []` (emtpy). However, the `In Progress` instructions inside the same file explicitly state:

> "IF blocked by dependency THEN add a blocking link, set status to Blocked until resolved, and record blocker ID and prior status as a comment on this ticket."

This means the workflow prescribes a state change to `Blocked` that is structurally impossible for BUG tickets. Furthermore, QUESTION sub-tasks created under a BUG (per the cross-cutting hierarchy rule) have no corresponding AT-4/AT-5 auto-transitions to actually block/unblock the parent BUG.

**References:**
- `bug.yaml` — `allowed_transitions`, `automatic_transitions`, `In Progress.instructions`
- `SKILL.md` — "QUESTION type can be created under any ticket type at any stage... It automatically blocks the parent ticket"

**Proposed Resolution:**  
Add `Blocked` status to `bug.yaml` with `stage_goal` and `responsible_roles`. Add it to `allowed_transitions` (allow entry from `Open`, `In Progress`; allow exit to `Open`, `In Progress`). Add AT-4 (`child_blocker_created`) and AT-5 (`all_blockers_cleared`) automatic transitions, mirroring the pattern from `feature.yaml`.

**Resolution:**  
> Implement proposed solution.

---

## Finding #2 — SKILL.md and `dev_story.yaml` contradict when implementation sub-tasks are created

**Category:** Inconsistency  
**Severity:** High

**Description:**  
SKILL.md states:

> "During grooming, the **DESIGN sub-task is created**... Once the DESIGN sub-task is closed, the implementation sub-tasks (DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, DEVOPS) are created."

This implies a two-phase sub-task creation: DESIGN only during Grooming, then all others after DESIGN closes (still within the Development stage of the parent story).

However, `dev_story.yaml` Grooming `instructions` explicitly require **all** sub-tasks to be created during Grooming:

> "Create DESIGN-XXX sub-task… Create DEV-XXX sub-task(s)… Create UNITTEST-XXX… Create TESTCASE-XXX… Create TESTEXEC-XXX… Create DEVOPS-XXX…"

And the Grooming `transition_dods` confirms: "ALL sub-tasks created (DESIGN, DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, DEVOPS as needed)".

Agents following SKILL.md would only create DESIGN during Grooming. Agents following the YAML would create everything.

**References:**
- `SKILL.md` — Phase 4, "Grooming and Implementation Planning Sub-Task" section
- `dev_story.yaml` — `Grooming.instructions`, `Grooming.transition_dods`

**Proposed Resolution:**  
Align one source with the other. Two options:
1. **Preferred:** Update SKILL.md to match the YAML: all sub-tasks are created during Grooming, DESIGN must be **completed** before DEV can start (already enforced by Dev DoD requiring DESIGN closed).
2. Alternatively, update the YAML to defer DEV/UNITTEST/etc. creation until DESIGN is closed, but this requires adding a new mechanism to trigger sub-task creation after DESIGN closure.

**Resolution:**  
> Implement the preferred solution: update SKILL.md to reflect that all sub-tasks are created during Grooming, with DESIGN as a prerequisite for starting DEV work.

---

## Finding #3 — FEATURE `In Development` status name is misleading (refers to Design, not coding)

**Category:** Ambiguity  
**Severity:** Medium

**Description:**  
Phase 3 in SKILL.md is called the "Design" phase and explicitly states that it corresponds to the **`In Development`** status of FEATURE tickets:

> "This phase starts once all analysis sub-tasks of the feature are closed and corresponds to the 'In Development' status of the FEATURE tickets."

`feature.yaml` confirms this with description: `"Design sub-tasks in progress (BA/SA DESIGN stage)"`.

The status name `In Development` universally implies coding/implementation work, not design or documentation activity. Agents and developers reading the FEATURE ticket in `In Development` status could incorrectly conclude that code implementation is underway for that Feature, rather than BA/SA design deliverables.

Additionally, this conflicts with the DEV-STORY lifecycle, where `Development` status actually means code is being written.

**References:**
- `SKILL.md` — Phase 3 description
- `feature.yaml` — `In Development` status description
- `dev_story.yaml` — `Development` status description

**Proposed Resolution:**  
Rename the FEATURE status from `In Development` to `In Design` (or `Design`) to reflect that it covers BA/SA/UX design sub-tasks. Update all references in `feature.yaml` (status definitions, `allowed_transitions`, `automatic_transitions`, ticket instructions, and DoD criteria) and in SKILL.md.

**Resolution:**  
> Apply the renaming of FEATURE `In Development` status to `In Design` across all relevant documentation and YAML files to eliminate confusion between design and implementation stages. Update SKILL.md narrative to reflect the new status name while describing Phase 3 activities.

---

## Finding #4 — EPIC `required_fields` includes singular `feature_request` but EPICs are many-to-many with Features

**Category:** Inconsistency  
**Severity:** Medium

**Description:**  
`epic.yaml` declares:
```yaml
required_fields: [id, type, title, status, feature_request, created, updated]
```

The `feature_request` field in `.workflow.yaml` is a `string` type representing a single ID. However, SKILL.md states that the relationship is many-to-many:

> "Features can belong to multiple Epics if they contribute to multiple end-to-end scenarios."

And the link type `FeatureContains` is described as: "Feature Request ↔ Epic (many-to-many, bidirectional)."

If an EPIC is linked to multiple Features via `FeatureContains` links, the `feature_request` (singular string) required field can only hold one ID — making it impossible to properly represent Epics that belong to multiple Features without violating the schema.

**References:**
- `epic.yaml` — `required_fields`
- `.workflow.yaml` — `fields` section (`feature_request` field type); `link_types.FeatureContains`
- `SKILL.md` — "Features can belong to multiple Epics"

**Proposed Resolution:**  
Change `feature_request` in EPIC to either:
1. An optional single initial Feature link (the one that triggered Epic creation) — keep as string but make it optional.
2. Remove from `required_fields` entirely and rely solely on `FeatureContains` links to represent the relationship.

Also update the `feature_request` field definition in `.workflow.yaml` to clarify whether it stores a single or multiple IDs, or remove it from EPIC requirements.

**Resolution:**  
> Remove the `feature_request` field from the EPIC completely, as the many-to-many relationship is already captured via `FeatureContains` links. Update `epic.yaml` `required_fields` to exclude `feature_request`. Ensure SKILL.md and any related documentation reflect that EPIC-Feature relationships are managed through links, not a dedicated field.

---

## Finding #5 — SKILL.md states "EPICs do not have sub-tasks" but EPICs support QUESTION sub-tasks

**Category:** Inconsistency  
**Severity:** Low

**Description:**  
SKILL.md's Ticket Type Reference section states:

> "EPICs do not have sub-tasks but are linked to Features and Dev Stories through the `EpicLink` and `FeatureContains` relationships."

However, `epic.yaml` includes AT-4 (`child_blocker_created` for QUESTION types) and AT-5 (`all_blockers_cleared`), which are automatic transitions triggered by QUESTION sub-tasks blocking the Epic. The SKILL.md cross-cutting section also states:

> "The QUESTION type can be created under **any ticket type** at any stage."

These are contradictory statements. The YAML configuration says EPICs can be blocked by QUESTION children; the narrative says EPICs have no sub-tasks.

**References:**
- `SKILL.md` — "EPICs do not have sub-tasks", "QUESTION type can be created under any ticket type"
- `epic.yaml` — `automatic_transitions` AT-4, AT-5

**Proposed Resolution:**  
Update SKILL.md to clarify: "EPICs do not have implementation sub-tasks, but QUESTION sub-tasks can be created under an EPIC for clarification purposes." The hierarchy diagram should also be updated to show QUESTION as allowed under EPIC.

**Resolution:**  
> Apply the proposed clarification to SKILL.md and update the ticket hierarchy diagram to reflect that QUESTION sub-tasks can be created under EPICs, while maintaining that EPICs do not have implementation sub-tasks like DEV-STORYs.

---

## Finding #6 — DEV-STORY creation timing is contradictory across sources

**Category:** Inconsistency  
**Severity:** High

**Description:**  
Three sources give conflicting signals about when DEV-STORY tickets are created relative to the FEATURE status:

1. **SKILL.md Phase 3** says: "At the end of the design phase, all design sub-tasks are closed, the FEATURE ticket is moved to 'Waiting for Implementation', and **a DEV-STORY ticket is created** in the Grooming status."  
   → Implies DEV-STORYs are created **after** FEATURE moves to Waiting for Implementation.

2. **`feature.yaml` `In Development` DoD** (criterion for moving to Waiting for Implementation) includes: "BA Design Sub-Task Closed with: … **Developer Stories created and linked**" — implying DEV-STORYs must exist **before** the FEATURE can move to Waiting for Implementation.

3. **`feature.yaml` `Waiting for Implementation` instructions** say: "IF Developer Stories missing THEN create and nest them under FEATURE-XXX" — suggesting DEV-STORYs may not exist yet when `Waiting for Implementation` is entered.

Sources 1 and 2 contradict each other. Source 3 is consistent with 1 but contradicts 2.

**References:**
- `SKILL.md` — Phase 3 description
- `feature.yaml` — `In Development.transition_dods`, `Waiting for Implementation.instructions`

**Proposed Resolution:**  
Decide on a canonical moment for DEV-STORY creation:
- **Option A:** DEV-STORYs are created as part of BA-DES sub-task work (within `In Development` FEATURE status). Update `feature.yaml` DoD accordingly, remove redundant "IF Developer Stories missing" check from Waiting for Implementation, and update SKILL.md to say DEV-STORYs are created **before** FEATURE moves to Waiting for Implementation.
- **Option B:** DEV-STORYs are created only when FEATURE enters Waiting for Implementation. Remove DEV-STORY creation from BA-DES DoD criteria and update SKILL.md.

**Resolution:**  
> Apply option A as proposed.

---

## Finding #7 — DEV-STORY `Analysis` status is absent from the SKILL.md Phase 4 narrative

**Category:** Gap  
**Severity:** Medium

**Description:**  
`dev_story.yaml` defines a full `Analysis` status for DEV-STORY with `Open → Analysis → Grooming` transitions, its own `stage_goal`, `responsible_roles`, `instructions`, and DoD criteria (including "Release Notes field filled with meaningful description" and "Technical scope documented").

SKILL.md's Phase 4 narrative describes the DEV-STORY lifecycle as: "grooming and planning, development, testing, and deployment stages." The Analysis status is not mentioned at all. The Phase 4 statement "Implementation phase starts once DEV-STORY tickets are created and moved to the Open status" further implies DEV-STORYs go directly from Open to Grooming.

This means an agent following only SKILL.md would not know the Analysis stage exists or is required.

**References:**
- `SKILL.md` — Phase 4, Workflow Rules
- `dev_story.yaml` — `Analysis` status, `Open.transition_dods`, `Analysis.transition_dods`

**Proposed Resolution:**  
Add the DEV-STORY Analysis stage to the SKILL.md Phase 4 narrative: describe it as a technical scope clarification stage for the story (distinct from the Feature-level analysis) where constraints and dependencies are identified before grooming begins.

**Resolution:**  
> Apply the proposed resolution.

---

## Finding #8 — CODEREVIEW ticket has no `Resolved` status, inconsistent with all other sub-task types

**Category:** Inconsistency  
**Severity:** Low

**Description:**  
Every other sub-task type (BA-ANA, SA-ANA, BA-DES, SA-DES, DESIGN, DEV, UNITTEST, TESTCASE, TESTEXEC, DEVOPS, BUG-SUB, WORK) follows the lifecycle: `New → Open → In Progress → Resolved → Closed`.

`codereview.yaml` deviates from this pattern. It goes: `New → Open → [Correction ↔ Corrected] → Closed`. There is no `Resolved` status. The `Open` transitions allow going directly to `Closed` (approved) without a Resolved intermediate step.

While functionally valid (approval = closed), this inconsistency means agents applying a general "wait for Resolved" rule to detect completion of a CODEREVIEW sub-task will behave incorrectly. The `dev_story.yaml` Development DoD correctly says "All CODEREVIEW sub-tasks Closed" (not Resolved), but any generic monitoring logic looking for `Resolved` would miss the CODEREVIEW completion.

**References:**
- `codereview.yaml` — `allowed_transitions`, `statuses`
- `dev_story.yaml` — `Development.transition_dods`

**Proposed Resolution:**  
Two options:
1. Add a `Resolved` status to CODEREVIEW (approval confirmed, waiting for archive) before `Closed`, to align with the standard sub-task lifecycle.
2. Explicitly document in SKILL.md and `dev_story.yaml` that CODEREVIEW is the only sub-task type with a non-standard lifecycle (no Resolved stage), so agents know to check for `Closed` specifically.

**Resolution:**  
> Analyze all entries of the "wait for resolved" pattern across the YAMLs and SKILL.md. In general this pattern should wait for any of task termial statuses, not the specific "Resolved" status becuse resolution may be different, e.g. "Closed" or "Cancelled". List below all places where "wait for Resolved" is used, and update for waiting for any terminal status if this is awaiting for completion. Don't refer to any specific statuses or configuration files because it should be determined dynamically based on configuration, using specific interfaces, not direct references. 

---

## Finding #9 — EPIC auto-transition mechanism uses hierarchical child filter but DEV-STORYs are children of FEATURE, not EPIC

**Category:** Ambiguity / Gap  
**Severity:** High

**Description:**  
SKILL.md Rule #4 states: "Epic should be moved to In Progress when its first Dev Story enters Development."  
`epic.yaml` AT-2 implements this with:
```yaml
- rule: first_child_reaches_status
  child_filter:
    types: [dev_story]
  child_statuses: [Development, ...]
  source_status: Open
  target_status: In Progress
```

The `child_filter` rule implies it monitors **direct hierarchical children** of the EPIC. However, according to the ticket hierarchy, DEV-STORYs are children of FEATURE, not of EPIC. The EPIC-DEV-STORY relationship is maintained via the `EpicLink` link field (on DEV-STORY) and `EpicLink` link type — not via physical parent-child folder nesting.

If `child_filter` only covers direct hierarchical children, the auto-transition will never fire because DEV-STORYs will never be direct children of an EPIC. The same issue applies to AT-1 (all DEV-STORYs reach terminal → EPIC to Resolved/Done).

**References:**
- `SKILL.md` — Rule #4, "Phase 4 — Implementation", "EPIC automatically transitioned..."
- `epic.yaml` — `automatic_transitions` AT-1, AT-2
- `.workflow.yaml` — `link_types.EpicLink`, hierarchy structure

**Proposed Resolution:**  
Clarify in the automatic_transitions spec whether `child_filter` considers both hierarchical children AND tickets linked via `EpicLink`. If it does not, the rule must be changed to:
```yaml
child_filter:
  types: [dev_story]
  relationship: linked  # via EpicLink
```
Or add an explicit `link_filter` field to the rule syntax. The rule format should be formally documented.

**Resolution:**  
> "its first Dev Story enters Development." mean "the first Dev Story linked to the Epic via EpicLink enters Development", not "the first Dev Story that is a hierarchical child of the Epic enters Development". Update SKILL.md to clarify this point and ensure the YAML rule is correctly configured to monitor linked DEV-STORYs, not hierarchical children if possible (look at .ept\docs\customer_input\adhoc_modification_03.md for possible automatic transition type definitions). 

---

## Finding #10 — BUG-SUB description says "linked to parent Bug ticket" but hierarchy places it under DEV-STORY

**Category:** Inconsistency  
**Severity:** Medium

**Description:**  
`bug_subtask.yaml` description reads:

> "Bug sub-task: investigation and fix activity linked to a **parent Bug ticket**."

The ticket hierarchy in SKILL.md places BUG-SUB under DEV-STORY:
```
DEV-STORY
└── BUG-SUB (created during testing if defects found)
```

The `bug_subtask.yaml` ticket instructions also say: "create a BUG-SUB ticket under appropriate **DEV-STORY**." This confirms BUG-SUB lives under DEV-STORY, but the description field contradicts this by saying "parent Bug ticket."

Furthermore, the top-level `bug.yaml` (BUG) has no mechanism to create BUG-SUB children. The SKILL.md hierarchy shows BUG only having QUESTION as a child. BUG-SUB and BUG are functionally different: BUG is a production/UAT defect; BUG-SUB is a defect found during internal testing inside a DEV-STORY.

**References:**
- `bug_subtask.yaml` — `description`, `Open.instructions`
- `SKILL.md` — Ticket Hierarchy, "BUG-SUB: Defect sub-task created under a Dev Story when bugs are found during testing"
- `bug.yaml` — no child BUG-SUB relationship

**Proposed Resolution:**  
Fix `bug_subtask.yaml` description to read: "Bug sub-task: defect investigation and fix activity nested under a DEV-STORY, created when defects are found during QA testing." Remove any reference to "parent Bug ticket" to eliminate confusion with the top-level BUG ticket type.

**Resolution:**  
> Apply the proposed resolution.

---

## Finding #11 — WORKITEM scope is contradictory between hierarchy diagram and cross-cutting description

**Category:** Inconsistency  
**Severity:** Low

**Description:**  
SKILL.md's "Cross-Cutting Sub-Tasks" section states:

> "The WORK type is a generic unclassified sub-task that can be used for ad-hoc work that does not fit into any of the other defined types."

The section heading is "children of any ticket", implying WORK can be a child of any ticket type.

However, the hierarchy diagram only shows WORK under `FEATURE` and `TASK`:
```
FEATURE
└── WORK
TASK
└── WORK
```

DEV-STORY, BUG, EPIC, and RESOURCE-REQ are not shown as valid parents for WORK. The `workitem.yaml` instructions also refer to "parent **Task** context" specifically.

**References:**
- `SKILL.md` — "Cross-Cutting Sub-Tasks (children of any ticket)", Ticket Hierarchy diagram
- `workitem.yaml` — `New.instructions` ("Review related documentation and parent Task context")

**Proposed Resolution:**  
Decide the intended scope:
- If WORK can be a child of any ticket: update the hierarchy diagram to show WORK under all relevant parents, and update `workitem.yaml` instructions to generalize "parent Task context" to "parent ticket context."
- If WORK is only for TASK and FEATURE: update the cross-cutting section header and description to reflect the actual allowed parents.

**Resolution:**  
> The WORK type is only intended for use under FEATURE and TASK tickets, not all ticket types. Implement the second option.

---

## Finding #12 — DEV-STORY Analysis→Grooming DoD references Feature Design sub-tasks that may not yet exist

**Category:** Ambiguity  
**Severity:** Medium

**Description:**  
`dev_story.yaml` Analysis status DoD (criteria for transitioning to Grooming) includes:

> "DoD met for all BA-SUB and SA-SUB in parent Feature Request (DESIGN stage)"

This criterion requires that the BA Design sub-task (BA-DES) and SA Design sub-task (SA-DES) of the parent FEATURE are complete. However, DEV-STORYs for a Feature are created **during or after** the Feature's design work (per Finding #6). If DEV-STORYs are created after BA-DES/SA-DES close, this DoD criterion will always be satisfied trivially and provides no real gate. If DEV-STORYs are created before design is complete, this criteron becomes a meaningful gate but conflicts with the stated creation timing.

The criterion uses non-standard shorthand "BA-SUB and SA-SUB" which refers to BA-DES and SA-DES sub-tasks of the Feature, not sub-tasks of the DEV-STORY itself. This is ambiguous — an agent may confuse "BA-SUB" with BA-ANA (which has the same naming pattern).

**References:**
- `dev_story.yaml` — `Analysis.transition_dods`
- `feature.yaml` — `In Development` status (where BA-DES/SA-DES live)
- SKILL.md — Phase 3 and Phase 4 boundary

**Proposed Resolution:**  
Replace ambiguous shorthand with explicit names: "BA Design Sub-Task (BA-DES) and SA Design Sub-Task (SA-DES) of the parent Feature closed." Then, as part of resolving Finding #6, determine whether this DoD gate is still meaningful given the resolved creation timing, and remove it if it becomes trivially satisfied.

**Resolution:**  
> Aplply the proposed resolution.

---

## Finding #13 — BA-ANA `Resolved` DoD requires SA-ANA and UX-ANA to be in `Resolved`, but SA-ANA has no symmetric requirement

**Category:** Inconsistency  
**Severity:** Low

**Description:**  
`ba_subtask_analysis.yaml` Resolved DoD criteria include:

> "SA-SUB and UX-SUB (if exists) in Resolved status"

This means BA-ANA cannot move to Closed until SA-ANA (and UX-ANA) are also Resolved. However, `sa_subtask_analysis.yaml` Resolved DoD has no corresponding requirement for BA-ANA to be Resolved. SA-ANA can close independently while BA-ANA is still open.

This asymmetry means SA-ANA can complete and archive before BA-ANA finishes, potentially leaving BA-ANA with stale SA artifacts. If the intent is mutual collaborative completion (BA and SA must finish together before either closes), the constraint should be symmetric.

**References:**
- `ba_subtask_analysis.yaml` — `Resolved.transition_dods`
- `sa_subtask_analysis.yaml` — `Resolved.transition_dods` (no BA requirement)

**Proposed Resolution:**  
Either:
1. Add a symmetric criterion to `sa_subtask_analysis.yaml` Resolved DoD: "BA Analysis Sub-Task (BA-ANA) in Resolved status."
2. Remove the constraint from BA-ANA if the intent is simply that SA-ANA starts before BA-ANA can close (which is enforced by the `In Progress` DoD, not Resolved DoD).

**Resolution:**  
> Add a symmetric criterion to `sa_subtask_analysis.yaml` Resolved DoD: "BA Analysis Sub-Task (BA-ANA) in Resolved status." This enforces that both BA and SA analysis sub-tasks must reach Resolved before either can close, ensuring mutual completion.

---

## Finding #14 — FEATURE `Resolved → Closed` DoD is empty — no verification criteria

**Category:** Gap  
**Severity:** Medium

**Description:**  
`feature.yaml` defines the `Resolved → Closed` transition with an empty DoD:

```yaml
Resolved:
  transition_dods:
    - target_statuses: [Closed]
      dod_criteria: []
```

For all other non-terminal statuses in `feature.yaml` and across all ticket types, the DoD defines explicit verification criteria. An empty DoD means any agent can move a FEATURE from Resolved to Closed without any checks — even if there are outstanding links, unresolved questions, or incomplete release documentation.

**References:**
- `feature.yaml` — `Resolved.transition_dods`
- Contrast: `dev_story.yaml` has a detailed `Resolved → Closed` DoD (backward compatibility, release notes, acceptance criteria, etc.)

**Proposed Resolution:**  
Add meaningful DoD criteria to FEATURE `Resolved → Closed`, such as:
- All linked DEV-STORYs are Closed (already enforced by AT-1, but explicit verification is good practice)
- Resolution field set (Done/Rejected/Canceled/Duplicated)
- All linked QUESTION tickets in terminal status
- Release documentation updated if required
- No open blocking links

**Resolution:**  
> Apply proposed resolution.

---

## Finding #15 — `release_notes` is in `optional_fields` but is required before Grooming via `pre_grooming_required`

**Category:** Ambiguity  
**Severity:** Low

**Description:**  
`dev_story.yaml` declares:
```yaml
optional_fields: [..., release_notes, ...]
pre_grooming_required: [release_notes]
```

The field is simultaneously "optional" (standard schema label implying it can be omitted) and "required before Grooming" (a workflow enforcement point). Agents or tooling that use `optional_fields` to determine whether a field can be left blank will correctly allow skipping `release_notes` at creation time, but may miss the enforcement mechanism in `pre_grooming_required`.

SKILL.md Rule #6 also calls this out: "Dev Story must have `release_notes` before Grooming" — but the field's placement in `optional_fields` can lead to confusion.

**References:**
- `dev_story.yaml` — `optional_fields`, `pre_grooming_required`
- `SKILL.md` — Rule #6

**Proposed Resolution:**  
Add a `conditionally_required_fields` list or similar construct to make this pattern explicit in the schema. Alternatively, add a note directly in the field definition (via a `note` property) or in the status instruction of `Analysis` to flag that `release_notes` must be populated before the transition to Grooming is permitted. Update SKILL.md to clarify that "optional" means "not required at creation" — not "optional throughout the lifecycle."

**Resolution:**  
> Add instruction for the `Analysis` status. The field itself should be kept in `optional fields` to allow creation without it, but the `Analysis` status instructions should explicitly state that it must be filled before moving to Grooming and mention in the DoD criteria to move to the Grooming status.

---

## Finding #16 — EPIC `New → Open` DoD includes "First linked Developer Story enters Development (automatic)" which is impossible at that stage

**Category:** Inconsistency  
**Severity:** Medium

**Description:**  
`epic.yaml` DoD for transitioning from `New` to `Open` includes:

> "First linked Developer Story enters Development (automatic)"

At the time an EPIC is in `New` status, no Developer Stories have been created yet (they are created in Phase 3 / Feature Waiting for Implementation). It is structurally impossible for a DEV-STORY to be in Development when an EPIC is still in `New`. This criterion belongs to the `Open → In Progress` DoD (which is correctly listed as an AT-2 trigger), not in `New → Open`.

**References:**
- `epic.yaml` — `New.transition_dods`
- `epic.yaml` — `automatic_transitions` AT-2
- SKILL.md — Phase 1 (Epics created during Feature Analysis, well before any DEV-STORY exists)

**Proposed Resolution:**  
Remove "First linked Developer Story enters Development (automatic)" from the `New → Open` DoD criteria. It is correctly captured in AT-2 which fires from `Open` to `In Progress`. The `New → Open` DoD should focus on Epic scope definition and Feature linkage.

**Resolution:**  
> Apply the proposed resolution.

---

## Finding #17 — `dev_story.yaml` Grooming DoD references DESIGN sub-task but instructs it to be created only after Grooming transition

**Category:** Inconsistency / Ambiguity  
**Severity:** Medium

**Description:**  
`dev_story.yaml` `Development` instructions state:

> "Execute DESIGN sub-task first (must close before DEV starts)."

And the `Development` DoD requires: "DESIGN sub-task Closed."

However, the DESIGN sub-task is created **during Grooming** (per Grooming instructions). This means DESIGN is created in Grooming, but executed and closed only during Development — creating a split lifecycle where a sub-task is born in one parent stage and completed in another.

The DESIGN sub-task's own YAML (`design.yaml`) `Open` DoD requires: "Developer Story in Grooming" — confirming it is tied to Grooming. But its work (producing design notes, estimates, and sub-task assignments) logically happens **before** Development begins. The ambiguity: is DESIGN closed before the DEV-STORY moves to Development (as a prerequisite for the transition), or is it closed during Development?

**References:**
- `dev_story.yaml` — `Grooming.instructions`, `Development.instructions`, `Development.transition_dods`
- `design.yaml` — `Open.transition_dods` ("Developer Story in Grooming")

**Proposed Resolution:**  
Clarify that DESIGN must be **closed** as part of the Grooming DoD (before `Grooming → Development` transition), not closed during Development. Add "DESIGN sub-task Closed" to the `dev_story.yaml` `Grooming → Development` DoD. Remove "Execute DESIGN sub-task first" from Development instructions (it would already be closed). This aligns with SKILL.md's statement "This sub-task is created first during the grooming phase and must be closed before any development work begins."

**Resolution:**  
> Apply proposed solution.

---

*End of findings — 17 issues documented.*

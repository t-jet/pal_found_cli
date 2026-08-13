# Business Design — BA-DES-007

## Store Skills in a Standard `.agents/skills` Folder for All Harnesses

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-007 |
| **Feature** | FEATURE-006 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-006, SA-ANA-006 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines how all agent skills move to the standard `.agents/skills`
folder so every supported harness discovers and loads the same content. Skill
folders are renamed with the confirmed `pal-found-` prefix (ND-010-04). One
canonical location removes duplicated copies per harness and keeps
maintenance consistent across the programme.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-007-01 | All agent skills must be stored in the standard `.agents/skills` folder. |
| BR-D-007-02 | Every supported agent harness must be able to discover and load the skills from that folder. |
| BR-D-007-03 | Skill content must be stored once; no duplicate copies for individual harnesses. |
| BR-D-007-04 | After migration, no skill content may live only in the old Claude-specific location. |
| BR-D-007-05 | Harnesses that do not recognize the standard folder must have clear instructions for pointing them at the skills. |
| BR-D-007-06 | Skill folder names must use the confirmed `pal-found-` prefix. |

## 3. Logical Flow (business terms)

1. An inventory lists every skill folder and its current location.
2. Each skill folder is renamed with the `pal-found-` prefix and moved into
  the standard `.agents/skills` folder.
3. A discovery check runs on each supported harness: the harness must find
  every skill in the standard folder.
4. For harnesses that do not recognize the standard folder, onboarding
  instructions explain how to point the harness at the skills.
5. Once discovery is confirmed on all harnesses, the old Claude-specific
  location is removed or reduced to a pointer, so no skill content lives
  only in the old location.

## 4. UI/UX (abstract)

The change is content-structural; the visible effect is on how harnesses
surface skills:

- An agent in any supported harness can be asked to use a skill and the
  harness finds the skill in `.agents/skills`.
- A skill author adds or updates a skill once in `.agents/skills` and every
  harness uses that content.
- Onboarding a new harness: the harness either loads `.agents/skills`
  directly or follows documented instructions that point at it.
- Error experience: a harness that cannot see the skills receives clear
  setup instructions instead of silently ignoring them.

## 5. API Specification (abstract)

No application interfaces change. The design relies on harness-level
capabilities:

- A standard folder convention that a harness can scan for skills.
- A configuration point per harness that can point to a custom skill
  location where the convention is not supported.
- Skill folders containing a self-contained description file that the
  harness reads to load the skill.

## 6. Data Structures (business terms)

- Skill folder record: folder name (with `pal-found-` prefix), description
  file, supporting content, owning harnesses.
- Location map record: each skill, its standard-folder location, and any
  legacy location to retire.
- Harness capability record: harness name, whether it supports the standard
  folder natively, and its configuration instructions.

## 7. Acceptance Criteria

- AC-D-007-01: Given a supported agent harness, when it loads skills from
  `.agents/skills`, then it discovers all `pal-found-*` skills.
- AC-D-007-02: Given a skill author, when they add or update a skill, then
  they store it once in `.agents/skills` and all harnesses use that content.
- AC-D-007-03: Given the old Claude-specific layout, when migration
  completes, then no skill content exists only in the old location.
- AC-D-007-04: Given a harness that does not support the standard folder,
  when it is onboarded, then clear instructions exist for pointing it at
  the skills.
- AC-D-007-05: Given all skill folders, when naming is checked, then each
  uses the `pal-found-` prefix.

## 8. Migration Procedure

1. Build the skill inventory and the harness capability record.
2. Rename and move each skill folder into `.agents/skills` with the
  confirmed prefix; update internal references between skills.
3. Run the discovery check per harness (AC-D-007-01) and record results.
4. Write onboarding instructions for harnesses that do not support the
  standard folder.
5. After all checks pass, remove the old Claude-specific location (or
  replace it with a pointer), verifying no skill content lives only there.
6. Update programme documentation (distribution guides, README) to cite the
  standard folder.
7. Rollback: keep the old location read-only until all discovery checks
  pass, so skills can be restored if a harness fails discovery.

## 9. Developer Story Scope

Two stories: (1) migrate and rename all skill folders into `.agents/skills`;
(2) harness discovery verification and onboarding instructions.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-006 |
| Epic | EPIC-009 |
| BA design sub-task | BA-DES-007 |
| SA counterpart | SA-DES-006 |
| Analysis | BA-ANA-006, SA-ANA-006 (Closed, PO-approved) |
| Naming decisions | ND-010-04 (QUESTION-075, Closed) |

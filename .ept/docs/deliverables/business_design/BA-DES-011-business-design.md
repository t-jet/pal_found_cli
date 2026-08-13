# Business Design — BA-DES-011

## Rename the `foundry_` Prefix to `pal_found_` Across All Three Projects

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-011 |
| **Feature** | FEATURE-010 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-010, SA-ANA-010 (Closed, PO-approved) |
| **Requirement source** | Project Owner change request 2026-08-12 |

---

## 1. Design Overview

The design defines how the `foundry_` prefix changes to `pal_found_` across
all public surfaces of the three projects. The Project Owner confirmed the
exact target names on 2026-08-12 (ND-010-01..04): repositories and the
Python package use `pal_found_`; console commands and agent skill folders
use `pal-found-`. The rename is cross-cutting: it constrains the design of
FEATURE-002..009 so target names are built in from the start. Only names
change; behaviour, operations, and data are unchanged.

## 2. Confirmed Naming Decisions

| # | Surface | Current | Target |
| --- | --- | --- | --- |
| ND-010-01 | Repository names | `foundry_cli`, `foundry_cli_tool`, `foundry_cli_skills` | `pal_found_cli`, `pal_found_cli_tool`, `pal_found_cli_skills` |
| ND-010-02 | Python package | `foundry_cli` | `pal_found_cli` |
| ND-010-03 | Console entry-point prefix | `foundry-` | `pal-found-` |
| ND-010-04 | Agent skill folder prefix | `foundry-` | `pal-found-` |

Source: QUESTION-072..075, all Closed 2026-08-12.

## 3. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-011-01 | All three repositories must use the confirmed `pal_found_` prefix in their public names. |
| BR-D-011-02 | The Python package must use the confirmed `pal_found_` name when installed. |
| BR-D-011-03 | All CLI commands must use the confirmed `pal-found-` prefix. |
| BR-D-011-04 | All agent skills must use the confirmed `pal-found-` prefix in names and folder layout. |
| BR-D-011-05 | Published documentation must use the new names; stale `foundry_` references remain only in clearly marked historical notes. |
| BR-D-011-06 | The rename must not change tool behaviour, supported operations, or data; only names change. |
| BR-D-011-07 | Migration notes and announcements must tell existing users how their clones, scripts, and references are affected. |

## 4. Logical Flow (business terms)

1. A rename inventory lists every public surface: repository names, package
  name, command names, skill folder names, and documentation references.
2. The rename is applied in dependency order: package and commands first,
  then skill folders, then repository names, with references updated at
  each step.
3. A naming sweep scans all published content for stale `foundry_`
  references and converts them (or marks them as historical notes).
4. A behaviour check confirms the tool performs identically after the
  rename.
5. Release announcements and migration notes are published so existing
  users can migrate their clones and scripts.

## 5. UI/UX (abstract)

No custom interface is built. Abstract user experience:

- A user installs the package under the confirmed name and runs commands
  with the confirmed prefix.
- A user browsing the three repositories sees the confirmed names.
- A user loading agent skills sees the confirmed `pal-found-` folder names.
- A user reading documentation finds the new names with historical notes
  where old names are mentioned.
- Migration experience: existing users are told what changed and how to
  update clones, scripts, and skill references.

## 6. API Specification (abstract)

No application interfaces change; the design relies on rename behaviours:

- A package can be published and installed under a new name.
- Commands can be exposed under a new prefix while behaviour stays the same.
- Skill folders can be renamed while remaining discoverable.
- Repository names can change with the old names redirecting or being
  documented as historical.

## 7. Acceptance Criteria

- AC-D-011-01: Given the three repositories, when the rename is applied,
  then every repository name uses the confirmed `pal_found_` prefix.
- AC-D-011-02: Given the Python package, when a user installs it, then the
  installed package carries the confirmed name.
- AC-D-011-03: Given the CLI tool, when a user runs its commands, then
  every command uses the confirmed `pal-found-` prefix.
- AC-D-011-04: Given the agent skills, when they are distributed and
  loaded, then skill names and folder layout use the confirmed `pal-found-`
  prefix.
- AC-D-011-05: Given the published documentation, when a user reads it,
  then no active `foundry_` name remains outside clearly marked historical
  notes.
- AC-D-011-06: Given an existing user of the tool, when the rename ships,
  then the tool performs identically; only names change.

## 8. Migration Procedure

1. Freeze content changes and publish the rename inventory so every surface
  is known before the move.
2. Apply the rename in dependency order:
   a. Package and console commands: republish under `pal_found_cli` /
      `pal-found-` (aligns with FEATURE-004 and FEATURE-005).
   b. Skill folders: rename to `pal-found-*` in the standard
      `.agents/skills` folder (aligns with FEATURE-006 and FEATURE-007).
   c. Repository names: rename `pal_found_cli`, `pal_found_cli_tool`,
      `pal_found_cli_skills` with old names redirecting or documented as
      historical (aligns with FEATURE-002 and FEATURE-003).
3. Update documentation references at each step; run the naming sweep
  (AC-D-011-05).
4. Run the behaviour check (AC-D-011-06) and the acceptance criteria.
5. Publish migration notes and release announcements telling users how to
  update clones, scripts, and skill references.
6. Rollback: keep old-name redirects and a release tag for the last
  old-name state so users can revert if a rename step fails; verify
  behaviour before each rollback decision.

## 9. Developer Story Scope

Two stories: (1) rename package, commands, skill folders, and repository
names per the confirmed mapping; (2) documentation sweep, migration notes,
and behaviour verification.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-010 |
| Epics | EPIC-009, EPIC-010 |
| BA design sub-task | BA-DES-011 |
| SA counterpart | SA-DES-010 |
| Analysis | BA-ANA-010, SA-ANA-010 (Closed, PO-approved) |
| Naming decisions | ND-010-01..04 (QUESTION-072..075, Closed 2026-08-12) |

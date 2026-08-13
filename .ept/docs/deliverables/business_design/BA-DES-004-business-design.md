# Business Design — BA-DES-004

## Split the Project into Three Repositories

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-004 |
| **Feature** | FEATURE-003 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-004, SA-ANA-003 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines how the single combined repository becomes three
independent repositories: `pal_found_cli` (design documentation and
requirements tracking), `pal_found_cli_tool` (CLI tool source), and
`pal_found_cli_skills` (agent skills), per ND-010-01. The split gives each
asset its own version history, release cadence, and contributor base, and is
the structural prerequisite for the distribution features in the programme.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-004-01 | Each asset must live in its own repository: design, CLI tool, agent skills. |
| BR-D-004-02 | Each repository must have an independent version history and release lifecycle. |
| BR-D-004-03 | Content must be classified before the move so no file lands in the wrong repository. |
| BR-D-004-04 | Cross-repository references must be updated so they resolve to the correct location. |
| BR-D-004-05 | Existing history must be preserved for content that moves. |
| BR-D-004-06 | The design repository must remain the home of requirements tracking and documentation. |

## 3. Logical Flow (business terms)

1. An inventory classifies every file in the combined repository into one
   of three ownership groups: design, tool, or skills.
2. The three target repositories are created and the classified content is
   moved, preserving history where required.
3. References between repositories (documentation pointing at tool or
   skills content) are updated to the new locations.
4. A consistency check confirms each repository contains only its own
   content type and that all cross-references resolve.
5. The old combined repository is retired as a workspace; the design
   repository becomes the entry point for the programme.

## 4. UI/UX (abstract)

No new user interface is built; the change is structural. The abstract user
experience:

- A user looking for CLI source opens `pal_found_cli_tool` and finds the
  source there.
- A user looking for skill content opens `pal_found_cli_skills` and finds
  the skill folders there.
- A user looking for requirements and design documentation opens
  `pal_found_cli` and finds it there.
- A user following a documentation link to a repository or file reaches the
  correct new location without a broken reference.

## 5. API Specification (abstract)

No application interfaces change. The design relies on repository-level
capabilities:

- A repository can be created with the correct name and content set.
- History can be carried along when content moves.
- A reference from one repository to another can be expressed as a stable
  link (URL or path) that resolves for users.

## 6. Data Structures (business terms)

- Content classification record: each file or folder, its ownership group
  (design/tool/skills), and its destination repository.
- Repository inventory record: repository name, purpose, content set, and
  entry-point documentation.
- Reference register: each cross-repository reference, its old location,
  and its new location.

## 7. Acceptance Criteria

- AC-D-004-01: Given the split project, when a user browses any of the
  three repositories, then each contains only its own content type.
- AC-D-004-02: Given the CLI tool repository, when a user searches for CLI
  source code, then it is present there.
- AC-D-004-03: Given the agent skills repository, when a user searches for
  skill content, then it is present there.
- AC-D-004-04: Given the design repository, when a user searches for
  requirements and design documentation, then it is present there.
- AC-D-004-05: Given a cross-repository reference, when a user follows it,
  then it resolves to the correct location.
- AC-D-004-06: Given the moved content, when history is verified, then
  required history is preserved.

## 8. Migration Procedure

1. Build the content classification record for the combined repository;
   confirm every item has exactly one ownership group.
2. Create the three target repositories with the confirmed names.
3. Move design and tracking content into `pal_found_cli`; move CLI source
   into `pal_found_cli_tool`; move skill folders into `pal_found_cli_skills`,
   carrying history with the move.
4. Update the reference register: rewrite cross-repository links to the new
   locations and remove stale references.
5. Run the consistency check (AC-D-004-01..05) and fix discrepancies.
6. Retire the old combined layout as the working home and repoint all
   workflow entry points (issue templates, contribution guides, CI
   references) at the three new repositories.
7. Rollback: keep the old repository read-only until the consistency check
   passes, so content can be recovered if the split fails.

## 9. Developer Story Scope

Two stories: (1) classify and move content with history into the three
repositories; (2) update cross-repository references and workflow entry
points, then run the consistency check.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-003 |
| Epic | EPIC-010 |
| BA design sub-task | BA-DES-004 |
| SA counterpart | SA-DES-003 |
| Analysis | BA-ANA-004, SA-ANA-003 (Closed, PO-approved) |
| Naming decisions | ND-010-01 (QUESTION-072, Closed) |

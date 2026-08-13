# Business Analysis — BA-ANA-010

## Rename `foundry_` Prefix to `pal_found_` Across All Three Projects

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-010 |
| **Feature** | FEATURE-010 |
| **Status** | Resolved — pending Project Owner approval (In Progress→Resolved 2026-08-12) |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner change request 2026-08-12 |

---

## 1. Business Case

The three projects in this delivery use the `foundry_` prefix in their public
names: the repository names (`foundry_cli`, `foundry_cli_tool`,
`foundry_cli_skills`), the Python package, the CLI command names, and the agent
skill names. The Project Owner reports that this prefix is confusing: it is too
similar to other projects in the wider ecosystem and to Microsoft Foundry, so
users cannot tell this toolset apart from unrelated products.

The requirement is to change the prefix from `foundry_` to `pal_found_` across
all three projects. The rename touches every public surface a user sees:
repository names, the package name, command names, skill names, and all
documentation that references them. Because the projects are at the analysis
stage (FEATURE-002..009 under EPIC-009 and EPIC-010), the rename is best
decided now, before implementation, so the target names are built in from the
start.

The Project Owner confirmed the exact target names on 2026-08-12 through the
blocking QUESTION tickets (QUESTION-072..075, all closed). The confirmed
decisions are recorded in section 2. Repository names and the Python package
use the underscore form `pal_found_`; CLI entry points and agent skill folders
use the hyphen form `pal-found-`.

## 2. Naming Decisions (Confirmed by Project Owner, 2026-08-12)

| # | Decision | Current name | Confirmed target | Status |
| --- | --- | --- | --- | --- |
| ND-010-01 | Repository names | `foundry_cli`, `foundry_cli_tool`, `foundry_cli_skills` | `pal_found_cli`, `pal_found_cli_tool`, `pal_found_cli_skills` | CONFIRMED (QUESTION-072) |
| ND-010-02 | Python package name | `foundry_cli` | `pal_found_cli` | CONFIRMED (QUESTION-073) |
| ND-010-03 | Console entry-point prefix | `foundry-` (e.g. `foundry-datasets`) | `pal-found-` (e.g. `pal-found-datasets`) | CONFIRMED (QUESTION-074) |
| ND-010-04 | Agent skill folder prefix | `foundry-` skill names and folders | `pal-found-` skill names and folders | CONFIRMED (QUESTION-075) |

All four decisions were confirmed by the Project Owner on 2026-08-12. The rename
uses two forms: underscore (`pal_found_`) for repository names and the Python
package, hyphen (`pal-found-`) for CLI entry points and skill folder names. The
remaining sections are consistent with these confirmed names.

## 3. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-010-01 | All three repositories must use the `pal_found_` prefix in their public repository names. |
| BR-010-02 | The Python package must use the confirmed `pal_found_` name when installed. |
| BR-010-03 | All CLI commands must use the confirmed `pal-found-` prefix so users can identify the toolset by command name. |
| BR-010-04 | All agent skills must use the confirmed `pal-found-` prefix in skill names and folder layout. |
| BR-010-05 | Published documentation must use the new names and must not leave stale `foundry_` references except clearly marked historical notes. |
| BR-010-06 | The rename must not change tool behavior, supported operations, or data; only names change. |

## 4. Acceptance Criteria

- AC-010-01: Given the three repositories, when the rename is applied, then every repository name uses the confirmed `pal_found_` prefix.
- AC-010-02: Given the Python package, when a user installs it, then the installed package carries the confirmed name.
- AC-010-03: Given the CLI tool, when a user runs its commands, then every command uses the confirmed `pal-found-` prefix.
- AC-010-04: Given the agent skills, when they are distributed and loaded, then skill names and folder layout use the confirmed `pal-found-` prefix.
- AC-010-05: Given the published documentation, when a user reads it, then no active `foundry_` name remains outside clearly marked historical notes.
- AC-010-06: Given an existing user of the tool, when the rename ships, then the tool performs identically; only names change.

## 5. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Installation | Users install a package under the new name; instructions and tooling must be updated in step with the package name. |
| Command usage | Users call commands under the new prefix; scripts and documentation that call the old commands stop working until updated. |
| Skill distribution | Skills are cloned and copied under new folder names; agent configurations that reference skill folders must be updated. |
| Contribution | Repository names change; existing forks, clones, and bookmarks of the old names must be migrated by their owners. |
| Documentation | All references across design, analysis, and skill documents are renamed; historical context is preserved in notes. |
| Release management | New releases publish under the new names; release announcements must state the rename clearly. |

## 6. Changes in Access Restrictions

- Repository access rules are unchanged; only the repository names change.
- No user credentials, permissions, or access tiers change as part of the rename.
- Public visibility settings from FEATURE-002 apply unchanged to the renamed repositories.

## 7. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | The names confirmed on 2026-08-12 are final for this analysis; a later name change is handled as a new requirement. |
| Assumption | No other project or product currently uses the proposed names in a way that would create new confusion. |
| Risk | Existing users, clones, and scripts reference the old names and break or point to stale content after the rename. |
| Risk | Documentation misses some reference and leaves mixed naming after the rename. |
| Mitigation | Migration notes and rename announcements; documentation sweep as part of the acceptance criteria. |

## 8. Request Rate Changes

The rename does not change request volumes against Foundry. Tool usage patterns
stay the same; only the command names change. Installation and distribution
traffic may shift temporarily as users migrate to the new names, but expected
volumes stay low.

## 9. Data Size Changes

The rename does not change stored data, dataset sizes, or transfer volumes.
Repository content size stays effectively unchanged (only names and references
are edited).

## 10. Naming Questions to Project Owner

| QUESTION | Decision | Project Owner answer (2026-08-12) |
| --- | --- | --- |
| QUESTION-072 | Repository names | `pal_found_cli`, `pal_found_cli_tool`, `pal_found_cli_skills` |
| QUESTION-073 | Python package name | `pal_found_cli` |
| QUESTION-074 | Console entry-point prefix | `pal-found-` |
| QUESTION-075 | Agent skill folder prefix | `pal-found-` |

## 11. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-010 (Analysis) |
| BA sub-task | BA-ANA-010 (Resolved — pending Project Owner approval) |
| SA counterpart | SA-ANA-010 (Resolved) |
| Requirement source | Project Owner change request 2026-08-12 |
| Naming questions | QUESTION-072, QUESTION-073, QUESTION-074, QUESTION-075 (all Closed 2026-08-12) |
| Approval question | QUESTION-076 (created 2026-08-12, addressed to project-owner) |

# Business Analysis — BA-ANA-004

## Split the Project into Three Repositories

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-004 |
| **Feature** | FEATURE-003 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

The project is a single repository today. The Project Owner wants three separate
repositories: this one for design documentation and requirements tracking, one for
the CLI tool source, and one for the agent skills. Splitting gives each asset an
independent version history, release cadence, and contributor base. It also makes
public hosting and per-asset distribution (pip, conda, git clone) practical, since
each repository can be managed and published on its own.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-004-01 | The project must be split into three separate repositories: design/documentation, CLI tool, and agent skills. |
| BR-004-02 | Each repository must have its own version history and independent release lifecycle. |
| BR-004-03 | A user looking for CLI tool source must find it in the CLI tool repository. |
| BR-004-04 | A user looking for skill content must find it in the agent skills repository. |
| BR-004-05 | Design documentation and requirements tracking stay in the design/documentation repository. |
| BR-004-06 | Cross-repository references (documentation pointing at tool or skills) must be clear and resolvable. |

## 3. Acceptance Criteria

- AC-004-01: Given the split project, when a user browses any of the three repositories, then each contains only its own content type.
- AC-004-02: Given the CLI tool repository, when a user searches for CLI source code, then it is present there.
- AC-004-03: Given the agent skills repository, when a user searches for skill content, then it is present there.
- AC-004-04: Given the design repository, when a user searches for requirements and design documentation, then it is present there.
- AC-004-05: Given a reference from one repository to another, when a user follows it, then it resolves to the correct location.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Contribution | Contributors work on one focused repository per asset instead of one combined project. |
| Release management | Each repository releases independently; combined releases require coordination. |
| Documentation | Design docs live in their own repository with their own history. |
| Requirements tracking | Tracking data stays in the design repository, separate from code. |
| Onboarding | New users learn three repositories and their relationships instead of one monolith. |

## 5. Changes in Access Restrictions

- Access is granted per repository rather than per project.
- The design/documentation repository may have a different contributor set than the CLI tool or skills repositories.
- No Foundry credentials are affected by the split.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | Existing submodules for tool and skills already point at separate repositories and can be promoted. |
| Assumption | Historical content can be relocated without losing required history. |
| Risk | Content split incorrectly, leaving files in the wrong repository. |
| Risk | Cross-repository references break during the move. |
| Mitigation | Clear content classification before the move; verify references after the split. |

## 7. Request Rate Changes

The split itself does not change request rates to any service. Clone and download
traffic is redistributed across three repositories; total volume is unchanged.

## 8. Data Size Changes

Content is redistributed across three repositories; total data volume is unchanged.
Each repository remains small.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-003 (Open) |
| Epic | EPIC-010 — Public repositories and distribution of the Foundry CLI tool |
| BA sub-task | BA-ANA-004 |
| SA counterpart | SA-ANA-003 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

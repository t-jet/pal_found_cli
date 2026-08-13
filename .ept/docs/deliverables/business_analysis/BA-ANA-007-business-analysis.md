# Business Analysis — BA-ANA-007

## Distribute foundry_cli_skills via Git Clone and Skill Copy

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-007 |
| **Feature** | FEATURE-007 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

The skills are distributed as files, not as an installable package. Cloning the
foundry_cli_skills repository and copying the skill folders into the target
harness is a simple, dependency-free distribution method. Clear user instructions
make it reliable for every harness and easy to update by re-cloning.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-007-01 | Users must be able to obtain all skills by cloning the foundry_cli_skills repository. |
| BR-007-02 | Users must be able to copy skill folders into a target harness following documented instructions. |
| BR-007-03 | The repository must provide clear instructions for cloning, copying, and updating skills. |
| BR-007-04 | Instructions must work for every supported harness. |
| BR-007-05 | Updating must be possible by re-cloning or pulling the repository and re-copying. |

## 3. Acceptance Criteria

- AC-007-01: Given a user, when they clone the foundry_cli_skills repository, then they receive all skill content.
- AC-007-02: Given a cloned repository, when the user follows the copy instructions, then the skills become available in the target harness.
- AC-007-03: Given a skills repository update, when a user pulls or re-clones, then they can refresh their local skills to the latest version.
- AC-007-04: Given a user on any supported harness, when they follow the instructions, then the steps are clear and complete.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Installation | Users install skills by cloning and copying; no package manager needed. |
| Updates | Users refresh skills by pulling the repository. |
| Harness onboarding | Copy instructions must match the target harness layout, including the standard folder (FEATURE-006). |
| Support | Installation issues reduce to clone/copy steps that are easy to diagnose. |
| Release management | Skill releases are repository states; no separate artifact publication. |

## 5. Changes in Access Restrictions

- Cloning is public after FEATURE-002; no authentication required.
- No additional restrictions beyond repository access rules.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | Users can run git and can locate the target harness skills folder. |
| Assumption | Copying skill folders does not break harness discovery. |
| Risk | Users copy to the wrong folder and the harness does not load the skills. |
| Risk | Local copies drift from the repository over time. |
| Mitigation | Clear instructions with target paths; update-by-re-clone guidance. |

## 7. Request Rate Changes

Clone traffic increases with the number of users. Volume is low; no consumer-side rate changes required.

## 8. Data Size Changes

The skills repository is small. One-time clone plus periodic pulls is lightweight.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-007 (Open) |
| Epic | EPIC-009 — Harness-agnostic distribution and self-contained content of Foundry agent skills |
| BA sub-task | BA-ANA-007 |
| SA counterpart | SA-ANA-007 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

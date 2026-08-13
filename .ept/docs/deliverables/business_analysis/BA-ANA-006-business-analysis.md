# Business Analysis — BA-ANA-006

## Store Skills in a Standard `.agents/skills` Folder for All Harnesses

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-006 |
| **Feature** | FEATURE-006 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

Skills are currently stored in a Claude-specific layout (`.claude/skills`), which
other agent harnesses such as Copilot do not use. Moving all skills to the
standard `.agents/skills` folder lets every harness discover and load the same
skill content. One canonical location removes duplicated skill copies and makes
maintenance consistent across harnesses.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-006-01 | All agent skills must be stored in the standard `.agents/skills` folder. |
| BR-006-02 | Every supported agent harness must be able to discover and load the skills from that folder. |
| BR-006-03 | Skill content must be stored once; no duplicate copies for individual harnesses. |
| BR-006-04 | After migration, no skill content may live only in the old Claude-specific location. |
| BR-006-05 | Harnesses that do not recognize the standard folder must have clear instructions for pointing them at the skills. |

## 3. Acceptance Criteria

- AC-006-01: Given a supported agent harness, when it loads skills from `.agents/skills`, then it discovers all foundry skills.
- AC-006-02: Given a skill author, when they add or update a skill, then they store it once in `.agents/skills` and all harnesses use that content.
- AC-006-03: Given the old Claude-specific layout, when migration completes, then no skill content exists only in the old location.
- AC-006-04: Given a harness that does not support the standard folder, when it is onboarded, then clear instructions exist for pointing it at the skills.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Harness onboarding | New harnesses load skills from one standard location. |
| Skill maintenance | Authors update one copy instead of per-harness copies. |
| Distribution | The skills repository layout matches the standard, simplifying git-based distribution. |
| Documentation | Documentation references one canonical skill location. |
| Upgrades | Skill updates propagate to all harnesses at once. |

## 5. Changes in Access Restrictions

- No new access restrictions; the folder is part of the skills repository.
- Content visibility follows the repository access rules defined by FEATURE-002.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | The standard `.agents/skills` layout is accepted by the target harnesses. |
| Assumption | Migration can be done without losing skill content or history. |
| Risk | A harness does not recognize the standard folder and silently ignores skills. |
| Risk | Old and new locations drift during migration. |
| Mitigation | Documented onboarding instructions; verify discovery on each harness; remove old location after migration. |

## 7. Request Rate Changes

No request-rate change to any external service. Skill loading is local to each harness.

## 8. Data Size Changes

The skills folder is a set of small markdown files. Total size is unchanged by the move.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-006 (Open) |
| Epic | EPIC-009 — Harness-agnostic distribution and self-contained content of Foundry agent skills |
| BA sub-task | BA-ANA-006 |
| SA counterpart | SA-ANA-006 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

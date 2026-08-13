# Business Analysis — BA-ANA-009

## Document All JSON Formats and Parameter Variants in Each Skill File

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-009 |
| **Feature** | FEATURE-009 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

Each CLI skill can be used only when the user knows the exact input formats and
allowed parameter variants the tool accepts. Today that knowledge may live outside
the skill file. The Project Owner requires each specific skill file to fully
describe all JSON formats and allowed parameter variants for its tool, so the tool
can be used correctly without consulting any other source. This makes every
namespace skill self-contained.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-009-01 | Each specific CLI skill file must document every JSON format the tool accepts as input. |
| BR-009-02 | Each specific CLI skill file must document every allowed parameter variant for each operation. |
| BR-009-03 | A user with only the skill file must be able to use the tool correctly without consulting any other source. |
| BR-009-04 | Documented formats and variants must match the tool they describe. |
| BR-009-05 | Updates to the tool must be reflected in the skill documentation. |

## 3. Acceptance Criteria

- AC-009-01: Given a specific CLI skill file, when a user reads it, then it lists every JSON format the tool accepts.
- AC-009-02: Given a specific CLI skill file, when a user reads it, then it lists every allowed parameter variant for each operation.
- AC-009-03: Given only the skill file, when a user runs the tool, then they can do so correctly without consulting any other source.
- AC-009-04: Given the tool and its skill file, when they are compared, then the documented formats and variants match the tool.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Tool usage | Users and agents run the tool correctly with only the skill as reference. |
| User support | Fewer errors caused by unknown input formats. |
| Maintenance | Skill updates must track tool changes. |
| Distribution | Self-contained skills travel unchanged through all distribution channels. |
| Quality | Documentation accuracy becomes part of release verification. |

## 5. Changes in Access Restrictions

- No access-restriction change; documentation addition only.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | Every operation's formats and variants can be enumerated and documented. |
| Assumption | Skill files remain small enough to stay readable. |
| Risk | Documentation drifts from the tool, causing wrong usage. |
| Risk | Skill files grow beyond the composition limit and need splitting. |
| Mitigation | Match documentation to the tool at review time; follow composition rules for large files. |

## 7. Request Rate Changes

No request-rate change; documentation is static content.

## 8. Data Size Changes

Skill files grow to include formats and variants. Keep each file under the
composition limit; split into parts if needed.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-009 (Open) |
| Epic | EPIC-009 — Harness-agnostic distribution and self-contained content of Foundry agent skills |
| BA sub-task | BA-ANA-009 |
| SA counterpart | SA-ANA-009 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

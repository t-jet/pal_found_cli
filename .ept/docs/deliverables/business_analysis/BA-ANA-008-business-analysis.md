# Business Analysis — BA-ANA-008

## Add Palantir Foundry Platform and Capability Descriptions to Skills

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-008 |
| **Feature** | FEATURE-008 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

Skill users may not know what Palantir Foundry is or what a specific CLI skill
covers. Adding a brief platform description to the main skill and short capability
descriptions to each specific skill — using text from official Palantir Foundry
web pages — lets users understand the context of each tool without leaving the
skill file. This supports the self-contained-skill goal (FEATURE-009).

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-008-01 | The main skill must contain a brief description of the Palantir Foundry platform. |
| BR-008-02 | Each specific CLI skill must contain a brief description of the Foundry capability its tool covers. |
| BR-008-03 | Description text must be sourced from official Palantir Foundry web pages. |
| BR-008-04 | Descriptions must be brief and understandable by a non-expert user. |
| BR-008-05 | Descriptions must be consistent with the platform and capability facts used across all skills. |

## 3. Acceptance Criteria

- AC-008-01: Given the main skill, when a user opens it, then it contains a brief description of the Palantir Foundry platform.
- AC-008-02: Given any specific CLI skill, when a user opens it, then it contains a brief description of the Foundry capability the tool covers.
- AC-008-03: Given a capability description, when it is reviewed, then its text traces to an official Palantir Foundry web page.
- AC-008-04: Given all skill descriptions, when they are compared, then no two skills describe the same capability with conflicting facts.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| User onboarding | Users understand what Foundry is and what each tool does before using it. |
| Skill readability | Each skill becomes self-explanatory. |
| Maintenance | Capability descriptions must be kept in sync with official sources. |
| Distribution | Descriptions travel with the skills in every distribution channel. |
| Support | Fewer basic questions about what a tool is for. |

## 5. Changes in Access Restrictions

- No access-restriction change; content addition only.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | Official Palantir Foundry web pages provide suitable description text. |
| Assumption | Descriptions can be quoted or paraphrased within licensing constraints. |
| Risk | Official descriptions change after being copied into skills. |
| Risk | Descriptions drift from the actual capability covered by a CLI skill. |
| Mitigation | Cite the source page in the skill; review descriptions when official pages change. |

## 7. Request Rate Changes

No request-rate change; skill content is static markdown loaded locally.

## 8. Data Size Changes

Descriptions add a small amount of text to each skill file. Negligible size increase.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-008 (Open) |
| Epic | EPIC-009 — Harness-agnostic distribution and self-contained content of Foundry agent skills |
| BA sub-task | BA-ANA-008 |
| SA counterpart | SA-ANA-008 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

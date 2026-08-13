# Business Design — BA-DES-009

## Add Palantir Foundry Platform and Capability Descriptions to Skills

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-009 |
| **Feature** | FEATURE-008 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-008, SA-ANA-008 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines the content structure for platform and capability
descriptions inside the skill files. The main skill (`pal-found` general
knowledge skill) carries a brief description of the Palantir Foundry
platform; each specific `pal-found-*` CLI skill carries a brief description
of the Foundry capability its tool covers. All description text is sourced
from official Palantir Foundry web pages so facts stay consistent.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-009-01 | The main skill must contain a brief description of the Palantir Foundry platform. |
| BR-D-009-02 | Each specific CLI skill must contain a brief description of the Foundry capability its tool covers. |
| BR-D-009-03 | Description text must be sourced from official Palantir Foundry web pages. |
| BR-D-009-04 | Descriptions must be brief and understandable by a non-expert user. |
| BR-D-009-05 | Descriptions must be consistent: no two skills may describe the same capability with conflicting facts. |
| BR-D-009-06 | Each description must record its source page so the text can be re-checked when official pages change. |

## 3. Logical Flow (business terms)

1. A content author selects the official Palantir Foundry page for the
  platform and for each capability covered by a CLI skill.
2. The author drafts a brief description per skill from the source page,
  recording the source reference.
3. The main skill gains the platform description; each specific skill gains
  its capability description in a standard content section.
4. A consistency review compares all descriptions for conflicting facts and
  checks brevity and non-expert readability.
5. Descriptions ship with the skills in every distribution channel
  (FEATURE-006, FEATURE-007).

## 4. UI/UX (abstract)

The change is content-level. Abstract user experience:

- A user opening the main skill reads a short statement of what Palantir
  Foundry is, in plain language.
- A user opening any specific skill reads a short statement of what the
  covered capability does and how the tool relates to it.
- A user can find the source page reference next to each description to
  verify or extend their understanding.
- Error experience: none specific; the content is static and loaded locally
  with the skill.

## 5. API Specification (abstract)

No application interfaces change. The design defines content rules:

- A standard content section in each skill file for the capability
  description, with a source-reference field.
- A platform description block in the main skill with a source-reference
  field.
- A review procedure that compares descriptions against each other and
  against the official source pages.

## 6. Data Structures (business terms)

- Platform description record: text, source page reference, review date.
- Capability description record: skill name, capability name, text, source
  page reference, review date.
- Review record: list of skills reviewed, conflicting-fact findings,
  resolution, date.

## 7. Acceptance Criteria

- AC-D-009-01: Given the main skill, when a user opens it, then it contains
  a brief description of the Palantir Foundry platform.
- AC-D-009-02: Given any specific CLI skill, when a user opens it, then it
  contains a brief description of the Foundry capability the tool covers.
- AC-D-009-03: Given a capability description, when it is reviewed, then its
  text traces to an official Palantir Foundry web page.
- AC-D-009-04: Given all skill descriptions, when they are compared, then no
  two skills describe the same capability with conflicting facts.
- AC-D-009-05: Given the platform description, when it is checked, then it
  is brief and understandable by a non-expert.

## 8. Migration Procedure

1. Compile the list of official source pages: one platform page and one
  page per covered capability.
2. Draft the platform description and the capability descriptions with
  source references; keep each to a short paragraph.
3. Add the standard content section to the main skill and to each specific
  skill.
4. Run the consistency review (AC-D-009-03..05) and fix any conflicting or
  stale text.
5. Ship the updated skills through the standard distribution paths.
6. Record the review date and source references so re-checks happen when
  official pages change.
7. Rollback: descriptions are additive content; reverting means restoring
  the prior skill files from the repository history.

## 9. Developer Story Scope

Two stories: (1) platform description for the main skill with source
references; (2) capability descriptions for every specific skill with a
consistency review.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-008 |
| Epic | EPIC-009 |
| BA design sub-task | BA-DES-009 |
| SA counterpart | SA-DES-008 |
| Analysis | BA-ANA-008, SA-ANA-008 (Closed, PO-approved) |
| Naming decisions | ND-010-04 (QUESTION-075, Closed) |

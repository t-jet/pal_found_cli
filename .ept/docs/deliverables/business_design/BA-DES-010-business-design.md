# Business Design — BA-DES-010

## Document All JSON Formats and Parameter Variants in Each Skill File

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-010 |
| **Feature** | FEATURE-009 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-009, SA-ANA-009 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines the content structure that makes every specific
`pal-found-*` CLI skill self-contained: each skill file fully documents
every JSON format the tool accepts and every allowed parameter variant for
each operation. A user with only the skill file can use the tool correctly
without consulting any other source. Skill files stay within the
composition limit; large skills split into parts.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-010-01 | Each specific CLI skill file must document every JSON format the tool accepts as input. |
| BR-D-010-02 | Each specific CLI skill file must document every allowed parameter variant for each operation. |
| BR-D-010-03 | A user with only the skill file must be able to use the tool correctly without consulting any other source. |
| BR-D-010-04 | Documented formats and variants must match the tool they describe. |
| BR-D-010-05 | Updates to the tool must be reflected in the skill documentation. |
| BR-D-010-06 | Skill files must comply with the composition rules (no single file over the limit; parts split when needed). |

## 3. Logical Flow (business terms)

1. For each specific skill, a content author enumerates every operation the
  tool supports.
2. For each operation, the author records the input JSON format(s) and every
  allowed parameter variant, verified against the tool itself.
3. The author writes the documentation into the skill file under a standard
  content section, keeping the file within the composition limit.
4. A match check compares the documentation with the tool so the two cannot
  drift.
5. When the tool changes, the skill documentation is updated in the same
  change cycle.

## 4. UI/UX (abstract)

The change is content-level. Abstract user experience:

- A user reads a skill file and finds, per operation, the input format and
  the allowed parameter variants, with examples.
- A user or agent constructs a correct command using only the skill file.
- A user verifying the documentation compares it with the tool behaviour
  and finds them consistent.
- Error experience: the documentation reduces format-related errors because
  all variants are listed; no external look-up is required.

## 5. API Specification (abstract)

No application interfaces change. The design defines content rules for
documentation:

- A standard documentation section per operation: purpose, input format
  specification, parameter variant list, example.
- A match procedure that verifies the documentation against the tool.
- Composition rules: file length limits with part splitting for large
  skills.

## 6. Data Structures (business terms)

- Operation record: operation name, purpose, input format specification,
  parameter variant list, example.
- Skill documentation record: skill name, list of operation records, match
  check result, review date.
- Match record: comparison between documented variants and tool behaviour,
  discrepancies, resolution, date.

## 7. Acceptance Criteria

- AC-D-010-01: Given a specific CLI skill file, when a user reads it, then
  it lists every JSON format the tool accepts.
- AC-D-010-02: Given a specific CLI skill file, when a user reads it, then
  it lists every allowed parameter variant for each operation.
- AC-D-010-03: Given only the skill file, when a user runs the tool, then
  they can do so correctly without consulting any other source.
- AC-D-010-04: Given the tool and its skill file, when they are compared,
  then the documented formats and variants match the tool.
- AC-D-010-05: Given any skill file, when its length is checked, then it
  stays within the composition limit (parts split if needed).

## 8. Migration Procedure

1. Prioritize the skill files by operation count; start with the largest
  skills where drift risk is highest.
2. For each skill, enumerate operations and build the operation records,
  verifying each format and variant against the tool.
3. Write the standard documentation section into the skill file; if the
  file exceeds the composition limit, split it into parts with the main
  file carrying the references.
4. Run the match check (AC-D-010-04) per skill and fix discrepancies.
5. Update the distribution documentation and any cross-references.
6. Make skill documentation part of tool change cycles so formats stay in
  step.
7. Rollback: documentation changes are reverted from the repository history
  if a match check fails after a change.

## 9. Developer Story Scope

One story covers the documentation structure, per-skill enumeration,
match checks, and composition-compliant splitting.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-009 |
| Epic | EPIC-009 |
| BA design sub-task | BA-DES-010 |
| SA counterpart | SA-DES-009 |
| Analysis | BA-ANA-009, SA-ANA-009 (Closed, PO-approved) |
| Naming decisions | ND-010-04 (QUESTION-075, Closed) |

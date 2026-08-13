# Architecture Analysis — SA-ANA-009

## Document All JSON Formats and Parameter Variants in Each Skill File

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-009 |
| **Feature** | FEATURE-009 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| 18 namespace skill files | partial usage guidance | every JSON input format and parameter variant documented |
| CLI implementation | source of truth for formats | unchanged; documentation matches it |
| Skill file size | within limits | may grow; composition rule applied when needed |
| Users and agents | may need external sources | self-contained skill usage (BR-009-03) |

The authoritative source for formats and variants is the CLI itself: the
argparse definitions for parameter variants and the JSON body handling for input
formats. Documentation is derived from and verified against that source.

## 2. Architecture Approach

Each namespace skill becomes self-contained for usage: it lists every JSON
format the tool accepts as input (BR-009-01) and every allowed parameter variant
for each operation (BR-009-02). A user with only the skill file can run the tool
correctly (BR-009-03).

Content structure inside each skill:

- A formats section: one entry per JSON-bearing option, with the accepted
  schema and an example.
- A parameters section: one entry per operation, listing required and optional
  parameters, allowed values, and variants such as flags, short forms, and
  positional alternatives.

Accuracy is enforced by matching the documented formats and variants to the CLI
parser at review time (BR-009-04, AC-009-04). Skill files that grow past the
300-line composition limit split into parts under a subdirectory, with the main
skill file referencing the parts, so each file stays readable.

## 3. Technology Stack

- Markdown documentation inside the skill files
- CLI source (argparse and JSON handling) as the verification reference
- No code, no dependencies, no build step

## 4. General Implementation Approach

1. For each of the 18 namespace skills, enumerate the operations and their
   parameters from the CLI source.
2. Document each JSON input format with schema and example (AC-009-01).
3. Document each allowed parameter variant per operation (AC-009-02).
4. Verify that a user with only the skill file can run the tool (AC-009-03).
5. Cross-check documented formats and variants against the tool (AC-009-04).
6. Split any skill file that exceeds the composition limit.

## 5. General Migration Approach

- Phase 1 (audit): extract formats and variants from the CLI source per skill.
- Phase 2 (document): write the sections into each skill file.
- Phase 3 (verify): run a usage-only check and a tool-conformance check.
- Phase 4 (maintain): update skill documentation on every tool change
  (BR-009-05).

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Doc drift | Documentation diverges from the tool | Tool-conformance review (AC-009-04); update on tool changes |
| Wrong usage | User follows stale formats | Self-contained accuracy enforced at review |
| File size | Skill grows past the composition limit | Split into parts with references from the main file |
| Enumeration gaps | A variant left undocumented | Audit derived from parser source, not from memory |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-009 (Analysis) |
| Epic | EPIC-009 |
| BA sub-task | BA-ANA-009 |
| SA sub-task | SA-ANA-009 |
| BA deliverable | BA-ANA-009-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |

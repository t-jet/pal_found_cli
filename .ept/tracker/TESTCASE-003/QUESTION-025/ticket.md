---
id: QUESTION-025
type: question
title: TESTCASE-003 review request — approve QA test-case specification for foundry-datasets (33 ops)
status: Closed
addressed_to: tech-lead
created: 2026-07-21
updated: 2026-07-22
priority: Critical
assignee: tech-lead
reporter: qa-engineer
time_spent_hours: 0.5
---

# QUESTION-025: TESTCASE-003 review request — approve QA test-case specification for foundry-datasets (33 ops)

## Description

# Review Request — TESTCASE-003 Test-Case Specification

## What is being requested

Approval of the QA test-case specification for the `foundry-datasets` skill
(DEV-STORY-005). This approval is required to satisfy TESTCASE-003 In-Progress → Resolved
DoD criterion #9 ("Test cases reviewed and approved") and the QA-engineer
`<Test_Case_Design>` rule which mandates review by the Tech Lead or Architect before
test execution begins.

## What to review

1. **TESTCASE-003 body** — Acceptance Criteria AC-TC-1 through AC-TC-9 (33 operations,
   exit-code taxonomy, ADR-007 access control, retry/config/output/logging, phantom-test
   verification, AC coverage, review/approval, discrepancy tracking).
2. **TESTCASE-003 comment `20260721-233807-qa-engineer`** — consolidated test-case
   specification with the TC1.1–TC13.4 scenario matrix and AC↔TC traceability table.
3. **Deliverable reference file** (for per-scenario detail):
   `.ept/docs/deliverables/qa/TESTCASE-003-test-cases.md` — TC1.1–TC13.4 rows with
   Scenario · Input · Expected · Pass Criteria columns, and the D-1..D-9 discrepancy
   table.

## Context already verified

- Implementation under test exists and is testable:
  `.claude/skills/foundry_datasets_cli.py` (33 operations across 5 clients).
- Unit suite (UNITTEST-003) passes: 96 tests at 91.91% line coverage.
- Parser smoke test passes; `build_parser()` succeeds.
- All 9 design-phase discrepancies (D-1..D-9) are closed as QUESTION-015..QUESTION-023
  (all terminal status). Architect resolved D-1 (33 canonical operations per the
  QUESTION-015 ruling) and D-8 (AccessControlError envelope). See comment
  `20260721-233807-qa-engineer` for the full D-1..D-9 status matrix.

## Decision needed

Approve as-is, approve with requested revisions, or reject. When closing this QUESTION,
please explicitly state one of:
- "**APPROVED** — TESTCASE-003 ready for Resolved transition" (and note any caveats), or
- "**REVISIONS REQUIRED**" with a list, or
- "**REJECTED**" with rationale.

If approved, qa-engineer will transition TESTCASE-003 In Progress → Resolved.

## Acceptance Criteria

The Tech Lead review must verify the following before issuing an APPROVED / REVISIONS REQUIRED / REJECTED decision:

- [ ] **AC-1 — 33 operations reflected.** TESTCASE-003 body ACs (AC-TC-1 … AC-TC-9) reference real implemented operations: all 33 dataset operations (11 Dataset + 5 Branch + 5 File + 6 Transaction + 6 View) per the architect ruling in QUESTION-015 (D-1 resolved: 33 canonical). Implementation at `.claude/skills/foundry_datasets_cli.py`.
- [ ] **AC-2 — Consolidated spec comment complete.** TESTCASE-003 comment `20260721-233807-qa-engineer` covers all scenarios (TC1.1–TC13.4) and the AC↔TC traceability matrix, with exit codes mapped to the ADR-001 taxonomy for every scenario.
- [ ] **AC-3 — Deliverable file present and referenced.** `.ept/docs/deliverables/qa/TESTCASE-003-test-cases.md` exists and is the source of per-scenario detail (Scenario · Input · Expected · Pass Criteria columns + D-1..D-9 discrepancy table). Path was verified at write time.
- [ ] **AC-4 — Discrepancies closed.** All D-1..D-9 design-phase discrepancies are resolved and recorded as terminal QUESTION-015..QUESTION-023 (Closed/Resolved), with the resolution documented in comment `20260721-233807-qa-engineer`.
- [ ] **AC-5 — Decision explicit.** Reviewer states one of: APPROVED, REVISIONS REQUIRED, or REJECTED, so qa-engineer can act on it deterministically.

## Research Done

- [x] Read TESTCASE-003 ticket body, comment `20260721-233807-qa-engineer`, and the 33-op implementation file.
- [x] Read UNITTEST-003 results (96 tests passing at 91.91% coverage) confirming the implementation is testable, not phantom.
- [x] Studied related documentation via `.ept/docs/document_index.md`: SRS-001, ADR-001 (exit codes), ADR-005 (log format), ADR-007 (READONLY independence).
- [x] Reviewed the full question-type workflow (`get type-info question`): New→Open and Open→In Progress DoD criteria reviewed; this QUESTION is a duplicate-free clarification/approval request (no open QUESTION-XXX children under QUESTION-025).
- [x] Reviewed parent (TESTCASE-003) comments, links, and the QUESTION-015–023 resolution set.
- [x] Verified the deliverable file path `.ept/docs/deliverables/qa/TESTCASE-003-test-cases.md` exists on disk.
- [x] Addressee identified: `tech-lead` (per the TESTCASE design mandate that test cases be reviewed by Tech Lead or Architect; tech-lead is the DEV-STORY/TESTCASE reviewer of record).

## Related Documentation

- **SRS-001 — Software Requirements Specification** — `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` (functional/non-functional requirements for the Foundry CLI).
- **ADR-001 — Exit Code Taxonomy** — `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md` (structured exit-code scheme referenced by every scenario's Expected column).
- **ADR-005 — Log Format** — `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md` (NDJSON stderr logging tested in AC-TC logging scenarios).
- **ADR-007 — Operation-Level READONLY Independence** — `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md` (per-operation READONLY flag, basis for AccessControlError scenarios).
- **Workflow SKILL §Phase 4 — QA** — `.ept/skills/workflow/SKILL.md` (TESTCASE/TESTEXEC sub-task role in the DEV-STORY lifecycle, QA sign-off gate).
- **Document index** — `.ept/docs/document_index.md` (master index used for DoD study).

## Notes

- **APPROVED** → qa-engineer transitions TESTCASE-003 from In Progress → Resolved and begins TESTEXEC-003 execution planning.
- **REVISIONS REQUIRED** → qa-engineer applies the requested changes to the test-case deliverable/body and re-requests review (QUESTION-025 → Clarification → Clarified → Resolved cycle if needed, or a new review comment).
- **REJECTED** → qa-engineer opens a new QUESTION to the Architect for design-level arbitration, and TESTCASE-003 is transitioned to Blocked pending resolution.
- **Parent context:** TESTCASE-003 is a child of DEV-STORY-005 (QA phase). This QUESTION blocks TESTCASE-003 via Blocks links (to be confirmed) per workflow rule #5; Q-025 reaching a terminal status restores the parent's prior (In Progress) status.
- **No time reporting on this QUESTION yet** — `time_spent_hours` is not required until the In Progress → Resolved/Canceled transition (Open→In Progress DoD), and will be set at handoff completion.

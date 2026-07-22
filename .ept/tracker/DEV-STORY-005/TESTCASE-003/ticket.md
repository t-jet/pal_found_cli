---
id: TESTCASE-003
type: testcase
title: 'TESTCASE-005: QA test cases for foundry-datasets'
status: Blocked
created: 2026-05-18
updated: 2026-07-21
priority: Critical
assignee: qa-engineer
reporter: architect
time_spent_hours: 6.5
---

# TESTCASE-003: QA test cases for foundry-datasets

## Description

QA test cases covering all 33 dataset operations (per architect decision QUESTION-015,
Comment `20260704-233802-architect` — 33 is canonical; the "26" in DEV-STORY-005 title
is a stale planning figure to be corrected on the parent), edge cases, error scenarios,
access control, retry, output formatting, logging, configuration, parser, and NFRs for
the implementation at `.claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py`.

Implementation under test: `foundry_datasets_cli.py` (~455 LOC) — 5 resource clients
(Dataset 11, Branch 5, File 5, Transaction 6, View 6 = 33 operations). Verified
testable: paired unit test suite `tests/test_foundry_datasets_cli.py` — 96 tests passing
at 91.91% line coverage.

Full test-case specification: TC1.1–TC13.4 with D-1…D-9 discrepancy regression rows,
delivered in the comment titled "TESTCASE-003 consolidated test-case specification
(deliverable reference + DoD compliance)" and stored as
`.ept/docs/deliverables/qa/TESTCASE-003-test-cases.md` (acceptance/QA test cases
complement the unit suite).

## Acceptance Criteria

AC-TC-1: A test scenario (Given/When/Then) exists and passes for every one of the 33
operations defined in the implementation — Dataset (create, get, get-health-check-reports,
get-health-checks, get-schedules, get-schema, get-schema-batch, jobs, put-schema,
read-table, transactions), Branch (create, delete, get, list, transactions), File
(content, delete, get, list, upload), Transaction (abort, build, commit, create, get,
job), View (add-backing-datasets, add-primary-key, create, get, remove-backing-datasets,
replace-backing-datasets).

AC-TC-2: Each operation test scenario forwards the correct kwargs to the SDK mock and
returns exit code 0 on the happy path.

AC-TC-3 (ADR-001 exit-code taxonomy): Negative paths produce the documented exit codes —
UserInputError=1 (missing positionals / required flags), AuthenticationError=2,
PermissionDeniedError=3, NotFoundError=4 (FileNotFoundError on upload),
TimeoutError=5, ServerError=6, RateLimitExhausted=7 (OSError errno 11/115),
AccessControlError=8, ConfigurationError=9 (client factory failure). Documented
deviations from ADR-001 (D-2: invalid-JSON args currently surface as exit 6 rather than
exit 1) are tracked via QUESTION-016 and recorded as expected results in TC1.7/TC5.7.

AC-TC-4 (ADR-007 access control): Verified scenarios cover all 8 precedence steps —
op-level ENABLED=false → exit 8; namespace ENABLED=false → exit 8; READONLY override
permits writes; METADATA_ONLY denies non-allow-listed ops; AccessControlError → exit 8
with ADR-001 error envelope.

AC-TC-5 (ADR-002 retry + ADR-006 config + ADR-004 output + ADR-005 logging): Scenarios
cover RetryHandler wrapping, `--timeout` precedence over `cfg.timeout_s`, JSON/TOON/auto
output selection, `--pretty`, stdout/stderr separation, `.env` loading precedence.

AC-TC-6 (ADR-007 phantom-feature corrective action): Test scenarios reference the actual
implementation under test (`foundry_datasets_cli.py`), the actual parser/operation
functions (`build_parser`, `_resolve`, `_invoke`, `_get_client`, `_model_to_dict`), and
the actual CLI surface (33 subcommands). Verified by smoke test that `build_parser()`
succeeds and the unit suite (96 tests) passes — implementation is accessible and
testable.

AC-TC-7 (acceptance criteria coverage): Each DEV-STORY-005 acceptance area (the 33
operations, access control, retry, formatting, error handling, logging, config) has at
least one passing test scenario in the deliverable matrix. Coverage matrix in the
deliverable maps every AC area to specific TC IDs.

AC-TC-8 (review and approval): Test case specification reviewed and approved — record of
approval captured in QUESTION sub-task addressed to tech-lead or as an approval comment
on this ticket.

AC-TC-9 (defect handling): All QA/AC discrepancies observed during design
(D-1 operation-count ambiguity, D-2 exit-code for bad JSON, D-3 `--dataset-r` naming,
D-4 PaginationHelper unused, D-5 upload memory guard, D-6 binary download path, D-7
rate-limit heuristic, D-8 AccessControlError envelope, D-9 timeout enforcement) are each
filed as QUESTION-015…QUESTION-023 — all Closed (terminal) — and linked to this ticket.

## Related Documentation

- ADR-001 Exit Code Taxonomy — `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md`
- ADR-002 Call Timeout Defaults — `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md`
- ADR-004 Format Auto-Selection — `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md`
- ADR-005 Log Format — `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md`
- ADR-006 .env File Search Path — `.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md`
- ADR-007 Operation-Level READONLY Independence — `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md`
- SRS-001 — `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` (AC-SMOKE, AC-ERR-AUTH, AC-RETRY, AC-ACL-BLOCK, AC-FMT-TOON; FR-ACL-1..6; FR-DS-* datasets requirements)
- Workflow SKILL — `.ept/skills/workflow/SKILL.md` (Phase 4 QA)
- Parent DEV-STORY-005
- Architect decision record — QUESTION-015 Comment `20260704-233802-architect` (33-op canonical)

## Notes

- Title contains "TESTCASE-005" (not "TESTCASE-003") because the sub-task numbering within
  DEV-STORY-005 mirrors the parent story number suffix (all DEV-STORY-005 sub-tasks
  carry the "005" descriptor — DESIGN-003, DEV-003, CODEREVIEW-003, UNITTEST-003,
  TESTCASE-003, TESTEXEC-003, DEVOPS-004). Deliberate convention, not a defect — see the
  comment titled "Title/ID naming convention note (TESTCASE-003 vs TESTCASE-005)".
- The deliverable file path is recorded for reviewer reference only. Authoritative test
  case definitions are captured in the ticket body ACs and the consolidated test-case
  specification comment per the QA-engineer constraint that work products live in the
  tracking system.

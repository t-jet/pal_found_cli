---
id: TESTEXEC-014
type: testexec
title: 'TESTEXEC-014: QA execution for foundry-orchestration CLI'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: qa-engineer
reporter: architect
estimated_hours: 8
time_spent_hours: 8
---

# TESTEXEC-014: TESTEXEC-014: QA execution for foundry-orchestration CLI

## Description

# TESTEXEC-014: QA execution for foundry-orchestration CLI

## Description

Execute the TESTCASE-014 test cases against the foundry-orchestration CLI (DEV-014) after development closes. Run targeted orchestration suites plus the full regression suite with coverage, and log results per sibling TESTEXEC conventions (e.g. TESTEXEC-013). Create BUG-SUB-014.x sub-tasks for any defects found.

## Acceptance Criteria

- [ ] All TESTCASE-014 cases executed and results logged as comments on this ticket.
- [ ] Targeted foundry-orchestration tests pass (mock-based; no live Foundry).
- [ ] Full regression suite passes with coverage meeting the pyproject.toml threshold (80% branch).
- [ ] Static analysis, security scan, compile, and packaging gates green.
- [ ] Any defects triaged: BUG-SUB-014.x created and linked if found; none left open at completion.
- [ ] Execution evidence documented in a TESTEXEC-014 results log (deliverable or comments).

## Related Documentation

- .ept/docs/deliverables/qa/TESTCASE-014-test-cases.md
- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- .ept/docs/deliverables/qa/TESTEXEC-013-execution-log.md (sibling reference)

## Notes

Runs after DEV-014 and CODEREVIEW-014 close. If defects found, create BUG-SUB sub-tasks under DEV-STORY-014.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

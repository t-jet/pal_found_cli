---
id: BUG-SUB-013
type: bug_subtask
title: 'BUG-SUB: trailing whitespace on migration-touched project files fails git diff --check
  (rename docs sweep gate)'
status: Closed
created: 2026-08-14
updated: 2026-08-14
priority: High
assignee: qa-engineer
reporter: qa-engineer
time_spent_hours: 1.0
---

# BUG-SUB-013: BUG-SUB: trailing whitespace on migration-touched project files fails git diff --check (rename docs sweep gate)

## Description

# BUG-SUB: trailing whitespace on migration-touched project files fails git diff --check (rename docs sweep gate)

## Severity
High - hygiene defect in migration-touched project files that must be cleaned before the docs-sweep gate passes (architect disposition QUESTION-130, comment 20260814-145706-architect).

## Affected Version
HEAD 5746815 (docs: complete rename migration verification), working tree state 2026-08-14.

## Steps to Reproduce
1. From repository root run: git diff --check -- . ':(exclude).ept/tracker/**'
2. Observed exit code: 2.
3. Trailing whitespace flagged on added lines of the following project-owned files (9 currently; QUESTION-130 listed 10 including .ept/self-improvement/ticket-helper.md which is currently clean after earlier 2026-08-14 edits):
- AGENTS.md
- .github/agents/ba.agent.md
- .github/agents/crawl4ai.agent.md
- .github/agents/devops-engineer.agent.md
- .github/agents/python-developer.agent.md
- .github/agents/qa-engineer.agent.md
- .github/agents/tech-lead.agent.md
- .ept/agents/workflow-mgr.md
- .ept/skills/workflow/SKILL.md
(.ept/tracker/** excluded as out of scope per QUESTION-130.)

## Expected Behavior
git diff --check with .ept/tracker excluded exits 0 after the required trivial fix: strip trailing whitespace from the 10 project-owned migration-touched files (RNG-11 expected result: PASS).

## Actual Behavior
git diff --check exits 2; trailing whitespace remains on added lines in the project-owned files listed above. RNG-11 verdict: FAIL (cleanup pending). src/, tests/, .agents/skills/, .ept/docs/ remain whitespace-clean.

## Test Execution Reference
TESTEXEC-037 scenario RNG-11 (TESTCASE-037, comment 20260814-172912-qa-engineer); evidence in TESTEXEC-037 results comment.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

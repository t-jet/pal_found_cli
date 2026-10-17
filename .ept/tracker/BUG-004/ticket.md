---
id: BUG-004
type: bug
title: Skills validation fails in standalone checkout without CLI source
status: Closed
affected_version: c1f2a3b
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# Skills validation fails in standalone checkout without CLI source

## Reproduction

Push skills commit c1f2a3b to GitHub main and inspect Validate skills run 37426786404 on Ubuntu with Python 3.11.16. Ruff checks pass. Pytest reports 32 passed and 1 failed. The documented examples parser test raises ModuleNotFoundError: No module named pal_found_cli.

## Expected

GitHub validation checks documented command examples in a standalone skills checkout and passes with available CLI parser code.

## Actual

The test assumes a sibling pal_found_cli_tool source tree that is absent in a standalone GitHub checkout.

## Acceptance criteria

- CI establishes a reproducible compatible CLI parser source or test dependency without changing user installation guidance.
- Validator passes in a clean standalone checkout and continues checking all documented examples.
- Independent review and QA verify the fix; exact run URL and commit recorded.

## Related documentation

- .ept/docs/document_index.md
- TASK-005; FEATURE-013

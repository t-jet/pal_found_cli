---
id: BUG-SUB-011
type: bug_subtask
title: Honor global FOUNDRY_AGENTIC_CLI_ENABLED=false before client creation
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: python-developer
time_spent_hours: 1
---

# BUG-SUB-011: Honor global FOUNDRY_AGENTIC_CLI_ENABLED=false before client creation

## Description

Fix the global access-control precedence defect found by TESTEXEC-012. Real `ConfigLoader` plus `AccessControlGuard` ignores `FOUNDRY_AGENTIC_CLI_ENABLED=false`, so both Language Models inference writes remain permitted. Namespace and exact-operation enablement controls already behave correctly.

## Acceptance Criteria

- Global `FOUNDRY_AGENTIC_CLI_ENABLED=false` blocks every operation before client creation with `AccessControlError` and CLI exit 8.
- `anthropic_model.messages` and `open_ai_model.embeddings` are both denied under global false; actual client calls remain zero.
- Namespace and exact-operation `ENABLED=false` behavior and precedence remain unchanged.
- Add regression tests using real `ConfigLoader` and `AccessControlGuard` for both Language Models operations and representative operations from other namespaces.
- Targeted and full regression, Ruff, mypy, Bandit, coverage, packaging, and privacy gates pass.

## Reproduction

Set `FOUNDRY_AGENTIC_CLI_ENABLED=false`, load configuration through `ConfigLoader`, and call `AccessControlGuard` for `anthropic_model.messages` and `open_ai_model.embeddings`. Expected: `AccessControlError` and CLI exit 8 before client creation. Actual: both checks report `blocked=False`.

## Related Documentation

- DEV-STORY-012
- TESTEXEC-012
- `.ept/docs/deliverables/qa/TESTEXEC-012-language-models-results.md`

## Notes

High functional/security defect isolated to global enablement precedence. No open question.

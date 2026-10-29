---
id: BUG-018
type: bug
title: Ontology CLI returns exit 6 for SDK permission denial while error envelope says 3
status: Closed
affected_version: pal_found_cli_tool-bfdee738-dirty
created: 2026-10-13
updated: 2026-10-14
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
component: ontologies
---

# BUG-018: Ontology CLI returns exit 6 for SDK permission denial while error envelope says 3

## Description

# Defect
Ontology CLI main discards ErrorSerializer.serialize return code in generic exception handler. SDK PermissionDeniedError from API 403 is serialized with exit_code 3, but process main returns EXIT_SERVER_ERROR 6.

# Reproduction
Windows PowerShell, Python environment with foundry_sdk, current pal_found_cli_tool worktree HEAD bfdee738. Run `python -m pytest .ept/tmp/ontology_independent_qa.py::test_sdk_permission_denial_returns_exit_3 -q --basetemp=.ept/tmp/ontology_independent_pytest`. Test mocks retry execution to raise SDK PermissionDeniedError after CLI guard passes. No credentials or Foundry call.

# Expected
Per ADR-001 and ErrorSerializer classification, stdout error envelope exit_code 3 and process exit code 3 for SDK HTTP 403. Policy guard denial remains exit 8.

# Actual
Serializer prints envelope `exit_code: 3`, `http_status: 403`, `exception_type: PermissionDeniedError`; `main()` returns 6. Independent run: 25 pass, 2 fail; one other failure is a test-double issue being corrected.

# Acceptance criteria
Return serializer classified code for SDK failures, with regression test for 403 and unrelated 500. Preserve policy guard exit 8. Independent QA verifies process and envelope codes match.

# Test reference
TASK-006 QA design comment 20261013-112831-@qa-engineer and Tech Lead approval 20261013-113103-@tech-lead; BUG-011 independent QA execution.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

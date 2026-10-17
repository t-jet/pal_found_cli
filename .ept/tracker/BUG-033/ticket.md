---
id: BUG-033
type: bug
title: Windows counter-file replace causes concurrent tracker read failure
status: Closed
affected_version: tracker-local-20261014
created: 2026-10-14
updated: 2026-10-14
priority: High
resolution: Done
assignee: project-manager
reporter: qa-engineer
---

# BUG-033: Windows counter-file replace causes concurrent tracker read failure

## Description

# Reproduction

From Windows PowerShell in the repository, run `python -m pytest .ept/tools/tracker/tests -q --basetemp=.ept/tmp/bug032_full_suite`. During BUG-032 independent verification, 436 tests passed and `test_parallel_ticket_and_link_creates_preserve_both_counters` failed. A link-create child process called `increment_link_counter`, then `load_id_counters`; opening `.id-counters.yaml` raised `PermissionError: [Errno 13] Permission denied` during concurrent atomic replacement. The CLI process exited 1. Fixture is isolated under `.ept/tmp`; no production tracker data used.

# Expected

Concurrent ticket and link creates both succeed. Counter readers tolerate brief Windows replace sharing conflicts; no FileOperationError escapes.

# Actual

`tracker.exceptions.FileOperationError: Failed to load ID counters: [Errno 13] Permission denied` from `tracker/index.py` `load_id_counters`; mixed subprocess exit 1, pytest exit 1. Intermittent: focused link suite 18/18 and prior independent CLI probe passed.

# Reference

BUG-032 QA execution comment 20261014-171207-@qa-engineer and approved design 20261014-170939-@tech-lead. Follow-up broad gate exposed residual race. High severity because tracker writes can fail under concurrent operation.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

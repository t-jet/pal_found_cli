# TESTEXEC-007 - Foundry Filesystem CLI test execution log

## Scope

This log records QA execution for DEV-STORY-006, the `foundry-filesystem` CLI covering 31 filesystem API v2 operations.

Related test design: `TESTCASE-007-test-cases.md`.

## Environment

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| OS | Windows-10-10.0.26200-SP0 |
| Python | 3.11.9 |
| Commit | `075a2be` |
| Test data | Mocked Foundry SDK clients and local CLI parser/dispatch fixtures |
| Live credentials | Not required |

## Execution summary

| Run | Command | Result |
|---|---|---|
| Targeted filesystem suite | `python -m pytest tests/test_foundry_filesystem_cli.py tests/test_filesystem_console_wrapper.py -q --cov=src/foundry_cli --cov-report=term-missing` | 115 tests passed. Command exit code was 1 because repo-wide coverage was measured from the targeted subset only: 36.51% below the configured 80% gate. No filesystem test failed. |
| Full regression suite | `python -m pytest -q --cov=src/foundry_cli --cov-report=term-missing` | 586 tests passed. Coverage gate passed at 81.96%. |

## Test case results

| Test case range | Evidence |
|---|---|
| FS-TC-001 to FS-TC-009 | Covered by parser, catalog, dispatch, nested `Resource.Role`, and pagination catalog tests in `tests/test_foundry_filesystem_cli.py`. |
| FS-TC-010 to FS-TC-011 | Covered by pagination aggregation and stderr metadata tests in `tests/test_foundry_filesystem_cli.py`. |
| FS-TC-012 to FS-TC-016 | Covered by ACL, retry, and error path tests using mocked SDK/config dependencies. |
| FS-TC-017 to FS-TC-020 | Covered by JSON, TOON, and auto-format output formatter tests. |
| FS-TC-021 to FS-TC-031 | Covered by model conversion, missing command, exit code mapping, retry scope, B3 invocation scope, and console entry point tests. |
| FS-TC-032 to FS-TC-034 | Partially covered by packaged import and console wrapper tests; editable install console help is represented by entry point metadata and wrapper behavior, not a separate installed-environment smoke run. |

## Defects

No test execution defects were found.

## Notes

The targeted command proved the filesystem-specific assertions. Its non-zero exit came from applying the repository coverage threshold to a subset run. The full suite is the authoritative coverage gate for this execution.

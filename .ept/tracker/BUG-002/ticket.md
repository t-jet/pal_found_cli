---
id: BUG-002
type: bug
title: Test TC-E2E-001 missing directory setup — FileNotFoundError on chdir
status: Closed
affected_version: 0.1.0-dev
created: 2026-05-19
updated: 2026-05-19
priority: Low
assignee: qa-engineer
reporter: qa-engineer
---

# BUG-002: Test TC-E2E-001 missing directory setup — FileNotFoundError on chdir

## Description

During TESTEXEC-002 test execution, TC-E2E-001 failed with FileNotFoundError.

**Root Cause:** The test creates `git_root / '.git'` and `git_root / '.env'` but calls `monkeypatch.chdir(git_root / 'src')` without first creating the `src` directory.

**Evidence:**
```
FileNotFoundError: [WinError 2] The system cannot find the file specified: 'T:\\tmp\\pytest-of-pds\\pytest-1\\test_TC_E2E_001_git_root_to_cl0\\project\\src'
```

**Fix Required:** Add `(git_root / 'src').mkdir()` before the `monkeypatch.chdir(git_root / 'src')` call in `test_exec_common_components.py`.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

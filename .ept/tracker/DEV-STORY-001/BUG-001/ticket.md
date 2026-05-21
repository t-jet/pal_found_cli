---
id: BUG-001
type: bug
title: ConfigLoader CWD fallback broken when no git root — TC-CL-INT-004 fails
status: Rejected
affected_version: local-dev
created: 2026-05-19
updated: 2026-05-20
priority: High
assignee: developer
reporter: qa-engineer
---

# BUG-001: ConfigLoader CWD fallback broken when no git root — TC-CL-INT-004 fails

## Description

During TESTEXEC-002 test execution, TC-CL-INT-004 (ConfigLoader CWD fallback) failed.

**Root Cause:** In `config_loader.py`, the CWD `.env` fallback is nested INSIDE the `if git_root:` block (line ~83). When no git root is found (`git_root` is None), the code skips directly to Order 3 (env vars only), and never attempts to load `.env` from CWD.

**Expected:** When no git root exists, ConfigLoader should fall back to loading `.env` from CWD.

**Actual:** `loaded_file` remains None when no git root is found, even if `.env` exists in CWD.

**Evidence:**
```
AssertionError: assert None == 'T:\\tmp\\pytest-of-pds\\pytest-1\\test_TC_CL_INT_004_cwd_fallbac0\\no_git\\.env'
```

**Fix Required:** Move the CWD `.env` fallback outside the `if git_root:` block so it executes when git_root is None.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

Subject: Corrections applied — D1 and D2 resolved
Created: 2026-07-27T13:12:46
Updated: 2026-07-27T13:12:46
---
## Corrections for CODEREVIEW-005

Both defects from the 2026-07-27 architect review have been implemented and verified. Full suite run: **315 passed** (no regressions).

---

### D1 (HIGH) — Missing integration test: retry within tracing scope

**Status:** Resolved.

Per DESIGN-005 section 7 (test matrix row: "Integration — Retry within tracing scope — Every attempt carries same B3 context") and TESTCASE-005.

**Test added:** `tests/test_tracing_provider.py`, function `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` at **line 172**.

The test does exactly what the finding required:
1. Builds a `RetryHandler` (max_retries=2, jitter=False, timeout_s=None) and a `TracingProvider(enable=True)` against a mocked `foundry_sdk` module exposing real `ContextVar`s (`TRACE_ID_VAR`, `SPAN_ID_VAR`, `SAMPLED_VAR`).
2. Wraps a coroutine (`transient_then_ok`) that raises `requests.RequestException` on the first attempt, then returns `"ok"` on the second.
3. Records the value of all three SDK context vars on **every** attempt.
4. Asserts the observed context tuple on attempt 2 equals the tuple on attempt 1 — i.e., the same B3 context is carried across retry attempts (trace_id, span_id, and sampled are identical).
5. After `execute_traced()` returns, asserts all three SDK vars are restored to their default (None).

This directly exercises `RetryHandler.execute_traced()` at `src/foundry_cli/common/retry.py` lines 505-514 (`with tracing.scope(supplied): return await self.execute(...)`). The implementation was already correct; only the test was absent.

---

### D2 (MEDIUM) — `download_dir` permissions are umask-dependent

**Status:** Resolved.

**Source fix:** `src/foundry_cli/common/binary_download_handler.py`, **line 113** — added `self._restrict_directory(download_dir)` immediately after `download_dir.mkdir(mode=0o700)` (now line 112). `_restrict_directory` invokes `os.chmod(path, 0o700)` on POSIX (no-op on Windows), bypassing the kernel umask so the per-download UUID directory is owner-only regardless of process umask. This makes protection consistent with the root directory, which already received the same call at line 102.

**Test added:** `tests/test_binary_download.py`, function `test_download_dir_permissions_are_umask_independent_on_posix` at **line 227**. It records every `os.chmod` call, performs a real download, then asserts that the UUID directory (parent == download root, name != root) received an explicit `chmod` with mode `0o700` and that the on-disk mode matches `0o700`.

---

### OWASP self-review

- D2 closes an access-control gap (CWE-732: Incorrectly Configured File Permissions). The download directory now has the same owner-only guarantee as the root.
- D1 adds no product change; it only adds coverage for the existing trace-context isolation design. No new attack surface.
- No hardcoded credentials, tokens, or secrets introduced.

### Test results

- Targeted: `tests/test_tracing_provider.py tests/test_binary_download.py` -> 31 passed.
- Full suite: `pytest -q` -> 315 passed.

Ready for re-review.

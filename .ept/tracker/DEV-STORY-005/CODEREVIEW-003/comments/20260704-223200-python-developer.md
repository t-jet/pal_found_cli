Subject: Correction Complete — All 7 Findings Fixed + Bonus Parser Bug
Created: 2026-07-04T22:32:00
Updated: 2026-07-04T22:32:00
---
## Correction — All Findings Addressed

Acknowledging each finding from the 2026-05-20 review and describing the fix:

### CRITICAL-1: `_invoke_async` missing `timeout` — FIXED
Removed `_invoke_async` entirely. `main()` now resolves `timeout = args.timeout or cfg.timeout_s` and passes it positionally to `_invoke(resource, operation, client, args, timeout)`. Verified by `test_main_resolves_timeout_from_cli_flag` and `test_main_falls_back_to_cfg_timeout`.

### CRITICAL-2: `async` wrapped in `run_in_executor` — FIXED
`_invoke` is now awaited directly inside `RetryHandler.execute(_invoke, ...)` — no thread-pool executor. Aligns with SAD-001 async discipline (`asyncio.run()` entry, `await` throughout).

### WARNING-1: `RetryHandler` imported but unused — FIXED
Instantiated in `main()` and `await retry_handler.execute(_invoke, ...)` wraps every SDK call (ADR-002 exponential backoff + jitter). Verified by `test_main_uses_retry_handler`.

### WARNING-2: `timeout` never extracted — FIXED
`timeout = getattr(args, "timeout", None) or getattr(cfg, "timeout_s", None)`. CLI flag wins, falls back to project default. Note: the config attribute is `cfg.timeout_s` (not `cfg.timeout` as the review text guessed).

### WARNING-3: Missing `args.operation` validation — FIXED
Added an early `if not getattr(args, "operation", None): return EXIT_USER_INPUT` after the resource check. Verified by `test_main_returns_user_input_when_no_operation`.

### MINOR-1: Dead imports — FIXED
Removed unused `METADATA_SEPARATOR` import and the unused `EXIT_AUTH` import.

### MINOR-2: Fragile `parents[4]` path — FIXED
Replaced with a depth-bounded upward walk that locates `src/foundry_cli/__init__.py`. Falls back to the old fixed-depth only as a last resort so any failure surfaces as a normal ImportError.

### Bonus parser bug found during fix
The `--timeout` / `--format` / `--pretty` / `--page-size` / `--page-token` / `--batch-pages` options were defined on the resource-level parent parser but were unreachable when placed after the operation positional, producing `unrecognized arguments`. Moved them onto each leaf operation subparser via a shared `_common_parser()` parent so options are accepted in both positions. Verified by `test_timeout_option_accepted_after_operation` and siblings.

### OWASP Top-10 Self-Review
- A01 Broken Access Control: `AccessControlGuard.check()` invoked before every SDK call; AccessControlError mapped to `EXIT_ACCESS_CONTROL`.
- A02 Cryptographic Failures: N/A — no crypto in this module.
- A03 Injection: No SQL/shell construction; JSON args parsed with `json.loads` (raises ValueError → user-input exit).
- A04 Insecure Design: Timeout always resolved from config default; no unbounded hangs.
- A05 Security Misconfiguration: No hardcoded credentials/tokens; all auth via `AsyncClientFactory` + `ConfigLoader`.
- A07 Auth Failures: Token sourced exclusively from `ConfigLoader` (env / .env).
- A09 Security Logging: `LogSetup.configure()` called; structured logs on stderr.
- A10 SSRF: N/A — host from config, not user input.

No security issues outstanding.

### Verification
- `python -m py_compile` — clean
- `python -m pytest tests/test_foundry_datasets_cli.py` — **96 passed**
- Coverage on `foundry_datasets_cli.py`: **91.91%** (>=80% threshold)

### Files Changed
- `.claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py` — fixes above
- `tests/test_foundry_datasets_cli.py` — expanded to 96 tests covering all 33 operations, timeout resolution, retry integration, operation validation, and exception handlers

Transitioning to **Corrected** for re-review.

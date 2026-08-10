Subject: Implementation complete - files and verification evidence
Created: 2026-08-10T02:50:16
Updated: 2026-08-10T02:50:16
---
## Files created/modified (DEV-016)

### Created
- `src/foundry_cli/streams/__init__.py` — package re-export
- `src/foundry_cli/streams/scripts/__init__.py`
- `src/foundry_cli/streams/scripts/foundry_streams_cli.py` — the 15-op CLI
- `src/foundry_cli/streams/metadata-allow-list.md` — packaged 3/12 policy
- `.claude/skills/foundry-streams/SKILL.md` — Claude skill doc
- `.claude/skills/foundry-streams/scripts/foundry_streams_cli.py` — thin launcher

### Modified
- `src/foundry_cli/common/access_control_guard.py` — added `reset` to `_WRITE_VERBS` (stream.reset, subscriber.reset_offsets)
- `tests/test_access_control_guard.py` — reset-verb write-classification regression tests
- `pyproject.toml` — console entry point `foundry-streams`, package-data, ruff E402 scope
- `tests/test_foundry_streams_cli.py` — created under UNITTEST-016 scope

## Verification evidence

- **File existence**: verified via directory listing and git status (all files tracked in commit `0c88063`).
- **Compile**: `python -m compileall -q src/foundry_cli/streams src/foundry_cli/common/access_control_guard.py` exit 0.
- **Lint**: `ruff check src/foundry_cli/streams src/foundry_cli/common/access_control_guard.py` — All checks passed.
- **Types**: `mypy src/foundry_cli/streams` — Success, no issues found.
- **CLI surface**: `foundry-streams --help` exit 0; parser exposes `dataset` (create), `stream` (create/get/get-end-offsets/get-records/publish-binary-record/publish-record/publish-records/reset), `subscriber` (create/commit-offsets/delete/get-read-position/read-records/reset-offsets) = exactly 15 ops.
- **ACL reset verb**: `stream.reset` and `subscriber.reset_offsets` now blocked under global READONLY (step 5) and under METADATA_ONLY; `_is_write_operation("reset")`/`_is_write_operation("reset_offsets")` True; shared ACL suite 74 passed.
- **Unit tests**: `tests/test_foundry_streams_cli.py` — 28 passed, 0 failed. Coverage streams 90% branch (gate ≥80% met).
- **Full regression**: 1146 passed, total coverage 86.09% branch, exit 0.
- **Runtime probes**: unknown op exit 1; `--max-records` out of bounds exit 1 with clear message; metadata-only blocks writes exit 8; permitted reads pass ACL.
- **Commit**: `0c88063` (HEAD, all changes committed).
- **OWASP self-review**: no hardcoded credentials; local validation (JSON, bounds, bounded binary file read) before client creation; no secrets echoed; retries disclose at-least-once semantics for writes.

## Decisions

- Story title claimed 17 operations; the vendored SDK exposes exactly 15 (Dataset 1, Stream 7, Subscriber 7) — implemented 15 per DESIGN-016 corrected count.
- `stream get-records` maps `--max-records` (default 100, max 10,000) to SDK `limit`; `subscriber read-records` maps `--max-records` (default 100, max 1,000) to SDK `limit`; offsets committed only with `--auto-commit` or explicit `commit-offsets`.
- `publish_binary_record` reads the `--file` content bounded at 16 MiB after the ACL decision, before client construction.
- Streams namespace default timeout is `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` (120s), overridable via `--timeout`.

## Time reported

estimated_hours: 16, time_spent_hours: 8.

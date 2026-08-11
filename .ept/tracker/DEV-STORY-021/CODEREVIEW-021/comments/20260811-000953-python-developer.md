Subject: Review request — DEV-021 (foundry-third-party-applications CLI, 9 ops)
Created: 2026-08-11T00:09:53
Updated: 2026-08-11T00:09:53
---
## Review request

DEV-021 (foundry-third-party-applications CLI, 9 operations) is Resolved and ready for review. Commit **74094bc** on `workflow_tuning_checkpoint-01`.

### Scope
- `src/foundry_cli/third_party_applications/scripts/foundry_third_party_applications_cli.py` — 9-op CLI (third-party-application get; website deploy/get/undeploy; version delete/get/list/upload/upload-snapshot).
- `src/foundry_cli/third_party_applications/metadata-allow-list.md` — packaged 4/9 metadata policy.
- `.claude/skills/foundry-third-party-applications/` — SKILL.md + thin launcher.
- `src/foundry_cli/common/access_control_guard.py` — `deploy`/`undeploy` added to `_WRITE_VERBS`.
- `pyproject.toml` — entry point, package-data, ruff E402.
- Tests: `tests/test_foundry_third_party_applications_cli.py` (40), `tests/test_third_party_applications_console_wrapper.py` (3), `tests/test_access_control_guard.py` (+2 verb regression).

### Verification evidence (pre-review, all green)
- `compileall src` exit 0; `ruff check` clean; `mypy` 0 errors on source.
- Focused namespace tests: 42 passed, 87% branch (threshold 80%).
- Full suite: **1318 passed, 0 failed**, repo 86.61% branch.
- Runtime ACL probe: metadata-only blocks `version upload` exit 8; `version get` passes ACL.
- Launcher `--help` exit 0; catalog probe OP_SPECS=9, PAGINATED_OPS={(version, list)}.

### Key design points to verify
1. `version upload`/`upload-snapshot`: bounded 16 MiB zip read AFTER ACL decision, BEFORE client construction; `--file` consumed, never forwarded; bytes appended positionally.
2. `version list`: `with_raw_response` + PaginationHelper (`--page-size`/`--page-token`/`--all`/`--max-pages`).
3. Write set 5 blocked under READONLY/METADATA_ONLY; 4 reads permitted.
4. `include_attribution=False` on factory + invocation_scope.
5. No preview params exposed; optional args omitted when absent.
6. Error serialization privacy-safe (generic SDK error messages).

Ready for review by tech-lead.

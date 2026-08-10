Subject: Implementation plan
Created: 2026-08-09T22:04:53
Updated: 2026-08-09T22:04:53
---
## Implementation Plan — DEV-014 foundry-orchestration CLI

### Scope
Implement `foundry-orchestration` CLI exposing exactly 20 Orchestration v2 operations per DESIGN-014 and DEV-STORY-014 contract (Build 6, Job 2, Schedule 10, ScheduleVersion 2, ScheduleRun 0).

### Deliverables
1. `src/foundry_cli/orchestration/__init__.py`
2. `src/foundry_cli/orchestration/scripts/__init__.py`
3. `src/foundry_cli/orchestration/scripts/foundry_orchestration_cli.py` — OP_SPECS catalog (exactly 20 entries, NO ScheduleRun), parser, dispatch, JSON validators (schedule.create/replace, build.create), pagination (3 cursor-paged ops), ACL, tracing, retry, output/error contracts
4. `src/foundry_cli/orchestration/metadata-allow-list.md` — packaged policy (12 PERMITTED / 8 BLOCKED)
5. `.claude/skills/foundry-orchestration/SKILL.md` + `scripts/foundry_orchestration_cli.py` thin launcher
6. `pyproject.toml` — console entry point `foundry-orchestration`, package data, ruff per-file-ignore E402
7. Shared `AccessControlGuard._WRITE_VERBS` update: add `launch`, `promote`, `pause`, `unpause` (mandated by DESIGN-014; shared change)

### Approach
- Canonical namespace pattern as in DEV-013 (same batch): `_ArgumentParser`→`CLIInputError` exit 1; OP_SPECS tuple; `_common_parser`; `_spec_for`; `_get_client` from `client.orchestration` (Build/Job/Schedule/ScheduleVersion); `_validate_timeout`; `_model_to_dict`.
- No binary downloads (no BinaryDownloadHandler per DESIGN-014).
- Pagination: exactly 3 ops (build jobs, build search, schedule runs) via PaginationHelper with `--page-size/--page-token/--all/--max-pages`; get_batch and search responses are single-call (no helper).
- JSON validation before client creation for schedule.create, schedule.replace, build.create inputs.
- ACL: `AccessControlGuard(cfg, "ORCHESTRATION", metadata_allowlist_path=...)`; 8 mutating ops (build.cancel, build.create, schedule.create/delete/pause/replace/run/unpause) blocked under readonly exit 8; build.search and schedule.get_affected_resources are semantic reads.
- Metadata-only: 12 PERMITTED / 8 BLOCKED per allow-list, evaluated before client construction.
- include_attribution=False; B3 via invocation_scope; RetryHandler transient-only with at-least-once disclosure for mutating ops.

### Verification
- pytest focused + full suite; ruff; mypy; branch coverage ≥80% on orchestration namespace; console entry point smoke.

### Decisions
- Follow TESTCASE-014 interface (`--all`/`--max-pages` exact-page pattern).
- Allow-list mirrors canonical metadata-allow-list.md orchestration section.
- ScheduleRun has 0 public SDK methods → no dispatch entries.

Subject: Implementation plan
Created: 2026-08-09T22:04:51
Updated: 2026-08-09T22:04:51
---
## Implementation Plan — DEV-013 foundry-models CLI

### Scope
Implement `foundry-models` CLI exposing exactly 23 Models v2 operations per DESIGN-013 and DEV-STORY-013 contract.

### Deliverables
1. `src/foundry_cli/models/__init__.py`
2. `src/foundry_cli/models/scripts/__init__.py`
3. `src/foundry_cli/models/scripts/foundry_models_cli.py` — OP_SPECS catalog (23 entries), parser, dispatch, JSON validators, pagination (4 cursor-paged ops), streaming downloads (3 ops), ACL integration, B3 tracing, retry, output/error contracts
4. `src/foundry_cli/models/metadata-allow-list.md` — packaged policy (12 PERMITTED / 11 BLOCKED)
5. `.claude/skills/foundry-models/SKILL.md` + `scripts/foundry_models_cli.py` thin launcher
6. `pyproject.toml` — console entry point `foundry-models`, package data, ruff per-file-ignore E402
7. Shared `AccessControlGuard._WRITE_VERBS` update: add `launch`, `promote`, `pause`, `unpause` (mandated by DESIGN-013/014)

### Approach
- Copy canonical namespace pattern (language_models/audit/aip_agents): `_ArgumentParser` raising `CLIInputError` (exit 1), `OP_SPECS` tuple, `_common_parser` with --timeout/--format/--pretty, `_spec_for`, `_get_client` nested resolution from `client.models`, `_validate_timeout` (1..3600), `_model_to_dict`.
- Pagination: exactly 4 ops use PaginationHelper with `--page-size/--page-token/--all/--max-pages` (40-page cap, exact-page pattern, with_raw_response fakes); `--offset/--page-size` on series/artifact JSON are service slicing only (forward once, no helper); trainer list has no pagination flags.
- Downloads: series parquet, artifact-table json/parquet via `with_streaming_response` + `BinaryDownloadHandler.save` with atomic persistence, metadata envelope, response closure, unsafe-name rejection.
- ACL: `AccessControlGuard(cfg, "MODELS", metadata_allowlist_path=...)` before client and file effects; write set = transform_json + creates + promote_version + launch; experiment search is semantic read.
- Attribution: `include_attribution=False` on scope and create; B3 restored after success/failure.
- Retries: `RetryHandler(timeout_s=timeout)` with ADR-004 transient-only; cursor-local retry state; at-least-once disclosure for mutating ops.
- Errors: ADR-001 envelope via ErrorSerializer; no secrets/bodies/content in stdout/stderr/logs.

### Verification
- `python -m pytest` focused + full suite; ruff; mypy; branch coverage ≥80% on models namespace; console entry point smoke.

### Decisions
- Follow TESTCASE-013 interface: `--all`/`--max-pages` (not legacy `--batch-pages`).
- Allow-list mirrors canonical `metadata-allow-list.md` models section (12/11).
- QUESTION-035 canceled — ACL verb additions are explicitly mandated by approved designs.

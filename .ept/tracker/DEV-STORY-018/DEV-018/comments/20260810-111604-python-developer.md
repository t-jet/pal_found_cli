Subject: Implementation plan
Created: 2026-08-10T11:16:04
Updated: 2026-08-10T11:16:04
---
## Implementation plan

Design: DESIGN-018-media-sets-cli.md (DESIGN-018 Closed, tech-lead). Canonical structure from sql_queries/streams CLIs.

Files to create:
- `src/foundry_cli/media_sets/__init__.py`
- `src/foundry_cli/media_sets/scripts/__init__.py`
- `src/foundry_cli/media_sets/scripts/foundry_media_sets_cli.py` (OP_SPECS 19 ops on single MediaSet client; DOWNLOAD_OPS = get_result/read/read_original/retrieve via with_streaming_response + BinaryDownloadHandler with FR-DL envelope; upload/upload_media bounded binary file read after ACL before client; transaction lifecycle flags create/commit/abort/clear; include_attribution=True per FR-ATTR-4; 9-op write set; metadata allow-list 5 PERMITTED/14 BLOCKED; no pagination)
- `src/foundry_cli/media_sets/metadata-allow-list.md` (5/14 matching canonical)
- `.claude/skills/foundry-media-sets/SKILL.md`
- `.claude/skills/foundry-media-sets/scripts/foundry_media_sets_cli.py` (thin launcher)

Shared-layer: AccessControlGuard._WRITE_VERBS additions for `register` and `calculate` (media_sets write set per DESIGN-018) + regression tests in tests/test_access_control_guard.py.

pyproject.toml: entry point foundry-media-sets, package-data, ruff per-file-ignores.

Verification: compileall, ruff, mypy, unit tests (UNITTEST-018).

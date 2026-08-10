Subject: Implementation complete — files and verification
Created: 2026-08-10T11:35:17
Updated: 2026-08-10T11:35:17
---
## Files created/modified

- src/foundry_cli/media_sets/__init__.py
- src/foundry_cli/media_sets/scripts/__init__.py
- src/foundry_cli/media_sets/scripts/foundry_media_sets_cli.py (OP_SPECS 19 ops on single MediaSet client)
- src/foundry_cli/media_sets/metadata-allow-list.md (5 PERMITTED / 14 BLOCKED)
- .claude/skills/foundry-media-sets/SKILL.md
- .claude/skills/foundry-media-sets/scripts/foundry_media_sets_cli.py (thin launcher)
- src/foundry_cli/common/access_control_guard.py (register + calculate added to _WRITE_VERBS for media_sets write set)
- tests/test_access_control_guard.py (regression test test_media_sets_verbs_are_writes)
- pyproject.toml (entry point foundry-media-sets, package-data, ruff per-file-ignores)
- .ept/docs/document_index.md

## Key decisions
- Four binary downloads (get_result/read/read_original/retrieve) via with_streaming_response + BinaryDownloadHandler with FR-DL JSON envelope; --output required.
- Two binary uploads (upload/upload_media) read --file bounded 16 MiB after ACL decision before client; upload_media requires --filename.
- include_attribution=True per FR-ATTR-4 (FIRST namespace): invocation_scope and create both pass True; attribution RIDs read from FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS; prior ATTRIBUTION_VAR restored after success/failure (shared factory, verified by tests).
- ACL write set 9 ops (abort/calculate/clear/commit/create/register/transform/upload/upload_media); content reads (get_result/read/read_original/retrieve) semantic reads but blocked in metadata-only.
- Transaction lifecycle: create/commit/abort/clear/upload pass through as flags; no auto-managed transactions.

## Verification (MANDATORY DoD)
- Files verified on disk via file search (5 files in src/foundry_cli/media_sets/ + 2 skill files + shared ACL change).
- compileall: exit 0. ruff: All checks passed. mypy: Success, 57 source files, no issues.
- Unit tests: tests/test_foundry_media_sets_cli.py 31 tests pass, 87% branch coverage; full suite 1214 passed 86.28% branch.
- bandit: clean (exit 0). CLI --help exit 0; launcher exit 0.
- Committed at 62c269f (workflow_tuning_checkpoint-01).
- OWASP self-review: no secrets; bounded downloads/uploads; ACL before client/file effects; fail-closed allow-list; attribution RIDs never logged.

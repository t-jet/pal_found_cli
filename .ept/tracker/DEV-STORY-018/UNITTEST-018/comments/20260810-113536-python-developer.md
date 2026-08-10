Subject: Tests complete — results and coverage
Created: 2026-08-10T11:35:36
Updated: 2026-08-10T11:35:36
---
## Test suite

File: tests/test_foundry_media_sets_cli.py (31 tests, 87% branch coverage).

Coverage per acceptance criteria:
- All 19 operations exercised; exact catalog count and (resource, operation, client_path, method) tuples asserted.
- Binary download bounded-stream behavior: read/read_original/retrieve/get_result via with_streaming_response + BinaryDownloadHandler; FR-DL envelope fields (file_path, file_size, checksum_md5, checksum_sha256, mime_type, truncated, source_size, source_size_at_least); truncation when stream exceeds max_download_bytes; unsafe filename rejection; response context closed.
- Binary uploads: upload/upload_media bounded file read after ACL before client; missing file rejected before client creation.
- ACL write/read classification: 9 writes blocked under READONLY; classification asserted via AccessControlGuard._is_write_operation.
- Metadata-only policy: packaged allow-list parses to exactly 5 permitted / 14 blocked; runtime blocks all 14 (mutations + content reads) and permits 5 metadata reads under FOUNDRY_AGENTIC_CLI_METADATA_ONLY.
- Attribution regression: include_attribution=True on invocation_scope and create; real AsyncClientFactory.invocation_scope restores prior ATTRIBUTION_VAR after success and after exception (FR-ATTR-4).
- JSON validation (transformation-json), transaction lifecycle dispatch, timeouts, error taxonomy (exit 6/5), TOON output, console boundary.

Results: 31/31 pass; full suite 1214 passed (up from 1148), 86.28% branch; ruff/mypy/compileall/bandit clean. Committed at 62c269f.

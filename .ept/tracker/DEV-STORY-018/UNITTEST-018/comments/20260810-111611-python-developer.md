Subject: Test plan
Created: 2026-08-10T11:16:11
Updated: 2026-08-10T11:16:11
---
## Test plan

File: tests/test_foundry_media_sets_cli.py (mirror test_foundry_sql_queries_cli.py for downloads).

Coverage:
- Catalog: exactly 19 ops, unique pairs, exact (resource, operation, client_path, method) tuples.
- Parser: every declared argument for all 19 ops; unknown op rejection.
- Dispatch: each op routes to exact nested MediaSet client; optional args omitted when absent; JSON args (transformation-json) decoded and validated.
- Binary downloads: read/read_original/retrieve/get_result use with_streaming_response + BinaryDownloadHandler; bounded truncation behavior; FR-DL envelope fields (file_path, file_size, checksum_md5, checksum_sha256, mime_type, truncated, source_size, source_size_at_least); --output required; unsafe filename rejection; response closed.
- Binary uploads: upload/upload_media read --file bounded after ACL before client.
- ACL: 9 writes blocked under READONLY; content reads (get_result/read/read_original/retrieve) blocked under metadata-only; write classification asserted via AccessControlGuard check.
- Metadata-only: 5 permitted / 14 blocked against packaged allow-list.
- Attribution regression: include_attribution=True on scope and create; prior ATTRIBUTION_VAR state restored after success and after failure.
- Errors/timeouts/output formats/privacy/console boundary.

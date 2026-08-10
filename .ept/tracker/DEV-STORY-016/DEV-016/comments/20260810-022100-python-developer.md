Subject: New to Open triage complete
Created: 2026-08-10T02:21:00
Updated: 2026-08-10T02:21:00
---
## New → Open triage

- **Status**: DEV-016 confirmed New → transitioned to Open.
- **Documentation studied**: DESIGN-016 (15-op catalog across Dataset 1 / Stream 7 / Subscriber 7, ADR-003 batch strategy, FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S=120, 3/12 metadata policy), canonical env-var reference, metadata allow-list, DESIGN-013/014 for the canonical CLI structure, shared common library.
- **SDK surface verified**: `foundry_sdk.v2.streams` exposes exactly 15 public operations — Dataset.create (name, parent_folder_rid, schema, branch_name?, compressed?, partitions_count?, stream_type?); Stream.create/get/get_end_offsets/get_records(limit required, partition_id required, start_offset?, view_rid?)/publish_binary_record(body, view_rid?)/publish_record(record, view_rid?)/publish_records(records, view_rid?)/reset(compressed?, partitions_count?, schema?, stream_type?); Subscriber.create(subscriber_id, read_position?)/commit_offsets(offsets, view_rid?)/delete/get_read_position(view_rid?)/read_records(auto_commit?, limit?, partition_ids?, view_rid?)/reset_offsets(position). `preview` excluded. No ResourceIterator → no pagination.
- **Critical thinking**: story title says 17 ops but the vendored SDK exposes exactly 15 — implement 15 per DESIGN-016 (corrected count). CLI resource subcommands are `dataset`, `stream`, `subscriber`. `stream.get_records` requires the SDK `limit`/`partition_id`; CLI exposes `--max-records` (default 100, max 10000) mapped to SDK `limit`. `subscriber.read_records` uses `--max-records` (default 100, max 1000) and `--partition-ids-json`; offsets committed only with `--auto-commit`. `stream.publish_binary_record` reads the `--file` content as bytes. The shared `AccessControlGuard` write classification must add the `reset` verb (stream.reset, subscriber.reset_offsets currently unclassified as writes) — same class of change as DESIGN-013/014 launch/promote/pause/unpause.
- **Questions**: none — all requirements clear.
- **Blockers**: none. Links: Contains LINK-00538, ParentChild LINK-00539, RelatesTo CODEREVIEW-016 LINK-00550/551, Blocks LINK-00553/554 — all registered and correct.
- **Required fields**: status, assignee (python-developer), priority (High), dates — validated.

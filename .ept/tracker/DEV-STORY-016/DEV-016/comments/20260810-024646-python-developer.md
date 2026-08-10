Subject: Implementation plan
Created: 2026-08-10T02:46:46
Updated: 2026-08-10T02:46:46
---
## Implementation plan — foundry-streams CLI (15 operations)

### Deliverables (Acceptance Criteria)
- `src/foundry_cli/streams/__init__.py`
- `src/foundry_cli/streams/scripts/__init__.py`
- `src/foundry_cli/streams/scripts/foundry_streams_cli.py` — the packaged CLI
- `src/foundry_cli/streams/metadata-allow-list.md` — packaged 3/12 policy
- `.claude/skills/foundry-streams/SKILL.md` + `.claude/skills/foundry-streams/scripts/foundry_streams_cli.py` thin launcher
- Shared: add `reset` verb to `AccessControlGuard._WRITE_VERBS`
- `pyproject.toml` updates: console entry point `foundry-streams`, package-data, ruff E402 scope

### Catalog (OP_SPECS snake_case; CLI kebab-case; resources dataset/stream/subscriber)
1. dataset.create — required --name, --parent-folder-rid, --schema-json; optional --branch-name, --compressed, --partitions-count, --stream-type — WRITE
2. stream.create — dataset_rid, --branch-name, --schema-json; optional compressed/partitions-count/stream-type — WRITE
3. stream.get — dataset_rid, stream_branch_name — READ
4. stream.get-end-offsets — + optional --view-rid — READ
5. stream.get-records — + required --partition-id; optional --start-offset, --view-rid; --max-records (default 100, max 10,000) → SDK limit — READ (semantic)
6. stream.publish-binary-record — + required --file; optional --view-rid; bounded file read (16 MiB) — WRITE
7. stream.publish-record — + required --record-json; optional --view-rid — WRITE
8. stream.publish-records — + required --records-json; optional --view-rid — WRITE
9. stream.reset — optional --schema-json, --compressed, --partitions-count, --stream-type — WRITE
10. subscriber.create — + required --subscriber-id; optional --read-position-json — WRITE
11. subscriber.commit-offsets — + required --offsets-json; optional --view-rid — WRITE
12. subscriber.delete — — WRITE
13. subscriber.get-read-position — optional --view-rid — READ
14. subscriber.read-records — optional --auto-commit, --partition-ids-json, --view-rid; --max-records (default 100, max 1,000) → SDK limit — READ (semantic)
15. subscriber.reset-offsets — + required --position-json — WRITE

### Key design decisions
- Implement exactly 15 ops (SDK-exposed surface); story title "17" is stale (corrected in DESIGN-016).
- ADR-003 batch reads: aggregate and emit on exit; never progressive.
- ACL write set (10): dataset.create, stream.create, publish_binary_record, publish_record, publish_records, stream.reset, subscriber.create, commit_offsets, delete, reset_offsets. Add `reset` verb to shared `_WRITE_VERBS` so reset/reset_offsets stay write-classified.
- Metadata-only permits exactly 3: stream.get, stream.get_end_offsets, subscriber.get_read_position.
- include_attribution=False; streams timeout env FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S (default 120s) per ADR-003.
- JSON args: schema, record, records, offsets, position, read_position, partition_ids.

### Verification plan
- compileall exit 0; ruff; mypy; unit tests via UNITTEST-016 (100% pass, ≥80% branch).
- Regression tests for reset-verb write classification in shared ACL suite.
- Commit all changes to the repository.

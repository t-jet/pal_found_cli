Subject: Review request — DEV-018 Resolved
Created: 2026-08-10T11:38:35
Updated: 2026-08-10T11:38:35
---
## Review request

DEV-018 (foundry-media-sets CLI, 19 operations) is Resolved at commit 62c269f. Implementation files verified on disk and compiling.

- Catalog: OP_SPECS exactly 19 on single MediaSet client; nested dispatch via client.media_sets.MediaSet.
- Binary downloads: get_result/read/read_original/retrieve via with_streaming_response + BinaryDownloadHandler (FR-DL envelope, bounded).
- Binary uploads: upload/upload_media bounded 16 MiB file read after ACL before client.
- ACL: 9-op write set; AccessControlGuard._WRITE_VERBS extended with register + calculate (regression tests added); packaged metadata allow-list 5 PERMITTED / 14 BLOCKED.
- include_attribution=True per FR-ATTR-4 (first namespace); prior ATTRIBUTION_VAR restored after success/failure.
- Verification: compileall 0, ruff clean, mypy clean (57 files), bandit clean, 31 focused tests pass (87% branch), full suite 1214 passed 86.28% branch.

Files: src/foundry_cli/media_sets/, .claude/skills/foundry-media-sets/, src/foundry_cli/common/access_control_guard.py. Reviewer: tech-lead.

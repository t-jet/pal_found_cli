Subject: Correction and local verification
Created: 2026-10-13T23:33:41
Updated: 2026-10-13T23:33:41
---
# Correction
Updated `pal-found-orchestration/references/01-build-job.md` and `02-schedule.md`. `build.create` now describes its one-time target. `build.jobs`, `build.search`, and `schedule.runs` describe item-list stdout, separate stderr page metadata, page flags, and cursor continuation. `schedule.create` and `schedule.replace` describe trigger request configuration using the SDK `time` trigger fields. `schedule.get`, `schedule.get_affected_resources`, `schedule.get_batch`, and `schedule.runs` now state read access prerequisites without implying schedule management permission.
# Source check
Local CLI `pal_found_orchestration_cli.py` has the three operations in `PAGINATED_OPS`, uses `_fetch_raw_page` and `_paginate_operation`, formats collected list to stdout, then calls `PaginationHelper.emit_metadata()` for stderr. Local SDK `orchestration/models.py` defines `TimeTrigger` with `cronExpression` and `timeZone`; `schedule.py` accepts `Trigger` for create/replace; `build.py` accepts `BuildTarget` for create.
# Verification
Offline skill gate: 9 passed, exit 0. Orchestration CLI suite: 32 passed, exit 0. Skills git diff --check on two files: exit 0. Self-review: documentation-only; no new input handling, network operation, access-control path, or secret. Independent QA must review revised six rows and refresh source hashes before Closed.

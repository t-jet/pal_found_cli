Subject: Implementation plan (New → Open — DoD)
Created: 2026-07-22T23:30:41
Updated: 2026-07-22T23:30:41
---
## Implementation Plan — AccessControlGuard & PaginationHelper (DEV-004)

Parent: DEV-STORY-003 | Design: DESIGN-004 (Closed) | Pair: UNITTEST-004 | Review: CODEREVIEW-004

### Source docs reviewed (via `.ept/docs/document_index.md`)
- SRS-001 §4.2 FR-ACL-1..6 — three-tier access model + 8-step precedence
- SRS-001 §4 FR-PAG-1..5 — pagination requirements
- ADR-001 (exit code 8), ADR-005 (stderr metadata after `# ---metadata-start---`), ADR-007 (op-level READONLY=false override only)
- Canonical env-var reference — transformation rule: `{NS}_{CLASS}_{OP}_{CONTROL}`, operation kept verbatim
- metadata-allow-list.md — deny-by-default, 162 PERMITTED entries

### Gap analysis (current implementation vs. SPEC)

**AccessControlGuard — 1 bug:**
1. `_operation_env_key` reorders verb+object (`put_schema` → `DATASETS_SCHEMA_PUT`) instead of keeping the operation verbatim (`DATASETS_DATASET_PUT_SCHEMA`). This breaks the Step-3 operation-level `_READONLY=false` override for multi-word write ops. **Reproduced:** AC-9 case (`READONLY=true` + `DATASETS_DATASET_PUT_SCHEMA_READONLY=false`) currently BLOCKS at step 5 instead of PERMITTING. Fix: build the op-level key as `{NS}_{RESOURCE}_{OP}` with the operation name left untouched, matching the canonical transformation rule.

**PaginationHelper — 1 bug:**
2. `_extract_items` checks `hasattr(response, "items")` before `isinstance(response, dict)`. Every dict has a `.items()` method, so the dict branch is unreachable; `getattr(dict, "items")` returns the bound method (not a list) → `TypeError` on iteration. Fix: move the `isinstance(response, dict)` branch above the `hasattr` check.

**CLI integration — 1 gap:**
3. `foundry_datasets_cli.py` parses `--batch-pages` and `--page-size`/`--page-token` but never instantiates `PaginationHelper`. Batch aggregation (FR-PAG-4), max cap enforcement (FR-PAG-5), stderr page-token metadata emission (FR-PAG-2/AC-12) are all unimplemented. Fix: for paginated operations, wrap the SDK call with `PaginationHelper`, aggregate results, and call `emit_metadata()` after stdout output.

### Files to modify
- `src/foundry_cli/common/access_control_guard.py` — fix `_operation_env_key` (bug #1)
- `src/foundry_cli/common/pagination_helper.py` — fix `_extract_items`/`_extract_next_token` ordering (bug #2)
- `.claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py` — wire PaginationHelper for paginated ops (gap #3)

### Out of scope (siblings, not mine)
- UNITTEST-004 — paired unit coverage (separate sub-task)
- CODEREVIEW-004 — tech-lead's review gate

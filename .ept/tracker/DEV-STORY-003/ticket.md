---
id: DEV-STORY-003
type: dev_story
title: Implement AccessControlGuard, PaginationHelper
status: Development
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-07-22
priority: Critical
assignee: architect
reporter: architect
story_points: 8
release_notes: 'AccessControlGuard and PaginationHelper shared infrastructure: enforce SRS/SAD access-control
  precedence, metadata-only/read-only tiers, metadata allow-list behavior, pagination
  controls, page-token metadata, and batched page aggregation for namespace skills.'
---

# DEV-STORY-003: Implement AccessControlGuard, PaginationHelper

## Description

AccessControlGuard: 8-step precedence matrix (FOUNDRY_ACCESS_TIER -> namespace -> operation flags); enforces READONLY (ADR-007) and METADATA_ONLY tiers. PaginationHelper: transparent page iteration for all paginated SDK operations.

## Acceptance Criteria

### AccessControlGuard (FR-ACL: Three-Tier Access Model)

- [ ] **AC-1** Implements the 8-step precedence model exactly as defined in SRS-001 §4.2 (FR-ACL-5): ENABLED check (op → namespace), READONLY override (op → namespace), global READONLY, METADATA_ONLY override (namespace), global METADATA_ONLY, default FULL ACCESS. First matching rule wins.
- [ ] **AC-2** Enforces three access tiers per SRS-001 FR-ACL-1: Full (default), Read-only, Metadata-only
- [ ] **AC-3** Read-only tier blocks all write operations; all read operations permitted (FR-ACL-2)
- [ ] **AC-4** Metadata-only tier blocks data content reads AND all writes; only metadata reads permitted (FR-ACL-3)
- [ ] **AC-5** `METADATA_ONLY=true` implies `READONLY=true` — writes are BLOCKED (FR-ACL-4)
- [ ] **AC-6** Metadata allow-list uses deny-by-default stance for unclassified operations (FR-ACL-6), loading allow-list from canonical metadata-allow-list.md
- [ ] **AC-7** Raises `AccessControlError` with exit code 8 (per ADR-001) and structured JSON error envelope on any block
- [ ] **AC-8** Supports per-operation READONLY independence from namespace-level control (ADR-007)
- [ ] **AC-9** Acceptance test: `FOUNDRY_AGENTIC_CLI_READONLY=true` + `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false` → write PERMITTED for that specific operation (SRS FR-ACL-5 example)

### PaginationHelper (FR-PAG: Pagination)

- [ ] **AC-10** Exposes `--page-size`, `--page-token`, and `--batch-pages` CLI arguments on all paginated operations (FR-PAG-3)
- [ ] **AC-11** Default behavior: return first page only (FR-PAG-1); uses `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE` (default 100)
- [ ] **AC-12** When next page token is available, emit it to stderr as part of metadata JSON (FR-OUT-2, FR-PAG-2) with `# ---metadata-start---` separator per ADR-005
- [ ] **AC-13** When `--batch-pages N` specified, retrieve up to N pages and aggregate results before emitting (FR-PAG-4)
- [ ] **AC-14** Maximum `--batch-pages` value is 40, enforced from `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (FR-PAG-5)
- [ ] **AC-15** Coordinates with OutputFormatter for page aggregation (per SAD-001 §4 component relationships)

### Non-Functional

- [ ] **AC-16** Components are implemented as Python classes within `_foundry_cli_common.py` with full type hints (Python 3.11+)
- [ ] **AC-17** Unit tests achieve ≥80% code coverage for both components
- [ ] **AC-18** Integration tests verify 8-step precedence evaluation with all 8 steps exercised individually

## Related Documentation

### Architecture & Requirements

- [SAD-001 §4 — C4 Level 3 Component Diagram](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md#4-c4-level-3---component-diagram) — AccessControlGuard, PaginationHelper component definitions and relationships
- [SAD-001 §6.3 — Access Control Block Sequence Diagram](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md#63-access-control-block) — 8-step evaluation flow in sequence diagram
- [SAD-001 §10 — Implementation Roadmap](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md#10-implementation-roadmap) — DEV-STORY-003 placement in Phase 1 (Sprint 1-2)
- [SRS-001 §4.2 — FR-ACL: Three-Tier Access Model](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md#fr-acl-three-tier-access-model) — 8-step precedence model, FR-ACL-1 through FR-ACL-6
- [SRS-001 §4 — FR-PAG: Pagination](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md#fr-pag-pagination) — FR-PAG-1 through FR-PAG-5, pagination requirements
- [SRS-001 §4 — FR-OUT-2](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md#fr-out-2) — Pagination metadata emitted to stderr as JSON

### Architecture Decision Records
- [ADR-001 — Exit Code Taxonomy](.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Exit code 8 for AccessControlError
- [ADR-005 — Log Format](.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md) — Metadata JSON to stderr with `# ---metadata-start---` separator
- [ADR-007 — Operation-Level READONLY Independence](.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md) — Per-operation READONLY flag independence from namespace-level control

### Supporting Artifacts
- [Canonical Environment Variable Reference](.ept/docs/deliverables/architecture/canonical-env-var-reference.md) — FOUNDRY_AGENTIC_CLI_READONLY, FOUNDRY_AGENTIC_CLI_METADATA_ONLY, FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE, FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES
- [Metadata Allow-list](.ept/docs/deliverables/architecture/metadata-allow-list.md) — Approved metadata fields for Metadata-only tier (FR-ACL-6)

## Notes

### Blockers (as of 2026-05-18)
- **QUESTION-006** (In Progress, addressed to business-analyst): Acceptance criteria drafted by architect above based on SRS/SAD research; awaiting BA review and formal approval. Blocks New → Open transition.
- **FEATURE-001** (In Design): Parent Feature must reach `Waiting for Implementation` before DEV-STORY-003 can advance to Open per DoD.

### Technical Scope
- Two classes in `_foundry_cli_common.py`: `AccessControlGuard` and `PaginationHelper`
- AccessControlGuard depends on: ConfigLoader (for flags), metadata allow-list file
- PaginationHelper coordinates with: OutputFormatter (for page aggregation), AsyncClientFactory (for paginated API calls)
- Both are foundational shared infrastructure — no namespace-specific logic

### Environment Variables Used
- `FOUNDRY_AGENTIC_CLI_READONLY` (default: false) — global read-only gate
- `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` (default: false) — global metadata-only gate
- `FOUNDRY_AGENTIC_CLI_{NS}_ENABLED` / `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_ENABLED` — namespace/op enable flags
- `FOUNDRY_AGENTIC_CLI_{NS}_READONLY` / `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY` — READONLY override flags
- `FOUNDRY_AGENTIC_CLI_{NS}_METADATA_ONLY` — METADATA_ONLY namespace override
- `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE` (default: 100)
- `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (default: 40)

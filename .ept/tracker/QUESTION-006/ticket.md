---
id: QUESTION-006
type: question
title: 'DEV-STORY-003: Acceptance criteria contain TODO placeholders — needs BA completion'
status: Closed
addressed_to: business-analyst
created: 2026-05-17
updated: 2026-05-18
priority: Medium
assignee: architect
reporter: architect
---

# QUESTION-006: DEV-STORY-003: Acceptance criteria contain TODO placeholders — needs BA completion

## Description

DEV-STORY-003 (AccessControlGuard, PaginationHelper) has TODO placeholders in all three critical sections: Acceptance Criteria, Related Documentation, and Notes. The ticket currently contains only minimal description and one TODO bullet for acceptance criteria. BA needs to define proper acceptance criteria aligned with SAD-001 §4 (Component Diagram), §6.3 (Access Control Block sequence), and the SRS FR-ACL requirements. Additionally, Related Documentation section has TODO — links to SAD-001 §4, §6.3, SRS Section 4.2 (8-step precedence model), ADR-007 should be provided.

## Answer (BA Resolution — 2026-05-18)

The following acceptance criteria are authoritative and derived directly from SRS-001 §3 (FR-PAG, FR-ACL), §4.2 (8-Step Precedence Model), SAD-001 §4 (Component Diagram), §6.3 (Access Control Block sequence), and ADR-007 (Operation-Level READONLY).

---

### AccessControlGuard — Acceptance Criteria

**AC-1: Operation-level ENABLED=false blocks operation (Step 1)**
- **Given** FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_ENABLED=false is set
- **When** datasets dataset put-schema is invoked
- **Then** exit code is 8, stdout contains {"error": {"type": "AccessControlError", "message": "Operation blocked: ENABLED=false for DATASETS_DATASET_PUT_SCHEMA"}}, and no SDK call is made

**AC-2: Namespace-level ENABLED=false blocks all operations in namespace (Step 2)**
- **Given** FOUNDRY_AGENTIC_CLI_DATASETS_ENABLED=false is set
- **When** any datasets namespace operation is invoked (e.g., datasets dataset list)
- **Then** exit code is 8, stdout contains {"error": {"type": "AccessControlError", "message": "Namespace blocked: ENABLED=false for DATASETS"}}, and no SDK call is made

**AC-3: Operation-level READONLY=false overrides global READONLY (Step 3 — WRITE PERMITTED)**
- **Given** FOUNDRY_AGENTIC_CLI_READONLY=true and FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false are both set
- **When** datasets dataset put-schema is invoked
- **Then** the write operation is permitted and proceeds to the SDK (SRS-001 §4.2 Step 3), confirming the override grants write permission for this specific operation

**AC-4: Namespace-level READONLY=false overrides global READONLY (Step 4 — WRITE PERMITTED)**
- **Given** FOUNDRY_AGENTIC_CLI_READONLY=true and FOUNDRY_AGENTIC_CLI_DATASETS_READONLY=false are both set
- **When** any write operation in the datasets namespace is invoked
- **Then** the write operation is permitted and proceeds to the SDK (SRS-001 §4.2 Step 4)

**AC-5: Global READONLY=true blocks all writes (Step 5 — READ-ONLY tier)**
- **Given** FOUNDRY_AGENTIC_CLI_READONLY=true is set and no per-namespace or per-operation READONLY=false override exists
- **When** a write operation (e.g., datasets dataset put-schema) is invoked
- **Then** exit code is 8, stdout contains {"error": {"type": "AccessControlError", "message": "Operation blocked: read-only mode active"}}, and no SDK call is made

**AC-6: Read operations are permitted under READONLY=true**
- **Given** FOUNDRY_AGENTIC_CLI_READONLY=true is set
- **When** a read operation (e.g., datasets dataset list) is invoked
- **Then** exit code is 0, read data is returned on stdout, confirming read-only tier permits all reads (FR-ACL-2)

**AC-7: Namespace-level METADATA_ONLY=false overrides global METADATA_ONLY (Step 6)**
- **Given** FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true and FOUNDRY_AGENTIC_CLI_DATASETS_METADATA_ONLY=false are both set
- **When** a data content read in the datasets namespace is invoked
- **Then** the content read is permitted and proceeds to the SDK (SRS-001 §4.2 Step 6)

**AC-8: Global METADATA_ONLY=true blocks content reads + writes (Step 7 — METADATA-ONLY tier)**
- **Given** FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true is set
- **When** a data content read operation is invoked
- **Then** the operation is blocked if the operation is NOT in the metadata allow-list (FR-ACL-6, deny-by-default), exit code is 8, and stdout contains {"error": {"type": "AccessControlError", "message": "Operation blocked: not in metadata allow-list"}}

**AC-9: Default behavior is FULL ACCESS (Step 8)**
- **Given** no access control env vars are set (all defaults)
- **When** any operation is invoked
- **Then** the operation proceeds with full access (Step 8 default), confirming no access control restriction applies

---

### PaginationHelper — Acceptance Criteria

**AC-10: First page only by default**
- **Given** a list/search operation is invoked without pagination arguments
- **When** the API returns results with a 
extPageToken
- **Then** stdout contains only the first page of results, and stderr metadata JSON contains the page_token field with the next cursor value (FR-PAG-1, FR-PAG-2)

**AC-11: --page-size argument controls results per page**
- **Given** --page-size 10 is specified on a paginated operation
- **When** the operation is invoked
- **Then** at most 10 items are returned in the result set, and stderr metadata confirms the page size

**AC-12: --page-token argument resumes from cursor**
- **Given** --page-token tok123 is specified on a paginated operation
- **When** the operation is invoked
- **Then** the API is called with the provided page token, and results start from the position indicated by that cursor (FR-PAG-3)

**AC-13: --batch-pages N aggregates up to N pages**
- **Given** --batch-pages 3 and --page-size 10 are specified
- **When** the API has data available across 3+ pages
- **Then** stdout contains a combined array of up to 30 items (TOON or JSON per format rules), and stderr metadata contains the next cursor if more pages exist, or null if exhausted (FR-PAG-4)

**AC-14: --batch-pages maximum is 40**
- **Given** --batch-pages 41 is specified
- **When** the operation is invoked
- **Then** the CLI rejects the value and returns an argument parsing error (FR-PAG-5, FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES=40)

**AC-15: Pagination metadata uses ADR-005 separator on stderr**
- **Given** any paginated operation is invoked
- **When** the operation completes successfully
- **Then** stderr contains the # ---metadata-start--- separator followed by a JSON object containing pagination metadata (page_token, total_items, pages_fetched) per ADR-005

---

### Non-Functional Acceptance Criteria (shared with DEV-STORY-003)

**AC-16: Access control guard executes before any SDK call (zero side-effects)**
- **Given** FOUNDRY_AGENTIC_CLI_DATASETS_ENABLED=false is set
- **When** any datasets operation is invoked
- **Then** the AccessControlGuard raises AccessControlError and exits before AsyncFoundryClient makes any HTTP request, confirming the layered security model from SAD-001 §1.3

**AC-17: Access control decision is logged**
- **Given** an access control check is performed
- **When** the guard evaluates the 8-step precedence
- **Then** an NDJSON log record is emitted to stderr with ccess_decision: "BLOCKED" or ccess_decision: "PERMITTED" per ADR-005 log schema

**AC-18: Precedence model — first matching step wins**
- **Given** FOUNDRY_AGENTIC_CLI_DATASETS_ENABLED=false AND FOUNDRY_AGENTIC_CLI_READONLY=true are both set
- **When** a datasets operation is invoked
- **Then** Step 1 (namespace ENABLED=false) wins before Step 5 (global READONLY), confirming the "first match wins" precedence ordering from SRS-001 §4.2

---

## Related Documentation

| Document | Section | Relevance |
|---|---|---|
| SRS-001 §4 | FR-ACL (Three-Tier Access Model) | FR-ACL-1 through FR-ACL-6 define the access control requirements this component implements |
| SRS-001 §4.2 | 8-Step Precedence Model | The authoritative precedence table; AC-1 through AC-9 map to Steps 1–8 |
| SRS-001 §3.4 | FR-PAG (Pagination) | FR-PAG-1 through FR-PAG-5 define pagination requirements; AC-10 through AC-15 implement these |
| SRS-001 §5.3 | Configuration Reference | FOUNDRY_AGENTIC_CLI_READONLY, METADATA_ONLY, DEFAULT_PAGE_SIZE, MAX_BATCH_PAGES env var defaults |
| SAD-001 §4 | Component Diagram | AccessControlGuard and PaginationHelper component definitions with interfaces |
| SAD-001 §6.3 | Access Control Block Sequence | Sequence flow showing guard evaluation before SDK call |
| ADR-007 | Operation-Level READONLY | Confirms operation-level READONLY=true is NOT supported; only ENABLED=false and READONLY=false override exist |
| ADR-005 | Log Format | NDJSON log schema on stderr with ccess_decision field; # ---metadata-start--- separator |

## Notes

- **ADR-007 constraint:** Per ADR-007, FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=true where parent READONLY is not already true SHALL be ignored. The guard does NOT evaluate independent operation-level READONLY=true. Write blocking at operation level is achieved via ENABLED=false instead.
- **Metadata allow-list:** The metadata allow-list (.ept/docs/deliverables/architecture/metadata-allow-list.env) uses deny-by-default for METADATA_ONLY tier. Operations not explicitly listed are blocked for content reads.
- **Tier implication:** METADATA_ONLY=true implies READONLY=true (FR-ACL-4). The guard must enforce both constraints when METADATA_ONLY is active.
- **Exit code:** All access control violations return exit code 8 (per ADR-001 exit code taxonomy for AccessControlError).

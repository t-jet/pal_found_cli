# TESTCASE-004 - QA Test Cases for AccessControlGuard and PaginationHelper

**Parent:** DEV-STORY-003  
**Author:** qa-engineer  
**Date:** 2026-07-26  

## Scope

This deliverable covers QA case design for `AccessControlGuard` and `PaginationHelper` in `src/foundry_cli/common/`, plus datasets CLI parser integration where pagination flags must be exposed to operations.

## Coverage matrix

| Requirement area | Test case IDs |
|---|---|
| Access-control precedence, steps 1-8 | TC-ACL-001 through TC-ACL-011 |
| Metadata-only allow-list behavior | TC-ACL-012 through TC-ACL-017 |
| Access-control error contract and logging | TC-ACL-018 through TC-ACL-020 |
| Pagination defaults, params, batching, cap | TC-PAG-001 through TC-PAG-010 |
| Pagination stderr metadata | TC-PAG-011 through TC-PAG-013 |
| Datasets CLI pagination flag exposure | TC-CLI-001 through TC-CLI-003 |
| Smoke and environment-dependent labels | TC-SMK-001 through TC-SMK-004 |

## Preconditions

- Python 3.11 or 3.12 environment with project test dependencies installed.
- `src/` import path available, as done by current pytest modules.
- No real Foundry credentials required for smoke/unit tests that mock SDK calls.
- Environment-dependent CLI tests need valid `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME`, and disposable Foundry dataset/file resources.
- Metadata allow-list source: `.ept/docs/deliverables/architecture/metadata-allow-list.md`.
- Reference docs: SRS FR-ACL, SRS FR-PAG, ADR-005, ADR-007, SAD DEV-STORY-003 component design.

## Test scenarios

### AccessControlGuard

| ID | Scenario | Given | When | Then | Expected output |
|---|---|---|---|---|---|
| TC-ACL-001 | Step 1 blocks operation | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_CREATE_ENABLED=false` | `guard.check("dataset", "create")` | Operation is blocked before other rules | `AccessControlError`, `exit_code=8`, `step=1` |
| TC-ACL-002 | Step 1 wins over READONLY override | Global `READONLY=true`, op `ENABLED=false`, op `READONLY=false` | `dataset.create` is checked | `ENABLED=false` has precedence | `AccessControlError`, `step=1`, blocked env var is op `ENABLED` |
| TC-ACL-003 | Step 2 blocks namespace | `FOUNDRY_AGENTIC_CLI_DATASETS_ENABLED=false` | Any datasets operation is checked | Namespace block applies | `AccessControlError`, `step=2` |
| TC-ACL-004 | Step 2 wins over namespace READONLY override | Global `READONLY=true`, namespace `ENABLED=false`, namespace `READONLY=false` | `dataset.create` is checked | Namespace enabled block applies first | `AccessControlError`, `step=2` |
| TC-ACL-005 | Step 3 permits specific write | Global `READONLY=true`, `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false` | `dataset.put_schema` is checked | Specific write is permitted | No exception; SDK may be called |
| TC-ACL-006 | Step 4 permits namespace write override | Global `READONLY=true`, `FOUNDRY_AGENTIC_CLI_DATASETS_READONLY=false` | `dataset.create` is checked | Namespace override permits write | No exception |
| TC-ACL-007 | Step 4 namespace readonly blocks writes | `FOUNDRY_AGENTIC_CLI_DATASETS_READONLY=true` | `dataset.create` is checked | Write blocked in namespace | `AccessControlError`, `step=4` |
| TC-ACL-008 | Step 5 global readonly blocks writes | `FOUNDRY_AGENTIC_CLI_READONLY=true` | `dataset.create` or `dataset.put_schema` is checked | Write blocked globally | `AccessControlError`, `step=5` |
| TC-ACL-009 | Step 5 global readonly permits reads | `FOUNDRY_AGENTIC_CLI_READONLY=true` | `dataset.get` is checked | Read operation is permitted | No exception |
| TC-ACL-010 | Step 6 namespace metadata-only override | Global `METADATA_ONLY=true`, `FOUNDRY_AGENTIC_CLI_DATASETS_METADATA_ONLY=false` | `file.content` is checked | Namespace override permits content read | No exception |
| TC-ACL-011 | Step 8 default full access | No ACL env vars set | `dataset.create` and `dataset.get` are checked | Default permits both | No exception |
| TC-ACL-012 | Global metadata-only denies content read | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and allow-list marks `datasets.file.content` blocked | `file.content` is checked | Content read is denied | `AccessControlError`, `step=7` |
| TC-ACL-013 | Global metadata-only permits allow-listed metadata read | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and `datasets.dataset.get` is `PERMITTED` | `dataset.get` is checked | Metadata read is permitted | No exception |
| TC-ACL-014 | Global metadata-only denies table content | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and `datasets.dataset.read_table` is `BLOCKED` | `dataset.read_table` is checked | Table content is denied | `AccessControlError`, `step=7` |
| TC-ACL-015 | Metadata-only blocks writes | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | `dataset.create` is checked | Writes are blocked because metadata-only implies readonly | `AccessControlError`, `step=7` |
| TC-ACL-016 | Allow-list parser accepts canonical permitted rows only | Markdown table contains backticked `datasets.dataset.get` with `PERMITTED`, plus blocked/lowercase/unbackticked rows | Allow-list is loaded | Only canonical `PERMITTED` backticked SDK paths are accepted | Allow-list set contains `datasets.dataset.get` only |
| TC-ACL-017 | Deny by default for unlisted metadata-like operation | Global metadata-only true, operation not in allow-list | `dataset.get_sensitive_content` is checked | Unlisted operation is denied | `AccessControlError`, message says not in metadata allow-list |
| TC-ACL-018 | Operation-level READONLY=true is ignored without parent readonly | Op `READONLY=true`, global/namespace readonly false | `dataset.create` is checked | ADR-007 no independent operation readonly is honored | No exception |
| TC-ACL-019 | Error exposes serializer details | Access block occurs | Error object is inspected | Details include blocked rule fields | `details.blocked_rule.operation`, `env_var`, `value`, `step` present |
| TC-ACL-020 | Access decision logging contract | Guard logs permitted and blocked decisions | Logger receives records | Records include `access_decision`, operation, step, reason | Valid NDJSON-compatible extras |

### PaginationHelper

| ID | Scenario | Given | When | Then | Expected output |
|---|---|---|---|---|---|
| TC-PAG-001 | Default first page only | SDK fake returns items and next token | `PaginationHelper(page_size=10).paginate(fake)` | One SDK call is made | Items from first page, `pages_fetched=1`, next token stored |
| TC-PAG-002 | `--page-size` maps to SDK params | `PaginationHelper(page_size=50)` | `get_sdk_params()` | Page size is forwarded | `{"page_size": 50}` |
| TC-PAG-003 | `--page-token` maps to SDK params | `PaginationHelper(page_size=25, page_token="abc")` | `get_sdk_params()` | Initial token is forwarded | `{"page_size": 25, "page_token": "abc"}` |
| TC-PAG-004 | Batch pages aggregate results | Fake SDK returns three pages | `batch_pages=3` paginate call | Three pages are requested and concatenated | Combined list has all page items |
| TC-PAG-005 | SDK page token propagation | Fake SDK returns `tok1`, then `tok2` | `batch_pages=3` paginate call | Later calls use returned tokens | Calls include page tokens in order |
| TC-PAG-006 | Stop when no next token | Fake SDK returns `next_page_token=None` on first page | `batch_pages=5` paginate call | No extra calls occur | One page fetched; next token absent |
| TC-PAG-007 | Max batch cap clamps large values | `batch_pages=1000` | Helper constructed | Value clamps to hard cap | `batch_pages == 40` |
| TC-PAG-008 | Env cannot raise max batch cap above 40 | `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES=100` | Module reload/helper creation | Hard cap remains 40 | `MAX_BATCH_PAGES == 40` |
| TC-PAG-009 | Invalid page size rejected | `page_size=0`, `-1`, string, float | Helper constructed | Bad values fail fast | `ValueError` or `TypeError` naming `page_size` |
| TC-PAG-010 | Invalid batch pages rejected | `batch_pages=0` or `-1` | Helper constructed | Bad values fail fast | `ValueError` naming `batch_pages` |
| TC-PAG-011 | Stderr metadata separator emitted | Helper has fetched pages and token | `emit_metadata()` | ADR-005 separator precedes JSON | First stderr line is `# ---metadata-start---` |
| TC-PAG-012 | Metadata includes next token when present | `_next_page_token="cursor42"` | `emit_metadata()` | Cursor is emitted | JSON has `next_page_token`, `pages_fetched`, `total_items`, `page_size` |
| TC-PAG-013 | Metadata omits token when no more pages | `_next_page_token=None` | `emit_metadata()` | No false cursor is emitted | JSON omits `next_page_token` and retains counts |

### Datasets CLI pagination exposure

| ID | Scenario | Given | When | Then | Expected output |
|---|---|---|---|---|---|
| TC-CLI-001 | Paginated operations expose all flags | Build parser from `foundry_datasets_cli.py` | Parse each paginated operation with `--page-size 10 --page-token tok --batch-pages 2` | Parser accepts all three flags | Args have `page_size=10`, `page_token="tok"`, `batch_pages=2` |
| TC-CLI-002 | Non-paginated operations do not require pagination flags | Build parser | Parse representative non-paginated operation without page flags | Required operation args still parse | No pagination-induced failure |
| TC-CLI-003 | CLI forwards page params to SDK | Mock client and invoke paginated operation | Run main path with page flags | SDK receives page params | SDK kwargs include `page_size` and `page_token`; batch behavior follows helper cases |

## Edge cases

| ID | Case | Expected handling |
|---|---|---|
| EC-001 | Empty page result with no next token | Returns empty list; metadata records `total_items=0` and no cursor |
| EC-002 | Response is dict with `items` key | Uses dict key, not `dict.items()` method |
| EC-003 | Response object exposes `items` and next token attributes | Attribute fallback works |
| EC-004 | Large `batch_pages` above cap | No more than 40 SDK calls |
| EC-005 | Unknown operation under metadata-only | Denied unless canonical allow-list row exists |
| EC-006 | Mutating verbs beyond create/update/delete (`publish`, `deploy`, `clear`, `build`) | Classified as writes and blocked by readonly |

## Negative cases

| ID | Case | Expected handling |
|---|---|---|
| NEG-001 | Operation `ENABLED=false` conflicts with `READONLY=false` override | Blocked by step 1 |
| NEG-002 | Namespace `ENABLED=false` conflicts with namespace `READONLY=false` override | Blocked by step 2 |
| NEG-003 | `READONLY=true` at operation level without parent readonly | Ignored per ADR-007 |
| NEG-004 | `datasets.file.content` under global metadata-only | Exit 8 through `AccessControlError` |
| NEG-005 | `datasets.dataset.read_table` under global metadata-only | Exit 8 through `AccessControlError` |
| NEG-006 | Zero or negative page size | Constructor rejects input |
| NEG-007 | Zero or negative batch pages | Constructor rejects input |
| NEG-008 | Lowercase `permitted`, unbackticked SDK path, or blocked allow-list row | Parser rejects row |

## Expected outputs

- Successful helper checks return normally; CLI smoke paths return exit code `0`.
- Access-control blocks raise `AccessControlError` and map to exit code `8`.
- User input validation for pagination constructor raises `ValueError` or `TypeError`; CLI parser failures map to user input exit code `1` when executed through CLI.
- Pagination metadata goes to stderr after exact separator `# ---metadata-start---`.
- Result payloads remain on stdout; stderr holds logs/metadata only.
- Batch output is an aggregated list of items from all fetched pages up to the cap or first missing next token.

## Test data

| Name | Value |
|---|---|
| Dataset RID | `ri.foundry.main.dataset.test` |
| File path | `/path/to/file.csv` |
| Page tokens | `tok1`, `tok2`, `cursor42` |
| ACL env override | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false` |
| Global readonly | `FOUNDRY_AGENTIC_CLI_READONLY=true` |
| Global metadata-only | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` |
| Allow-list permitted row | `` `datasets.dataset.get` \| PERMITTED `` |
| Allow-list blocked rows | `` `datasets.file.content` \| BLOCKED ``, `` `datasets.dataset.read_table` \| BLOCKED `` |

## Smoke and environment labels

| ID | Label | Scope | Dependency |
|---|---|---|---|
| TC-SMK-001 | Smoke, no external dependency | `pytest tests/test_access_control_guard.py` | Local Python only |
| TC-SMK-002 | Smoke, no external dependency | `pytest tests/test_pagination_helper.py` | Local Python only |
| TC-SMK-003 | Smoke, no external dependency | Parser-only datasets CLI cases | Local Python only |
| TC-SMK-004 | Environment-dependent | Real datasets CLI operation with live SDK client | Valid Foundry host/token and disposable resources |

## Existing automated coverage reviewed

- `tests/test_access_control_guard.py` covers all 8 precedence steps, `ENABLED=false` precedence, `READONLY=false` overrides, global metadata-only allow-list behavior, allow-list parser rules, ADR-007 readonly independence, write classification, and `AccessControlError` details.
- `tests/test_pagination_helper.py` covers dict/object extraction, page-size validation, page-token propagation, batch aggregation, hard max cap 40, no-next-token handling, and ADR-005 stderr metadata.
- `tests/test_foundry_datasets_cli.py` covers parser and CLI integration paths. TESTCASE-004 keeps a separate CLI exposure scenario so TESTEXEC-004 can confirm every paginated operation accepts `--page-size`, `--page-token`, and `--batch-pages`.

## Traceability to TESTCASE-004 acceptance criteria

| Acceptance criterion | Covered by |
|---|---|
| ACL precedence conflicts, `ENABLED=false`, `READONLY=false` overrides | TC-ACL-001 through TC-ACL-008 |
| Global metadata-only behavior for `file.content`, `dataset.get`, `read_table`, writes | TC-ACL-012 through TC-ACL-015 |
| Metadata allow-list parsing, canonical backticked SDK paths, `PERMITTED` only | TC-ACL-016 through TC-ACL-017 |
| Pagination CLI behavior for `--page-size`, `--page-token`, `--batch-pages` | TC-PAG-001 through TC-PAG-013, TC-CLI-001 through TC-CLI-003 |
| Invalid/zero page sizes, max batch cap, no next token, stderr separator, SDK propagation | TC-PAG-005 through TC-PAG-013 |
| Every paginated operation exposes all three flags | TC-CLI-001 |
| Smoke vs environment-dependent labels | TC-SMK-001 through TC-SMK-004 |

## Review gate

This is a test case design deliverable. TESTEXEC-004 should execute these scenarios after required review/approval and file defects for any failures before parent DEV-STORY-003 QA sign-off.

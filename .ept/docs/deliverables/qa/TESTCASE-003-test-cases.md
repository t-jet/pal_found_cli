# TESTCASE-003 — QA Test Cases for foundry-datasets Skill

**Parent:** DEV-STORY-005
**Status:** Open → In Progress (design phase)
**Author:** qa-engineer
**Date:** 2026-07-04
**Scope:** Functional, integration, edge, negative, boundary, and error-path verification of `.claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py` against DEV-STORY-005 acceptance criteria, SRS-001 ACs (AC-SMOKE, AC-ERR-AUTH, AC-RETRY, AC-ACL-BLOCK, AC-FMT-TOON), and ADRs 001, 002, 004, 005, 006, 007.

**Implementation under test:** `foundry_datasets_cli.py` (455 LOC). Resource clients: Dataset (11 ops), Branch (5), File (5), Transaction (6), View (6) — **33 operations total** (see Discrepancy D-1: ticket/SKILL header advertises 33; DEV-STORY-005 title and dispatch brief say 26).

---

## Coverage Matrix

| AC area | Test case IDs |
|---|---|
| Dataset resource (11 ops) | TC1.1–TC1.13 |
| Branch resource (5 ops) | TC2.1–TC2.7 |
| File resource (5 ops) | TC3.1–TC3.9 |
| Transaction resource (6 ops) | TC4.1–TC4.8 |
| View resource (6 ops) | TC5.1–TC5.8 |
| Access Control (ADR-007 / SRS AC-ACL-BLOCK, FR-ACL-5, FR-ACL-6) | TC6.1–TC6.8 |
| Retry integration (ADR-002 / SRS AC-RETRY) | TC7.1–TC7.4 |
| Output formatting (ADR-004 / AC-FMT-TOON, AC-SMOKE) | TC8.1–TC8.6 |
| Error handling & exit codes (ADR-001 / AC-ERR-AUTH) | TC9.1–TC9.9 |
| Logging / metadata (ADR-005 / NFR-IFACE-2) | TC10.1–TC10.4 |
| Configuration loading (ADR-006) | TC11.1–TC11.3 |
| CLI parser / arg routing | TC12.1–TC12.6 |
| Non-functional (NFR-PLAT, NFR-DIST, NFR-IFACE) | TC13.1–TC13.4 |
| Discrepancies (regression) | D-1…D-9 (see §Discrepancies) |

---

## TC1 — Dataset resource (`dataset ...`)

**Reference:** DEV-STORY-005 ops list; SRS §4.

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC1.1 | `dataset get` happy path | valid `dataset_rid`, mocked client returns Dataset object | exit 0, stdout JSON with dataset fields | exit 0; parseable JSON |
| TC1.2 | `dataset get` missing dataset_rid positional | `dataset get` (no RID) | argparse error, exit 1 | exit 1; stderr mentions usage |
| TC1.3 | `dataset create` requires `--name` and `--parent-folder-rid` | `dataset create` (no flags) | argparse error, exit 1 | exit 1 |
| TC1.4 | `dataset create` happy path | both required flags, mocked client | exit 0, JSON dataset | exit 0 |
| TC1.5 | `dataset get-schema` with `--branch-name` | valid RID + branch | branch passed through to client | kwarg `branch_name` on mock |
| TC1.6 | `dataset get-schema-batch` JSON array parsing | `--dataset-r '["ri.1","ri.2"]'` | list parsed and forwarded as `dataset_rids` | kwarg `dataset_rids == ["ri.1","ri.2"]` |
| TC1.7 | `dataset get-schema-batch` invalid JSON | `--dataset-r 'not json'` | `json.JSONDecodeError` propagates → exit 6 (ServerError) | exit 6 (see D-2: should arguably be exit 1 UserInputError) |
| TC1.8 | `dataset put-schema` parses `--schema` JSON | `--schema '{"type":"struct"}'` | schema dict forwarded | kwarg correct |
| TC1.9 | `dataset read-table` passes pagination params | `--page-size 50 --page-token tok` | kwargs forwarded | page_size=50, page_token="tok" |
| TC1.10 | `dataset transactions` list with pagination | valid RID + page flags | kwargs forwarded | page_size/page_token passed |
| TC1.11 | `dataset jobs` happy path | valid RID | exit 0 | JSON output |
| TC1.12 | `dataset get-health-checks` / `get-health-check-reports` / `get-schedules` pass branch | valid RID + `--branch-name` | kwarg forwarded | branch_name passed |
| TC1.13 | Unknown dataset operation | `dataset frobnicate` | argparse error, exit 1 | exit 1 |

## TC2 — Branch resource (`branch ...`)

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC2.1 | `branch create` requires `--name` | missing flag | argparse error, exit 1 | exit 1 |
| TC2.2 | `branch create` happy path | RID, name, optional `--transaction-rid` | kwargs forwarded | exit 0 |
| TC2.3 | `branch delete` requires `--branch-name` | missing | exit 1 | exit 1 |
| TC2.4 | `branch get` happy path | RID, branch name | exit 0 | JSON |
| TC2.5 | `branch list` paginated | RID + page flags | kwargs forwarded | exit 0 |
| TC2.6 | `branch transactions` passes branch + pagination | RID, branch, page flags | kwargs forwarded | exit 0 |
| TC2.7 | Unknown branch operation | `branch foo` | exit 1 | exit 1 |

## TC3 — File resource (`file ...`)

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC3.1 | `file content` happy path | RID, `--file-path`, `--branch-name` | kwargs incl. branch, start/end txn | exit 0 |
| TC3.2 | `file content` requires `--file-path` | missing | exit 1 | exit 1 |
| TC3.3 | `file upload` reads file bytes | existing local file path | `content=<bytes>` forwarded | upload called with bytes |
| TC3.4 | `file upload` missing file_path | missing flag | exit 1 | exit 1 |
| TC3.5 | `file upload` non-existent file | bad path | `FileNotFoundError` → exit 4 | exit 4 (matches handler) |
| TC3.6 | `file upload` raises ValueError when file_path None | args manipulated so file_path None | `ValueError("file_path is required...")` raised | exception raised (pre-invocation guard at L217) |
| TC3.7 | `file delete` / `file get` pass transaction_rid | RID, path, txn | kwargs forwarded | exit 0 |
| TC3.8 | `file list` paginated | RID + page flags | exit 0 | JSON |
| TC3.9 | Unknown file operation | `file foo` | exit 1 | exit 1 |

## TC4 — Transaction resource (`transaction ...`)

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC4.1 | `transaction create` happy path | RID, optional branch | exit 0 | JSON |
| TC4.2 | `transaction abort/commit/build/get/job` all require `--transaction-rid` | missing flag | exit 1 each | exit 1 |
| TC4.3 | `transaction abort` happy path | RID + txn rid | exit 0 | JSON |
| TC4.4 | `transaction commit` happy path | RID + txn rid | exit 0 | JSON |
| TC4.5 | `transaction build` happy path | RID + txn rid | exit 0 | JSON |
| TC4.6 | `transaction get` happy path | RID + txn rid | exit 0 | JSON |
| TC4.7 | `transaction job` happy path | RID + txn rid | exit 0 | JSON |
| TC4.8 | Unknown transaction operation | `transaction foo` | exit 1 | exit 1 |

## TC5 — View resource (`view ...`)

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC5.1 | `view create` requires `--name`, `--parent-folder-rid` | missing | exit 1 | exit 1 |
| TC5.2 | `view create` happy path | name, parent, optional `--backing-datasets` JSON | exit 0 | JSON |
| TC5.3 | `view get` happy path | `--view-dataset-rid` | exit 0 | JSON |
| TC5.4 | `view add-backing-datasets` parses `--backing-datasets` JSON | `'["ri.1"]'` | list forwarded | kwarg correct |
| TC5.5 | `view add-primary-key` parses `--primary-key` JSON | `'["col1"]'` | list forwarded | kwarg correct |
| TC5.6 | `view remove/replace-backing-datasets` happy path | view rid + backing datasets | exit 0 | JSON |
| TC5.7 | Invalid JSON in `--backing-datasets` | `'not json'` | propagates → exit 6 | exit 6 (see D-2) |
| TC5.8 | Unknown view operation | `view foo` | exit 1 | exit 1 |

## TC6 — Access Control (ADR-007, SRS FR-ACL-1…6, AC-ACL-BLOCK)

**Reference:** SRS L360–378, ADR-007.

| ID | Scenario | Env | Expected | Pass Criteria |
|---|---|---|---|---|
| TC6.1 | AC-ACL-BLOCK: op-level ENABLED=false | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_ENABLED=false` + `put-schema` | exit 8 | exit 8 |
| TC6.2 | AC-ACL deny: namespace ENABLED=false | `FOUNDRY_AGENTIC_CLI_DATASETS_ENABLED=false` + any op | exit 8 | exit 8 |
| TC6.3 | FR-ACL-5 step-3 override | `FOUNDRY_AGENTIC_CLI_READONLY=true` AND `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false` + `put-schema` | write permitted | operation reaches SDK |
| TC6.4 | FR-ACL-6 metadata-only deny | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` + `file content` (not in allow-list) | exit 8 with `AccessControlError` JSON | exit 8 |
| TC6.5 | Global READONLY=true blocks writes | READONLY=true + `dataset put-schema` | exit 8 | exit 8 |
| TC6.6 | Global READONLY=true permits reads | READONLY=true + `dataset get` | operation proceeds | exit 0 |
| TC6.7 | Default full access | no ACL env set | operation proceeds | exit 0 |
| TC6.8 | AccessControlError → exit 8 path | guard raises `AccessControlError` | exit 8, error envelope on stdout | exit 8 (matches code L389–393 and L423–427) |

## TC7 — Retry integration (ADR-002, SRS AC-RETRY)

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC7.1 | RetryHandler wraps `_invoke` (L413) | retryable exc retried | call count > 1 on transient |
| TC7.2 | `--timeout` overrides `cfg.timeout_s` | CLI flag wins | timeout kwarg from flag |
| TC7.3 | `cfg.timeout_s` used when no `--timeout` | config value used | timeout kwarg from cfg |
| TC7.4 | AC-RETRY: 429 twice then success | exit 0 after retries | exit 0 (depends on RetryHandler honoring 429 — see BUG-SUB-002) |

## TC8 — Output formatting (ADR-004, AC-FMT-TOON, AC-SMOKE)

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC8.1 | `--format json` forces JSON | JSON on stdout | parseable JSON |
| TC8.2 | `--format toon` forces TOON | TOON table | non-JSON table |
| TC8.3 | `--format auto` + uniform list → TOON | TOON | table format |
| TC8.4 | `--format auto` + dict → JSON | JSON | JSON |
| TC8.5 | `--pretty` indents JSON | multi-line | contains `\n` |
| TC8.6 | Pydantic v1/v2 model conversion via `_model_to_dict` | serializable dict | dict output |

## TC9 — Error handling & exit codes (ADR-001, AC-ERR-AUTH)

| ID | Scenario | Expected exit | Pass Criteria |
|---|---|---|---|
| TC9.1 | No resource positional → help printed | 1 | exit 1 (L364–366) |
| TC9.2 | No operation positional → help printed | 1 | exit 1 (L369–371, WARNING-3 fix) |
| TC9.3 | AC-ERR-AUTH: invalid token → SDK auth error | 2 | exit 2 |
| TC9.4 | `PermissionError` raised by SDK | 3 | exit 3 (L428–431) |
| TC9.5 | `FileNotFoundError` (file upload missing file) | 4 | exit 4 (L432–435) |
| TC9.6 | `TimeoutError` raised | 5 | exit 5 (L436–439) |
| TC9.7 | Generic SDK exception (500) | 6 | exit 6 (L447–450) |
| TC9.8 | `OSError` with errno 11/115 → rate limit | 7 | exit 7 (L440–446) |
| TC9.9 | Client factory failure → exit 9 | 9 | exit 9 (L396–402) |

## TC10 — Logging / metadata (ADR-005, NFR-IFACE-2)

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC10.1 | NDJSON log emitted to stderr on WARNING+ | one JSON line per log | valid JSON |
| TC10.2 | Metadata separator format | matches ADR-005 | exact string |
| TC10.3 | Stdout/stderr separation (NFR-IFACE-2) | result on stdout, diagnostics on stderr | streams separated |
| TC10.4 | `--log-level` from config honored | level applied | level matches env |

## TC11 — Configuration loading (ADR-006)

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC11.1 | `.env` at repo root loaded | vars available | loaded |
| TC11.2 | Env vars override `.env` | override wins | override |
| TC11.3 | Missing required config → configuration error | exit 9 | exit 9 |

## TC12 — CLI parser / arg routing

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC12.1 | Kebab→snake resolution via OP_MAP | correct method called | snake_case op |
| TC12.2 | `_resolve` default path for unmapped resource | op.replace("-","_") | snake_case |
| TC12.3 | `_get_client` returns Dataset for resource=dataset | same client | identity |
| TC12.4 | `_get_client` returns Branch/File/Transaction/View | correct attr | correct attr |
| TC12.5 | Unknown resource at top level | argparse error | exit 1 |
| TC12.6 | `--batch-pages` accepted (common parser) | parsed without error | arg present |

## TC13 — Non-functional (NFR-PLAT, NFR-DIST, NFR-IFACE)

| ID | Scenario | Expected | Pass Criteria |
|---|---|---|---|
| TC13.1 | Runs on Python 3.11 / 3.12 | no syntax/import errors | imports clean |
| TC13.2 | Runs on Windows/macOS/Linux | no OS-specific failures | platform-agnostic paths |
| TC13.3 | `_model_to_dict` handles nested list/dict/None | no crash | serialized |
| TC13.4 | Project-root discovery (L31–45) robust to relocation | finds package or graceful fallback | path resolved |

---

## Discrepancies (AC / Implementation conflicts)

Each discrepancy below is filed as a separate QUESTION ticket addressed to **architect**, with a Blocks link to DEV-STORY-005 and a Question link to TESTCASE-003 (same pattern as TESTCASE-001).

| ID | Discrepancy | Severity | Filed as |
|---|---|---|---|
| D-1 | **Operation count mismatch.** DEV-STORY-005 title says "26 operations"; implementation and SKILL.md advertise **33 operations** (Dataset 11, Branch 5, File 5, Transaction 6, View 6). Dispatch brief also said "26". Either the AC count is stale or 7 operations were added without an AC update. | Critical | QUESTION-015 |
| D-2 | **Invalid JSON args → wrong exit code.** `json.loads(...)` on `--dataset-r`, `--schema`, `--backing-datasets`, `--primary-key` raises `json.JSONDecodeError` (a `ValueError`) which is NOT caught at parse time — it propagates to `retry_handler.execute` and then to the generic `except Exception` (L447) returning **exit 6 ServerError**. ADR-001 expects user-input validation errors → **exit 1 UserInputError**. | High | QUESTION-016 |
| D-3 | **`--dataset-r` flag name is ambiguous/truncated.** The `get-schema-batch` parser registers `--dataset-r` (singular, dest=`dataset_rids`). SKILL.md example uses `--dataset-r`. AC/SRS convention and every other RID flag use `--dataset-rids` or `--dataset-rid`. Naming is inconsistent and easy to mistype. | Medium | QUESTION-017 |
| D-4 | **PaginationHelper documented but unused.** SKILL.md "Architecture" section lists `PaginationHelper` implementing `--page-size`, `--page-token`, `--batch-pages`. The CLI parses these flags and passes `page_size`/`page_token` to the SDK but **never performs batch paging** (`--batch-pages` is parsed and ignored). SRS `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` and ADR-003 batch strategy are not honored. | High | QUESTION-018 |
| D-5 | **`file upload` reads entire file into memory.** L218–220 does `fobj.read()` then forwards `content=<bytes>`. SRS `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` (1.5 MB) bound exists for downloads but **no upload size guard**. Large uploads may exhaust memory or exceed SDK limits. | Medium | QUESTION-019 |
| D-6 | **No `--download-path` / binary envelope handling.** SRS lists `FOUNDRY_AGENTIC_CLI_DOWNLOAD_PATH` and NFR-IFACE/AC-SMOKE imply binary download envelopes (JSON). The CLI does not write binaries to disk and does not check `MAX_DOWNLOAD_BYTES` for `file content` / `file get`. | Medium | QUESTION-020 |
| D-7 | **`OSError` rate-limit heuristic is fragile.** L444 maps `errno in (11, 115)` to exit 7. EAGAIN/EWOULDBLOCK is 11 on Linux but the SDK raises HTTP 429 as an `HttpError`/`ApiError`, not `OSError`. This branch is likely dead code; actual 429 will fall through to exit 6. | Medium | QUESTION-021 |
| D-8 | **Missing `AccessControlError` import path test.** `AccessControlError` is imported from `access_control_guard` (L58) but ADR-001 exit code 8 mapping in `ErrorSerializer` was flagged unreachable in TESTCASE-001 (BUG-SUB-004). The datasets CLI relies on its own explicit `except AccessControlError` handler (L389, L423) returning `EXIT_ACCESS_CONTROL` directly — bypassing `ErrorSerializer.serialize`. Verify the envelope on stdout still contains the ADR-001 schema fields. | Medium | QUESTION-022 |
| D-9 | **No request timeout enforcement.** `--timeout` / `cfg.timeout_s` is forwarded as `request_timeout=` kwarg to the SDK, but there is no `asyncio.wait_for()` wrapper (consistent with BUG-SUB-001). If the SDK ignores `request_timeout`, the call can hang indefinitely. | Medium | QUESTION-023 |

---

## Notes

- All test cases are **acceptance/QA test cases** (black-box, CLI-level). They complement the 96 unit tests at 91.91% line coverage and are intended for execution against a real or mock Foundry instance during the QA phase.
- Discrepancies D-1 through D-9 are each tracked in a QUESTION ticket and must be resolved before TESTCASE-003 can move to Resolved.

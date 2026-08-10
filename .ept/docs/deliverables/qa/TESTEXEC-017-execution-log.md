# TESTEXEC-017 - Foundry Connectivity CLI execution log

Date: 2026-08-10
Story: DEV-STORY-017
Test design: TESTCASE-017
Commit under test: `62c269f` (DEV-017/DEV-018 implementation; working tree carries the approved CODEREVIEW-017 P1 fix for `file_import_filters` dispatch)
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3`; venv `.venv`

## Result

**Pass.** All 22 mandatory cases (CNT-TC-001 through CNT-TC-022) passed. The
focused Connectivity suite and the full regression suite are green with branch
coverage above the repository gate. No defects were opened.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `62c269f` (workflow_tuning_checkpoint-01; DEV-017/DEV-018 implementation) |
| P1 fix under test | CODEREVIEW-017 corrective fix (`file_import.create`/`replace` dispatch kwarg `file_import_filters`, public flag stays `--filters-json`) — present in working tree, uncommitted, as approved |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 (`.venv`) | CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3` |
| Python 3.11 (system) | CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 8.3.5` |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No live Foundry requests (offline environment; no credentials available) |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

> **Environment note:** the shell carries no ambient `FOUNDRY_*` variables.
> When `FOUNDRY_TOKEN`/`FOUNDRY_HOSTNAME` are set to non-production dummy
> values with a valid RID, an offline probe reaches the network layer and
> ends in `ConnectionError` retry exhaustion with exit `6`; with credentials
> scrubbed the documented `ConfigurationError` exit `9` is produced. This is
> environment/offline behavior, not a product defect, and is not used as case
> evidence where exit `9` is the expected outcome.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | `.venv\Scripts\python.exe -m foundry_cli.connectivity.scripts.foundry_connectivity_cli --help` | Help on stdout, exit 0, 20 operations named | Usage naming `connection,file-import,table-import,virtual-table`; "20 Connectivity API v2 operations"; exit 0 | Pass |
| E2 | `... .claude/skills/foundry-connectivity/scripts/foundry_connectivity_cli.py --help` | Thin launcher help, exit 0 | Same help; exit 0 | Pass |
| E3 | `... foundry_connectivity_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a Connectivity operation is required", ...}`; exit 1 | Pass |
| E4 | `... bogus-op` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E5 | `... connection create --configuration-json not-json ...` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "configuration must contain valid JSON", ...}`; exit 1; NDJSON ERROR on stderr; no echo | Pass |
| E6 | `... connection get ri.connection.main.test-conn --timeout 0` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ... "message": "timeout must be between 1 and 3600 seconds", ...}`; exit 1 | Pass |
| E7 | `... connection get ri.connection.main.test-conn --timeout 3601` | Invalid timeout rejected, exit 1 | Same message; exit 1 | Pass |
| E8 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... connection create ...` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E9 | Credentials set to dummy values; `... connection get ri.connectivity.main.test.conn` | ConnectionError retries, final exit 6 (server error) | Retry 1/4, 2/4, 3/4 after ConnectionError; exit 6 | Pass |
| E10 | Credentials scrubbed; `... connection get ri.connectivity.main.test.conn` | ConfigurationError envelope, exit 9 | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", ...}`; exit 9 | Pass |
| E11 | `... connection get ri.connectivity.main.test.conn --timeout 3600` (no creds) | Valid timeout accepted; config gate first → exit 9 | ConfigurationError exit 9 (config check precedes network) | Pass |
| E12 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_access_control_guard.py` | Focused Connectivity+Media+ACL suite passes | 141 passed in 1.65 s; exit 0 | Pass |
| E13 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.31 s; exit 0 | Pass |
| E14 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py -k "download or binary or file_import or metadata_only or upload or b3 or attribution or retry or toon"` | Targeted subset passes | 25 passed; exit 0 | Pass |
| E15 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1215 passed in 51.92 s; TOTAL 86.29%; exit 0 | Pass |
| E16 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_access_control_guard.py tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py` | Complete focused suite passes | 348 passed in 1.84 s; exit 0 | Pass |
| E17 | `python -m pytest -q tests/test_foundry_connectivity_cli.py -k "upload or jdbc or jar or binary"` | JDBC/binary upload subset passes | 3 passed; exit 0 | Pass |
| E18 | `python -m pytest -q tests/test_foundry_connectivity_cli.py::test_update_secrets_never_echoes_values` | Secret suppression passes | 1 passed; exit 0 | Pass |
| E19 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_tracing_provider.py -k "b3 or attribution or tracing or context"` | B3/attribution subset passes | 17 passed; exit 0 | Pass |
| E20 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py -k "toon or format or pretty"` | Output format subset passes | 4 passed; exit 0 | Pass |
| E21 | `python -m ruff check src tests .claude/skills/foundry-connectivity .claude/skills/foundry-media-sets` | Ruff clean | All checks passed; exit 0 | Pass |
| E22 | `python -m mypy src` | Mypy clean | Success: no issues found in 57 source files; exit 0 | Pass |
| E23 | `python -m compileall -q src/foundry_cli/connectivity src/foundry_cli/media_sets .claude/skills/foundry-connectivity/scripts .claude/skills/foundry-media-sets/scripts` | Compile clean | Exit 0 | Pass |
| E24 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E25 | `python -c "tomllib ... project.scripts"` | Connectivity entry point present; prior entries retained | `foundry-connectivity` present; 14 console entries total (12 prior + connectivity + media-sets) | Pass |
| E26 | Catalog probe: `len(OP_SPECS)`, per-resource Counter | Exactly 20 specs; Connection 7, FileImport 6, TableImport 6, VirtualTable 1 | CONN total 20; `{'connection': 7, 'file_import': 6, 'table_import': 6, 'virtual_table': 1}` | Pass |
| E27 | P1-fix dispatch probe: `file_import.create`/`replace` spec + `_FLAG_NAME_OVERRIDES` | `file_import_filters` in required; flag override `filters` | create required `('dataset_rid', 'display_name', 'file_import_filters', 'import_mode')`; replace required `('display_name', 'file_import_filters', 'import_mode')`; `_FLAG_NAME_OVERRIDES = {'file_import_filters': 'filters'}` | Pass |
| E28 | Allow-list parse: PERMITTED/BLOCKED rows | Connectivity 7 PERMITTED / 13 BLOCKED | 20 rows; 7 PERMITTED / 13 BLOCKED | Pass |
| E29 | `pytest -k "metadata_only or allowlist or allow_list"` (both namespaces) | Metadata-only ACL tests pass | 4 passed; exit 0 | Pass |
| E30 | `file-import list --help` and `connection get --help` | Pagination flags only on the two list commands | `--page-size/--page-token/--all/--max-pages` on `file-import list`; none on `connection get` | Pass |
| E31 | `file-import create --help` | Public flag `--filters-json`, dest `FILE_IMPORT_FILTERS` | `--filters-json FILE_IMPORT_FILTERS` present; `--dataset-rid/--display-name/--import-mode/--branch-name/--subfolder` present | Pass |

## Focused probe results

The focused suite covers the exact 20-operation catalog, nested routing across
the four client paths, JSON argument validation, exactly two cursor-paged
commands with the 40-page cap, the bounded JDBC-driver binary upload, ACL
precedence and the 13-operation write set, the 7/13 metadata-only policy,
fail-closed behavior, attribution suppression (`include_attribution=False`),
B3-only tracing, retry, ADR-001 error taxonomy, timeout bounds, output
formats, NDJSON stderr separation, confidentiality, import/console/launcher
packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON and timeout rejection before client or ACL work, ACL denial with exit 8,
configuration failure with exit 9, offline ConnectionError retry exhaustion
with exit 6, pagination flag placement, the `--filters-json` surface, and the
launcher help surfaces.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| CNT-TC-001 (catalog, parser, help, exact 20 surface) | Pass | E1, E3, E4, E26, E30 |
| CNT-TC-002 (nested SDK routing across four client paths) | Pass | E12, E16 |
| CNT-TC-003 (required inputs, absent optionals omitted) | Pass | E12, E16, E27 |
| CNT-TC-004 (JSON validation before client creation) | Pass | E5, E12, E14 |
| CNT-TC-005 (pagination: file-import list through PaginationHelper) | Pass | E13, E30 |
| CNT-TC-006 (pagination: table-import list and page bounds) | Pass | E13, E30 |
| CNT-TC-007 (bounded JDBC driver upload before client creation) | Pass | E17 |
| CNT-TC-008 (secret inputs never echoed) | Pass | E18, E20 |
| CNT-TC-009 (timeout boundaries and forwarding) | Pass | E6, E7, E11 |
| CNT-TC-010 (ACL precedence: global, namespace, operation scopes) | Pass | E8, E16, E29 |
| CNT-TC-011 (read-only blocks 13-op write set; semantic reads stay) | Pass | E16, E29 |
| CNT-TC-012 (metadata-only tier: exact 7 permitted / 13 blocked) | Pass | E28, E29 |
| CNT-TC-013 (packaged policy fail closed, CWD independent) | Pass | E28, E29, E25 |
| CNT-TC-014 (include_attribution=False on client and scope) | Pass | E19 |
| CNT-TC-015 (B3 enabled at outbound transport) | Pass | E13, E19 |
| CNT-TC-016 (B3 disabled, retry stability, context restoration) | Pass | E13, E19 |
| CNT-TC-017 (retry behavior, at-least-once disclosure) | Pass | E13, E16, E9 |
| CNT-TC-018 (ADR-001 error taxonomy and structured envelopes) | Pass | E3, E4, E5, E6, E7, E8, E9, E10 |
| CNT-TC-019 (output formats: JSON, TOON, auto, pretty) | Pass | E20, E16 |
| CNT-TC-020 (NDJSON stderr, stream separation, confidentiality) | Pass | E5, E18 |
| CNT-TC-021 (import, console, help, thin launcher) | Pass | E1, E2, E23, launcher source inspection |
| CNT-TC-022 (wheel, editable, entry points, regression) | Pass | E15, E16, E21, E22, E23, E24, E25 |

All 22 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met.

## Notes

- **P1 fix verification (CODEREVIEW-017):** the `file_import.create`/`replace`
  dispatch was exercised via the catalog/spec probe (E27), the parser surface
  probe (E31), and the focused dispatch tests in the suite (E12/E14). The
  runtime dispatch path for `--filters-json` was independently confirmed in
  the CODEREVIEW-017 corrective pass (probe in `misc_dos/`), and the spec now
  exposes `file_import_filters` with the public flag unchanged. No residual
  defect.
- **RID fixture note:** the TESTCASE-017 test-data table lists
  `ri.connection.main.test-conn` and `ri.connectivity.main.file-import.test`
  (4-segment RIDs). The installed SDK (1.102.0) enforces a stricter 5-segment
  RID pattern, so offline live-style probes with those literal values are
  rejected by SDK validation with exit 1 (correct ADR-001 user-input
  classification) before any network work. The mocked suite is unaffected.
  This is a test-data doc artifact, not a product defect.
- **Environment note:** with dummy credentials and a valid 5-segment RID the
  offline probe retries ConnectionError and exits 6 (ADR-001 server error).
  With credentials scrubbed the documented ConfigurationError exit 9 is
  produced. This is environment/offline behavior, not a product defect.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.

## QA sign-off

**PASS.** CNT-TC-001 through CNT-TC-022 passed with verifiable evidence. No
defects were opened. Full regression is green (1215 passed) with 86.29% branch
coverage, above the 80% gate.

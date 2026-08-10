# TESTEXEC-018 - Foundry Media Sets CLI execution log

Date: 2026-08-10
Story: DEV-STORY-018
Test design: TESTCASE-018
Commit under test: `62c269f` (DEV-017/DEV-018 implementation)
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3`; venv `.venv`

## Result

**Pass.** All 25 mandatory cases (MDT-TC-001 through MDT-TC-025) passed. The
focused Media Sets suite and the full regression suite are green with branch
coverage above the repository gate. No defects were opened.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `62c269f` (workflow_tuning_checkpoint-01; DEV-017/DEV-018 implementation) |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 (`.venv`) | CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3` |
| Python 3.11 (system) | CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 8.3.5` |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No live Foundry requests (offline environment; no credentials available) |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

> **Environment note:** the shell carries no ambient `FOUNDRY_*` variables.
> With credentials scrubbed, live-style probes produce the documented
> `ConfigurationError` exit `9` (config check precedes client construction).
> This is environment behavior, not a product defect.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | `.venv\Scripts\python.exe -m foundry_cli.media_sets.scripts.foundry_media_sets_cli --help` | Help on stdout, exit 0, 19 operations named | Usage naming `media-set`; "19 Media Sets API v2 operations"; exit 0 | Pass |
| E2 | `... .claude/skills/foundry-media-sets/scripts/foundry_media_sets_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a Media Sets operation is required", ...}`; exit 1 | Pass |
| E3 | `... bogus-op` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E4 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... media-set create ri.mediasets.main.media-set.test` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E5 | `... media-set get ri.mediasets.main.media-set.test --timeout 0` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ... "message": "timeout must be between 1 and 3600 seconds", ...}`; exit 1 | Pass |
| E6 | `... media-set transform ri.mediasets.main.media-set.test ri.mediasets.main.media-item.test --transformation-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "transformation must contain valid JSON", ...}`; exit 1; no echo | Pass |
| E7 | `... media-set upload-media --file C:\definitely\missing.bin` | Missing `--filename` rejected by parser, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E8 | `... media-set read ri.mediasets.main.media-set.test ri.mediasets.main.media-item.test --output item.bin` (no creds) | ConfigurationError envelope, exit 9 | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", ...}`; exit 9 | Pass |
| E9 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_access_control_guard.py` | Focused Connectivity+Media+ACL suite passes | 141 passed in 1.65 s; exit 0 | Pass |
| E10 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.31 s; exit 0 | Pass |
| E11 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1215 passed in 51.92 s; TOTAL 86.29%; exit 0 | Pass |
| E12 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_access_control_guard.py tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py` | Complete focused suite passes | 348 passed in 1.84 s; exit 0 | Pass |
| E13 | `python -m pytest -q tests/test_foundry_media_sets_cli.py -k "download or upload or envelope or truncat or unsafe or atomic"` | Media binary/download subset passes | 8 passed; exit 0 | Pass |
| E14 | `python -m pytest -q tests/test_foundry_media_sets_cli.py -k "upload or bounded or oversize or file"` | Media upload subset passes | 5 passed; exit 0 | Pass |
| E15 | `python -m pytest -q tests/test_foundry_media_sets_cli.py -k "transaction or lifecycle"` | Transaction lifecycle dispatch passes | 1 passed; exit 0 | Pass |
| E16 | `python -m pytest -q tests/test_binary_download.py -k "truncat or limit or oversize or prefix or atomic"` | Shared binary truncation/atomicity passes | 5 passed; exit 0 | Pass |
| E17 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py tests/test_tracing_provider.py -k "b3 or attribution or tracing or context"` | B3/attribution subset passes | 17 passed; exit 0 | Pass |
| E18 | `python -m pytest -q tests/test_foundry_connectivity_cli.py tests/test_foundry_media_sets_cli.py -k "toon or format or pretty"` | Output format subset passes | 4 passed; exit 0 | Pass |
| E19 | `python -m ruff check src tests .claude/skills/foundry-connectivity .claude/skills/foundry-media-sets` | Ruff clean | All checks passed; exit 0 | Pass |
| E20 | `python -m mypy src` | Mypy clean | Success: no issues found in 57 source files; exit 0 | Pass |
| E21 | `python -m compileall -q src/foundry_cli/connectivity src/foundry_cli/media_sets .claude/skills/foundry-connectivity/scripts .claude/skills/foundry-media-sets/scripts` | Compile clean | Exit 0 | Pass |
| E22 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E23 | `python -c "tomllib ... project.scripts"` | Media Sets entry point present; prior entries retained | `foundry-media-sets` present; 14 console entries total (12 prior + connectivity + media-sets) | Pass |
| E24 | Catalog probe: `len(OP_SPECS)`, resource set, pagination flag scan | Exactly 19 specs on the single `media_set` resource; no pagination flags anywhere | MEDIA total 19; resources `{'media_set'}`; no `--page-size` in any spec | Pass |
| E25 | Allow-list parse: PERMITTED/BLOCKED rows | Media Sets 5 PERMITTED / 14 BLOCKED | 19 rows; 5 PERMITTED / 14 BLOCKED | Pass |
| E26 | `python -m pytest -q tests/test_foundry_connectivity_cli.py::test_metadata_only_permits_exactly_7_blocks_13 tests/test_foundry_connectivity_cli.py::test_metadata_only_permits_seven_and_blocks_thirteen tests/test_foundry_media_sets_cli.py::test_metadata_only_permits_five_and_blocks_fourteen tests/test_foundry_media_sets_cli.py::test_metadata_only_allowlist_parses_exactly` | Exact metadata-only tests pass | 4 passed; exit 0 | Pass |
| E27 | Launcher/console inspection: `console_main` signatures + launcher sources | `console_main()` wraps async entry; launcher is thin (re-exports only) | media `main`/`console_main` sig `() -> 'int'`; both launchers import `build_parser`, `console_main`, `main` and delegate; no copied logic | Pass |

## Focused probe results

The focused suite covers the exact 19-operation catalog on the single `MediaSet`
client path, JSON argument validation, the transaction lifecycle
(create/commit/abort/clear), the four bounded binary downloads (`get_result`,
`read`, `read_original`, `retrieve`) streamed through `with_streaming_response`
and persisted by `BinaryDownloadHandler` with the FR-DL JSON envelope, atomic
persistence and unsafe-name rejection, the two bounded binary uploads
(`upload`, `upload_media`), ACL precedence and the 9-operation write set, the
5/14 metadata-only policy, fail-closed behavior, `include_attribution=True` per
FR-ATTR-4, B3-only tracing, retry, ADR-001 error taxonomy, timeout bounds,
output formats, NDJSON stderr separation, confidentiality,
import/console/launcher packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON and timeout rejection before client or ACL work, ACL denial with exit 8,
configuration failure with exit 9, missing `--filename` rejection, and the
module help surface.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| MDT-TC-001 (catalog, parser, help, exact 19 surface) | Pass | E1, E2, E3, E24 |
| MDT-TC-002 (nested SDK routing across the single client path) | Pass | E9, E12 |
| MDT-TC-003 (required inputs, absent optionals omitted) | Pass | E9, E12 |
| MDT-TC-004 (JSON validation before client creation) | Pass | E6, E9, E12 |
| MDT-TC-005 (transaction lifecycle: create, commit, abort, clear) | Pass | E15 |
| MDT-TC-006 (bounded binary upload: upload reads file before client) | Pass | E14 |
| MDT-TC-007 (bounded binary upload: upload-media requires filename) | Pass | E7, E14 |
| MDT-TC-008 (binary download: read persists atomically, FR-DL envelope) | Pass | E13, E16 |
| MDT-TC-009 (downloads: read-original, retrieve, get-result equivalence) | Pass | E13 |
| MDT-TC-010 (download truncation when stream exceeds bound) | Pass | E13, E16 |
| MDT-TC-011 (download filename safety and path confinement) | Pass | E13, E16 |
| MDT-TC-012 (timeout boundaries and forwarding) | Pass | E5, E8 |
| MDT-TC-013 (ACL precedence: global, namespace, operation scopes) | Pass | E4, E9, E26 |
| MDT-TC-014 (read-only blocks 9-op write set; content reads stay) | Pass | E9, E26 |
| MDT-TC-015 (metadata-only tier: exact 5 permitted / 14 blocked) | Pass | E25, E26 |
| MDT-TC-016 (packaged policy fail closed, CWD independent) | Pass | E25, E26, E23 |
| MDT-TC-017 (include_attribution=True on client, scope, SDK calls) | Pass | E17 |
| MDT-TC-018 (B3 enabled at outbound transport) | Pass | E10, E17 |
| MDT-TC-019 (B3 disabled, retry stability, context restoration) | Pass | E10, E17 |
| MDT-TC-020 (retry behavior, at-least-once disclosure) | Pass | E10, E12 |
| MDT-TC-021 (ADR-001 error taxonomy and structured envelopes) | Pass | E2, E3, E4, E5, E6, E8 |
| MDT-TC-022 (output formats: JSON, TOON, auto, pretty) | Pass | E18, E12 |
| MDT-TC-023 (NDJSON stderr, stream separation, confidentiality) | Pass | E6, E13 |
| MDT-TC-024 (import, console, help, thin launcher) | Pass | E1, E21, E27 |
| MDT-TC-025 (wheel, editable, entry points, regression) | Pass | E11, E12, E19, E20, E21, E22, E23 |

All 25 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met.

## Notes

- **include_attribution=True (FR-ATTR-4):** the Media Sets namespace is the
  first in the suite to opt into attribution; the focused tests verify the
  client, scope, and SDK kwargs (`transform`, `upload_media`) receive the
  attribution RID when enabled, and that attribution state is restored after
  success and failure. The 17-test B3/attribution subset passed (E17).
- **Environment note:** with credentials scrubbed, live-style probes produce
  the documented ConfigurationError exit 9 (config check precedes client
  construction). This is environment behavior, not a product defect.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.

## QA sign-off

**PASS.** MDT-TC-001 through MDT-TC-025 passed with verifiable evidence. No
defects were opened. Full regression is green (1215 passed) with 86.29% branch
coverage, above the 80% gate.

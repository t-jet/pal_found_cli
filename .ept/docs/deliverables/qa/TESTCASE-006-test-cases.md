# TESTCASE-006 - QA test cases for Foundry Ontologies CLI

**Parent:** DEV-STORY-007  
**Author:** qa-engineer  
**Date:** 2026-07-28  
**Design basis:** SAD-001 DEV-STORY-007 scope, canonical environment variable reference, ADR-001, ADR-002, ADR-004, ADR-005, ADR-007, DESIGN-005 shared common contracts  
**Implementation verified:** `src/foundry_cli/ontologies/scripts/foundry_ontologies_cli.py`, `src/foundry_cli/ontologies/scripts/__init__.py`, `pyproject.toml` console entry point

## Scope

This deliverable defines QA coverage for DEV-STORY-007, the `foundry-ontologies` CLI namespace. The implemented scope is 67 canonical Foundry Ontologies API v2 operations across these resource groups:

| Resource group | Operation count |
|---|---:|
| `action` | 3 |
| `action_type` | 4 |
| `action_type_full_metadata` | 2 |
| `attachment` | 4 |
| `attachment_property` | 4 |
| `cipher_text_property` | 1 |
| `geotemporal_series_property` | 2 |
| `linked_object` | 2 |
| `media_reference_property` | 3 |
| `object_type` | 7 |
| `ontology` | 4 |
| `ontology_interface` | 8 |
| `ontology_object` | 5 |
| `ontology_object_set` | 7 |
| `ontology_transaction` | 1 |
| `ontology_value_type` | 2 |
| `query` | 1 |
| `query_type` | 2 |
| `time_series_property_v2` | 3 |
| `time_series_value_bank_property` | 2 |
| **Total** | **67** |

Coverage includes operation catalog integrity, parser exposure, SDK dispatch, pagination, binary upload/download, ACL enforcement, retry, error serialization, JSON/TOON output, console wrapper/package entry point, and B3-only tracing.

Tracing coverage must validate SDK-native B3 multi-header propagation through the shared invocation scope. W3C `traceparent`/`tracestate` is out of scope for this story.

## Coverage matrix

| Area | Test case IDs | Count |
|---|---|---:|
| Catalog, parser, dispatch for all 67 operations | TC-ONT-CAT-001 through TC-ONT-CAT-003 | 3 |
| Client routing and argument coercion | TC-ONT-DSP-001 through TC-ONT-DSP-004 | 4 |
| Pagination | TC-ONT-PAG-001 through TC-ONT-PAG-003 | 3 |
| Binary upload/download | TC-ONT-BIN-001 through TC-ONT-BIN-005 | 5 |
| ACL, retry, errors, output, tracing | TC-ONT-RUN-001 through TC-ONT-RUN-007 | 7 |
| Console wrapper and packaging | TC-ONT-PKG-001 through TC-ONT-PKG-003 | 3 |
| **Total designed cases** | | **25** |

## Preconditions

- Python 3.11 or 3.12 with project test dependencies installed.
- `src/` available on `PYTHONPATH`.
- No live Foundry credentials required; tests use mocked SDK clients, async fakes, and temporary files.
- Shared common components are available: `ConfigLoader`, `AccessControlGuard`, `AsyncClientFactory`, `RetryHandler`, `PaginationHelper`, `BinaryDownloadHandler`, `OutputFormatter`, and `ErrorSerializer`.
- Reference contracts: ADR-001 exit codes, ADR-002 timeouts, ADR-004 JSON/TOON selection, ADR-005 stderr metadata/log format, ADR-007 operation-level ACL independence, and DESIGN-005 B3 tracing/binary handling.

## Test scenarios

| ID | Scenario | Given | When | Then | Expected result |
|---|---|---|---|---|---|
| TC-ONT-CAT-001 | Catalog has exactly 67 operations | `OP_SPECS` is loaded | Catalog entries are counted by `(resource, operation)` | No duplicate pair exists | 67 total specs and 67 unique operation keys |
| TC-ONT-CAT-002 | Parser exposes every canonical operation | Each spec supplies a resource, operation, and positional arguments | `build_parser().parse_args()` receives kebab-case resource/operation names | The parser accepts the command | Parsed resource/operation match the catalog; common options like `--timeout` and `--format` bind correctly |
| TC-ONT-CAT-003 | Catalog identifies paginated operations | Specs containing both `page_size` and `page_token` are selected | `PAGINATED_OPS` is built | The set matches the catalog | 16 operations are paginated, including `ontology_object.list` and `query_type.list` |
| TC-ONT-DSP-001 | Dispatch covers all catalog operations | A fake client method exists for each spec | `_invoke()` runs for every operation | The configured SDK method is awaited once | `request_timeout` is forwarded; positional and optional args map to SDK kwargs |
| TC-ONT-DSP-002 | Nested SDK clients route correctly | Mock SDK root has `ontologies.Action`, `ontologies.Ontology.ActionType`, and `ontologies.Ontology.QueryType` | `_get_client()` resolves resource clients | The resource receives the right nested client | Root and nested resources do not cross-route |
| TC-ONT-DSP-003 | JSON CLI arguments deserialize before SDK call | JSON-bearing args such as `parameters`, `requests`, `select`, `where`, `object_set`, and `attribution` are supplied as strings | `_invoke()` builds kwargs | JSON strings become Python objects | Invalid JSON raises `ValueError` and maps to exit 1 through `main()` |
| TC-ONT-DSP-004 | Kebab CLI names resolve to snake SDK names | CLI operation name contains hyphens | `_resolve()` runs | Operation name is normalized | `get-full-metadata` resolves to `get_full_metadata` |
| TC-ONT-PAG-001 | Paginated invocation batches pages | SDK returns items plus `next_page_token` | `_invoke_paginated()` runs with `PaginationHelper(batch_pages=2)` | Two pages are fetched | Items aggregate in order; helper records pages fetched and next token |
| TC-ONT-PAG-002 | Pagination helper handles dict responses | SDK returns dict pages with `"items"` and `next_page_token` | Helper extracts data | Dict keys are used, not the dict `.items()` method | Items and tokens are correct, including no-token final page |
| TC-ONT-PAG-003 | Pagination metadata emits to stderr | Helper has page count, item count, page size, and optional next token | `emit_metadata()` runs after successful output | ADR-005 separator and JSON metadata are written to stderr | `next_page_token` is present only when more pages remain |
| TC-ONT-BIN-001 | Attachment upload reads body file | `attachment upload` has `--body-file` and no explicit content metadata | `_invoke()` runs | File bytes are sent as first body arg | `content_length` defaults to byte length; `content_type` defaults to `application/octet-stream` |
| TC-ONT-BIN-002 | Attachment upload validates filename | `attachment upload` lacks filename | `_invoke()` runs | Validation fails before SDK call | `ValueError("filename is required...")`; `main()` returns exit 1 |
| TC-ONT-BIN-003 | Media reference upload omits attachment headers | `media_reference_property upload` has a body file | `_invoke()` runs | File bytes are sent | `content_length` and `content_type` are not injected for this resource |
| TC-ONT-BIN-004 | Binary downloads use bounded download handler | Download operations return bytes or streams | `_invoke()` detects `binary_download=True` | Result is saved by `BinaryDownloadHandler` | Output is the download envelope from `to_dict()` |
| TC-ONT-BIN-005 | Download accepts sync and async chunk iterators | SDK returns bytes, sync iterator, or async iterator | `_bytes_iter()` wraps result | Handler consumes bytes uniformly | No chunk is dropped; handler, not CLI code, owns path safety and truncation behavior |
| TC-ONT-RUN-001 | Main success path uses ACL, retry, output, and B3 scope | Mock config, ACL guard, factory invocation scope, retry handler, and SDK client are installed | `main()` executes `ontology get --format json` | The operation succeeds | ACL checks `("ontology", "get")`; retry wraps invocation; B3 invocation scope is entered; JSON prints to stdout; exit 0 |
| TC-ONT-RUN-002 | ACL denial stops before SDK call | ACL guard raises `AccessControlError` | `main()` runs | Error is serialized | Exit 8; SDK client is not invoked |
| TC-ONT-RUN-003 | User input errors serialize consistently | Upload is missing required CLI input or JSON args are invalid | `main()` catches `ValueError` | Error is serialized | Exit 1 per ADR-001 |
| TC-ONT-RUN-004 | Permission, not-found, timeout, rate-limit, and server errors map to taxonomy | Retry-wrapped invocation raises representative exceptions | `main()` catches each exception | ErrorSerializer handles output | Exit codes: 3 permission, 4 not found, 5 timeout, 7 rate limit for retryable `OSError`, 6 server fallback |
| TC-ONT-RUN-005 | Retry applies around dispatch | Retry handler is mocked and records calls | `main()` invokes any operation | Invocation function is passed to retry | Transient handling stays in `RetryHandler`; CLI does not reimplement retry logic |
| TC-ONT-RUN-006 | JSON and TOON output both work | Formatter receives a dict and a list of homogeneous dicts | `OutputFormatter` formats output | Valid text is returned | JSON contains quoted keys; auto/TOON path produces compact tabular text when suitable |
| TC-ONT-RUN-007 | Skill and runtime wording remain B3-only | Skill text and invocation scope are inspected | Tests scan text and success path | No W3C contract appears | `B3` appears; `W3C` does not appear in the ontology skill text |
| TC-ONT-PKG-001 | Packaged module exposes catalog | `foundry_cli.ontologies.scripts.foundry_ontologies_cli` is imported | Catalog is inspected | Public module has the same operation spec | 67 operations and expected `ontology.get` method |
| TC-ONT-PKG-002 | Console wrapper returns async main exit code | `main()` is monkeypatched to return 31 | `console_main()` runs | `asyncio.run(main())` result is returned | Exit code 31 is propagated |
| TC-ONT-PKG-003 | Package entry point is registered | `pyproject.toml` is inspected | Console scripts are read | `foundry-ontologies` maps to packaged module | Entry point target is `foundry_cli.ontologies.scripts.foundry_ontologies_cli:console_main` |

## Edge cases

| ID | Case | Expected handling |
|---|---|---|
| EC-ONT-001 | Empty CLI input or resource without operation | Parser prints help; exit 1 |
| EC-ONT-002 | Unknown resource/operation after normalization | Error serialized; exit 1 |
| EC-ONT-003 | `page_size` or `batch_pages` is zero, negative, non-integer, or over the hard cap | `PaginationHelper` rejects invalid values or clamps above the cap |
| EC-ONT-004 | Final paginated page has no next token | Metadata omits `next_page_token` and keeps count fields |
| EC-ONT-005 | SDK returns non-awaitable result | `_resolve_result()` passes it through without awaiting |
| EC-ONT-006 | Binary download result is bytes, sync iterator, or async iterator | `_bytes_iter()` normalizes to async bytes chunks |
| EC-ONT-007 | Optional boolean flags omitted vs present | Omitted flags stay `None`; present flags become `True` |
| EC-ONT-008 | Stream operation has an SDK `format` arg and global CLI `--format` | Global output format is separate from `--stream-format` |

## Negative cases

| ID | Case | Expected handling |
|---|---|---|
| NEG-ONT-001 | ACL denies namespace or operation | Exit 8; no SDK dispatch |
| NEG-ONT-002 | Missing upload `--body-file` | `ValueError`; exit 1 |
| NEG-ONT-003 | Attachment upload missing filename | `ValueError`; exit 1 |
| NEG-ONT-004 | Malformed JSON supplied to a JSON arg | `ValueError`; exit 1 |
| NEG-ONT-005 | `PermissionError`, `FileNotFoundError`, `TimeoutError`, retryable `OSError`, generic exception | Exit 3, 4, 5, 7, or 6 as applicable |
| NEG-ONT-006 | W3C trace headers are asserted instead of B3 | Test design error; this story requires B3-only validation |
| NEG-ONT-007 | Error output includes bearer tokens, body bytes, temp paths, or raw response content | Defect; shared `ErrorSerializer` must redact sensitive material |

## Expected outputs

| Outcome | Exit code |
|---|---:|
| Successful ontology operation | `0` |
| Parser/user input/invalid JSON/upload validation failure | `1` |
| Permission denied | `3` |
| Not found | `4` |
| Timeout | `5` |
| Server or unexpected failure | `6` |
| Rate-limit retryable `OSError` | `7` |
| ACL denial | `8` |
| Configuration failure from shared config/client setup | `9` |

Stdout carries formatted command results. Stderr carries structured logs and pagination metadata per ADR-005. Binary download output is the persisted download envelope returned by `BinaryDownloadHandler`; binary upload output is the SDK response after body/header handling.

## Test data

| Name | Value |
|---|---|
| Ontology RID/API name | `ontology-rid`, `ontology-api-name` |
| Object type | `object-type` |
| Primary key | `primary-key-value` |
| Action | `action-api-name` |
| Query | `query-api-name` |
| JSON args | `{"x": 1}`, `["x"]`, object-set and selection payloads |
| Page size/token | `1`, `25`, `tok`, `next` |
| Binary payload | `b"abc"` and chunk iterators over `b"a"`, `b"b"` |
| Upload content metadata | `filename`, `content_length`, `content_type` |
| Output formats | `json`, `toon`, `auto`, `--pretty` |
| Trace context | B3 `trace_id`, `span_id`, `sampled` provided by shared invocation scope |

## Existing automated coverage reviewed

As of 2026-07-28, the targeted ontology suite covers these cases through `tests/test_foundry_ontologies_cli.py`, `tests/test_pagination_helper.py`, and `tests/test_ontologies_console_wrapper.py`. Parametrized parser and dispatch tests run across all 67 catalog operations. Focused tests cover paginated dict extraction, batch page limits, metadata emission, binary upload/download paths, ACL denial, retry wrapping, error exit codes, JSON/TOON output, console wrapper behavior, package import, and B3-only skill text.

## Traceability to DEV-STORY-007 acceptance criteria

| Acceptance area | Covered by |
|---|---|
| 67 canonical operations | TC-ONT-CAT-001, TC-ONT-CAT-002, TC-ONT-DSP-001 |
| Parser/catalog correctness | TC-ONT-CAT-001 through TC-ONT-CAT-003 |
| SDK dispatch and nested client routing | TC-ONT-DSP-001 through TC-ONT-DSP-004 |
| Pagination | TC-ONT-PAG-001 through TC-ONT-PAG-003 |
| Binary upload/download | TC-ONT-BIN-001 through TC-ONT-BIN-005 |
| ACL | TC-ONT-RUN-001, TC-ONT-RUN-002, NEG-ONT-001 |
| Retry | TC-ONT-RUN-001, TC-ONT-RUN-005 |
| Error serialization and exit taxonomy | TC-ONT-RUN-003, TC-ONT-RUN-004, NEG-ONT-007 |
| JSON/TOON output | TC-ONT-RUN-006 |
| Console wrapper and package entry point | TC-ONT-PKG-001 through TC-ONT-PKG-003 |
| B3-only tracing | TC-ONT-RUN-001, TC-ONT-RUN-007, NEG-ONT-006 |

## Review gate

This test case design is ready for Tech Lead or Architect review. TESTEXEC-006 execution evidence should cite the test modules and command output above. Any failing scenario must produce a BUG-SUB before QA approval. Formal tracker transition/comment work is intentionally excluded from this file because ticket-helper owns ticket mutation.

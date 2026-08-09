# TESTCASE-007 - Foundry Filesystem CLI QA test cases

## Scope

These test cases cover DEV-STORY-006, the `foundry-filesystem` CLI for 31 `foundry_sdk.v2.filesystem` operations:

- `folder`: `children`, `create`, `get`, `get-batch`, `replace`
- `project`: `add-organizations`, `create`, `create-from-template`, `get`, `organizations`, `remove-organizations`, `replace`
- `resource`: `add-markings`, `delete`, `get`, `get-access-requirements`, `get-batch`, `get-by-path`, `get-by-path-batch`, `markings`, `permanently-delete`, `remove-markings`, `restore`
- `resource-role`: `add`, `list`, `remove`
- `space`: `create`, `delete`, `get`, `list`, `replace`

The cases cover parser exposure, SDK dispatch, nested `Resource.Role` routing, five paginated operations, shared infrastructure, ADR-001 exit codes, ACL precedence, output formats, package entry points, and `.claude` skill launcher behavior.

## Preconditions

- Python 3.11+ environment with project dependencies installed.
- Repo root is the working directory.
- Files exist:
  - `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py`
  - `.claude/skills/foundry-filesystem/SKILL.md`
  - `.claude/skills/foundry-filesystem/scripts/foundry_filesystem_cli.py`
  - `tests/test_foundry_filesystem_cli.py`
  - `tests/test_filesystem_console_wrapper.py`
- `pyproject.toml` exposes console entry point `foundry-filesystem = "foundry_cli.filesystem.scripts.foundry_filesystem_cli:console_main"`.
- Unit tests may use mocks for SDK clients, auth/config, retry, ACL, and pagination. Live Foundry credentials are not required for design validation.

## Test scenarios

| ID | Scenario | Given | When | Then |
|---|---|---|---|---|
| FS-TC-001 | Operation catalog completeness | The filesystem CLI module is imported | Inspect `OP_SPECS` | Exactly 31 unique `(resource, operation)` pairs exist and match the DEV-STORY-006 resource counts. |
| FS-TC-002 | Parser accepts every operation | `build_parser()` is available | Parse each operation command with required positional and option arguments | Parser accepts all 31 commands and maps kebab-case CLI names to resource/operation values. |
| FS-TC-003 | Operation help is available | `build_parser()` is available | Parse each operation with `--help` | Each help path exits with code `0` and prints usage. |
| FS-TC-004 | Folder SDK dispatch | A mocked `client.filesystem.Folder` is provided | Invoke `folder children/create/get/get-batch/replace` | The matching SDK method is awaited once with positional args, JSON-decoded body args, and `request_timeout`. |
| FS-TC-005 | Project SDK dispatch | A mocked `client.filesystem.Project` is provided | Invoke all seven project operations | The matching SDK method is awaited once with expected kwargs and `request_timeout`. |
| FS-TC-006 | Resource SDK dispatch | A mocked `client.filesystem.Resource` is provided | Invoke all 11 resource operations | The matching SDK method is awaited once with expected kwargs and `request_timeout`. |
| FS-TC-007 | Resource-role nested routing | A mocked `client.filesystem.Resource.Role` is provided | Call `_get_client(cfg, "resource_role", factory)` and invoke `add/list/remove` | Routing resolves to `Resource.Role`; role payloads are JSON-decoded before SDK dispatch. |
| FS-TC-008 | Space SDK dispatch | A mocked `client.filesystem.Space` is provided | Invoke all five space operations | The matching SDK method is awaited once with expected kwargs and `request_timeout`. |
| FS-TC-009 | Pagination catalog | `PAGINATED_OPS` is inspected | Compare against operation specs containing `page_size` and `page_token` | Only `folder.children`, `project.organizations`, `resource.markings`, `resource-role.list`, and `space.list` are paginated. |
| FS-TC-010 | Multi-page aggregation | A paginated SDK method returns `items` plus `next_page_token` | Invoke the operation with `--page-size 1 --batch-pages 2` | Output aggregates both pages; helper records `pages_fetched=2`; second call receives the next token. |
| FS-TC-011 | Pagination metadata on stderr | A paginated operation returns a next token | Run `main()` for `folder children folder-rid --page-size 1 --format json` | Exit code is `0`; stdout contains result data; stderr includes `next_page_token` metadata after the metadata separator. |
| FS-TC-012 | ACL allows permitted operation | `AccessControlGuard.check` permits `resource.get` | Run `resource get resource-rid` with mocked SDK | CLI calls ACL before SDK, uses retry handler, emits formatted output, and exits `0`. |
| FS-TC-013 | ACL denies blocked operation | `AccessControlGuard.check` raises `AccessControlError` | Run `resource get resource-rid` | CLI skips SDK creation, serializes error JSON, and exits `8`. |
| FS-TC-014 | Readonly override behavior | Global readonly is true and operation override is `READONLY=false` | Check a write operation such as `folder.create` | ACL permits only when override allows it; otherwise write operation exits `8`. |
| FS-TC-015 | Metadata-only allow-list permits reads | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | Check allow-listed reads such as `resource.get`, `space.list`, and `project.organizations` | ACL permits these operations because they are listed in `metadata-allow-list.md`. |
| FS-TC-016 | Metadata-only blocks writes | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | Check write/delete operations such as `space.create`, `resource.delete`, `resource-role.add` | ACL blocks each operation and CLI exits `8`. |
| FS-TC-017 | JSON output mode | SDK returns a dict | Run operation with `--format json` | Stdout is valid JSON and exit code is `0`. |
| FS-TC-018 | TOON output mode | SDK returns a uniform array of dicts | Run operation with `--format toon` | Stdout is TOON-compatible tabular text and exit code is `0`. |
| FS-TC-019 | Auto format selects TOON | SDK returns a non-empty uniform array of dicts | Run operation with `--format auto` | Stdout uses TOON per ADR-004. |
| FS-TC-020 | Auto format falls back to JSON | SDK returns a dict, empty list, scalar list, or heterogeneous dict array | Run operation with `--format auto` | Stdout uses JSON per ADR-004. |
| FS-TC-021 | Structured model conversion | SDK returns Pydantic-like objects, dicts, lists, bytes, or `None` | Call `_model_to_dict()` | Output is JSON-serializable; byte payloads become length envelopes. |
| FS-TC-022 | Missing command handling | No resource or no operation is provided | Run `main()` | CLI prints help and exits `1`. |
| FS-TC-023 | Invalid JSON input handling | A JSON argument such as `--roles` or `body` contains malformed JSON | Run the matching operation | CLI serializes a user-input error and exits `1`. |
| FS-TC-024 | Authentication error mapping | Retry/SDK call raises auth-related exception | Run a valid operation | Error JSON is emitted and exit code is `2`. |
| FS-TC-025 | Not found mapping | SDK call raises 404/FileNotFoundError | Run a valid operation | Error JSON is emitted and exit code is `4`. |
| FS-TC-026 | Timeout mapping | SDK call times out or raises timeout | Run a valid operation with configured timeout | Error JSON is emitted and exit code is `5`. |
| FS-TC-027 | Rate-limit mapping | SDK call exhausts retries after HTTP 429 | Run a valid operation | Error JSON is emitted and exit code is `7`. |
| FS-TC-028 | Configuration error mapping | Config loading fails or required env is missing | Run a valid operation | Error JSON is emitted and exit code is `9`. |
| FS-TC-029 | Retry wrapper use | A retryable operation succeeds after transient failure | Run a valid operation through `main()` | Retry handler is invoked; final stdout contains success payload and exit code is `0`. |
| FS-TC-030 | B3 tracing scope | Async client factory exposes `invocation_scope` | Run a successful operation | CLI enters the invocation scope before SDK client creation and exits it after the call. |
| FS-TC-031 | Console entry point | `console_main()` wraps async `main()` | Monkeypatch `main()` to return a sentinel code | `console_main()` returns the sentinel code. |
| FS-TC-032 | Packaged module help | Package is importable from `src` | Run `python -m foundry_cli.filesystem.scripts.foundry_filesystem_cli --help` | Process exits `0` and lists `folder`, `project`, `resource`, `resource-role`, and `space`. |
| FS-TC-033 | Claude skill launcher help | `.claude/skills/foundry-filesystem/scripts/foundry_filesystem_cli.py` exists | Run launcher with `--help` | Process exits `0` and delegates to the packaged parser. |
| FS-TC-034 | Editable install metadata | Project is installed editable | Run `foundry-filesystem --help` | Console script exits `0` and prints filesystem CLI usage. |

## Edge cases

- Empty SDK result list uses JSON in auto mode.
- Single-item uniform arrays use TOON in auto mode.
- Heterogeneous arrays use JSON in auto mode.
- Optional boolean flags (`--preview`, `--include-inherited`, `--resource-level-role-grants-allowed`) set `True` only when present.
- Structured JSON arguments are decoded for `body`, role collections, organization lists, markings, and template variables.
- Pagination with `--batch-pages 1` fetches one page and emits the next token when available.
- Pagination with no next token emits terminal metadata without requesting another page.
- Timeout values use CLI `--timeout` when provided; otherwise `FOUNDRY_AGENTIC_CLI_TIMEOUT_S`/config default applies.
- Missing resource and missing operation produce help instead of SDK calls.

## Negative cases

| ID | Case | Expected result |
|---|---|---|
| FS-NEG-001 | Unknown resource or operation | Argparse rejects input or CLI returns exit `1`; no SDK call occurs. |
| FS-NEG-002 | Malformed JSON for structured args | Error JSON on stdout; exit `1`. |
| FS-NEG-003 | Missing `FOUNDRY_TOKEN` or malformed config | Error JSON on stdout; exit `9`. |
| FS-NEG-004 | Auth failure from SDK | Error JSON on stdout; exit `2`. |
| FS-NEG-005 | Permission denied from SDK | Error JSON on stdout; exit `3`. |
| FS-NEG-006 | Resource missing | Error JSON on stdout; exit `4`. |
| FS-NEG-007 | Timeout | Error JSON on stdout; exit `5`. |
| FS-NEG-008 | Server failure after retry policy | Error JSON on stdout; exit `6`. |
| FS-NEG-009 | Rate limit exhausted | Error JSON on stdout; exit `7`. |
| FS-NEG-010 | ACL disabled/readonly/metadata-only block | Error JSON on stdout; exit `8`. |

## Expected outputs

- Success: exit `0`; result payload on stdout in JSON, TOON, or auto-selected format.
- User input error: exit `1`; JSON error envelope on stdout.
- Authentication error: exit `2`; JSON error envelope on stdout.
- Permission denied: exit `3`; JSON error envelope on stdout.
- Not found: exit `4`; JSON error envelope on stdout.
- Timeout: exit `5`; JSON error envelope on stdout.
- Server error: exit `6`; JSON error envelope on stdout.
- Rate limit exhausted: exit `7`; JSON error envelope on stdout.
- Access control block: exit `8`; JSON error envelope on stdout.
- Configuration error: exit `9`; JSON error envelope on stdout.
- Pagination metadata: compact JSON on stderr after `# ---metadata-start---`; never TOON.
- Diagnostic logs: NDJSON on stderr and separate from metadata.

## Test data

| Name | Value |
|---|---|
| Folder RID | `ri.foundry.main.folder.test` |
| Project RID | `ri.foundry.main.project.test` |
| Resource RID | `ri.foundry.main.resource.test` |
| Space RID | `ri.foundry.main.space.test` |
| Template RID | `ri.foundry.main.template.test` |
| Path | `/QA/Filesystem/sample` |
| Organization RIDs | `["ri.multipass..organization.test"]` |
| Marking IDs | `["marking-test"]` |
| Roles | `[{"principal_id": "user-test", "role_id": "viewer"}]` |
| Batch body | `{"rids": ["ri.foundry.main.resource.test"]}` |
| Pagination | `--page-size 1 --batch-pages 2` with first page returning `next_page_token="next"` |
| Output payload | `[{"rid": "one", "displayName": "One"}, {"rid": "two", "displayName": "Two"}]` |

## Review requirement

TESTCASE-007 can move to Resolved only after Tech Lead or Architect approval confirms these scenarios are valid against DEV-STORY-006 and DESIGN-007. Test execution must not begin from this design until that approval is recorded.

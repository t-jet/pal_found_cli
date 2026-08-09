# DESIGN-008 - Foundry Functions CLI

## Scope

DEV-STORY-008 adds `foundry-functions`, a namespace CLI for seven Functions API v2 operations.

## Operation catalog

| CLI resource | Operation | SDK client path | SDK method | Positional args | Options |
|---|---|---|---|---|---|
| `query` | `execute` | `Query` | `execute` | `query_api_name` | `parameters`, `attribution`, `branch`, `preview`, `trace_parent`, `trace_state`, `transaction_id`, `version` |
| `query` | `get` | `Query` | `get` | `query_api_name` | `preview`, `version` |
| `query` | `get-by-rid` | `Query` | `get_by_rid` | none | `rid`, `include_prerelease`, `preview`, `version` |
| `query` | `get-by-rid-batch` | `Query` | `get_by_rid_batch` | `body` | `preview` |
| `query` | `streaming-execute` | `Query` | `streaming_execute` | `query_api_name` | `parameters`, `attribution`, `branch`, `ontology`, `preview`, `trace_parent`, `trace_state`, `transaction_id`, `version` |
| `value-type` | `get` | `ValueType` | `get` | `value_type_rid` | `preview` |
| `version-id` | `get` | `ValueType.VersionId` | `get` | `value_type_rid`, `version_id_version_id` | `preview` |

Structured arguments parsed from JSON: `parameters`, `attribution`, and `body`.

Boolean flags: `include_prerelease` and `preview`.

No operations expose `page_size` and `page_token`, so `PAGINATED_OPS` is empty for this namespace.

## Implementation plan

- Add `src/foundry_cli/functions/scripts/foundry_functions_cli.py` using the `OP_SPECS` pattern from filesystem and ontologies.
- Route clients from `AsyncClientFactory().create(cfg).functions`.
- Use namespace `FUNCTIONS` for `AccessControlGuard`.
- Convert SDK/Pydantic results through `_model_to_dict`.
- Treat `streaming_execute` byte responses as a byte-length envelope through `_model_to_dict`, matching filesystem behavior for bytes.
- Add `foundry-functions` to `[project.scripts]`.
- Add `.claude/skills/foundry-functions/SKILL.md` and a launcher script that delegates to the packaged module.

## Test plan

- Add parser tests for all seven operations and `--help`.
- Add dispatch tests verifying client path, method name, positional args, JSON decoding, boolean flags, and `request_timeout`.
- Add tests for root and nested client routing, including `ValueType.VersionId`.
- Add main-path tests for ACL, retry, output, B3 invocation scope, and representative error mappings.
- Add console wrapper tests for packaged entry point behavior.
- Keep repository coverage above the configured 80% threshold.

## Estimates

| Sub-task | Hours |
|---|---:|
| DESIGN-008 | 4 |
| DEV-008 | 10 |
| UNITTEST-008 | 6 |
| CODEREVIEW-008 | 3 |
| TESTCASE-008 | 4 |
| TESTEXEC-008 | 4 |
| DEVOPS-008 | 2 |

## Risks

- `streaming_execute` returns bytes/NDJSON. The first implementation will emit a byte-length envelope instead of parsing NDJSON records.
- Query execution has optional trace fields that overlap with B3 environment propagation. The CLI will expose SDK fields without claiming W3C support.
- Live Foundry credentials are not required for unit tests; QA execution uses mocked SDK clients.

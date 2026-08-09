# TESTCASE-009 - Foundry Admin CLI QA test cases

## Scope

These test cases cover DEV-STORY-009, the `foundry-admin` CLI for 66 `foundry_sdk.v2.admin` operations. The suite must verify catalog coverage, parser/help behavior, SDK routing, structured JSON arguments, boolean flags, pagination, `ADMIN` ACL checks, output formatting, byte response handling for profile pictures, ADR-001 exit codes, console script packaging, and the `.claude` skill launcher.

## Preconditions

- Python 3.11+ environment with project dependencies installed.
- Repo root is the working directory.
- Implementation files exist after DEV-009:
  - `src/foundry_cli/admin/scripts/foundry_admin_cli.py`
  - `.claude/skills/foundry-admin/SKILL.md`
  - `.claude/skills/foundry-admin/scripts/foundry_admin_cli.py`
  - `tests/test_foundry_admin_cli.py`
  - `tests/test_admin_console_wrapper.py`
- `pyproject.toml` exposes `foundry-admin = "foundry_cli.admin.scripts.foundry_admin_cli:console_main"`.
- Tests may use mocked SDK clients, config, ACL, retry, and output formatting. Live Foundry credentials are not required.

## Test scenarios

| ID | Scenario | Expected result |
|---|---|---|
| ADM-TC-001 | Operation catalog completeness | Exactly 66 unique `(resource, operation)` entries match DESIGN-009. |
| ADM-TC-002 | Parser accepts every operation | All 66 operations parse with required positionals/options and kebab-case command names. |
| ADM-TC-003 | Help paths | Root, resource, and operation help exit `0` without config or SDK loading. |
| ADM-TC-004 | SDK client routing | Each resource resolves to the correct `client.admin.<Resource>` or nested subclient. |
| ADM-TC-005 | SDK dispatch | Each operation calls the expected SDK method once with positionals, kwargs, and `request_timeout`. |
| ADM-TC-006 | JSON argument decoding | `attributes`, `administrators`, `body`, `initial_members`, `initial_permissions`, `initial_role_assignments`, `marking_ids`, `organizations`, `principal_ids`, `role_assignments`, and `where` decode before dispatch. |
| ADM-TC-007 | Boolean flags | `--include-expirations`, `--preview`, and `--transitive` pass `True` only when present. |
| ADM-TC-008 | Pagination catalog | Only the 11 DESIGN-009 paginated operations expose pagination flags and enter pagination handling. |
| ADM-TC-009 | Async iterator pagination | Mocked SDK async iterators are collected up to `page_size * batch_pages` and emit metadata. |
| ADM-TC-010 | Page-envelope pagination | Dict/list page-envelope doubles aggregate pages and preserve next page token. |
| ADM-TC-011 | ACL namespace | `AccessControlGuard.check` uses namespace `ADMIN` and blocks before SDK creation when denied. |
| ADM-TC-012 | Read-only blocks writes | Create, delete, replace, add, remove, preregister, and revoke operations exit `8` when ACL blocks them. |
| ADM-TC-013 | Metadata-only behavior | Metadata-only mode permits only allow-listed admin metadata reads and blocks unclassified operations. |
| ADM-TC-014 | ADR-001 exit codes | Auth, permission, not found, timeout, rate limit, server, user input, access control, and config errors map to expected codes. |
| ADM-TC-015 | JSON output | Successful object responses with `--format json` emit valid JSON and exit `0`. |
| ADM-TC-016 | TOON output | Uniform list responses with `--format toon` emit TOON-compatible output. |
| ADM-TC-017 | Auto output | Auto format chooses TOON only for uniform non-empty arrays, otherwise JSON. |
| ADM-TC-018 | Model conversion | Pydantic-like objects, dicts, lists, `None`, and bytes convert to JSON-serializable values. |
| ADM-TC-019 | Profile picture bytes | `user profile-picture` byte payloads emit a byte-length envelope, not raw bytes. |
| ADM-TC-020 | Missing command | Missing resource or operation prints help, exits user-input code, and skips SDK calls. |
| ADM-TC-021 | Malformed JSON | Invalid structured JSON exits user-input code and skips SDK method invocation. |
| ADM-TC-022 | Retry wrapper | Retry handler wraps SDK invocation and can recover from a transient mocked failure. |
| ADM-TC-023 | B3 invocation scope | CLI enters `AsyncClientFactory.invocation_scope(cfg)` around SDK client creation and call. |
| ADM-TC-024 | Console wrapper | `console_main()` runs async `main()` and returns its exit code. |
| ADM-TC-025 | Packaged module help | `python -m foundry_cli.admin.scripts.foundry_admin_cli --help` exits `0`. |
| ADM-TC-026 | Claude skill launcher | `.claude/skills/foundry-admin/scripts/foundry_admin_cli.py --help` exits `0`. |
| ADM-TC-027 | Editable install script | After `python -m pip install -e .`, `foundry-admin --help` exits `0`. |
| ADM-TC-028 | Full regression | Full pytest suite with coverage passes the repository 80% gate. |

## Negative cases

| ID | Case | Expected result |
|---|---|---|
| ADM-NEG-001 | Unknown resource or operation | Argparse rejects input or CLI exits user-input code; SDK is not called. |
| ADM-NEG-002 | Missing required positional or option | Parser exits before dispatch. |
| ADM-NEG-003 | Malformed JSON for structured args | Error JSON on stdout, user-input exit code, no SDK method call. |
| ADM-NEG-004 | Missing config | Error JSON on stdout, configuration exit code. |
| ADM-NEG-005 | Auth failure | Error JSON on stdout, auth exit code. |
| ADM-NEG-006 | Permission failure | Error JSON on stdout, permission exit code. |
| ADM-NEG-007 | Missing resource | Error JSON on stdout, not-found exit code. |
| ADM-NEG-008 | Timeout | Error JSON on stdout, timeout exit code. |
| ADM-NEG-009 | Server failure after retry | Error JSON on stdout, server exit code. |
| ADM-NEG-010 | Rate limit exhausted | Error JSON on stdout, rate-limit exit code. |
| ADM-NEG-011 | Access control block | Error JSON on stdout, access-control exit code. |

## Test data

| Name | Value |
|---|---|
| Enrollment RID | `ri.admin.enrollment.test` |
| Authentication provider RID | `ri.admin.auth-provider.test` |
| Group ID | `group-001` |
| User ID | `user-001` |
| Marking ID | `marking-001` |
| Marking category ID | `category-001` |
| Organization RID | `ri.admin.organization.test` |
| Role ID | `role-001` |
| Provider ID | `provider-001` |
| Principal IDs JSON | `["user-001","group-001"]` |
| Role assignments JSON | `[{"roleId":"role-001","principalId":"user-001"}]` |
| Attributes JSON | `{"department":["data"],"region":["emea"]}` |
| Search filter JSON | `{"type":"and","conditions":[]}` |
| Batch body JSON | `[{"id":"user-001"}]` |
| Profile bytes | `b"image-bytes"` |

## Result criteria

TESTEXEC-009 passes only when focused admin tests, lint, type checks, help/package checks, editable install script check, and full regression with coverage all pass. Any failed admin behavior creates a BUG-SUB under DEV-STORY-009.

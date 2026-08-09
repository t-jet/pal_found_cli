# DESIGN-009 - Foundry Admin CLI

Story: DEV-STORY-009
Status: Approved for grooming
Date: 2026-07-29

## Scope

Build `foundry-admin`, a namespace CLI and Claude skill for all 66 public `foundry_sdk.v2.admin` operations. The implementation follows the existing datasets, ontologies, filesystem, and functions CLI pattern.

The CLI will use:

- `AsyncClientFactory().create(cfg).admin`
- `AccessControlGuard(cfg, "ADMIN")`
- `RetryHandler`
- `OutputFormatter`
- `ErrorSerializer`
- `PaginationHelper` for list/search operations
- SDK-native invocation scope for B3 tracing

No live Foundry credentials are required for unit or QA execution. Tests use mocked SDK clients and common components.

## Operation catalog

| Resource | Operations | Count |
|---|---|---:|
| `authentication-provider` | `get`, `list`, `preregister-group`, `preregister-user` | 4 |
| `cbac-banner` | `get` | 1 |
| `cbac-marking-restrictions` | `get` | 1 |
| `enrollment` | `get`, `get-current` | 2 |
| `enrollment-role-assignment` | `add`, `list`, `remove` | 3 |
| `group` | `create`, `delete`, `get`, `get-batch`, `list`, `list-current`, `replace`, `search` | 8 |
| `group-member` | `add`, `list`, `remove` | 3 |
| `group-membership` | `list` | 1 |
| `group-membership-expiration-policy` | `get`, `replace` | 2 |
| `group-provider-info` | `get`, `replace` | 2 |
| `host` | `list` | 1 |
| `marking` | `create`, `get`, `get-batch`, `list`, `replace` | 5 |
| `marking-category` | `create`, `get`, `list`, `replace` | 4 |
| `marking-member` | `add`, `list`, `remove` | 3 |
| `marking-role-assignment` | `add`, `list`, `remove` | 3 |
| `organization` | `create`, `get`, `list-available-roles`, `replace` | 4 |
| `organization-guest-member` | `add`, `list`, `remove` | 3 |
| `organization-role-assignment` | `add`, `list`, `remove` | 3 |
| `role` | `get`, `get-batch` | 2 |
| `user` | `delete`, `get`, `get-batch`, `get-current`, `get-markings`, `list`, `profile-picture`, `revoke-all-tokens`, `search` | 9 |
| `user-provider-info` | `get`, `replace` | 2 |

Total: 66 operations.

## Argument handling

The parser uses kebab-case for resources, operations, and option names. SDK method names remain snake_case internally.

Structured JSON arguments must be parsed before SDK dispatch:

- `attributes`
- `administrators`
- `body`
- `initial_members`
- `initial_permissions`
- `initial_role_assignments`
- `marking_ids`
- `organizations`
- `principal_ids`
- `role_assignments`
- `where`

Boolean flags:

- `--include-expirations`
- `--preview`
- `--transitive`

Pagination flags are exposed only on paginated operations:

- `--page-size`
- `--page-token`
- `--batch-pages`

## Paginated operations

The following operations use the shared pagination helper:

- `group list`
- `group search`
- `group-member list`
- `group-membership list`
- `host list`
- `marking list`
- `marking-category list`
- `marking-member list`
- `marking-role-assignment list`
- `user list`
- `user search`

The CLI must support both SDK async iterators and page-envelope test doubles, matching the filesystem implementation.

## Security

Admin has destructive and security-sensitive operations. `AccessControlGuard` must run before client creation or SDK dispatch. Write operations include `create`, `delete`, `replace`, `add`, `remove`, `preregister_group`, `preregister_user`, and `revoke_all_tokens`.

Metadata-only mode should allow only operations present in the existing metadata allow-list. Unclassified admin operations remain blocked by default under metadata-only mode.

## Files

Implementation:

- `src/foundry_cli/admin/__init__.py`
- `src/foundry_cli/admin/scripts/__init__.py`
- `src/foundry_cli/admin/scripts/foundry_admin_cli.py`
- `.claude/skills/foundry-admin/SKILL.md`
- `.claude/skills/foundry-admin/scripts/foundry_admin_cli.py`
- `pyproject.toml`

Tests:

- `tests/test_foundry_admin_cli.py`
- `tests/test_admin_console_wrapper.py`

## Test requirements

Unit and QA coverage must verify:

- all 66 operations are present and unique
- parser accepts every operation
- help exits with code 0
- SDK routing reaches `client.admin.<Resource>` and nested subresources
- JSON args are decoded before dispatch
- boolean flags default to omitted and pass `True` when present
- pagination uses shared helper on the 11 paginated operations
- `ADMIN` ACL namespace is checked before SDK calls
- ADR-001 exit codes are preserved
- `profile-picture` byte output uses the byte-length envelope unless later routed through binary download handling
- packaged module and `.claude` launcher help work
- editable install exposes `foundry-admin`
- full regression suite stays above the 80% coverage gate

## Acceptance

DEV-STORY-009 can move from Grooming to Development after DESIGN-009 is closed and the implementation, unit test, code review, QA, and deployment subtasks exist and are linked under the story.

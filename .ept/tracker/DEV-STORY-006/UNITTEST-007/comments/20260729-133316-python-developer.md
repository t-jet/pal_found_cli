Subject: Unit test evidence
Created: 2026-07-29T13:33:16
Updated: 2026-07-29T13:33:16
---
## Unit test evidence

Changed paths:
- `tests/test_foundry_filesystem_cli.py`
- `tests/test_filesystem_console_wrapper.py`
- `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py` (minimal ADR-001 return-code fix exposed by new tests)

Commit: `075a2be` (`Add filesystem CLI unit tests`)

Coverage and test evidence:
- `python -m pytest tests\	est_foundry_filesystem_cli.py tests\	est_filesystem_console_wrapper.py -q` -> `114 passed in 0.56s`.
- `python -m ruff check tests\	est_foundry_filesystem_cli.py tests\	est_filesystem_console_wrapper.py src\\foundry_cli\\filesystem\\scripts\\foundry_filesystem_cli.py` -> `All checks passed!`.
- `python -m pytest --cov=foundry_cli --cov-branch --cov-report=term-missing -q` -> `585 passed in 6.36s`; total coverage `81.96%`, above 80% gate.

Scope covered:
- 31-operation catalog uniqueness and parser acceptance.
- Every operation `--help` exits 0.
- Dispatch invokes every SDK method and passes `request_timeout`.
- Nested `resource-role` client resolves to `client.filesystem.Resource.Role`.
- Five paginated operations use `PaginationHelper`; main emits `next_page_token` pagination metadata to stderr.
- JSON, TOON, and auto output mode wiring.
- ACL denial returns exit 8 and skips SDK factory.
- ADR-001 return codes verified for auth 2, not found 4, ACL 8, config 9.
- `console_main()` returns and propagates the async `main()` exit code.

Notes:
- Tests use mocked SDK clients/config/factory/retry/ACL; no network calls.
- Test commands emitted existing environment warnings from `requests` dependency version matching and `pytest-asyncio` default loop-scope deprecation; no warning was suppressed.

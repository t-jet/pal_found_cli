Subject: Corrective evidence - SDK async iterator filesystem pagination
Created: 2026-07-29T14:48:49
Updated: 2026-07-29T14:48:49
---
## Correction evidence - 2026-07-29

Status before work: `Correction`.

Reviewer finding addressed:
- Filesystem paginated operations no longer treat SDK `AsyncResourceIterator` responses as dict/list page envelopes.
- Affected operations: `folder.children`, `project.organizations`, `resource.markings`, `resource_role.list`, and `space.list`.

Code changes:
- `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py`: `_invoke_paginated()` now calls the SDK once, detects async iterator protocol via `__aiter__`/`__anext__`, consumes items with `async for`, caps collection by `page_size * batch_pages`, and reads cursor metadata from SDK iterator/page iterator when available.
- The page-envelope path remains as fallback for compatibility with dict/list-style responses.

Tests added/updated:
- `tests/test_foundry_filesystem_cli.py`: added `_AsyncResourceIteratorDouble` with `__aiter__`, `__anext__`, and SDK-like `get_next_page_token()`.
- Updated parametrized pagination coverage for all five filesystem paginated operations to use the async iterator protocol.
- Kept explicit fallback coverage for dict/list page envelopes.
- Updated `main()` pagination metadata test to use SDK-like async iterator behavior.

Verification:
- `pytest tests/test_foundry_filesystem_cli.py tests/test_filesystem_console_wrapper.py` -> 115 passed.
- `pytest` -> 586 passed.
- `pytest --cov=foundry_cli --cov-report=term-missing` -> 586 passed, total coverage 81.96%, above 80% gate.
- `ruff check src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py tests/test_foundry_filesystem_cli.py tests/test_filesystem_console_wrapper.py` -> passed.
- `mypy src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py tests/test_foundry_filesystem_cli.py tests/test_filesystem_console_wrapper.py` -> passed.
- `ruff check src tests` -> passed.
- `mypy src` -> passed.

Known unrelated verification noise:
- `ruff check .` fails on existing `.claude` and `.ept` tracker/skill files outside this correction scope.
- `mypy src tests` fails on existing test typing issues outside touched filesystem files.

OWASP self-review:
- No new input parsing surface beyond existing argparse pagination arguments.
- No filesystem, network-on-import, credential, token, or logging changes.
- ACL path remains before SDK invocation in `main()`.
- Error serialization and exit-code handling unchanged.

Questions/blockers:
- No linked QUESTION tickets found for CODEREVIEW-007.
- No blocker remains for the requested correction.

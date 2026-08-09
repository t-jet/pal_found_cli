Subject: Test plan
Created: 2026-07-29T13:28:03
Updated: 2026-07-29T13:28:03
---
## Test plan

Reviewed workflow instructions, `.ept/docs/document_index.md`, ADR-001, ADR-004, filesystem entries in canonical env var and metadata allow-list docs, and DEV-007 context. UNITTEST-007 is not blocked; DEV-007 is Closed, so filesystem CLI implementation is ready for unit tests.

Planned scope:
- Add/adjust tests only in `tests/test_foundry_filesystem_cli.py` and `tests/test_filesystem_console_wrapper.py`.
- Verify 31 operation catalog/parser exposure and operation `--help` exits 0.
- Verify dispatch and nested `resource-role` client selection.
- Verify paginated filesystem operations use `PaginationHelper` and emit `next-page-token` metadata to stderr.
- Verify JSON, TOON, and auto output mode wiring.
- Verify ACL denial stops SDK dispatch and maps to exit 8.
- Verify ADR-001 mappings for auth 2, not found 4, ACL 8, and config 9.
- Verify `console_main` returns and propagates `asyncio.run(main())` exit code.
- Run targeted filesystem tests with branch coverage evidence and ensure project coverage gate remains >=80% if practical in local run.

Subject: Test plan — foundry-widgets CLI (8-op corrected catalog)
Created: 2026-08-11T02:09:19
Updated: 2026-08-11T02:09:19
---
## Test plan (UNITTEST-022)

### Scope
Unit and integration tests for the 8-op foundry-widgets CLI per corrected catalog (QUESTION-043, tech-lead comment 20260811-005035). All SDK transport mocked — no live Foundry connection. Watch for FOUNDRY_* env leakage between tests.

### Files
1. tests/test_foundry_widgets_cli.py — catalog, parser, dispatch, validation, ACL, metadata policy, pagination, upload, attribution, errors, timeout, output, console.
2. tests/test_widgets_console_wrapper.py — console_main asyncio boundary + .claude launcher delegation + launcher --help.

### Coverage areas (per tech-lead test-plan adjustments)
1. Catalog integrity: len(OP_SPECS)==8; exact (resource, operation, client_path, method) order; PAGINATED_OPS=={("release","list")}.
2. Parser surface for every op (incl. --settings-json for set-widget-set-by-id, --file/--repository-version for publish); unknown op and missing required flag rejected.
3. Dispatch: exact SDK kwargs for each op (settings dict for set_widget_set_by_id, repository_version for publish, request_timeout everywhere).
4. Bounded zip upload for repository publish: reads file bounded 16 MiB AFTER ACL decision BEFORE client; oversized/missing file exit 1 and create_calls==0.
5. Pagination for release list: with_raw_response + PaginationHelper; multi-page collection; page-token threading; default single page; --all/--max-pages.
6. ACL: write set (enable, set_widget_set_by_id, release.delete, repository.publish) blocked under READONLY and METADATA_ONLY (exit 8, create_calls==0); 4 reads permitted; AccessControlGuard._is_write_operation regression.
7. Metadata-only policy: packaged allow-list permits exactly 4 (release.get/list, repository.get, widget_set.get) and blocks 4.
8. include_attribution=False on invocation_scope + factory.create.
9. Error taxonomy: unknown op exit 1; SDK error exit 6 with privacy-safe message; TimeoutError exit 5.
10. Timeout bounds 1..3600; invalid timeout exit 1.
11. Output formats json/toon; console_main wraps asyncio.run.
12. Launcher delegation + --help exit 0.

### Verification
Focused pytest (100% pass), coverage >= 80% branch on widgets namespace, ruff/mypy clean, full-suite regression, no real network calls.

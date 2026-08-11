Subject: Unit tests complete — 41 tests, 89% branch coverage (commit 1b15565)
Created: 2026-08-11T02:21:40
Updated: 2026-08-11T02:21:40
---
## Files created
1. `tests/test_foundry_widgets_cli.py` — 38 tests covering the 8-op corrected catalog.
2. `tests/test_widgets_console_wrapper.py` — 3 console/launcher tests.
3. `tests/test_access_control_guard.py` — added `test_widgets_verbs_are_writes` regression (enable/set_widget_set/set_widget_set_by_id classified as writes).

## Coverage areas (per tech-lead test-plan adjustments 20260811-005035)
1. Catalog integrity: len(OP_SPECS)==8; exact (resource, operation, client_path, method) order; PAGINATED_OPS=={("release","list")}; excluded-ops assertion (disable/get/pause/set_widget_set NOT in catalog).
2. Parser surface for every op (incl. --settings-json for set-widget-set-by-id, --file/--repository-version for publish); unknown op (dev-mode-settings disable) and missing required flag rejected.
3. Dispatch: exact SDK kwargs for each op (settings dict for set_widget_set_by_id, repository_version for publish, request_timeout everywhere).
4. Bounded zip upload for repository publish: reads file bounded 16 MiB AFTER ACL decision BEFORE client; missing/oversized file exit 1 and create_calls==0.
5. Pagination for release list: with_raw_response + PaginationHelper; multi-page collection with page-token threading; default single page.
6. ACL: write set (enable, set_widget_set_by_id, release.delete, repository.publish) blocked under READONLY and METADATA_ONLY (exit 8, create_calls==0); 4 reads permitted; AccessControlGuard._is_write_operation regression.
7. Metadata-only policy: packaged allow-list permits exactly 4 (release.get/list, repository.get, widget_set.get) and blocks 4.
8. include_attribution=False on invocation_scope + factory.create.
9. Error taxonomy: unknown op exit 1; SDK error exit 6 with privacy-safe message; TimeoutError exit 5.
10. Timeout bounds 1..3600; invalid timeout exit 1.
11. Output formats json/toon; console_main wraps asyncio.run; launcher delegation + --help exit 0.

## Results
- Focused run: 41 passed, 0 failed. Combined with ACL guard suite: 122 passed.
- Namespace branch coverage 89% (foundry_cli.widgets + access_control_guard combined 89.07%; widgets CLI alone 85%, __init__ 100%).
- Full regression: 1362 passed, 0 failed, repo 86.55% branch.
- No real network calls — all SDK transport mocked; FOUNDRY_* env scrubbed before test runs.

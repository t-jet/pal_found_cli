Subject: 2026-10-11 prepared-runtime regression evidence
Created: 2026-10-11T07:03:27
Updated: 2026-10-11T07:03:33
---
## Executed result
- Ran actual workspace transform through an in-memory Dataset substitute and the SQL CTAS through SQLite. Pytest: **7 passed, 1 failed**.
- Failing test_workspace_rejects_non_numeric_amount: input amount='invalid' wrote [{ 'customer_id': 'c1', 'total_amount': 'invalid' }] instead of rejecting the invalid numeric input before write_table. This is an output-schema defect.
- Coverage of transform.py: 9/9 statements, **100%**; this does not negate the semantic defect. Ruff and scoped Git diff check passed.
- SQLite checks join, null and duplicate arithmetic only. Spark SQL, Foundry preview, workspace publication, build and committed dataset were not executed. Prepared runtime is synthetic and network-free.
- UNITTEST-070 stays In Progress; the regression remains failing pending DEV-063 correction and independent review.

Subject: Developer root cause and fix plan
Created: 2026-10-18T22:43:50
Updated: 2026-10-18T22:43:50
---
## Root cause and plan
Original Marking and Role get_batch fixtures requested one ID but returned empty data maps. They checked only equality to those empty maps, so request/result identity went untested. Skills commit c9e6d48 changed each fixture to return a nonempty data map keyed by requested synthetic-value and an object with matching id. Verify POST body, typed result and errors, then hand to QA.
## Evidence
Integration content 68d569c, checkout 5d50cf8. Current example SHA256: Marking cb65ff8607729e1aaa234c215552bf331036b6aa16ce63f48ce6479cf316a8ba; Role be0018cd31e9d345dca5bc3f59e778d083d92f89e5f18d378280039a7f39da3d. Independent QA comment 20261018-224148-@qa-engineer details MockTransport request and result assertions. Fresh python -m pytest -q tests/test_offline_rest_wave1.py: 518 passed, exit 0. Test logs show requests/pytest warnings only; no application error log produced. Contributor time for historical fix was not measured; no hours claimed. Offline fake transport only, no live enrollment.

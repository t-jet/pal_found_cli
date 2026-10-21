Subject: Developer root cause and fix plan
Created: 2026-10-18T22:43:26
Updated: 2026-10-18T22:43:26
---
## Root cause and plan
Original CBAC fixture sent no marking IDs while asserting marking-specific output. At SDK 1.101.0 this left request/result identity untested. Fix in skills commit c9e6d48 supplied synthetic-value through marking_ids and expected markingIds query; 6701aca added required preview=true. Verify both GET requests, decoded classification/restrictions, errors, then hand to QA.
## Evidence
Integration content 68d569c, checkout 5d50cf8. Current example SHA256: Banner 1bdcc92085003ccac9d60ee2a0dc172476e22c7a3588092e00136e42c6e8f879; Restrictions 5942871e72fd0ccaa3e2b312989dcf6f725a578f573c81a3091bfbc4f629b61d. Independent QA comment 20261018-224141-@qa-engineer details MockTransport request and result assertions. Fresh python -m pytest -q tests/test_offline_rest_wave1.py: 518 passed, exit 0. Test logs show requests/pytest warnings only; no application error log produced. Contributor time was not measured; no hours claimed. Offline fake transport only, no live enrollment or policy authorization.

Subject: Implementation and regression evidence
Created: 2026-10-18T11:58:27
Updated: 2026-10-18T11:58:27
---
Fix: commit 79f1d7ffd285d5c49f6ce816a2065f5ef5e54840 on skills branch feature015/rest-081-corrections. `list_scenario_edited_objects` now returns Order locator `{'__primaryKey':'ORD-101','__apiName':'Order'}`. `list_scenario_edited_links` now uses the same source locator and Worker target locator `{'__primaryKey':'WRK-7','__apiName':'Worker'}`; `linkType:'assignedWorker'` is unchanged. No unrelated files changed.
SHA-256 of corrected files: invoke_list_scenario_edited_objects.py = 3fac616421ccc5a41b244b777df2812afe18bcdc480738d48b41afbde87e6673; invoke_list_scenario_edited_links.py = ccc5cc72ac695df75fb2245869f49727bbe275e69b3e062f5dcbc973f395849a.
Offline fixture output: both named operations reported serialized request, decoded result, and zero named errors passed. Regression command `python -m pytest -q tests/test_offline_rest_wave1.py tests/test_offline_rest_acceptance.py tests/test_offline_rest_acceptance_guards.py` = 541 passed in 33.13s. `git -c core.whitespace=cr-at-eol diff --cached --check` passed before commit. Independent QA verification and formal TESTEXEC-080 remain separate; LINK-01981 stays in place until QA handles it.

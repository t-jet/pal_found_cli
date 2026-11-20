Subject: Native SDK101 transport test plan and readiness
Created: 2026-11-18T13:23:22
Updated: 2026-11-18T13:23:22
---
Own only tests/test_offline_rest_083.py in isolated .ept/tmp/feature015_rest083_unit_modes_20261118 at ff70c30c99410b3b0784bcad934625b88d5e6e5c; preserve existing regression guards.

Read indexed authoring contract, exact partition, approved DESIGN-081 and implementation comments; DESIGN Closed, DEV-STORY-083 Development, DEV-081 In Progress with runnable examples. UNITTEST links contain no unresolved QUESTION.

Frozen SDK 1.101.0 commit 168d51910570b6966afa2320333ab36f6a3f7ccf source inventory: 25 operations, 150 available sync/async ordinary/raw/streaming forms, zero void results, zero native pagers or ordinary iterators, zero named operation errors, six bytes results, three nullable results, three raw binary uploads. Geotemporal continuation uses explicit pageToken response, bounded manually.

Append native authenticated MockTransport tests with network denial. Derive wire paths, HTTP methods, query/body/header/timeout, response types, actual async signatures and wrapper availability independently from SDK source. Cover meaningful typed results, missing required input, permission denial and timeout with exact request counts, upload/download bytes, bounded continuation, unfinished stream closure/cancellation and prebuffered-body trap. Validate own-file lint and pytest with JUnit/machine proofs and substantive mutation checks under parent .ept/tmp. Independent peer review follows; no formal acceptance claim, product/fixture edits, commit or push.

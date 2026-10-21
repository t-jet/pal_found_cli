Subject: Published SQL adapter fix and independent SDK verification
Created: 2026-10-21T23:59:39
Updated: 2026-10-21T23:59:39
---
Implementation author /root records peer review and runtime QA by separate agent
/root/tracker_capture_qa_21. Published tool fix a3a38ec434fdb046c329b850e716dc541fa87ecd reuses the existing required/optional/timeout
kwargs builder for downloads, removing only local output. This forwards required query to the real
SDK while preserving both Arrow download routes, optional typed parameters, timeout and bounded
atomic persistence. Author's four new actual-SDK wire tests reproduce three pre-fix missing-query
failures plus one passing get_results case; all 30 SQL tests pass on each SDK1.101 and SDK1.111,
Ruff src/tests passes and mypy reports no issues in 72 source files. An intermediate fixture used an
invalid untagged parameter dict; it was corrected to the official namedParameterMapping schema.
No product parameter policy or retry/timeout behavior was changed.

Independent reviewer separately inspected the source and reproduced the published066970 baseline
failure before zero HTTP requests. On each SDK1.101 and1.111, five independent real HTTP cases pass:
minimal query, typed named parameters plus dryRun/rowLimit, truncated download, GET results with
scalar ID/local output, and bounded GET results. They verify exact body, timeout17, saved bytes,
checksums and response closure. Evidence feature015_sql_query_independent_qa.json, SHA256 5166455154dd650b243020a62fbc1a49c5aefb043ab9708675bd769a3f167329.
All eight required CI checks pass at this exact head; snapshot feature015_tool_ci_a3a38ec.json, SHA256
50c8eefbebacb67e4fc4f9087cd93802819d7ecbbf70953aea2536c9f76fca89. This updates historical pending-work statements. No live tenant
request or server-side query execution is claimed. Root cause, related ownership, applicable
requirements and acceptance criteria were reviewed. No incoming Question or blocking link exists.

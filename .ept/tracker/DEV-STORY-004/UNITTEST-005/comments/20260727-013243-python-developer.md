Subject: Unit-test execution plan
Created: 2026-07-27T01:32:43
Updated: 2026-07-27T01:32:43
---
Build focused tests alongside DEV-005. Cover bounded limit+1 download streaming, exact-cap and unknown-length truncation, nullable source_size, source_size_at_least warnings, hashes, containment, and partial cleanup without draining. Cover normalized aliases, atomic JSON, cross-process lock behavior, Session.rid mapping, missing/null/string session_token without synthesis, expiry and idempotent purge. Verify corrupt state warns without secrets, is deleted under the alias lock, and leaves the alias absent. Cover SDK-native B3 propagation through TRACE_ID_VAR, SPAN_ID_VAR, and SAMPLED_VAR, with reset on success and every failure path plus concurrent and back-to-back isolation; do not assert deferred W3C traceparent support. Add config and integration regression cases, keep tests free of external connections, and contribute to the 80% coverage gate.

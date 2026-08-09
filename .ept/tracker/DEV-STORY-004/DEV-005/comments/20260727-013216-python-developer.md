Subject: Development execution plan
Created: 2026-07-27T01:32:16
Updated: 2026-07-27T01:32:16
---
Implement the DESIGN-005 contracts in five passes. First wire validated config, common exports, and CLI/SDK integration. Implement downloads with bounded limit+1 streaming, nullable source_size, source_size_at_least=limit+1 on unknown-size truncation, warning metadata, containment, hashes, and partial cleanup without draining the stream. Implement normalized session aliases with cross-process OS locks and atomic JSON; use Session.rid as session_id, accept session_token as missing, null, or string, and never synthesize it. Corrupt state must warn without secrets, be deleted under the alias lock, and leave the alias absent. Implement SDK-native B3 through TRACE_ID_VAR, SPAN_ID_VAR, and SAMPLED_VAR, defer W3C traceparent, and reset context tokens on every exit. Finish with typed integration checks and handoff to UNITTEST-005 and CODEREVIEW-005.

Subject: New to Open triage complete
Created: 2026-08-10T02:21:30
Updated: 2026-08-10T02:21:30
---
## New → Open triage

- **Status**: UNITTEST-016 confirmed New → transitioned to Open.
- **Documentation studied**: DESIGN-016 (15-op catalog, ADR-003 batch reads with --max-records, 3/12 metadata policy, reset verb ACL change), canonical env-var reference, metadata allow-list, DEV-016 implementation plan, and the established test suites for models/orchestration.
- **Critical thinking**: unit tests must be real unit tests (all SDK transport mocked, no live connections); coverage gate ≥80% branch on the new namespace; regression tests must prove `stream.reset` and `subscriber.reset_offsets` stay write-classified even under narrower override attempts.
- **Questions**: none.
- **Blockers**: none. Links: Contains LINK-00540, ParentChild LINK-00541 — registered and correct.
- **Required fields**: status, assignee (python-developer), priority (High), dates — validated.

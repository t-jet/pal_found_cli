Subject: Fix plan: classification parser contract and outcome checks
Created: 2026-10-18T17:36:31
Updated: 2026-10-18T17:36:31
---
Plan: correct the Marking.parse_classifications contract and guide against the official Palantir API; distinguish API batch errors from SDK-declared named errors; make the offline example verify both parsed and error outcomes for every submitted string; add focused SDK transport tests for empty and 1001-entry requests. Review FEATURE-015 REST source-fidelity design and DEV-STORY-072 context. Use SDK 1.101.0 with httpx.MockTransport; no live tenant or application logs apply. Preserve TESTEXEC-075 for formal QA.

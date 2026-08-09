Subject: Unit and integration tests complete
Created: 2026-08-09T14:29:40
Updated: 2026-08-09T14:29:40
---
Completed in commit d83fbbb with the scoped Language Models implementation and tests. The commit contains 11 files and 716 insertions, including parser/dispatch, ACL, policy, launcher, console wrapper, and focused tests. Independent evidence: 85 targeted tests and 1,012 full-suite tests pass; namespace branch coverage is 84.67%; Ruff, mypy, Bandit, help, wheel, and packaged-policy checks pass. The tests cover the exact two operations, JSON validation, real SDK routes and errors, write ACL and Tier 3 0/2, attribution/B3 restoration, retries, output/privacy, and installed execution. No external connection is used. All tests are committed, time is 8h, links are registered, and the In Progress DoD passes.

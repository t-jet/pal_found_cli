---
id: QUESTION-139
type: question
title: Provide owner-scoped credential or decline PUB-TC-009/011/012 for TESTEXEC-025
status: Closed
addressed_to: project-owner
created: 2026-09-28
updated: 2026-09-29
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# QUESTION-139: Provide owner-scoped credential or decline PUB-TC-009/011/012 for TESTEXEC-025

## Description

PROVIDE OWNER-SCOPED CREDENTIAL OR DECLINE PUB-TC-009/011/012

TESTEXEC-025 controlled-tranche execution (2026-09-28) hit a hard environmental
blocker for three authorized cases.

Background:
- QUESTION-131 (Closed) authorized: harmless tag+release+checksummed asset per
  repo (PUB-TC-009), read-only collaborator query (PUB-TC-011), read-only
  branch-protection query (PUB-TC-012).
- The executing QA environment has NO owner-scoped GitHub credential:
  * GITHUB_TOKEN / GH_TOKEN / GH_ENTERPRISE_TOKEN env vars all NOTSET
  * no `gh` CLI installed
  * no .ept/tmp/.gh_token (or any token file) present
  * git global config has `credential.helper=` explicitly disabled
- Anonymous reads work (quota reset, X-RateLimit 60/hr, ~52 remaining at probe).
  But the three cases above require write/auth:
  * GET /repos/{repo}/collaborators    -> HTTP 401 "Requires authentication"
  * GET /repos/{repo}/branches/main/protection -> HTTP 401 "Requires auth"
  * creating a tag+release+asset per repo -> requires write auth
- Evidence captured in .ept/tmp/testexec025-controlled-20260928 (anon-*-collab.json,
  anon-*-protection.json all 401; REST quota proof; heads.txt).

Question / decision needed from Project Owner:
1. Provision an owner-scoped credential into the QA environment so QA can
   execute PUB-TC-009/011/012 for real (token supplied via a protected channel),
   OR
2. Decline PUB-TC-009/011/012 as owner-scoped like PUB-TC-006/007/020 (skipped),
   accepting restricted-write as verified via: anonymous write denied
   (PUB-TC-010 PASS) + protection/collaborator endpoints requiring auth (401)
   + owner-declined skip. In this case QA will record them as owner-declined.

QA will not fabricate credentials or evidence. This question blocks TESTEXEC-025
until one of the two options is confirmed. If option 2 is chosen, no further
credential is needed and TESTEXEC-025 can be finalized to Resolved/Closed.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

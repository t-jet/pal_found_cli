---
id: QUESTION-132
type: question
title: Authorize public-to-private rollback test for TESTEXEC-025
status: Closed
addressed_to: project-owner
created: 2026-08-17
updated: 2026-09-28
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# QUESTION-132: Authorize public-to-private rollback test for TESTEXEC-025

## Description

PUB-TC-020 requires a real visibility rollback and must remain separate from ordinary fixture authorization. Please identify the exact repository or repositories in scope, approve a maintenance window, provide the pre-change settings and access baseline, explicitly authorize the public-to-private visibility change, name the recovery owner, define abort and restoration criteria, and identify who will verify and approve restored public access. The test must preserve canonical URLs and repository history, confirm intended private-state access restrictions without exposing credentials, restore the repositories to public, and verify anonymous browser, REST, HEAD, and clone access afterward. No visibility change may be attempted until the Project Owner supplies this authorization and recovery plan. QUESTION-113 proves public reachability but does not authorize a destructive visibility change; QUESTION-114 concerns publication evidence and does not provide this test window or recovery ownership.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

---
id: BUG-015
type: bug
title: Admin list skills promise pagination unavailable in CLI
status: Closed
affected_version: pal_found_cli_skills-worktree
created: 2026-10-12
updated: 2026-10-13
priority: Medium
resolution: Done
assignee: project-manager
reporter: project-manager
component: skills
---

# BUG-015: Admin list skills promise pagination unavailable in CLI

## Description

# Defect
Four Admin skill records tell users to continue when a next-page token is returned, but these SDK methods and CLI specs expose no page_token input: authentication_provider.list, enrollment_role_assignment.list, organization_guest_member.list, organization_role_assignment.list. The stated follow-up cannot be performed through the documented CLI.

## Acceptance criteria
- Explain actual result and continuation limit for all four operations.
- Do not imply callers can page with an unsupported flag; document a supported workaround only if verified.
- Source-check SDK signatures and CLI help; run offline skill gate.
- Independent QA verifies copied skill wording and records per-row result.

Related: FEATURE-012 DEV-STORY-042/043 and WORK-005.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

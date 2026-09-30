---
id: QUESTION-140
type: question
title: 'Branch-protection read blocked by token scope: provide admin-read credential or accept
  partial evidence for PUB-TC-012'
status: Closed
addressed_to: project-owner
created: 2026-09-29
updated: 2026-09-29
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# QUESTION-140: Branch-protection read blocked by token scope: provide admin-read credential or accept partial evidence for PUB-TC-012

## Description

# QUESTION-140: Branch-protection read blocked by token scope — provide admin-read credential or accept partial evidence

## Description

PUB-TC-012 (main-branch protection active) remains PARTIALLY verified after the
owner-scoped credential was provisioned via QUESTION-139 (option 1).

What works with the provided GITHUB_TOKEN (owner-scoped):

- `GET /repos/{repo}/branches` -> 200; `main` `protected` flag readable:
  pal_found_cli=protected:false, pal_found_cli_tool=protected:true,
  pal_found_cli_skills=protected:true.
- `GET /repos/{repo}/branches?protected=true` -> 200 (root=[],
  tool/skills=[main]).
- `GET /repos/{repo}/collaborators` -> 200 (PUB-TC-011 PASS).

What is DENIED with the provided token:

- REST `GET /repos/{repo}/branches/main/protection` -> HTTP 403 for all three
  repos (requires repository administration read scope; the provisioned token
  does not expose it).
- REST `GET /repos/{repo}/protected_branches` -> HTTP 404.
- GraphQL `repository.branchProtectionRules` -> "Resource not accessible by
  personal access token" for all three.

So the detailed protection policy (required reviews count, required status
checks/contexts, push restrictions, dismissals, force-push rules) is NOT
retrievable with the credential the owner provisioned. QA cannot claim a full
PASS for PUB-TC-012 without fabricating the policy evidence.

## Decision needed

1. Provision a credential (or grant scope to the existing one) that includes
   repository administration READ for branch-protection settings so QA can
   retrieve the actual rules for `main` on all three repos, OR
2. Explicitly accept the partial evidence as sufficient for PUB-TC-012:
   branch-protected flag is readable (tool/skills=protected, root=unprotected),
   collaborator roster confirms only the owner has push/admin, and anonymous
   write is denied (PUB-TC-010 PASS). In that case QA records PUB-TC-012 as
   PARTIAL (owner-accepted) and finalizes TESTEXEC-025 to Resolved/Closed.

## Evidence

- `.ept/tmp/testexec025-controlled-20260929/execution-log.md`
- `authed-<repo>-_branches_per_page_100.json` (protected flags)
- `authed-<repo>-protected-branches.json` (protected=true filter)
- GraphQL scope-denial responses (graphql-protection-summary.txt)

## Notes

No defect is implied in the repos themselves; this is purely a credential-scope
limitation. TESTEXEC-025 will remain blocked until one of the two options is
confirmed, per the QA closure gate (no fabricated completion).


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

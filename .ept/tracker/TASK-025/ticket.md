---
id: TASK-025
type: task
title: Remove three temporary filelock CI exceptions after supported Safety fix
status: Open
priority: High
assignee: devops-engineer
reporter: devops-engineer
created: 2026-11-19
updated: 2026-11-19
component: ci-security
due_date: 2026-11-24
---

# TASK-025: Remove three temporary filelock CI exceptions after supported Safety fix

## Scope
DevOps owns removal of temporary BUG-051 exceptions SFTY-20261017-72390, SFTY-20261017-54654 and SFTY-20261017-57659. Current mitigation retains vulnerable filelock 3.32.7 from Safety 3.8.1 and does not patch the package. First upstream review is due 2026-11-24, before November25. Hard expiry stays 2026-12-02 UTC; remove earlier when supported patched Safety ships. No automatic extension.

## Acceptance Criteria
- By 2026-11-24, check official Safety/filelock releases, supported dependency bounds and Python compatibility. Record observed versions, URLs, timestamps, resolver evidence and next action in comments. Recheck weekly and before expiry while exceptions remain.
- Once a supported Safety release resolves nonvulnerable filelock at least 4.2.1, verify normal resolution and pip check without forced overrides, forks or downgrades. Remove the three CI exceptions, obsolete exception-specific guards and vulnerable-version pins through independently reviewed source changes. Preserve existing nltk policy.
- Preserve full installed-environment dependency scanning including scanner dependencies, Bandit, strict failure on unsuppressed findings and all lint/type/test/build gates. Verify unrelated findings and expired entries block. Require independent security/compatibility QA, fresh normal candidate and merged-main all-eight-check success, plus applicable source/pin proof.
- If no supported fix exists by 2026-11-24, document unmet dependency condition and create a QUESTION under this task addressed to architect before expiry. Add Blocks and Question links and record prior status per workflow. Keep security blocking from December2UTC; escalate reviewed alternatives rather than silently renewing or weakening scanning.
- Resolve only after removal, reviewed source revision, CI evidence and independent verification are documented. A release check alone does not complete the task while exceptions remain. Any alternative remediation needs explicit decision and acceptance criteria through the QUESTION before changing scope.

## Deliverables
Reviewed removal change and immutable dependency, CI and QA evidence referenced from comments. No scheduler, email, automatic renewal or new global waiver.

## Related Documentation
.ept/docs/document_index.md; .ept/docs/deliverables/qa/WORK-007-release-pin-plan.md; BUG-051 comments20261118-080957-@devops-engineer and20261119-000019-@qa-engineer; QUESTION-198 route decision.

## Notes
Root task, High priority, assignee/reporter devops-engineer, due_date2026-11-24. RelatesTo BUG-051, TASK-022 and FEATURE-015 only. No new Blocks links or cycles. Existing BUG-051 mitigation acceptance remains separate from a supported package fix. Keep Open until actual follow-up execution begins.

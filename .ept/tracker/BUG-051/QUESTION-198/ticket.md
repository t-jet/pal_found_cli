---
id: QUESTION-198
type: question
title: Clarify supported CI dependency scanner remediation for Safety filelock conflict
status: Open
addressed_to: architect
created: 2026-11-18
updated: 2026-11-18
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-198: Clarify supported CI dependency scanner remediation for Safety filelock conflict

## Description

## Question
Do project requirements mandate Safety specifically, or permit maintained equivalent SCA tooling with the same full installed-environment scope, including scanner dependencies, strict failure on unsuppressed vulnerabilities, and no new ignores? Please identify a supported remediation path. If Safety is a hard requirement and no supported patched parent exists, identify the owner clarification needed. This question requests a decision; it does not authorize a tool or policy swap.

## Research Done
Reviewed document index, WORK-007 release-pin guidance, TASK-022, BUG-051 context/comments/links, tool ci.yml, pyproject.toml and existing policy. No duplicate question under BUG-051. CI44247425711 Python3.11.18/Linux and isolated WindowsPython3.11.9 reproduction establish scanner-self path Safety3.8.1 -> filelock>=3.16.1,<4.0 ->3.32.7. Project/runtime/dev install introduces no filelock. Local Safety reports same CVE-2026-112910/112908/112938 and exits64; pip check exits0. Dry-run Safety3.8.1 with filelock>=4.2.1,<5 exits1 ResolutionImpossible. Full evidence and hashes in BUG-051 comment20261118-080957-@devops-engineer; files .ept/tmp/bug051_security_triage_20261118/.

First-party GHSA-8mx5-7m5m-r77g, GHSA-6627-m3xw-93mp and GHSA-m462-7rxw-wvpg at https://github.com/tox-dev/filelock/security/advisories/ list patched4.2.1. Live https://pypi.org/pypi/filelock/json latest4.2.12 requiresPython>=3.11; published https://pypi.org/pypi/safety/json latest3.8.1 and upstream main retain<4.0. https://github.com/pyupio/safety/issues/925 open; https://github.com/pyupio/safety/pull/927 proposes patched bound but remains unmerged/unreviewed. No supported published parent upgrade identified. Older downgrade is unreviewed and not proposed. Existing full environment scope and prior time-bound nltk exception remain unchanged.

## Decision criteria
Name requirements/source establishing permitted scanner choice; identify supported dependency graph and validation plan; preserve full installed-environment coverage, strict failure, Bandit and all other CI gates; no forced4.x against constraints, advisory ignores, scope reduction or policy substitution. Separate scanner/tool decision from runtime compatibility. Require independent security/compatibility review and root approval before edits. No implementation authority or security acceptance granted by this question.

## Blocking boundary
Question blocks BUG-051 only; prior BUG-051 status Open. BUG-051 already blocks BUG-050 release acceptance. TASK-022 remains active and unblocked. Frozen tool files and publication pins stay unchanged.

## Acceptance Criteria

- Architect identifies whether Safety is mandatory, citing applicable requirements.
- Architect identifies supported remediation path preserving full environment scope and strict failure, or identifies required owner clarification.
- No source or policy edits occur before reviewed decision and root approval.

## Related Documentation

.ept/docs/document_index.md; .ept/docs/deliverables/qa/WORK-007-release-pin-plan.md; BUG-051 comment20261118-080957-@devops-engineer; TASK-022 publication criteria.

## Notes

Question blocks BUG-051, prior status Open. TASK-022 remains unblocked. Existing runtime files and security policy remain frozen.

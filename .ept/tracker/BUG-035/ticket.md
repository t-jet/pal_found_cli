---
id: BUG-035
type: bug
title: Audit skill omits required log API permission and OAuth scope
status: Resolved
affected_version: f30c97242c8fef553b72984bdaf02b3fe52d34db
created: 2026-10-16
updated: 2026-10-22
priority: High
assignee: python-developer
reporter: qa-engineer
component: skills
fix_version: 2190c40c3f73636b91348167b86cdb1bd7fb6fd7
---

# BUG-035: Audit skill omits required log API permission and OAuth scope

## Description

# Audit skill omits required API access prerequisites

## Severity and affected version

High. Skills audit candidate `f30c97242c8fef553b72984bdaf02b3fe52d34db`; `.agents/skills/pal-found-audit/SKILL.md` SHA-256 `c040dd592980bf28a93285171a541211e8871b0879b7fc83f293b3e09c5d74ba`.

## Reproduction

1. Read `.agents/skills/pal-found-audit/SKILL.md`, especially the `log_file.list` and `log_file.content` sections. It says only that inadequate permission fails; it does not name the needed grant or OAuth scope.
2. Search this skill and the core auth page for `api:audit-read` and `Create datasets with audit logs`: neither appears.
3. Compare the linked Palantir Audit overview, Authentication for API access, and List Log Files API reference.

## Expected

The copied standalone skill names the organization role workflow `Create datasets with audit logs for the organization` for the token's user or service user. For Developer Console OAuth applications, it also names the `api:audit-read` scope and the independent organization role assignment. The reader can request the exact prerequisite without opening public docs.

## Actual

The skill offers command examples but only says `inadequate permission` or `insufficient permission` fails. A novice cannot determine the exact role or scope offline. This fails FEATURE-015's local prerequisite and recovery criteria and DEV-STORY-043's standalone Audit operation acceptance criteria.

## Evidence

- Local: `.agents/skills/pal-found-audit/SKILL.md`, lines 29-48; no required role or scope elsewhere in the file.
- Palantir Audit overview: https://www.palantir.com/docs/foundry/security/audit-logs-overview (Authentication for API access, Required organization permissions).
- Palantir List Log Files API: https://www.palantir.com/docs/foundry/api/v2/audit-v2-resources/log-files/list-log-files (OAuth scope).
- Independent audit ledger: `maintainer/offline-knowledge-audit.json`, `pal-found-audit\\SKILL.md` QA row.

## Test execution reference

Independent FEATURE-015 20-skill audit under DEV-STORY-061. Static source comparison; no tenant request or credentials used.

## Separate source ambiguity

The overview says `nextPageToken` is always present, even with empty data, while the API reference describes an optional token at the final page. The skill's polling wording should be reconciled with the intended server contract during correction; this ticket's confirmed failure is the missing access prerequisites.


## Acceptance Criteria

- [x] Standalone Audit skill names the required organization workflow for the token user or application service user.
- [x] Developer Console guidance names `api:audit-read` and explains that OAuth scope does not grant the organization role.
- [x] Both list and content prerequisites are explicit; cursor guidance handles empty pages and absent continuation tokens.
- [x] Independent whole-page review and current focused Audit tests verify the correction.

## Related Documentation

- `pal_found_cli_skills/.agents/skills/pal-found-audit/SKILL.md`, Access prerequisites.
- `pal_found_cli_skills/maintainer/skill-independent-review-admin-governance-audit.json`.
- `.ept/tmp/feature015_bug034_035_readiness_20261022.json`, independent continuity and focused test evidence.
- `.ept/docs/document_index.md`, FEATURE-015 QA and release evidence index.

## Notes

Offline documentation acceptance only. FEATURE-015 coordinated release acceptance remains pending; BUG-034 stays open.

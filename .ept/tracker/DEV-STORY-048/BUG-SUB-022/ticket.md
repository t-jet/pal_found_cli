---
id: BUG-SUB-022
type: bug_subtask
title: Provide complete local Data Health configuration contracts
status: Closed
created: 2026-10-06
updated: 2026-10-07
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 8
time_spent_hours: 0.25
---

# Missing offline Data Health check configuration contracts

## Reproduction and observed result

Baseline skills bb26037813cda6dab5f51c03af9a0b08162a5f7e. Open pal-found-data-health/references/01-check-report.md line5 using only the owning skill. Author check.create or check.replace for any non-buildStatus configuration. The guide delegates fields to SDK model inspection and supplies only a buildStatus example. Supplied SDK documentation CheckConfig.md lists16 discriminator alternatives; their required/nested fields are absent locally. No runtime failure or live enrollment execution is claimed; the observed defect is missing reader knowledge.

## Expected result and acceptance

The independently usable Data Health skill defines every supported create/replace configuration discriminator and complete transitive field/enum/union contract locally, with exact create-versus-replace differences, adaptable examples and meaningful success/error checks. Identify actual prepared CLI SDK release and compare supplied source1.79.0 against frozen1.101.0 as appropriate; do not invent compatibility or API guarantees. Preserve six CLI operations and current examples.

## Ownership and fix plan

Existing FEATURE-012/DEV-STORY-048 owns Data Health operation knowledge. Fix only pal-found-data-health/references/01-check-report.md and new local configuration parts required for readable<=300-line leaves. Remove required SDK/public lookup instructions in favor of local contracts. Independent architect source review and QA offline non-buildStatus authoring/replace/error case verify repair. This defect blocks affected FEATURE-015 audit061 and integrated acceptance070, not completion of unrelated FEATURE-012 work. No CLI code/interface or installation instructions change.

## Sources

Supplied .ept/docs/customer_input/foundry-platform-python/docs/v2/DataHealth/{Check.md,models/CheckConfig.md,models/ReplaceCheckConfig.md} and every reachable configuration model; compare prepared/frozen SDK version before authoring. FEATURE-015 BA-DES-015/SA-DES-014 offline knowledge and dependency ownership contracts. Application logs are not applicable to a documentation-only knowledge gap; the quoted line and missing alternatives are reproducible evidence.

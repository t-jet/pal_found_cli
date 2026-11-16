---
id: BUG-049
type: bug
title: Third-party application standalone pages omit setup identity and recovery contracts
status: In Progress
affected_version: 523fd81d238d7a482db3c67af7b97d514c34bd2f
created: 2026-11-16
updated: 2026-11-16
priority: High
assignee: python-developer
reporter: qa-engineer
component: skills
---

# Third-party application standalone pages omit required setup and recovery

## Reproduction and environment

Copy only `pal-found-third-party-applications` from integration `523fd81d238d7a482db3c67af7b97d514c34bd2f` and provide prepared CLI/SDK tools. Read both pages without sibling skills or external documentation. `SKILL.md` has 58 lines, SHA-256 `1c957cb54c00e7c03ab50b3f5b368f028112bfaa2e034378b2d02e4ff0a296e2`; `references/01-applications.md` has 100 lines, SHA-256 `8f00b367d4afa7184662a6474c9e5cd7c90519cbeae6af2fc686b339802ac737`. Before/after bytes match. Both pages receive independent FAIL. Entry links to reference; reference lacks return link. All leaves satisfy 300-line limit.

## Expected and actual

Expected complete standalone prerequisites, identity/resource acquisition, response meanings and actionable recovery. Actual pages do not explain FOUNDRY_HOSTNAME, FOUNDRY_TOKEN, configuration precedence or required prepared artifacts. APP_RID is described as a real RID without explaining how to obtain and verify it. CLI uses UserTokenAuth; no built-in service-account OAuth grant flow exists. Local policy recovery and local/enrollment/admin boundaries remain unstated. Permission labels lack actionable recovery. No new universal scope or IAM permission should be invented where source is silent.

Eight documented CLI examples also fail because of separate runtime defect. Preserve documented canonical CLI usage and retest against its corrected candidate; do not hide defect with direct REST examples. First-page/list/resume semantics are not accepted until native CLI retest succeeds. No search operation exists; describe supported list-based discovery clearly.

## Acceptance criteria

- Complete both pages with prepared runtime/command boundary, bearer token and hostname setup, configuration precedence, application RID acquisition/verification, production archive prerequisites, and explicit local versus authorized enrollment and administrator-controlled steps.
- Explain supported identity handling and service-account limitations from actual CLI. State source silence about exact scopes/grants; do not invent scope strings or add OAuth credential flow that CLI lacks.
- Provide usable 401/403/404, missing configuration, policy denial, invalid file/version, conflict and paging failure/recovery guidance. Explain how to verify success after deploy, undeploy and delete. Preserve optional deployedVersion, subdomains, Version and null deletion CLI result meanings.
- Preserve nine operations, command syntax, binary upload constraints, snapshot lifetime, stdout/stderr paging distinction and local navigation. Add reference return link; each leaf remains at most 300 lines.
- Ground hosting UI/login/sharing/scan claims in supplied primary-source evidence or qualify unsupported details. External sources remain optional attribution after local explanation.
- Independent whole-page QA reruns all examples and negative/paging recovery cases with fixed runtime using native SDK 1.101.0 and 1.111.0 fake transports, denied public network and exact hashes. No live tenant claim or audit promotion until verified.

## Evidence and ownership

`.ept/tmp/thirdparty_whole_pages_review_20261116/review.json`, `raw_proof.json`, `console_process.json` and frozen `skill/`. Initial matrix: 26 actual CLI cases, 13 PASS and 13 FAIL; nine separate native SDK reference probes PASS and are not a CLI workaround. Source tag: SDK1.101.0 `168d51910570b6966afa2320333ab36f6a3f7ccf`. Tool candidate `db72226c97c55af290f09906dc04f53037513636`, module hash `b3a976e0c90c11fab60d0dca01dfd1baed37c4e6ecb24018bc085a9743aa4989`.

Guidance remediation belongs to DEV-STORY-061/FEATURE-015 and affects historical original DEV-STORY-021. It blocks DEV-STORY-061 audit and DEV-STORY-070 release acceptance. Existing Closed BUG-019 remains unchanged. See indexed BA-DES-015 and SA-DES-014 standalone contract and audit requirements.

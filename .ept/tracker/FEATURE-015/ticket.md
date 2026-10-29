---
id: FEATURE-015
type: feature
title: Make Foundry development guidance complete without public internet
status: Waiting for Implementation
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: project-manager
reporter: project-manager
component: skills
---

# FEATURE-015: Make Foundry development guidance complete without public internet

## Business need
Agents developing Foundry pipelines and applications in environments with restricted public internet must find required knowledge in distributed skill files. Current pal-found-dev reference prose delegates material steps to external documentation.

## Scope
Strengthen development guidance introduced by FEATURE-013 across all topics in development-skill-coverage.md, including separate REST API guidance. Audit essential external dependencies across all 20 skills and define finite affected scope during BA/SA analysis. FEATURE-012 retains existing CLI operation semantics; avoid duplicate implementation.

## Acceptance criteria
- Required concepts, behavior, procedures, prerequisites, examples, result interpretation and troubleshooting are available locally for each approved development topic.
- External URLs serve as optional provenance; completing covered workflows never requires opening public documentation.
- Local skill navigation resolves within distributed files, with no links to internal development documents.
- Independent reviewers complete defined development scenarios using local skills and preprovisioned tools. Review checks decisions, code or configuration, validation, results and recovery; link checks alone are insufficient. Authorized Foundry enrollment/API access remains distinct from public documentation access.
- User example topics receive concrete local guidance: repository navigation, transform preview, repository/Python unit tests, data expectations, branch settings, branching/release, project structure, production pipelines and local VS Code workflows.
- No installation or folder-copy prose appears inside skills.

## Related documents
Source topic matrix: .ept/docs/customer_input/development-skill-coverage.md. Prior approved requirements: BA-ANA-014-user-facing-foundry-skills.md and FEATURE-012 offline CLI scope. New analyses: BA-ANA-016 and SA-ANA-016.

## Planning
BA/SA analysis defines covered tasks, measurable offline completion checks, prerequisites and affected bundle scope. New Project Owner approvals precede design; approved design and grooming precede implementation. Plans and evidence are recorded in ticket comments.

## T37 scope correction (2026-10-06)
Project Owner requires offline development guidance for every REST operation available in the frozen Foundry Python SDK library. Coverage includes all services, resource clients and operation methods, with complete local request, response, error and transitive model knowledge. Governance project and folder navigation and modification, and AIP application capabilities, are explicit examples. The previous ten-method restriction is superseded. Version and stability labels must remain accurate; no operation or version mode may be silently excluded. SDK coverage is independent of the 351-operation CLI inventory.

WORK-003 and WORK-004 revise pending business and technical designs, record baseline impact, verify SDK provenance and inventory, revise stories and QA gates, and obtain fresh peer reviews. Closed BA-ANA-016 and SA-ANA-016 remain historical approved baselines. Revised owner design approval precedes grooming and implementation. Other 36 development topics, the 20-skill audit, GitHub-only delivery and no-installation prose remain in scope.

---
id: DESIGN-064
type: design
title: 'DEV-STORY-063: Groom technical scope and estimate'
status: Closed
created: 2026-10-06
updated: 2026-10-07
priority: High
assignee: tech-lead
reporter: tech-lead
estimated_hours: 2
time_spent_hours: 0.2
---

# Finalize bounded grooming

## Scope and acceptance

Record source/file ownership, six applicable tasks, estimates and independent lead reviews before closure.

Approved indexed BA-DES-015 and SA-DES-014 revision2, architecture parts and customer source map analyzed. T07/T08: references/pipelines/{sql,workspaces}.md; examples/workspaces/**; add links into pipelines.md through062 owner. Official transforms-sql overview/Spark reference and Code Workspaces getting-started/data/transform publication sources. J3 expected decisions: explicit input/output schema and dialect; deterministic join/null/duplicate fixture results; prepared runtime versus missing environment; preview result versus published transform/build/committed dataset. Publication permissions and branch selection are explicit. SQL/workspace APIs cannot be inferred from Python transform syntax. Each topic has six prescribed headings carrying seven elements and <=300 lines per leaf. All essential knowledge/assets local; no installation/copy/internal reader links. Frozen061 navigation enables authoring without claiming final audit complete. Scope 34 hours/3 points fits one contributor sprint plus independent review slots; measure actual effort and split unknown additional source scope before exceeding budget. Shared overview additions coordinated with owner062 or064. No infrastructure DEVOPS task; final GitHub delivery070. Source-derived expected decisions frozen here before content; formal TESTCASE starts only after runnable implementation. Registered contributor resources available; no unresolved clarification. No implementation until DESIGN Closed and story Development.

## Estimate and responsibility

2 contributor hours. Assignee tech-lead. Preserve edits from other contributors.

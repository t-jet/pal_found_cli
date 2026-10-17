---
id: CODEREVIEW-069
type: codereview
title: DEV-STORY-087 codereview J14 AIP REST contracts
status: Blocked
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: architect
reporter: tech-lead
estimated_hours: 12
---

# DEV-STORY-087 codereview

## Owned scope
47 exact operation IDs in .ept/docs/deliverables/development/FEATURE-015-rest-operation-partitions.json; partition hash 079d95a7516632df65ae4c73fbf629f8d520283bb59db014bf8f5b1bd4f68395.
Resources: v2.aip_agents.Agent, v2.aip_agents.AgentVersion, v2.aip_agents.Content, v2.aip_agents.Session, v2.aip_agents.SessionTrace, v2.language_models.AnthropicModel, v2.language_models.OpenAiModel, v2.models.Experiment, v2.models.ExperimentArtifactTable, v2.models.ExperimentSeries, v2.models.LiveDeployment, v2.models.Model, v2.models.ModelFunction, v2.models.ModelStudio, v2.models.ModelStudioConfigVersion, v2.models.ModelStudioRun, v2.models.ModelStudioTrainer, v2.models.ModelVersion.
Core069 owns structural contracts, full models/errors, service indexes and common patterns. This story owns resource behavior under references/rest/<version>/<service>/<Resource>.md (numbered leaves at most300lines) and reader examples/fixtures examples/rest/087/ inside standalone pal-found-dev. Tests own tests/test_offline_rest_087.py.

## Acceptance criteria
Independent architect reviews every owned method against frozen docs/source/API references, full corrected models/errors and actual runnable examples. Record exact per-operation findings and dispositions. Do not review own content; wait paired DEV Resolved.
Every operation has locally available signature/HTTP/body/typed inputs/results/nested models/errors/effects/availability/modes and bounded recovery. Every example supplies synthetic or precisely described tenant values, actual SDK call, request/response/error assertions. Use actual asynchronous return signatures, not inferred Awaitable types. Keep source silence explicit with authorized tenant verification; invent no universal scope or idempotency guarantee. Independently reconcile full model/error closure;3242 is not a cap. Governance covers hierarchy traversal and supported modification/access/uncertain-write recovery; AIP covers actual agents/versions/sessions and model capabilities, private/beta enablement, denied access, canceled streams and finite continuation as applicable to owned operations.

## Related documentation
BA-DES-015/SA-DES-014 revision2 and closed owner approvals QUESTION179/182. Indexed FEATURE-015-rest-authoring-contract.md and exact partition JSON. Primary SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0. Supplement SDK silence with relevant official API references while authoring. Preserve351 CLI operations and other authors, Apache2.0 copyright/license/NOTICE. No installation/copy/internal reader links. Final independent REST acceptance093, GitHub-only integrated publication070.

## Estimate and readiness
12 contributor hours; total72h candidate8points within80h two-week budget with reviewer/QA slots. Firstthree operation/example/constraint fixtures measured before scaling; split exact exclusive IDs if capacity exceeded. No implementation before DESIGNClosed, independent lead reviews and parentDevelopmentDoD. No infrastructure change; no DEVOPS child because070 owns release.

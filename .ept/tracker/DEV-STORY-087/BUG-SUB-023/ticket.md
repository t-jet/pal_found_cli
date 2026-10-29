---
id: BUG-SUB-023
type: bug_subtask
title: Document and bridge SDK1.101 ModelStudio config-version integer path failure
status: Closed
created: 2026-10-07
updated: 2026-10-07
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 3
time_spent_hours: 1
---

# SDK1.101 integer path encoding limitation

## Unsatisfied requirement
087 must provide faithful offline authoring and executable result/error handling for v2.models.ModelStudioConfigVersion.get; keep it in full425 catalog.

## Reproduction and actual result
Prepared Python3.11.9/foundry-platform-sdk1.101.0/OpenAPI1.1697.0/httpx0.28.1/Pydantic2.12.5. Call ModelStudioConfigVersionClient.get(valid studio RID,1) through common MockTransport. It raises quote_from_bytes() expected bytes before transport. Actual source parameter model_studio_config_version_version is an integer; api_client.py526–529 calls quote(v,safe="") without converting integer path parameters. Frozen commit168d51910570b6966afa2320333ab36f6a3f7ccf. .ept/tmp/trial-domain-fixtures.py and rest-fixture-trial.json record realSDK94pass/thisonefailure; two binarybody assertion errors already corrected.

## Expected result and owned fix
Skill explains exact SDK/version limitation and gives supported direct REST alternative for GET /v2/models/modelStudios/{modelStudioRid}/configVersions/{modelStudioConfigVersionVersion}, correctly URL-encoding studioRID and decimal version, preview query, authorized header, timeout, typed SDK response and named/generic errors. Preserve actual failed nativeSDK reproduction. No silent monkeypatch, fabricated nativeSDK success, upgradedversion or operation exclusion. Own087 reader guide and examples/rest/087/model_studio_config_version.py plus regression tests; SDKcheckout/library remains source baseline.

## Acceptance
Offline realHTTP MockTransport checks exact path/query/header, full SDK response and typed named/generic error handling. Independent source/architect and QA review verify workaround fidelity and original failure before closing. Fixture success does not prove enrollment access; actual authorized call remains declared live boundary. This is one operation's authoring defect, not a wholeSDK exclusion. No unresolved design question; FEATURE015 revision2 approvals and parent087Development reviewed. Three contributor hours candidate; split if workaround expands.

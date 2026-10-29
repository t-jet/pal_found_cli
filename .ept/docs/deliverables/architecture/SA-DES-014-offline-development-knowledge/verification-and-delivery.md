# 3. Verification, migration and delivery

## 3.1 Automated checks

V owns test changes and the final verification story. Keep existing Python/pytest stack. Replace the test asserting exactly five reference files with manifest-based topic reachability and local Markdown file/anchor validation. Nested references use their actual parent path when linking the entry point. The number of parts is an authoring decision within the topic contract.

Maintain `tests/fixtures/offline/topic-register.json` with 37 stable topic IDs, exact local headings and required component destinations. Maintain `tests/fixtures/offline/rest-contract-register.json` with all 425 operation identities, version/stage, source identity/hash, local contract/example/model/error destinations and derived closure. These are test inputs, not distributed reader dependencies. Their values support structural checks; semantic approval comes from independent tasks. Distributed examples contain every needed fixture under the owning skill.

For each topic, the topic register records all seven BA element destinations, including an explicit `access_boundary` destination for local steps, authorized enrollment steps and administrator prerequisites. This destination may share the `Prerequisites` heading. Structural validation checks its reachability; semantic review checks the actual distinctions and the reader's resulting decision.

Check all 20 skills for broken file/anchor links, escape outside an owning skill for a required reference, forbidden project/copy directions, new installation prose and source-only reading directives. The development skill contains no installation prose; existing approved CLI prerequisite blocks remain governed by their owning requirements. Review directive candidates manually; do not prohibit optional provenance URLs. Compare operation identifiers and namespaces against the frozen 351-record baseline. Changes require their FEATURE-012 owner and review. Retain existing documented example and metadata/access-control regressions.

Run standalone development-skill checks from a staged folder under parent `.ept/tmp`; make only this folder available to the task reader. Exclude sibling skills, repository tests, authoring sources and deliverable documents from its knowledge. Validate reachability and all required assets from this isolated tree. Use pytest temporary paths under `.ept/tmp`, through `--basetemp`, for this project.

Fixture examples run in a network-blocked test process: reject DNS lookup, socket connection and HTTP dispatch; supply the documented fake transport or fixture responses directly. Record the blocking mechanism and demonstrate that an attempted external request fails. Subprocess/browser examples require an equivalent deny rule or fixture-only runner, with evidence. Never label a monkeypatch of one HTTP library as proof that every process is disconnected.

## 3.2 Independent semantic journeys

QA prepares prompts and expected decisions before reading implementation output. The reviewer receives only the isolated skill, preprovisioned tool versions, synthetic fixtures and stated tenant/recorded UI context. Record exact local sections consulted. Expert memory cannot fill a missing essential fact. Report fixture verification separately from live Foundry execution.

| Journey | Fixtures and required outputs | Failure case |
| --- | --- | --- |
| J01 Repository pipeline lifecycle | orders/customers CSV, recorded Code/Branches/Tags/PR/Checks/Settings; transform, tests, expectation, preview interpretation, branch protection, release/build verification and project ownership plan | failed expectation or check blocks release; preview success alone is insufficient |
| J02 Incremental and fallback | append/update snapshots and branch views; decide incremental versus snapshot rebuild, transaction state and fallback | changed schema or fallback input requires explicit next action |
| J03 SQL/workspace | synthetic table and notebook state; valid SQL, limitations, output publication and checks | unsupported construct or missing output permission |
| J04 Ontology/interface/query | Order/Asset metadata with nullable fields; type/link/interface design and query result | incompatible interface/property or inaccessible object |
| J05 Actions/Functions | synthetic validation result and runtime-specific signatures; Action input, validation, Function tests/publication and expected effects | authorization/validation failure; no blind write replay |
| J06 Compute | container/configuration/Source fixture; execution mode, input/output/provenance, scaling and recovery plan | Source or execution-identity denial |
| J07 OSDK React | generated binding and OAuth configuration fixture; callback/query/loading/error state, Action and release plan | OAuth restriction or user permission denial |
| J08 Widgets | parameter/event schema and recorded playground/Workshop state; round trip, first release, subsequent preview, additional widget and Marketplace plan | missing first release or wrong parameter/event type |
| J09 Branch/security contexts | Git/dataset/Global snapshots and role table; choose context, review/rebase/fallback, integration boundary and safe merge | wrong branch or unavailable integration/merge permission |
| J10 Production support | lineage graph, build history, freshness/schema check and alert fixtures; diagnose root cause, schedule/support action and recovery evidence | healthy build with stale output or upstream permission failure |
| J11 REST reads | metadata, empty intermediate file/object pages, binary table and documented error envelopes; derive exact request/SDK call, parse results and stop within bounds | repeated cursor, partial retrieval, 401/403/404/429/503 or unsupported content type |
| J12 REST writes/status | create/upload/commit/get/abort recorded states and Build pending/terminal records; reconcile known transaction RID, handle uncertain outcome and finite status checks | timeout after write or pending state after budget exhaustion |
| J13 Governance REST application | project/folder/access fixtures; discover project, traverse folders, plan and validate supported modifications with explicit access effects | empty/repeated pages, inaccessible resource, rejected or uncertain write |
| J14 AIP REST application | Agent/version/session/model fixtures; choose available capability, author session/continuation or model request, validate output and cleanup | missing enablement, stream cancellation, version mismatch or iteration limit |

REST cases select methods from every one of the 20 API-version/service namespaces. Independent authors receive isolated skills, fixtures and preprovisioned tools with public network denied; their prompts omit method names and contracts. Every operation example executes against SDK-backed transport fixtures and asserts serialized request plus response/error handling. Governance and AIP cases require complete application code and safe write/stream behavior. Counts, URL scans and fixture-free prose review cannot replace semantic evidence.

Each journey rubric scores six independent dimensions: capability/lifecycle choice, prerequisites/version/identity, exact steps/configuration, complete example inputs/results, success checks, and failure/recovery. Each dimension is pass/fail with a local evidence link and observable output. All six must pass. All 37 topic rows require the same six-component review even when several rows share a journey. No averaging hides a missing topic.

The prerequisites/version/identity dimension explicitly scores the seventh BA element, access boundary. A pass requires identifying what can execute locally, what requires authorized enrollment connectivity, and what requires administrator enablement or provisioned artifacts. Incorrectly describing remote preview as disconnected, or omitting an enrollment or administrator prerequisite, fails that dimension. Six rubric dimensions therefore verify all seven business elements.

## 3.3 Measurable acceptance gates

| Gate | Required result |
| --- | --- |
| G1 Local graph | 37/37 topic roots reachable from entry; every required file/anchor/asset resolves within owning folder; every leaf at most 300 lines |
| G2 Topic completeness | 37/37 reviews verify all seven BA elements through six technical dimensions, including explicit local/enrollment/admin access boundaries in prerequisites; all 20 skill audits complete; zero essential public knowledge dependencies |
| G3 REST closure | 425/425 exact operation identities and complete contracts/examples; complete independently reconciled model/error closure, starting from 3,242 extracted symbols; stage counts 218 Stable, 129 Public Beta, 78 Private Beta; HTTP/SDK agree on 1.101.0 |
| G4 Examples | Every runnable example produces asserted success output and meaningful documented failure; bounds and stream closure checked; network-denial probe passes |
| G5 Semantic tasks | 14/14 independent journeys plus at least one independently authored case per API-version/service namespace pass all dimensions using isolated content; zero undocumented essential steps |
| G6 Preservation | 20 existing skill identities and 351 supported operation records preserved; existing regressions pass; zero unresolved task-critical shared FEATURE-012 blockers |
| G7 Fidelity | Every topic/method/model has an independent source review with applicable version/stage and exceptions; unresolved critical source conflicts zero |
| G8 Release | Reviewed immutable skills commit pushed to existing GitHub repository; remote SHA and validation run verified; parent gitlink recorded |

QA artifacts record prompt, tools/artifacts, blocked network mechanism, tenant versus fixture mode, local headings, resulting code/configuration/decisions, expected/actual outputs, gaps, reviewer and commit. Source review and task review should be performed by agents other than the content author. A failed gate returns work to its owning story; essential FEATURE-012 defects block both affected story and final verification.

The extracted 3,242-symbol count is a starting inventory, not a cap. Independent reconciliation records any additional indirect/compound forward-reference dependency, updates its source evidence and affected examples, and requires review of the full corrected closure before G3 passes.

## 3.4 Migration and release procedure

1. Freeze topic IDs, file ownership and all-operation catalog in approved BA/SA design; bind exact operation sets to stories. Independently reconcile released SDK 1.101.0 source/runtime and model/error closure during grooming.
2. Capture current Git SHA, 20 skill identities, operation inventory and existing test results. Complete the dependency audit and link essential shared defects before accepting affected content.
3. Author local task parts and examples; preserve current overview filenames. Replace essential public-reading instructions with local routes. Verify links whenever a leaf splits.
4. Update layout-sensitive tests, registers and fixture runners; run source review, independent semantic journeys and preservation checks against one immutable candidate.
5. Complete required code/content review, QA and ticketed deployment work. Push reviewed skills commit to existing GitHub origin without force; verify remote SHA and repository validation status. Record source/evidence links and parent gitlink through the release ticket.
6. If publication verification reveals a content defect, ticket the correction and publish a reviewed corrective or revert commit. Restore the previous verified content revision using normal Git history. Re-run affected gates before marking delivery complete.

Distribution is GitHub only. No package publication, installer, downloader, knowledge server, browser automation service or data migration is required. Preprovisioned Python/Node tools, packages, generated bindings, extensions, container artifacts and authorized enrollment access remain runtime prerequisites. A fully disconnected reader can author and test with supplied fixtures; live preview/build/publish/API steps must name their enrollment connectivity requirement explicitly.

[Back to design](../SA-DES-014-offline-development-knowledge.md)

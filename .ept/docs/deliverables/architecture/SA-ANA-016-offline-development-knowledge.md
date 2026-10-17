# SA-ANA-016: Offline Foundry development knowledge

| Field | Value |
| --- | --- |
| Feature | FEATURE-015 |
| Status | Closed; BA approved in QUESTION-176 and Project Owner approved in QUESTION-177 on 2026-10-06 |
| Date | 2026-10-06 |
| Related work | BA-ANA-016, FEATURE-012, completed FEATURE-013, SA-ANA-014, SA-DES-013 |

## 1. Problem and scope

The distributed development guide explains several platform concepts but sends readers to public documentation for required development steps. A reader cannot complete those tasks when public internet access is restricted. FEATURE-013 already required essential local explanations; FEATURE-015 strengthens that content and replaces verification that accepted source links as sufficient evidence.

Scope covers all 36 substantive subsections in customer `development-skill-coverage.md`, its reading order, and the separate REST API topic. The unit of acceptance is a development task with enough local information to make and verify its decisions. Each topic needs concepts, prerequisites, procedure, representative example, expected result, constraints, and troubleshooting. Grouping several topics in one local part remains valid when each topic meets that contract.

Public documentation access and access to an authorized Foundry enrollment are separate dependencies. Local fixture tests and planning can run without Foundry. Previews, builds, publishing, OAuth registration, and live API requests can require enrollment access, platform permissions, and services enabled by administrators. Runtime packages, generated application SDKs, tools, and sample data must already be available through the organization's approved provisioning process. The skill must explain the prerequisites and relevant failures without adding package installation or folder-copy instructions.

This finite knowledge set supports the development workflows in the approved topic register and their documented API examples. It does not establish completeness for every future Palantir API or enrollment-specific generated Ontology. Each REST workflow must carry every method and model contract it uses locally; a reference to an unspecified online endpoint is unacceptable. BA and Project Owner approval must confirm this coverage boundary before design.

## 2. Current implementation and affected interfaces

The audit inspected the 20 skill folders and their 108 Markdown files. `pal-found-dev` contains six files and 184 external URL occurrences. A search found 38 lines that combine a public URL with a possible reading directive. These counts identify review candidates; they do not classify every citation as a missing dependency.

| Current component | Observation and required change |
| --- | --- |
| `pal-found-dev/SKILL.md` | Existing task navigation can remain. Add a precise capability/prerequisite boundary and route required decisions to local content. |
| `references/pipelines.md` (128 lines) | Repository navigation, previews, repository/Python tests, expectations, branch settings, release design, project structure, production pipelines, and VS Code setup currently delegate material steps to links. Expand local procedures and worked examples. |
| `references/ontology-compute.md` (48 lines) | Several paragraphs cover Ontology types, Actions, Functions and Compute Modules. Add runtime-specific function authoring/tests, configuration steps, and container lifecycle examples with local contracts. |
| `references/applications-branching-security.md` (170 lines) | Review each OSDK, React, widget, branching, and permission workflow for configuration, test and release details that the reader must currently discover elsewhere. |
| `references/operations.md` (60 lines) | Add concrete lineage investigation, check selection, alert ownership, diagnosis and recovery procedures, including expected evidence after a correction. |
| `references/rest-api.md` (118 lines) | Host/auth/paging guidance and bounded examples exist. Operation discovery still requires online API pages. Bundle complete contracts used by covered recipes, including request/response models and error handling. |
| Other 19 skills | Audit every public citation in context. Repair an essential concept/procedure dependency discovered during review; preserve supported operation records. CLI operation contract gaps remain assigned to FEATURE-012. |
| Repository tests | Existing checks skip HTTP links and assert the exact five-part development layout. Replace that layout assumption with reachable local topic checks when parts split, and add semantic task acceptance. |

FEATURE-012 owns the 351 supported CLI operations, their input/effect/result/error descriptions, and interface correctness. FEATURE-015 owns complete development knowledge and its local dependencies. A shared CLI fact has one consistent meaning; a FEATURE-012 implementation ticket should handle a newly discovered operation defect. FEATURE-015 should link that dependency instead of creating conflicting operation semantics.

No CLI entry point, installed package API, Foundry endpoint, authentication scheme, permission policy, or service changes are required. Affected interfaces are Markdown navigation, examples consumed by agents, repository validation, and the Git revision distributed to users.

## 3. General approach and stack

Keep Markdown in each existing skill folder. A short entry point selects a task and links to topic overview pages; those pages link to smaller procedure/example/reference parts. Every relative link and asset must resolve within the owning skill folder. An independently distributed `pal-found-dev` folder must contain its own required explanations; another namespace skill may be named as optional supplementary guidance.

Split long guides at task boundaries while preserving the current entry points where practical. A leaf stays at or below 300 lines. Splitting should preserve an explicit path from a topic overview to its procedures, examples and troubleshooting. Files may use nested directories when the hierarchy makes navigation clearer. Do not compress essential instructions to preserve five filenames.

Use the current Python/pytest validation stack. No knowledge server, scraper service, browser extension, searchable database, or internet retrieval tool is needed at runtime. Authoring may use official Palantir sources and the local SDK checkout. Distribution contains authored Markdown and any small local example assets that readers need. A build-time source refresh is optional maintainer work, never a step the restricted reader must execute.

### 3.1 Local content contract

For every registered topic, the reviewer must identify local answers to these questions:

1. What capability fits this task, and what does its lifecycle or transaction boundary mean?
2. Which resource identifiers, permissions, runtime/language version, features and data are prerequisites?
3. Which controls, files or commands does the reader use, in what order, and why?
4. Which complete example demonstrates the decision, including inputs and expected output or state?
5. Which tests or observations establish success, and which failures change the next action?
6. What requires enrollment connectivity, what can use local fixtures, and what remains dependent on administrator configuration?

The pipeline example supplied by the user becomes a required acceptance journey. Local guidance must explain the Code/Branches/Tags/Pull Requests/Checks/Settings views; transform discovery and preview; repository test discovery and Python fixtures; expectation success/failure behavior; protected/default/fallback branch settings; review/merge/release/build sequence; project boundaries and production ownership; and local VS Code interpreter, authentication, preview and test prerequisites. It must explain what preview does and which result still requires a production build check.

Official [Python local development](https://www.palantir.com/docs/foundry/transforms-python/local-development) documents administrator enablement for extension/preview and the local test executable. [Local preview](https://www.palantir.com/docs/foundry/transforms-common/local-preview) distinguishes Python extension preview from Gradle preview executed remotely in Foundry. Those distinctions must appear in local text; describing all preview as disconnected execution would be incorrect. [Repository tests](https://www.palantir.com/docs/foundry/code-repositories/unit-tests) links to language-specific testing, so copying that high-level page alone would preserve the gap.

### 3.2 REST and SDK contracts

Use the checked-in SDK method/model documentation as authoring evidence. Record the source checkout revision, API family and version, method path, release stage, and reviewed SDK compatibility in the maintainer evidence. The inspected checkout is `2da67907be429c35f747eef565867ce81dd2cafc`; its package metadata says `0.0.0`, which does not establish a released SDK compatibility version.

Before publishing examples, resolve compatibility against the source contract and the actual supported SDK version used for verification. Distributed guidance should state the verified SDK/API/runtime scope in reader terms. It must not expose `.ept` paths or require the SDK source checkout. Distinguish platform SDK, generated Ontology SDK, and CLI support.

Each covered REST recipe needs local method/path, parameter meanings, required scope and permissions, request/response content types, response fields, errors, and every referenced nested model needed to form the request and interpret its result. Add a navigable local contract index for those recipes. An open-ended instruction to locate an operation online cannot remain the first development step. The local catalog should identify its coverage explicitly; no contract may claim that an unreviewed method is supported.

Keep v1/v2 and Functions TypeScript v1/v2/Python examples separate. Enrollment-specific object API names and generated types remain reader-supplied prerequisites, with local instructions for finding and validating them in the authorized enrollment. Follow official [API versioning](https://www.palantir.com/docs/foundry/api/general/overview/versioning): the URL identifies the major API version; examples should tolerate additional response fields and enum values within that version.

Preserve bounded paging, total request limits, timeouts, repeated-token detection and write replay guidance. A successful HTTP response must be interpreted according to its contract; asynchronous work needs documented completion checks. Tests use synthetic pages, errors and state transitions, including empty intermediate pages and uncertain write outcomes.

### 3.3 Source provenance and authored content

Use official sources to write task guidance in the project's own words. Citations remain optional provenance near the claims they support; the procedure must stand alone if the reader ignores every external URL. The maintainer coverage register records topic, local heading, source URL or SDK contract, review date, source version and reviewer. Maintainer artifacts stay outside distributed skills.

Do not bundle wholesale website exports as a substitute for authored guidance. That would carry irrelevant navigation, unresolved links, screenshots, and stale instructions into the skill. If implementation reuses SDK documentation or code under its Apache-2.0 license, preserve the applicable license and notices in repository distribution assets and record adaptations. Direct quotations from public pages should remain short; the recommended content is original explanation and examples grounded in official behavior.

## 4. Offline verification and acceptance evidence

Static link tests are necessary but cannot show that an agent knows how to perform a task. A keyword or heading count also cannot distinguish a complete workflow from a paragraph that delegates its steps. Add both static checks and task reviews.

| Gate | Evidence required |
| --- | --- |
| Local graph | Starting from the entry point, every required topic, procedure, example and schema is reachable. Every relative file/anchor link resolves inside a separately staged skill folder. No internal project paths. |
| Topic contract | All 36 topic rows plus REST map to local concepts, prerequisites, procedure, example, outcome and failure guidance. Missing elements fail review. |
| Citation independence | Reviewer reads with public URLs ignored or inaccessible. No covered decision depends on retrieving a public page, downloading a schema, or searching a public site. |
| Examples | Runnable examples use preprovisioned tools and synthetic fixtures. Verify meaningful output, failure paths, bounds and version-specific contracts. Label pseudocode clearly and supply the decisions needed to translate it. |
| Semantic journeys | An independent reviewer performs or derives a concrete task using only the staged skill and supplied fixtures/prerequisites. Record exact local headings used, resulting code/configuration/test plan and outcome. Any required missing fact fails acceptance. |
| Preservation | Existing operation inventories, local examples, prohibited-content checks and independent skill distribution checks remain applicable. |

The minimum journey set covers the user pipeline sequence, an incremental/fallback decision, SQL limitations and workspace publication, Ontology/interface/query design, Action/Function validation and permission failure, Compute Module build/configuration/mode selection, OSDK React application auth/query/release, Workshop widget interaction/test/distribution, three branching layers, production lineage/check/failure diagnosis, and a REST integration using local endpoint/model lookup with paging/errors. This is a scenario set for design refinement, not a substitute for reviewing every topic row.

For fixture-based acceptance, block network calls so a sample cannot accidentally retrieve missing knowledge. Where a journey includes a real Foundry operation, reviewers can use synthetic enrollment responses or a recorded UI state to verify code and next-action decisions. Report that result as documentation/fixture verification, not as a successful live deployment. Live enrollment smoke tests remain optional additional evidence unless an approved story specifically requires them.

Reject a journey that succeeds only because the reviewer supplies prior undocumented Foundry knowledge. The review record should expose the missing local instruction rather than accepting expert inference. This gate addresses the failure that previous structural tests did not detect.

## 5. Migration and delivery boundaries

1. Freeze the 36-topic register plus REST scope and audit findings during approved design. Link shared gaps to FEATURE-012 and identify exclusive content ownership.
2. Author expanded local guides and contract parts. Replace every required public-reading directive with local navigation while retaining optional source citations.
3. Update layout-sensitive tests and add the offline rubric/fixtures. Preserve the 20 skill names and the 351-operation register.
4. Run source-fidelity review and independent semantic journeys against the separately staged skill. Every missing dependency returns to its content owner.
5. Publish the reviewed skills revision to its existing GitHub repository through a ticketed release task; pin the parent repository gitlink as required. No PyPI/Conda packaging or installation text belongs to this feature.
6. Restore the prior verified Git revision if content verification fails after publication. No data migration or CLI release is required.

Design can divide authorship into pipelines/workspaces, Ontology/Functions, Compute Modules, applications/widgets/branching/security, production support, REST contracts, and integration verification. These are estimates of responsibility boundaries; BA design owns the final story set. Content stories should fit one sprint and split when local task boundaries make that estimate unreliable.

## 6. Alternatives, risks and estimate

| Approach | Assessment |
| --- | --- |
| Authored local task guides with local contract parts | Recommended. Fits the existing Markdown stack and makes task completeness reviewable. Requires source review and maintenance. |
| Download every linked website page | Large redundant bundle; dependent links and images can remain unresolved. Page availability cannot establish task completeness. |
| Delete public URLs without adding content | Removes provenance and preserves missing instructions. Fails semantic journeys. |
| Retrieval service or online fallback | Adds a runtime public access dependency and fails the requested restricted environment behavior. |

The SDK checkout contains 2,335 Markdown files. Mirroring every SDK page is substantially larger than completing the approved development workflows and their used contracts. This analysis recommends explicit recipe/contract coverage. If Project Owner requires all SDK operations as a complete offline API reference, that larger contract set must be enumerated and estimated during approval/design; it must not be silently claimed by a generic REST guide.

Planning estimate: 12 to 20 person-days after design approval for source-backed authoring, local examples/contracts, semantic review, test changes and release verification. Estimate assumes the approved topic register and covered REST recipes, existing runtime prerequisites, and no CLI implementation. Full SDK mirroring needs a separate estimate after catalog scope is agreed. Grooming should revise estimates using actual source and example depth.

Primary risks are stale platform behavior, mixed SDK/language versions, insufficient examples hidden by passing static tests, runtime prerequisites confused with offline knowledge, and duplicated shared facts drifting across skills. Mitigations are versioned provenance, local scope statements, runtime-specific parts, independent task review, explicit enrollment prerequisites, and shared-fact consistency checks.

The BA approved this analysis in QUESTION-176. The Project Owner approved both FEATURE-015 analyses on 2026-10-06; QUESTION-177 records that approval. Both questions and SA-ANA-016 are Closed. This approval authorizes detailed design only. Skill editing, implementation planning and publication follow approval of the new design and the normal feature workflow.

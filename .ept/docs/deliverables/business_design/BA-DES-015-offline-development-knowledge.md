# Business design: Complete offline Foundry development knowledge

| Field | Value |
| --- | --- |
| Document ID | BA-DES-015 |
| Feature / epic | FEATURE-015 / EPIC-015 |
| Status | Revision 2: Architect approved in QUESTION-184 and Lead Developer approved in QUESTION-186; Project Owner approved revision 2 in Closed QUESTION-182 on 2026-10-06; BA-DES-015 Closed |
| Basis | Approved BA-ANA-016 and SA-ANA-016; QUESTION-175 and QUESTION-177 |
| Technical counterpart | SA-DES-014 |
| Change record | Revision 2, 2026-10-06, WORK-003: T37 expands to every operation exposed by the frozen Foundry Platform REST SDK, including governance and AIP. Prior peer approvals cover revision 1 only. Closed analysis records remain the approved historical baseline; this design records the requested extension. |

## 1. Reader outcome and scope

An agent receives a covered Foundry development task and completes its planning, authoring, validation and delivery decisions using the distributed skill. Public documentation access is blocked. Every required definition, procedure, example and contract is available locally. Official public links provide optional attribution.

The scope comprises the 36 substantive subsections in the approved customer topic map and a separate REST topic. T37 covers every service, resource and operation exposed by the frozen Foundry Platform Python REST SDK across its API versions, including preview, beta and deprecated operations with their documented restrictions. Section 10 of that map guides reading order. Audit all 20 distributed skills and their local parts for essential public knowledge dependencies. Preserve the existing 351 CLI-operation inventory and FEATURE-012 ownership of CLI operation correctness. That count does not limit REST SDK coverage.

`pal-found-dev` must work as an independently distributed folder. Required content cannot reside only in another skill. Source provenance and project approval records belong outside distributed skills. No new installation or folder-copy prose is allowed; the development skill contains none. Existing approved CLI prerequisite blocks remain governed by their owning requirements.

## 2. Task flow and access boundaries

The reader follows: select development family → identify resources and prerequisites → choose applicable runtime, identity and branch → author/configure → validate → deliver through the documented platform path → interpret outcome → investigate or reconcile failure.

At each transition, guidance identifies the required input, effect and evidence. A release of code, a successful preview, a committed dataset transaction and a completed production build are distinct outcomes. A pending or partial outcome needs its own follow-up.

| Access condition | Reader can do | Completion boundary |
| --- | --- | --- |
| Public internet blocked; prepared tools and authorized enrollment available | Read all guidance locally; author and test; use permitted Foundry services | No task knowledge requires public browsing. Enrollment permissions and services still determine live execution. |
| Enrollment unavailable; prepared tools, fixtures and recorded platform states available | Author/test locally; derive configuration, expected platform effects and recovery decisions | Evidence describes fixture or procedure verification. It cannot claim a live preview, build or deployment. |
| Required runtime, generated binding, image, certificate, credential or data absent | Identify missing prerequisite and responsible organizational provisioning route | Explain the exact blocked step. Do not invent the artifact or replace missing guidance with installation instructions. |

Local Python preview and remotely executed preview must be distinguished. Supported language/runtime differences, administrator-enabled features, enrollment-specific API names and current versus legacy permission models must appear where they change the decision.

## 3. Knowledge records and reader interface

### 3.1 Local topic contract

Every row in section 4 requires:

1. Purpose, relevant resource relationships and tool choice.
2. Prerequisites, including supplied identifiers, permitted identity, runtime and prepared artifacts.
3. Ordered authoring/configuration procedure, with input meaning and relevant variation.
4. A complete representative example with marked illustrative values and adaptable context.
5. Validation steps and observable success, partial and pending outcomes.
6. Material limits, failure diagnosis and safe recovery or reconciliation.
7. Access boundary: locally possible steps, enrollment steps and administrator prerequisites.

Several rows may share an example when each row's decisions remain demonstrable. A sentence pointing to public documentation cannot supply an element of this contract.

### 3.2 Abstract information and interface requirements

The reader interface is a task-oriented entry point with local topic navigation. Display development families, relevant prerequisites and links to procedures/examples. A topic must provide a route back to navigation and to related local knowledge. No graphical application change is required.

The business information records are: topic identifier and completion outcome; prerequisite; ordered step; example input and expected result; outcome classification and next action; covered API contract; source attribution. Maintainer evidence adds author, source/version, review date, local heading, reviewer and finding disposition. SA-DES-014 defines file organization and verification implementation.

API guidance describes the business interaction: resource and identity → inputs → request → immediate result → any later completion observation → bounded recovery. Each used contract supplies local method/call meaning, identifiers, permissions, required inputs, response fields including needed nested structures, errors and lifecycle states. Keep direct REST, platform Python SDK, generated Ontology SDK and CLI separate. Actual enrollment-specific types are declared prerequisites with locally explained validation through authorized enrollment tooling.

T37 supplies task-to-service navigation and a searchable local index for every frozen SDK operation. Each operation has an adaptable SDK call example, complete input/output contract, required nested models, and an explanation of effects and documented restrictions. Shared authentication, pagination, streaming, retries and error knowledge may live in local common guides with direct links. Shared examples count only when the reader can derive that operation's exact invocation and handling without an external lookup. Missing source knowledge is an acceptance gap with an owner; it cannot silently remove an operation.

The primary baseline is Foundry Platform SDK 1.101.0, official source commit `168d519` and OpenAPI document 1.1697.0, verified by SA-DES-014. The supplied customer checkout is release 1.79.0 (`2da679`) despite its generated 0.0.0 placeholder. Record its compatibility differences against the primary baseline. T37 covers all operations available in 1.101.0; the historical checkout is compatibility evidence, not a second mandatory SDK distribution. Future SDK versions require a catalog refresh and review before a broader coverage claim.

The verified primary inventory contains 425 logical operations, 113 resources and 20 service/API-version namespaces (18 v2 and two v1). Stability annotations identify 218 Stable, 129 Public Beta and 78 Private Beta operations. Canonical logical operations are counted once; synchronous/asynchronous clients and response-wrapper forms still require local usage guidance. The supplied 1.79.0 baseline contains 397 operations and 107 resources; SA-DES-014 records the exact differences. Initial extracted closure contains 2,278 reachable model symbols and 964 reachable error symbols, 3,242 in total. Independent source reconciliation must add any omitted indirect or compound forward-reference dependencies and review the full corrected closure. Include every transitively referenced input/output type, enum and union, with cycle-safe navigation. This count is a starting inventory, not a coverage cap; totals alone do not establish complete explanations or approve compatibility.

### 3.3 Shared fact ownership

Ontology guidance owns object and Action authorization meaning; application guidance owns application identity/scopes/restrictions; Compute guidance owns execution identity and Sources. Branching/security guidance compares those boundaries without redefining them. Pipeline guidance owns dataset transaction and build relationships; REST guidance applies that meaning to explicit API contracts.

An operation defect discovered in the audit is assigned to an existing FEATURE-012 ticket or a correctly scoped new defect under that work. Link it to the affected FEATURE-015 story and record the blocked acceptance outcome. A dependency link alone does not satisfy acceptance: the essential local explanation must exist within standalone `pal-found-dev`, and the shared fact must be correct before its journey passes.

## 4. Finite topic and completion register

Each identifier below inherits section 3.1. Source titles correspond to the approved customer map. Story labels identify exclusive business outcome ownership; final ticket identifiers appear in section 7.

| ID | Source topic | Completion evidence | Owner |
| --- | --- | --- | --- |
| T01 | Platform/developer-tool overview | Select development family and explain resource relationships. | S1 |
| T02 | Development environments | Select local/hosted path and identify tools, data, identity and execution prerequisites. | S1 |
| T03 | 2.1 Code Repositories | Navigate Code, Branches, Tags, Pull Requests, Checks and Settings; prepare/review branch change and identify release outcome. | S2 |
| T04 | 2.2 Python Transforms | Declare I/O, register transform, choose supported computation/libraries and batch/incremental behavior. | S2 |
| T05 | 2.3 Tests/data quality | Run representative unit test and expectation; diagnose failure and decide deliverability. | S2 |
| T06 | 2.4 Local Python/VS Code | Validate prepared interpreter/auth/tooling, preview and tests; distinguish local and remote execution; submit change. | S2 |
| T07 | 2.5 SQL pipelines | Declare dataset inputs/output, author supported SQL, preview and verify schema/results and limits. | S3 |
| T08 | 2.6 Code Workspaces | Access prepared data, author transform and follow supported publication path. | S3 |
| T09 | 2.7 Production SDLC | Establish project boundaries/ownership; review/release code, build production data and validate delivery/recovery. | S2 |
| T10 | 2.8 Dataset transactions | Interpret states/visibility; distinguish direct writes and transform builds; diagnose failed/empty outputs. | S2 |
| T11 | 3.1 Ontology/types | Map backing data, stable keys/properties/links and verify objects/relationships. | S4 |
| T12 | 3.2 Interfaces | Define common contract, map concrete members and validate polymorphic consumer. | S4 |
| T13 | 3.3 Object Sets | Filter/traverse/query/aggregate; interpret results and bound expensive work. | S4 |
| T14 | 3.4 Actions | Configure parameters/rules/criteria/auth; test accepted/rejected submission; interpret edits and webhook/side effects. | S4 |
| T15 | 3.5 Functions | Choose supported runtime, author typed logic, test reads/edits/identity, publish version and verify consumer behavior. | S4 |
| T16 | 3.6 Ontology security | Distinguish schema/object/property/Action and current/legacy controls; validate permitted and restricted identities. | S4 |
| T17 | Compute fundamentals | Define workload/container contract and module lifecycle. | S5 |
| T18 | Compute execution models | Select Function/Pipeline mode; explain identity, Sources, networking, provenance/commit, scaling and usage. | S5 |
| T19 | Compute SDK/integration | Implement supported module/client contract and apply resource integration under intended identity. | S5 |
| T20 | 5.1 OSDK/Developer Console | Configure resources/restrictions/identity and validate prepared generated bindings. | S6 |
| T21 | 5.2 React lifecycle | Author data view/interaction, handle loading/errors/cache/subscriptions, test and publish. | S6 |
| T22 | Widget lifecycle | Define Widget Set, first release, added widget and subsequent version outcomes. | S6 |
| T23 | Widget development/testing | Use prepared local/hosted tooling and validate unpublished behavior. | S6 |
| T24 | Workshop integration | Bind parameters/events and relevant OSDK data; verify both directions of interaction. | S6 |
| T25 | Widget distribution | Publish version, explain host selection and applicable Marketplace path. | S6 |
| T26 | 7.1 Global Branching | Create/navigate/review/rebase/propose/merge multi-resource change with permissions and compatibility checks. | S7 |
| T27 | 7.2 Git/local branches | Apply protections/review/merge/fallback in repository release. | S7 |
| T28 | 7.3 Global versus Git | Identify both contexts and affected resources in development environment. | S7 |
| T29 | 7.4 Dataset/build branches | Select data/build context, resolve fallback and diagnose unexpected snapshot. | S7 |
| T30 | 7.5 Application branching | Check Ontology/Functions/Pipeline Builder support and limits before change/merge. | S7 |
| T31 | Platform security | Apply project roles/pipeline boundaries and explain access propagation. | S7 |
| T32 | Ontology/application security | Evaluate object/Action auth with OAuth scope and application restrictions. | S7 |
| T33 | Compute/branch security | Identify execution identity, Source/network limits and merge/resource access. | S7 |
| T34 | Lineage | Trace output to code/inputs/branch/build and interpret retention/deletion effects. | S8 |
| T35 | Monitoring/alerting | Select checks/health/monitoring, interpret evaluation/alert and investigation owner. | S8 |
| T36 | Pipeline support | Choose schedule/support action, diagnose failed/stale build and verify recovery. | S8 |
| T37 | REST development | Discover and author any frozen REST SDK operation using local contracts/models/examples; cover governance navigation/modification, AIP and every other SDK service with version and availability decisions. | S9 and REST domain stories |

## 5. Detailed acceptance contracts

| ID | Analysis trace | Required evidence and failure rule |
| --- | --- | --- |
| BD-015-01 | AC-015-01; BR-01..04 | All 37 rows mapped to exact local headings and all seven topic elements. Reviewer identifies example and completion evidence per row. Missing element fails. |
| BD-015-02 | AC-015-02,03; BR-03,04,08 | J1..J3 below complete using declared prepared artifacts and local guidance; distinguish previews/releases/builds and supported environment/runtime limits. |
| BD-015-03 | AC-015-04; BR-02..04,11 | J4/J5 produce reviewable model/query/function/action and restricted identity decision. Test rejected and accepted edits; explain side effects and runtime differences. |
| BD-015-04 | AC-015-05; BR-03,04,08,11 | J6 supplies module contract/configuration, mode decision, identity/Source checks, test result and failure recovery. |
| BD-015-05 | AC-015-06; BR-03,04,08 | J7/J8 produce reviewable app/widget interaction, loading/error checks, auth decisions and first/subsequent release interpretation. |
| BD-015-06 | AC-015-07; BR-02,03,11 | J9 distinguishes all three branch contexts, fallback/rebase/merge effects, support and permissions; identifies unexpected snapshot cause. |
| BD-015-07 | AC-015-08; BR-03,04,11 | J10 traces failed/stale output, chooses checks/alert ownership/schedule action and states recovery evidence. |
| BD-015-08 | AC-015-09; BR-03,04,09,11; owner T37 extension | Every frozen SDK operation maps to a complete local contract, adaptable invocation example and transitive model definitions. Inventory comparison has zero uncovered operations, unresolved model references or unexplained source differences. J11..J14 and a reviewer-selected operation from every service/API-version pair demonstrate discovery and correct handling without public lookup. Include stable, preview/beta and deprecated contracts with explicit restrictions; no exclusion without recorded owner approval. SA-DES-014 defines the exact frozen inventory and compatibility evidence. |
| BD-015-09 | AC-015-10; BR-05..08,12 | Audit records every public-reference occurrence across all 20 skills with context, classification, owner and disposition. No unresolved essential dependency. Local navigation/assets stay in owning folder; standalone development skill passes without sibling skill knowledge. |
| BD-015-10 | AC-015-11; BR-08,10 | Independent reviewer records prerequisites, restricted public access, local headings consulted, decisions/artifacts, success/failure evidence and gaps. Prior expert knowledge cannot supply an undocumented essential step. |
| BD-015-11 | AC-015-12; BR-09,10,12 | Independent source-fidelity review records source/API/runtime versions, differences and finding disposition. Preserve 351 operations and useful content; no new installation/copy prose or internal reader references. |
| BD-015-12 | AC-015-10..12; BR-06,07,12 | Reviewed GitHub revision and parent pin match accepted content. Publish only after all essential dependencies and journeys pass; record remote revision and verification. Restore prior verified revision if release fails. |

Public URL availability, heading counts and local-link success alone cannot approve any semantic criterion. Fixture tests demonstrate behavior only within their stated scenario; they do not prove live platform deployment.

## 6. Independent offline journeys

Reviewers receive the skill alone, scenario inputs and declared prepared runtime artifacts. Public retrieval is blocked. Authorized enrollment access or recorded UI/API state is named explicitly. A recorded platform step still requires the reader to derive inputs, expected effects, success evidence and failure decisions from local guidance.

| Journey | Task and adverse case | Required resulting artifact |
| --- | --- | --- |
| J1 | Python repository branch → transform → preview → unit test → expectation failure/repair → checks/review/release → production build/health. Include branch settings and project ownership. | Code/test and ordered release plan; evidence distinguishing preview, code release, transaction visibility and production completion. |
| J2 | Incremental versus snapshot transform and fallback input decision; unexpected historical input. | Choice with state/input reasoning, validation and recovery plan. |
| J3 | SQL output plus workspace publication and prepared local/hosted Python path; unsupported behavior or absent prerequisite. | SQL/configuration, schema/result checks, supported publication steps and explicit blocked step. |
| J4 | Linked model/interface/Object Set with empty or costly query. | Model mappings, bounded query and expected object/aggregation interpretation. |
| J5 | Runtime-specific Function/Action with permitted/restricted identities and side-effect failure. | Typed example/test plan, publishing/consumer version and edit/side-effect reconciliation decision. |
| J6 | Compute workload under Function/Pipeline modes; unavailable Source/network or identity failure. | Contract/configuration, image assumptions, mode comparison, validation and recovery evidence. |
| J7 | React OSDK view/interaction with loading, rejected access and update behavior. | App code/configuration/test plan, identity/scopes/restrictions and deployment result interpretation. |
| J8 | Workshop widget parameter/event interaction, first and next release, host version selection. | Widget/host configuration, interaction tests and release/distribution decision. |
| J9 | Git, dataset/build and Global branches with fallback/rebase/merge and unsupported application change. | Context/resource mapping, permission checks and correct next action. |
| J10 | Stale/failed production output through lineage/build/health/check/alert/schedule. | Investigation trail, owner, correction and recovery checks. |
| J11 | Local REST contract lookup → authenticated HTTP/SDK read → empty intermediate page/error/binary result. | Requests/models/result logic and finite stop conditions without public endpoint/model lookup. |
| J12 | Transaction create/upload/commit/get/abort and pending/terminal build state; uncertain write or exhausted status budget. | Known transaction identity, safe reconciliation and bounded completion checks without blind replay. |
| J13 | Governance application discovers project/folder hierarchy, inspects resource/access context and performs an authorized folder/resource modification; rejected access, stale hierarchy or uncertain write. | SDK application code and fixture results covering traversal, concrete modification inputs, permission assumptions, effect verification and reconciliation from local knowledge. |
| J14 | AIP application selects a supported AIP capability from the frozen SDK, authors its required session/request models and processes its documented execution/results; restricted access, preview prerequisite or unsuccessful/pending execution. | Concrete AIP SDK application code and fixture results, availability/version decision, result handling and bounded recovery derived locally. Choose actual operations in the frozen inventory; do not invent a capability. |

Every T01..T37 row needs semantic review even when a journey shares its example. Independent QA authors concrete fixtures and expected decisions during grooming. Source reviewers and journey reviewers must not approve their own authored content. Missing local facts return to their content owner; rerun affected journey and shared-fact checks after correction.

REST acceptance also selects at least one operation per service/API-version pair beyond the fixed journeys. QA chooses operations independently, records its selection rationale and verifies exact request/model/result decisions. Every operation receives contract and source-fidelity review; journey sampling supplements that complete review and cannot excuse incomplete operations. Execute fixtures with public access blocked; live enrollment is optional evidence and never implied by fixture success.

## 7. Story boundaries and ordering

All stories belong to FEATURE-015 and EPIC-015. Each owns one finite business outcome and must fit one sprint; estimates and implementation subtasks belong to grooming. Content owners coordinate shared facts under section 3.3. S1 owns entry navigation; content owners own their guide areas. S10 owns integration acceptance and GitHub publication evidence.

| Label | Outcome / topic ownership | Acceptance |
| --- | --- | --- |
| S1 / DEV-STORY-061 | Development routing/prerequisites T01/T02; complete 20-skill audit/disposition and essential general/namespace concept repairs in owning skills. Split repair scope through explicit linked stories during grooming if it exceeds one sprint; operation-contract defects remain FEATURE-012-owned. | BD-01,09,11 |
| S2 / DEV-STORY-062 | Python repository/local/testing/release/transaction guidance T03..T06,T09,T10. | BD-01,02,06,11 |
| S3 / DEV-STORY-063 | SQL and workspace guidance T07/T08. | BD-01,02,11 |
| S4 / DEV-STORY-064 | Ontology, interfaces, query, Actions, runtime Functions and ontology security T11..T16. | BD-01,03,11 |
| S5 / DEV-STORY-065 | Compute Modules T17..T19. | BD-01,04,11 |
| S6 / DEV-STORY-066 | React/OSDK and Workshop widget development/release T20..T25. | BD-01,05,11 |
| S7 / DEV-STORY-067 | Three branching layers and cross-platform security T26..T33. | BD-01,06,11 |
| S8 / DEV-STORY-068 | Production lineage, monitoring and support T34..T36. | BD-01,07,11 |
| S9 / DEV-STORY-069 | T37 SDK freeze, complete inventory/model closure, common SDK/HTTP patterns and local discovery/navigation. Domain stories own operation content exclusively. | BD-01,08,11 |
| S10 / DEV-STORY-070 | Independent T01..T36 source/standalone/offline J1..J10 verification, integration of accepted T37 evidence, 20-skill audit/preservation and reviewed GitHub delivery. | BD-01..12 |

The following T37 domain partitions are exclusive predicates over the exact SDK operation IDs in SA-DES-014. The verified union contains all 425 operations, with no overlap. Common catalog/model delivery belongs to S9; each domain story owns its operation explanations, examples and exhaustive source review. Shared models retain one declared maintainer. Points are candidates; grooming confirms effort and sprint capacity or splits explicit operation-ID subsets while preserving this union.

| Partition / ticket | Exclusive operation scope | Count | Candidate points |
| --- | --- | --- | --- |
| R1 / DEV-STORY-071 | v2.admin Group, GroupMember, GroupMembership, GroupMembershipExpirationPolicy, GroupProviderInfo, User and UserProviderInfo. | 27 | 5 |
| R2 / DEV-STORY-072 | All remaining v2.admin resources: authentication providers, enrollment, organizations, roles, hosts, markings and CBAC. | 40 | 5 |
| R3 / DEV-STORY-073 | All v2.filesystem, v2.audit and v2.third_party_applications; governance J13. | 48 | 8 |
| R4 / DEV-STORY-074 | All v1.datasets and v2.datasets; J11/J12 dataset/file/transaction examples. | 52 | 8 |
| R5 / DEV-STORY-075 | All v2.orchestration, v2.checkpoints and v2.data_health; J12 build example. | 29 | 5 |
| R6 / DEV-STORY-077 | All v1.ontologies. | 23 | 5 |
| R7 / DEV-STORY-079 | v2.ontologies ActionType, ActionTypeFullMetadata, ObjectType, Ontology, QueryType, OntologyValueType and OntologyInterface. | 32 | 5 |
| R8 / DEV-STORY-081 | v2.ontologies OntologyObject, OntologyObjectSet, LinkedObject, OntologyScenario and OntologyTransaction. | 22 | 5 |
| R9 / DEV-STORY-083 | Remaining v2.ontologies resources: Action, Query, Attachment and typed property resources. | 25 | 5 |
| R10 / DEV-STORY-085 | All v2.functions, including beta invocation. | 11 | 3 |
| R11 / DEV-STORY-087 | All v2.aip_agents, v2.language_models and v2.models; AIP J14. | 47 | 8 |
| R12 / DEV-STORY-089 | All v2.connectivity, v2.streams and v2.sql_queries. | 40 | 8 |
| R13 / DEV-STORY-091 | All v2.media_sets and v2.widgets. | 29 | 5 |

REST acceptance belongs to DEV-STORY-093 (candidate eight points), covering independent J11..J14, all 20 service/API-version discovery cases, complete operation/model closure evidence and adverse behavior checks. Domain reviews inspect every operation; acceptance checks never replace those reviews with a sample. S10 consumes accepted REST evidence and owns integrated T01..T37 review, J1..J10, 20-skill audit disposition, preservation and GitHub delivery. S9 is revised from five to eight candidate points. The REST work totals 91 candidate points across S9, 13 domains and independent acceptance; the expanded scope requires this additional work rather than the earlier single five-point story. Capacity and estimates remain subject to grooming.

S2..S9 depend on the approved scope/audit disposition from S1 and can proceed beside each other after shared fact agreements. S7 uses S2/S4/S5/S6 authoritative meanings. S9 uses S2 transaction/build semantics. REST domains depend on S9; REST acceptance depends on all domains and S9; S10 depends on REST acceptance and S1..S8, plus closure of essential shared FEATURE-012 dependencies. Story creation occurs during design; specific New-to-Open readiness requires FEATURE Waiting for Implementation. No implementation or grooming starts before new design approvals and required workflow gates.

S9 freezes the SDK source identity, OpenAPI document version, API versions and prepared SDK/runtime compatibility before domain authoring. A source checkout reporting package version 0.0.0 must not be presented as a published compatibility version. Compare any prepared release against the frozen source and record differences. Completeness uses the frozen inventory; compatibility with another release requires an explicit difference record and cannot shrink coverage. REST domain stories partition every inventoried operation exactly once; shared models have one declared maintainer and complete local navigation. Candidate estimates do not approve unknown audit repair or model-closure volume; grooming must split excessive work into exclusively owned, linked stories.

## 8. Migration and release procedure

1. Record current verified skills revision, 20 names, 351-operation inventory and existing navigation/content baseline. Capture all external-reference contexts and existing layout-dependent checks through S1.
2. Freeze the 37-row register and complete REST SDK operation/model inventory with approved business/technical design. Assign each essential dependency to a content story or linked FEATURE-012 CLI operation work with blocked acceptance identified.
3. Replace required public-reading instructions with local explanation/procedure/example/contract navigation. Preserve optional attribution and valid existing knowledge. Update authoritative shared facts consistently.
4. Review topic/source mappings and all local content paths. Validate each independently distributed folder and development skill without required sibling content. Update layout-sensitive validation to match navigable outcomes.
5. Run independent J1..J14, per-service/API-version REST discovery cases, all-row semantic review and complete REST contract/model/source review with public access blocked. Record gaps and resolve/retest them. Verify unchanged CLI operation coverage and prohibited-content rules.
6. Publish only accepted skills content to existing GitHub repository through ticketed deployment work; verify remote revision and parent pin. Add no packaging or installation work.
7. If publication contains a failed knowledge contract, restore the prior verified content revision through recorded corrective work, verify the remote content and rerun affected acceptance before republishing. No data or CLI migration is required.

## 9. Approval and completion

SA-DES-014 owns technical organization, complete SDK operation/model contracts, version verification and test mechanisms. BA-DES-015 owns task coverage, reader outcomes and acceptance. Required revised design approvals are architect, Lead Developer and Project Owner. Analysis approval authorizes design work only; the owner's scope correction authorizes this design revision, not implementation.

Completion requires indexed deliverables, finite linked stories, recorded dependency ownership, peer review and new owner design approval. Both revised designs were approved on 2026-10-06; design subtasks are Closed and FEATURE-015 is Waiting for Implementation. Publication is GitHub-only and follows implementation acceptance.

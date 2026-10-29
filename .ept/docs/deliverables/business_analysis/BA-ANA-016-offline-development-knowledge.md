# Business analysis: Complete offline Foundry development knowledge

| Field | Value |
| --- | --- |
| Document ID | BA-ANA-016 |
| Feature / epic | FEATURE-015 / EPIC-015 |
| Status | Closed; SA approved in QUESTION-174 and Project Owner approved in QUESTION-175 on 2026-10-06 |
| Date | 2026-10-06 |
| Sources | Project Owner request; restored development coverage map; BA-ANA-013/014; current distributed skills |

## 1. Business case and boundary

An agent developing a Foundry pipeline or application in an environment with restricted public internet must obtain the knowledge needed for its covered task from distributed skill files. Current development pages describe capabilities but ask readers to open public pages for essential syntax, setup, validation, and release procedures. These instructions stop an offline reader before the work is complete.

FEATURE-013 already promised usable core explanations offline and optional public references. FEATURE-015 corrects the remaining dependency and defines a stronger, observable completion standard. A topic must support a concrete development task through decisions, preparation, authoring, validation, delivery, result interpretation, and recovery. Renaming source links or deleting them does not meet this standard.

The finite knowledge boundary is the 36 substantive subsections in `development-skill-coverage.md`, plus a separate REST API development topic. Section 10 provides reading order. Coverage includes the supported concepts and development paths represented by those subsections, with local examples and material variations; it does not require reproducing every Palantir documentation page or every unrelated SDK endpoint.

The full 20-skill bundle must be checked for essential public knowledge dependencies. `pal-found-dev` is the main authoring scope. Existing general and namespace guidance must remain sufficient where a covered development task uses it. FEATURE-012 retains ownership of the existing 351-operation meaning, input, result, and example requirements. Shared gaps must be recorded against that work and linked, rather than creating duplicate operation implementation.

## 2. Business requirements

| ID | Requirement |
| --- | --- |
| BR-015-01 | Every subsection in the approved coverage inventory and the separate REST topic must have locally available knowledge sufficient for its covered development task. Each subsection must have a named completion outcome. |
| BR-015-02 | Each topic must explain purpose, resource relationships, tool choice, relevant behavior, prerequisites, and material limitations before its procedure. The reader must understand why each step is needed. |
| BR-015-03 | Each covered task must provide an ordered procedure, required inputs and configuration meaning, validation steps, delivery steps, observable results, and a safe next step when the result fails or remains uncertain. Public documentation must not supply a missing step. |
| BR-015-04 | Each development path must include a coherent local example. Code or configuration used in an example must have enough context to adapt it, verify its result, and identify illustrative values. Material differences in language, runtime, branch, execution mode, or permission model must be explained where they change the task. |
| BR-015-05 | External references may remain as optional source attribution. All instructions needed for task completion, including referenced definitions, API contracts, examples, tables, and diagrams, must be readable locally. Required information must not depend on a remote image, website, repository, or documentation download. |
| BR-015-06 | All 20 distributed skills must be audited for essential external knowledge dependencies. Every detected dependency must be locally resolved within the applicable approved scope or assigned to linked FEATURE-012 work with an explicit acceptance dependency. No uncovered essential dependency may be silently exempted. |
| BR-015-07 | An agent must be able to find and follow the required local content from the relevant skill entry point. An independently distributed `pal-found-dev` must contain its own required knowledge; another skill may provide optional deeper guidance. Required local navigation must resolve inside that skill and must not depend on internal project deliverables, tracker records, or the author's SDK checkout. |
| BR-015-08 | Public internet restrictions must be distinguished from authorized Foundry tenant access. Local tools, generated application bindings, dependencies, container images, credentials, certificates, and sample data needed by a task must be identified as preconditions where applicable. The skill must explain how a missing precondition prevents completion without adding installation or folder-copy instructions. |
| BR-015-09 | Local explanations must be faithful to official Palantir documentation and the supplied SDK documentation. Authors must preserve the meaning of prerequisites, limits, exceptions, and version differences. Missing or conflicting source evidence must be resolved before acceptance. |
| BR-015-10 | Offline acceptance must include semantic review of every inventory subsection and representative task execution or simulation for every development family. A check that links resolve or that topic names exist is insufficient. Reviewers must demonstrate completion using only distributed knowledge and declared preconditions. |
| BR-015-11 | Guidance must preserve existing access restrictions and distinguish authorization failures, invalid inputs, partial results, pending work, and uncertain write outcomes. Paging, retries, polling, transfers, and bulk operations must explain how to bound work and interpret incompleteness where relevant. |
| BR-015-12 | The change must preserve supported operation coverage and useful existing content. Source traceability and review evidence must remain in project deliverables. Distributed skills must contain no internal development-document links or skill installation/folder-copy prose. This feature must add no installation prose; `pal-found-dev` remains free of installation directions. Existing approved CLI prerequisite blocks in command skills remain subject to their owning requirements. |

## 3. Coverage inventory and completion outcomes

Every row below inherits BR-015-02 through BR-015-05. A reviewer must find local concepts, procedure, example, validation, expected outcome, and recovery guidance for the stated work. Closely related rows may share a worked example if each row's behavior and decisions remain demonstrable.

| Source subsection | Covered completion outcome |
| --- | --- |
| 1: Platform and developer-tool overview | Select an appropriate pipeline, Ontology, application, or compute development path and explain its resource relationships. |
| 1: Development environments | Choose local or hosted authoring and identify the available tool, data, authentication, and execution prerequisites. |
| 2.1: Code Repositories | Make a branch change, navigate files and checks, review the change, and identify the repository release outcome. |
| 2.2: Python Transforms | Declare inputs and outputs, register a transform, use supported computation and libraries, and distinguish batch and incremental behavior. |
| 2.3: Testing and data quality | Write and run a representative test and data expectation, inspect failure, and decide whether the output can be delivered. |
| 2.4: Local Python / VS Code | Use a prepared local environment for preview and tests, account for local/Foundry differences, and submit a validated change. |
| 2.5: SQL pipelines | Author a supported SQL transform with declared datasets, preview it, and validate output schema and results. |
| 2.6: Code Workspaces | Access data in a prepared workspace and follow its transform authoring and publication path. |
| 2.7: Production SDLC | Separate project boundaries, review changes, release code, build production outputs, and assess delivery and recovery. |
| 2.8: Dataset transactions | Explain transaction states and output visibility, distinguish direct writes from transform execution, and diagnose empty or failed outputs. |
| 3.1: Ontology fundamentals/types | Map backing data, stable keys, properties, and links into a usable model and verify representative objects and relationships. |
| 3.2: Interfaces | Define a common contract, map its members to concrete types, and validate a polymorphic consumer. |
| 3.3: Object sets/querying | Form and evaluate a filtered or linked Object Set, interpret aggregation/results, and bound costly queries. |
| 3.4: Actions | Configure parameters, rules, criteria, permissions, and side effects; test an accepted and rejected submission and explain resulting edits. |
| 3.5: Functions | Select a supported runtime, author typed logic, test reads/edits/identity, publish a version, and identify consumer behavior. |
| 3.6: Ontology security | Distinguish schema, object, property, Action, and legacy/current access controls and validate intended and restricted access. |
| 4: Fundamentals/architecture | Define a container workload and its module lifecycle with explicit input/output contracts. |
| 4: Execution models/transactions | Choose Function or Pipeline mode and identify identity, Sources, networking, provenance, commit behavior, scaling, and usage consequences. |
| 4: SDK/integration references | Implement a supported module client/function contract and integrate OSDK or platform resources under the chosen execution identity. |
| 5.1: OSDK/Developer Console | Configure application resources and restrictions, select authentication identity, and use prepared generated bindings for typed access. |
| 5.2: React lifecycle | Author a representative data view or interaction, handle loading/errors/cache or subscriptions, test, and publish the application. |
| 6: Widget lifecycle | Define a Widget Set and distinguish creation, first release, further widgets, and subsequent versions. |
| 6: Local development/testing | Develop and preview a prepared widget locally or in hosted tooling, then validate unpublished behavior. |
| 6: Workshop/React integration | Connect parameters and events, use relevant OSDK data, and verify changes flow between Workshop and the widget. |
| 6: Distribution | Publish a widget version, identify host version selection, and explain the applicable Marketplace distribution path. |
| 7.1: Global Branching | Create and navigate a multi-resource change, review/rebase/propose/merge it, and explain role and compatibility constraints. |
| 7.2: Git/local branches | Apply repository branch protection, review, merging, and fallback rules in a release task. |
| 7.3: Global versus Git | Identify both branch contexts in a development environment and explain which resources each change affects. |
| 7.4: Dataset/build branches | Select the intended dataset/build context, resolve fallbacks, and diagnose an unexpected input snapshot. |
| 7.5: Application-specific branching | Check support and limitations for Ontology, Functions, and Pipeline Builder before changing or merging them. |
| 8: Platform security | Apply project/role and pipeline security boundaries and explain access propagation in a development task. |
| 8: Ontology/application security | Evaluate object/Action authorization together with OAuth scopes and application restrictions before data access or edits. |
| 8: Compute/branch security | Identify execution identity, Source/network restrictions, and branch merge/resource access requirements. |
| 9: Lineage | Trace an output to code, inputs, branch, and build; explain retention/deletion effects within the supported task. |
| 9: Monitoring/alerting | Choose health/check/monitoring coverage, interpret an evaluation and alert, and identify the appropriate investigation. |
| 9: Pipeline support | Set a suitable scheduling/support path, investigate a failed or stale build, and validate recovery. |
| Additional: REST API development | Select a locally documented resource contract, prepare authenticated HTTP/SDK requests, handle pages/binary/errors/pending work, and reconcile writes safely. |

REST coverage must include local operation contracts for the worked tasks, with method or SDK call, identifiers, required permissions/scopes, input meaning, response interpretation, and material errors. The topic must explain how direct REST, the platform Python SDK, OSDK, and CLI differ. The complete unrelated SDK catalog is outside this feature's finite boundary.

## 4. Current dependency audit and affected scope

The audit covered all 20 skill entry points and searched their local Markdown parts for external references and instructions that delegate knowledge. A URL is not automatically a failure; its surrounding task must determine whether it supplies essential missing content.

| Bundle area | Observed condition | Required treatment |
| --- | --- | --- |
| `pal-found-dev` | Six Markdown pages contain 141 lines with external URLs. Pipeline guidance sends readers elsewhere for decorators/I/O, SQL syntax, libraries, local setup, tests, and release design. Ontology/compute and application guides defer runtime contracts, bootstrap, publishing, and integration details. REST text directs readers to endpoint pages for operation contracts. | Rework all 36 inventory subsections and REST against the completion standard, including locally available examples and recovery. |
| `pal-found`, datasets, orchestration, SQL queries, data health | Local concepts and operation parts already exist; these areas are consumed by pipeline/support journeys. Public source links also remain. | Verify that covered development paths can use this guidance without browsing. Attribute existing operation gaps to FEATURE-012 and link the affected acceptance work. |
| Ontologies, Functions, third-party applications, Widgets, connectivity, filesystem, admin | Local operation parts and context exist; these areas connect modeling, application delivery, permissions, and compute/network prerequisites. | Check the shared meanings and required operation information reached from development tasks. Preserve the namespace operation inventory. |
| AIP agents, audit, checkpoints, language models, media sets, models, streams | Local operation guidance exists and public references remain. The new request does not independently add new development families for these namespaces. | Audit essential public delegation throughout the bundle; preserve prior operation requirements and register any residual gaps against the correct existing scope. |

This audit identifies authoring priorities and acceptance boundaries. It does not claim that every namespace operation has passed a new semantic offline review. Design and acceptance must record each discovered essential dependency and its owner, so shared work cannot disappear between features. A FEATURE-012 link cannot exempt essential knowledge: `pal-found-dev` must remain usable when distributed alone, and any shared essential gap must block the applicable acceptance outcome until resolved.

## 5. Acceptance criteria and offline scenarios

| ID | Requirements | Observable check |
| --- | --- | --- |
| AC-015-01 | 01, 02, 03, 04 | Given the 37-row inventory above, a reviewer maps every row to distributed local content and verifies the complete content contract. Every row has a completion outcome and no essential missing definition or step. |
| AC-015-02 | 03, 04, 05 | With public browsing disabled, a reader completes a Python pipeline branch change: declared transform, preview, unit test, expectation failure and repair, checks/review/release, production build, and output/health validation. Navigation, tests, expectations, branch settings, release process, project structure, and production procedures are locally explained. |
| AC-015-03 | 03, 04, 08 | A reader authors and validates a SQL output and demonstrates local/hosted Python and workspace paths using prepared tools. It identifies unsupported execution behavior and environment differences without fetching guidance. |
| AC-015-04 | 02, 03, 04, 11 | A reader models linked objects and an interface, queries an Object Set, authors/tests a supported Function and Action, and explains accepted/rejected edits, webhook/side-effect outcomes, runtime differences, and restricted-user behavior from local content. |
| AC-015-05 | 03, 04, 08, 11 | A reader prepares a module contract and image/configuration using available artifacts, chooses execution mode, configures resources/Sources, tests the contract, identifies deployment outcome, and diagnoses identity/network/scaling failures. |
| AC-015-06 | 03, 04, 08 | A reader implements and tests a React/OSDK application and a Workshop widget using prepared bindings/dependencies, verifies parameters/events and data/error behavior, and explains application deployment and first/subsequent widget releases. |
| AC-015-07 | 02, 03, 11 | A reader distinguishes Git, dataset/build, and Global branch contexts; handles review/rebase/merge or fallback scenarios; identifies application support and permissions; and diagnoses an unexpected snapshot. |
| AC-015-08 | 03, 04, 11 | A reader traces a stale/failed production output through lineage and build context, interprets a health/check/monitoring result, chooses schedule/support action, and verifies recovery using local guidance. |
| AC-015-09 | 03, 04, 09, 11 | A reader prepares a supported REST and Python SDK read from local contracts, handles partial paging and a documented failure, interprets binary or pending results, and explains transaction/write reconciliation. It never needs a public endpoint page to supply an essential contract. |
| AC-015-10 | 05, 06, 07, 12 | Review covers all 20 skills and their local parts. Required links and assets resolve locally; external URLs are optional attribution. A separate check distributes only `pal-found-dev` and confirms that every required topic and asset remains available. No skill asks the reader to fetch missing task knowledge, open an internal project document, install the skills, or copy their folders. Every shared gap has an explicit disposition and acceptance dependency. No new installation prose is introduced, and `pal-found-dev` contains none. |
| AC-015-11 | 08, 10 | Scenario evidence records available tools/artifacts, authorized tenant access or recorded responses, blocked public access, local content consulted, decisions and outputs, validation results, failure/recovery, and unresolved knowledge gaps. Review fails if essential public knowledge is needed. |
| AC-015-12 | 09, 10, 12 | Independent source review confirms claims and examples against official Palantir and supplied SDK documentation, including meaningful versions and exceptions. Existing supported operation coverage remains intact; URL availability and keyword checks alone cannot approve content. |

Live tenant access is permitted when authorized. Reviewers may use mocks, recorded responses, and reviewable code/configuration for costly, destructive, or unavailable platform steps. They must still demonstrate that the distributed knowledge supplies every task decision and expected result. A procedure cannot pass by marking its unexplained essential step as simulated.

## 6. Process impact, access, volume, and risk

Pipeline work gains complete local authoring, testing, release, execution, and support guidance. Ontology/application work gains locally explained model, runtime, authentication, interface, validation, and publishing paths. Production support gains local investigation and recovery decisions. Review changes from checking readable files and source URLs to checking whether a reader can complete the covered work.

This feature changes documentation. It grants no credential, resource permission, network route, OAuth scope, or platform feature. Foundry tenant/API access remains necessary for live reads, previews, builds, publishing, and validation. A fully disconnected machine can perform available local authoring/tests and interpret recorded responses; the skill must identify the tenant step that remains impossible. Preprovisioned libraries, bindings, extensions, toolchains, and image artifacts are declared prerequisites; describing their role must not become installation instructions.

Documentation causes no API traffic or data transfer by itself. Examples can influence later request volume, so paging, polling, retries, and status checks must explain finite work and incomplete results. Data limits remain those of the underlying platform. Large datasets, transfers, generated artifacts, and container images require task-appropriate handling; authors must not invent throughput, row, file-size, or universal limits. Local knowledge content will grow and must remain navigable and maintainable.

| Type | Item | Handling |
| --- | --- | --- |
| Assumption | The restored topic map defines the covered development families. | Use the 36 subsections and separate REST topic as the finite acceptance inventory. |
| Assumption | Restricted public internet allows authorized tenant access where the task requires it. | State tenant/tool/artifact prerequisites and support recorded-response review where live access is unavailable. |
| Risk | Authors replace link lists with equally shallow summaries. | Require concrete local procedures, examples, validation, and recovery for each inventory row. |
| Risk | Source/runtime differences produce wrong code or permissions. | Preserve distinctions and verify each example against its applicable official source. |
| Risk | Shared operation gaps are reassigned and never completed. | Record explicit FEATURE-012 dependencies and prevent acceptance while an essential shared gap remains. |
| Risk | Local knowledge becomes stale or conflicts across skills. | Record source/version review evidence and review affected topics when platform or CLI behavior changes. |
| Risk | Tenant-specific values are mistaken for universal contracts. | Mark placeholders and distinguish documented behavior from enrollment-specific configuration. |
| Risk | Large copied manuals obscure tasks or reproduce irrelevant material. | Author task-focused explanations and examples with optional source attribution. |

## 7. Deliverables, traceability, and approval

Analysis deliverables are this finite requirements document, SA-ANA-016 architecture analysis, their document-index entries, and approval QUESTION records. Later stages must produce business/solution design, a coverage/dependency register, authored offline skill content, source review, and scenario evidence for AC-015-01 through AC-015-12. Implementation planning follows approved design.

BA-ANA-013 defines offline operation semantics and remains the FEATURE-012 baseline. BA-ANA-014 BR-013-08 and AC-013-09 define the prior offline core/optional-source promise. FEATURE-015 retains those promises and makes procedural completion measurable. Current authoring inputs include `development-skill-coverage.md`, `DEV-STORY-060-foundry-skill-source-review.md`, all distributed skill pages, and the supplied `foundry-platform-python/docs` material. Those project paths support authoring and review; they must not appear as reader dependencies in distributed skills.

Official example sources reviewed for the reported dependency include [repository navigation](https://www.palantir.com/docs/foundry/code-repositories/navigation), [Python unit tests](https://www.palantir.com/docs/foundry/transforms-python/unit-tests), and [widget development](https://www.palantir.com/docs/foundry/custom-widgets/development). Implementation must review applicable sources across the full inventory, rather than assume this sample verifies every future claim.

The architect approved BR-015-01 through BR-015-12 and AC-015-01 through AC-015-12 in QUESTION-174. Peer review clarified independently distributed skill completeness and preserved approved CLI prerequisites while prohibiting new installation prose. The Project Owner approved both FEATURE-015 analyses on 2026-10-06; QUESTION-175 records that approval. Both questions and BA-ANA-016 are Closed. This approval authorizes detailed design; implementation requires approval of the new design and completion of grooming.

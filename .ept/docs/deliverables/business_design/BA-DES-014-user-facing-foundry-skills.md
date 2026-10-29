# Business design: User-facing Foundry skills and development guidance

| Field | Value |
| --- | --- |
| Document ID | BA-DES-014 |
| Feature and epic | FEATURE-013; EPIC-013 |
| Status | Approved by architect, lead developer, and Project Owner |
| Basis | BA-ANA-014, SA-ANA-014, Project Owner approval in QUESTION-165 |

## 1. Outcome and scope

An agent receives a Foundry development task, finds `pal-found-dev`, identifies the relevant development area, understands the platform behavior and access boundary, and follows a coherent path from preparation through validation and operation. It can use the content offline. Public Palantir links provide evidence and deeper reading when available.

The same release removes internal project development references and the copy-folder instruction from existing distributed skills. The operation guidance already required by FEATURE-012 remains in place. This feature adds no Foundry operation, credential, permission, or application API.

## 2. Reader journeys and information model

| Journey | Expected path and decision |
| --- | --- |
| Pipeline development | Choose a visual pipeline, Code Repository, or Code Workspace; understand Python or SQL transform fit; preview and test; release; interpret builds, transactions, branches, lineage, health, and schedules. |
| Ontology development | Model object and link types, interfaces, and Object Sets; choose Actions or Functions for operational logic; understand permission boundaries and write effects. |
| Application development | Choose OSDK/React, a Workshop custom widget, or Compute Module for the task; understand Developer Console setup, identity, authorization, publishing, and runtime behavior. |
| API integration | Select a documented Foundry API resource; choose direct REST or SDK use; authorize requests; interpret data, pages, errors, and work that may still be running. |
| Production support | Trace inputs and outputs, inspect build/health/observability state, understand scheduling and branch context, and choose a safe follow-up. |

The agent-facing interface consists of the skill entry point and its local topic guides. Each topic has a short purpose, prerequisite concepts, typical lifecycle, decision points, material limits, and direct official source links. The entry point provides a task-based route to every topic. The topic text supplies the essential explanation; a public link is optional reading. Existing namespace skills continue to explain supported CLI operations when a development path reaches a callable operation.

The business information structure is `entry point → topic → workflow/decision → source`. A topic may point to another local topic for deeper context. Every local link must stay inside the independently distributed skill folder. A source reference points to a public official Foundry page. Internal project sources stay in this design and review evidence, not in the distributed skill.

There is no graphical interface or new application API. The abstract UI requirement is clear Markdown navigation: a reader should see the task names, choose a topic, and return to the entry point without needing a repository map. The abstract API requirement is unchanged: the skill describes direct REST, SDK, OSDK, and CLI as distinct ways of interacting with Foundry, and documents their boundary without adding or promising an endpoint.

## 3. Topic content and source traceability

The restored `development-skill-coverage.md` is the authoring inventory. Every row below requires an explanatory topic, not a list of links. Section 10 is a suggested learning order for navigation. The source examples are the main official references; authors should verify the linked page and expand them where needed.

| Group | Content that a novice must learn | Official starting references |
| --- | --- | --- |
| 1. Landscape and tool selection | What pipelines, Ontology, applications, and compute contribute; when to choose visual pipelines, code, workspaces, OSDK, or Compute Modules. | [Developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain), [app building](https://www.palantir.com/docs/foundry/app-building/overview), [pipeline tools](https://www.palantir.com/docs/foundry/building-pipelines/considerations-pb-cr) |
| 2. Python and SQL pipelines | Code Repository authoring and review; Python transform inputs/outputs, incremental behavior and compute; SQL limits; local/workspace paths; tests and expectations; release, builds, and dataset transactions. | [Code Repositories](https://www.palantir.com/docs/foundry/code-repositories/overview), [Python transforms](https://www.palantir.com/docs/foundry/transforms-python/overview), [SQL transforms](https://www.palantir.com/docs/foundry/transforms-sql/overview), [datasets](https://www.palantir.com/docs/foundry/data-integration/datasets) |
| 3. Ontology development | Types, properties, links, interfaces, Object Sets, Actions, Functions, and current permission model; distinguish reads, edits, and side effects. | [Ontology concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts), [Actions](https://www.palantir.com/docs/foundry/action-types/overview/index.html), [Functions](https://www.palantir.com/docs/foundry/functions/overview), [permissions](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions) |
| 4. Compute Modules | Container-based execution, Function and Pipeline modes, Sources and secrets, scaling, SDK integration, and how mode affects permissions and provenance. | [Overview](https://www.palantir.com/docs/foundry/compute-modules/overview), [execution modes](https://www.palantir.com/docs/foundry/compute-modules/execution-modes), [Sources](https://www.palantir.com/docs/foundry/compute-modules/sources) |
| 5. React with OSDK | Developer Console application, OAuth and application restrictions, OSDK generation, data access in React, development, test, and deployment. | [Developer Console](https://www.palantir.com/docs/foundry/developer-console/overview), [OSDK](https://www.palantir.com/docs/foundry/ontology-sdk), [React apps](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/overview) |
| 6. Workshop widgets | Widget Set creation, local preview, parameters/events with Workshop, OSDK use, first release and later publish, and distribution. | [Custom Widgets](https://www.palantir.com/docs/foundry/custom-widgets/overview), [development](https://www.palantir.com/docs/foundry/custom-widgets/development), [publish](https://www.palantir.com/docs/foundry/custom-widgets/publish) |
| 7. Branching | Different scopes and outcomes of Git/Code Repository branches, dataset/build branches, and Global Branching; branch security and application integration. | [Global Branching](https://www.palantir.com/docs/foundry/global-branching/overview), [data branching](https://www.palantir.com/docs/foundry/data-integration/branching), [VS Code distinction](https://www.palantir.com/docs/foundry/vs-code/global-branching) |
| 8. Security and governance | Project roles, pipeline access, current Ontology/object policies, Action authorization, Developer Console restrictions, Compute Sources, and branch permissions. Legacy Ontology permission material is labeled legacy. | [Projects and roles](https://www.palantir.com/docs/foundry/security/projects-and-roles), [object security](https://www.palantir.com/docs/foundry/object-permissioning/overview), [application permissions](https://www.palantir.com/docs/foundry/developer-console/permissions) |
| 9. Lineage and operations | Data Lineage, observability, Data Health, checks, scheduling, incident support, and how to read branch/build context before action. | [Data Lineage](https://www.palantir.com/docs/foundry/data-lineage/overview), [observability](https://www.palantir.com/docs/foundry/observability/overview), [maintaining pipelines](https://www.palantir.com/docs/foundry/maintaining-pipelines/overview) |
| Additional REST API topic | Direct HTTP and Python SDK relationship, API resource choice, identity and scopes, request/response meaning, pages, binary data, errors, limits, write uncertainty, and a supported read-only example. | [API overview](https://www.palantir.com/docs/foundry/api/general/overview), [developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain), [Developer Console permissions](https://www.palantir.com/docs/foundry/developer-console/permissions) |

## 4. Content records and REST journey

Each substantive topic should answer six questions: What Foundry resource or development tool is involved? Why would a developer use it? What must exist first? What is the normal create, test, publish, or operate path? Which permission or state boundary matters? What outcome proves the step is complete? Examples may be concise but must connect an input or choice to a Foundry effect or result.

The REST topic starts with enrollment host and a documented API version/resource. It explains credentials and Foundry authorization separately, then maps path, query, headers, and body to a supported request. It describes JSON, binary, and streamed responses where relevant; pages and next tokens; rate limits and retries; timeouts; and how to verify a write or asynchronous operation before reporting completion. Its read-only example must identify an official endpoint and match the local Python SDK documentation. It must say when the example is direct HTTP, Python SDK, OSDK, or CLI. It must not assume all interfaces expose the same operations or that a successful HTTP response proves a later process completed.

The development topic must keep the three Foundry branching layers separate. A Git branch holds code changes, a dataset/build branch selects data transactions or build context, and a Global Branch coordinates changes across supported applications. The topic should explain their relationships without presenting one branch's merge or fallback behavior as another's.

## 5. Cleanup and distribution rules

The cleanup applies to every distributed `SKILL.md` and local Markdown part, including input/reference guides. Remove links and prose that direct the reader to project ADRs, business analysis, solution design, tracker tickets, internal SDK source paths, or other authoring records. Public Palantir documentation links remain suitable as optional sources. Preserve an internal source trail in project deliverables or review comments, outside the distributed skills.

Remove the instruction beginning “Copy the entire ... folder, including `references/`” and equivalent packaging directions from task guidance. Keep the local guides themselves and their navigation links. Packaging instructions for repository maintainers may remain in repository-level installation material, outside distributed skill content.

Each skill folder remains independently readable offline, including its local parts. A link to a separate skill folder is not required for understanding. The existing 351-operation documentation gate remains applicable to the old skill set. The new development skill does not claim an operation is callable unless the installed CLI actually supports it.

## 6. Detailed acceptance and review

| ID | Traces to | Review condition |
| --- | --- | --- |
| AC-D-014-01 | BR-013-01, AC-013-01 | Review all distributed skill pages; no internal authoring document or local SDK path is addressed to the reader. Contextual use of words such as “design” in Foundry guidance remains allowed. |
| AC-D-014-02 | BR-013-02, AC-013-02 | The quoted copy-folder instruction and equivalent packaging directions are absent from skill content. Local guide navigation still works. |
| AC-D-014-03 | BR-013-03, 09; AC-013-03, 09 | An unfamiliar agent can find `pal-found-dev`, select pipeline or application guidance from the entry point, follow local links offline, and return to navigation. |
| AC-D-014-04 | BR-013-04, 05; AC-013-04..07 | A traceability review finds substantive explanations for every group and subsection in coverage-map sections 1–9. Each explains purpose, prerequisites, path, outcomes, and material constraints. |
| AC-D-014-05 | BR-013-06, 07; AC-013-08 | The separate REST topic distinguishes direct API, Python SDK, OSDK, and CLI; a reviewer can validate a read-only example, credential model, response, pagination, error, and async/write caveat against the cited source. |
| AC-D-014-06 | BR-013-08; AC-013-09 | Topic claims have direct official Palantir links. Removing network access does not remove essential explanations. Published links omit tracking parameters. |
| AC-D-014-07 | BR-013-10; AC-013-10 | Reviewers compare representative claims against official pages, local SDK docs, and FEATURE-012 guidance; conflicting or unsupported claims are resolved before acceptance. |
| AC-D-014-08 | BR-013-05, 10; AC-013-05..08 | Exercises for pipeline, application, branching, API, and operations journeys show that the agent can choose the right path, name the access boundary, and interpret an unfinished or partial outcome. |

Static checks can find forbidden internal paths, broken local links, missing topics, and stale packaging text. A reviewer must still judge whether the prose explains Foundry accurately. The review record should map every coverage-map subsection to one guide heading and its public source. The REST review should map each example to a documented endpoint or SDK method. No live credentials or destructive Foundry call is needed for this documentation acceptance.

## 7. Migration and release path

1. Inventory existing distributed skills and the new draft, including local parts. Capture the location of internal-document references, copy instructions, and relative links. Baseline FEATURE-012 operation coverage before editing.
2. Remove authoring references and packaging directions from existing skills. Review each removal in context so Foundry concept guidance and valid local navigation remain.
3. Build the development entry point and categorized guides. For each coverage-map subsection, add explanation and an official source; connect related areas without making another skill folder a required dependency.
4. Write the separate REST topic from official API material and the Foundry Python SDK docs. Check interface labels, permissions, examples, pages, errors, and pending outcomes against source behavior.
5. Review cross-topic claims, particularly SQL versus Python incremental behavior, the three branch layers, transaction commit, Action writeback, Compute execution modes, application authorization, and first widget release.
6. Verify local links and the copied offline bundle, review all topic mappings, and rerun existing operation-documentation checks. Resolve review findings before release. If content regresses, restore the prior skill text; no CLI rollback is part of this feature.

## 8. Developer Story boundaries

The stories below own separate content or a final review gate. Each should fit one sprint. A story stays New while FEATURE-013 is In Design. Technical task splitting and estimates belong to grooming.

| Story boundary | Owned outcome | Acceptance focus |
| --- | --- | --- |
| DEV-STORY-056: Existing skills cleanup | Remove internal-document references and copy-folder directions across the current distributed set. | AC-D-014-01, 02; preserve FEATURE-012 guidance and links. |
| DEV-STORY-057: Development entry and pipeline/operations guides | Task-based navigation and substantive coverage for source groups 1, 2, and 9. | AC-D-014-03, 04, 06, 08. |
| DEV-STORY-058: Ontology, Compute, application, branching, security guides | Substantive coverage for groups 3–8, with permission and branch distinctions. | AC-D-014-04, 06, 07, 08. |
| DEV-STORY-059: REST API development guide | Distinct source-backed API integration guidance and read-only example. | AC-D-014-05, 06, 07. |
| DEV-STORY-060: Offline and semantic integration review | Full subsection traceability, local-link validation, source review, and journey exercises. | AC-D-014-03..08; preserve FEATURE-012 gate. |

DEV-STORY-057 owns the `pal-found-dev` entry point. The REST and other content owners write their own guide areas. DEV-STORY-060 depends on DEV-STORY-056 through DEV-STORY-059. The cleanup story can run beside new content writing, but the integration review must assess both. Each Developer Story belongs to FEATURE-013 and EPIC-013. Story acceptance cites the applicable AC-D-014 criteria and identifies content ownership to avoid conflicting edits.

## 9. Dependencies and approvals

BA-ANA-014 and SA-ANA-014 are approved and Closed. SA-DES-013 owns technical layout and verification mechanisms; this document defines reader outcomes and business review conditions. Developer Stories require architect and lead developer review for one-sprint fit and dependency order. Project Owner approval of this design and the story boundaries is required before BA-DES-014 closes. FEATURE-013 advances only after BA and SA design subtasks close under the tracker workflow.

# Business analysis: User-facing Foundry skills and development knowledge

| Field | Value |
| --- | --- |
| Document ID | BA-ANA-014 |
| Feature | FEATURE-013 |
| Status | Closed; SA and Project Owner approved |
| Source | Project Owner request; `development-skill-coverage.md`; FEATURE-012 |

## 1. Business case and boundary

The installed Foundry skills should help an agent understand Foundry work without exposing the project's internal planning documents or distribution instructions. The current skills contain references to local SDK source paths and a copy-folder instruction. These are authoring details, not guidance for an agent carrying out a Foundry task.

The Project Owner also needs a `pal-found-dev` skill for planning and carrying out pipeline and application development. The restored coverage map names relevant Foundry subjects and official Palantir sources. The new skill should turn that map into practical, categorized explanations. A separate REST API development topic should explain how an application uses Foundry APIs, drawing on the Foundry Python SDK documentation for API concepts and behavior.

This feature changes skill content and its review criteria. It does not add a Foundry operation, alter platform permissions, or change how the installed CLI behaves. FEATURE-012 remains the baseline for accurate, offline operation guidance.

## 2. Business requirements

| ID | Requirement |
| --- | --- |
| BR-013-01 | Distributed skill text must not refer readers to internal project development documents, such as ADRs, design records, business analysis, tracker tickets, or local SDK source paths. Such sources may inform authoring but must not be prerequisites for using a skill. |
| BR-013-02 | Distributed skills must omit the instruction to copy an entire skill folder, including `references/`. Readers should see useful Foundry guidance and navigable local content without packaging directions in task guidance. |
| BR-013-03 | A discoverable `pal-found-dev` skill must explain how Foundry pipeline and application development areas relate, what each area is for, and when a developer would choose it. It must give usable guidance beyond a link list. |
| BR-013-04 | The development skill must cover every substantive group in the restored coverage map: platform/tool selection; Python and SQL pipelines; Ontology development; Compute Modules; React applications with OSDK; Workshop custom widgets; the three branching layers; security/governance; and lineage, monitoring, and production support. The reading-order section informs navigation, not a separate capability. |
| BR-013-05 | Each group must explain a representative development path, relevant prerequisites, lifecycle, outcomes, and material constraints. Where topics overlap, explanations must remain consistent with the existing Foundry skills. |
| BR-013-06 | A distinct REST API development topic must explain API access, resource and operation selection, authentication and authorization, request and response handling, pagination and asynchronous work where applicable, error handling, and safe use of writes. It must distinguish direct REST use, the Foundry Python SDK, and the installed CLI without claiming they have identical surfaces. |
| BR-013-07 | REST API guidance must derive behavior from the local Foundry Python SDK documentation and applicable official Palantir documentation. Examples must identify illustrative values and avoid implying that an undocumented endpoint or permission exists. |
| BR-013-08 | Each development topic must cite its relevant official Palantir pages with direct, reader-usable links. Core explanations must remain usable when the network is unavailable. Internal source paths and review traceability belong in project deliverables, not in distributed skills. |
| BR-013-09 | Readers must be able to navigate from the new skill's entry point to every topic and back. All distributed local links must resolve. |
| BR-013-10 | Review must verify topic coverage, source fidelity, absence of internal authoring references and copy-folder instructions, and consistency with FEATURE-012 operation guidance. |

## 3. Acceptance criteria

| ID | Requirement | Given / when / then |
| --- | --- | --- |
| AC-013-01 | BR-013-01 | Given any distributed skill page, when a reviewer searches its prose and links, then no internal project development document or local SDK source path is presented to the reader. |
| AC-013-02 | BR-013-02 | Given the distributed skills, when a reviewer reads their entry points, then the quoted copy-folder instruction and equivalent packaging directions are absent. |
| AC-013-03 | BR-013-03 | Given an agent new to Foundry development, when it reads `pal-found-dev`, then it can explain the role of each major development area and select a suitable starting path for a pipeline or application task. |
| AC-013-04 | BR-013-04 | Given the nine substantive groups in the restored map, when a reviewer compares them with the new skill, then every group has an identifiable, substantive topic and none is represented only by a source list. |
| AC-013-05 | BR-013-04, 05 | Given a pipeline task, when the agent reads the relevant topics, then it can distinguish Python and SQL development, tests and quality checks, release/build behavior, dataset transactions, and operational monitoring. |
| AC-013-06 | BR-013-04, 05 | Given an application task, when the agent reads the relevant topics, then it can distinguish Ontology modeling, Functions and Actions, Compute Modules, OSDK/React apps, and Workshop widgets, including the main permission boundary. |
| AC-013-07 | BR-013-04, 05 | Given a branching task, when the agent reads the skill, then it can distinguish Git/Code Repository branches, dataset/build branches, and Global Branching, including their scope and lifecycle. |
| AC-013-08 | BR-013-06, 07 | Given a task that calls for Foundry API integration, when the agent reads the REST API topic, then it can identify suitable API resources, authorize a request, interpret response/error/pagination behavior, and identify whether a write or pending result needs a follow-up check. The examples must match the cited SDK or official API material. |
| AC-013-09 | BR-013-08, 09 | Given an offline installation, when the agent follows local links from the new skill, then each topic is readable without network access; official source links remain optional for use and available for review. |
| AC-013-10 | BR-013-10 | Given the completed skill set, when reviewers compare its claims with official Palantir pages, SDK docs, and existing operation guidance, then unsupported or conflicting claims are corrected before acceptance. |

## 4. Coverage and traceability

| Source group in `development-skill-coverage.md` | Required knowledge in `pal-found-dev` | Criteria |
| --- | --- | --- |
| 1. Landscape and tool selection | Developer toolchain, applications, environments, and choice of visual pipelines or code | AC-013-03, 04 |
| 2. Python and SQL pipelines | Code Repositories, transforms, tests, local work, SQL, workspaces, release/builds, dataset transactions | AC-013-04, 05 |
| 3. Ontology development | Types, interfaces, Object Sets, Actions, Functions, and permissioning | AC-013-04, 06 |
| 4. Compute Modules | Execution modes, deployment, Sources, scaling, and operational behavior | AC-013-04, 06 |
| 5. React with OSDK | Developer Console, OSDK, OAuth/application restrictions, React lifecycle | AC-013-04, 06 |
| 6. Workshop custom widgets | Widget sets, development, parameters/events, OSDK, publishing | AC-013-04, 06 |
| 7. Branching | Git, dataset/build, Global Branching, and application integrations | AC-013-04, 07 |
| 8. Security and governance | Project, Ontology, Action, application, Compute, and branch boundaries | AC-013-04, 06, 08 |
| 9. Lineage and operations | Lineage, health checks, monitoring, scheduling, and production support | AC-013-04, 05 |
| Additional Project Owner request | REST API development informed by SDK and official API docs | AC-013-08 |

The coverage map's section 10 provides a suggested learning order. Skill navigation should reflect that order where helpful. Existing namespace skills provide operation-level detail; `pal-found-dev` supplies the development context that connects them.

## 5. Process impact, access, volume, and risks

Agent onboarding gains one development entry point. For pipeline work, readers must connect authoring, validation, release, builds, transactions, and support. For application work, readers must connect Ontology design, application authorization, development, publishing, and operations. The cleanup removes confusing internal references from both paths.

The skill grants no new access. It must state that project permissions, Ontology and Action policies, OAuth application restrictions, and service credentials still control use. API and SDK examples must avoid implying that authentication alone permits a request. Legacy permission material in the source map must be clearly marked as legacy when discussed.

Documentation creates no API traffic or data movement by itself. API examples can influence future request rates and transfer sizes. Pagination, polling, retries, uploads, downloads, and bulk reads therefore need practical guidance on bounded use and incomplete results. No fixed throughput or size limit should be invented from the source map.

| Type | Item | Handling |
| --- | --- | --- |
| Assumption | Restored coverage map is the intended topic inventory. | Use all nine substantive groups and treat its reading order as navigation advice. |
| Assumption | Official Palantir pages and the local Python SDK docs are authoring sources. | Cite official public pages in the skill; keep local source paths in project traceability only. |
| Risk | Some linked pages or terminology may change. | Verify official source content during authoring and review claims, not only links. |
| Risk | A high-level description may hide distinct transaction or branch behavior. | Include scope, lifecycle, and limitations for each area; check against existing skill claims. |
| Risk | REST examples may imply unsupported operations or universal SDK/CLI parity. | Match examples to source and label the interface being described. |
| Dependency | FEATURE-012 maintains offline CLI operation guidance. | Preserve its coverage while removing internal-document references. |

## 6. Deliverables and review

Required deliverables are this analysis and its document-index entry, an architecture analysis under SA-ANA-014, a business design and solution design in later workflow stages, the cleaned distributed skills, the new `pal-found-dev` skill, and review evidence against AC-013-01 through AC-013-10. The architect approved BR-013-01 through BR-013-10 and AC-013-01 through AC-013-10 in QUESTION-164. The Project Owner approved the same set in QUESTION-165 without changes.

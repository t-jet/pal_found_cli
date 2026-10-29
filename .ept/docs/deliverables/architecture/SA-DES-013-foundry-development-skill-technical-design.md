# Technical design: User-facing Foundry development skill

| Field | Value |
| --- | --- |
| Document ID | SA-DES-013 |
| Feature | FEATURE-013 |
| Status | Approved by BA, lead developer, and Project Owner |
| Date | 2026-10-04 |
| Basis | BA-ANA-014, SA-ANA-014, `development-skill-coverage.md`, FEATURE-012 offline skill contract |

## 1. Scope and decisions

The distribution will contain 20 Markdown skills: the existing platform skill, 18 CLI namespace skills, and a new `pal-found-dev` knowledge skill. The new skill explains how to develop pipelines and applications on Foundry. It does not add a CLI command, Python package dependency, Foundry endpoint, credential, or permission. The installed `pal_found_cli` package remains the executable interface for the 18 namespace skills. Direct REST and platform SDK examples in `pal-found-dev` describe separate integration choices; they are not promises of CLI coverage.

Existing skills will lose internal project-document references and the instruction to copy the skill folder. The skills repository README remains the place for copy and install procedures. Readers of distributed skills get local guidance and public Palantir links. Project ADRs, tracker tickets, `.ept` paths, and checked-in SDK files are authoring evidence only.

The `pal-found-dev` folder must work when copied alone. Its `SKILL.md` links only to files inside that folder. It may name `pal-found` and namespace skills as related optional skills in plain text; it must not link to `../pal-found/SKILL.md` or depend on that folder. The knowledge skill does not require the `pal_found_cli` install block because its development guidance is usable without that package. Command-specific skills keep their existing install prerequisite.

## 2. Files, ownership, and navigation

| Path in `pal_found_cli_skills` | Content and owner boundary |
| --- | --- |
| `.agents/skills/pal-found-dev/SKILL.md` | YAML name/description, Foundry development map, choice table, task-based links to all five local parts. No cross-folder link. |
| `pal-found-dev/references/pipelines.md` | Tool selection, Code Repositories/Workspaces, Python/SQL transforms, testing, local work, releases, builds, dataset transactions. |
| `pal-found-dev/references/ontology-compute.md` | Ontology types, interfaces, object sets, Actions, Functions, permissions, Compute Module lifecycle and execution. |
| `pal-found-dev/references/applications-branching-security.md` | Developer Console/OSDK, React apps, Workshop widgets, Git/dataset/Global Branching, cross-cutting security. |
| `pal-found-dev/references/rest-api.md` | Direct REST integration, Python platform SDK relationship, auth, request/response, paging, errors, retries, examples. |
| `pal-found-dev/references/operations.md` | Lineage, observability, health checks, scheduling, support. |
| Existing 19 `.agents/skills/pal-found*/` folders | Remove development-document references and copy instructions from `SKILL.md` and reference parts. Preserve operation semantics and local links. |
| `README.md` and `tests/test_distribution_commands.py` | Canonical 20-skill inventory and copied-folder verification. README alone explains copy procedure. |
| `tests/test_offline_skill_gate.py` and new focused tests | Include the knowledge skill in part-size/link checks; keep CLI install and 351-operation checks scoped to command skills; add user-facing content and topic gates. |

The entry point should tell a reader where to start for a pipeline, Ontology, application, API integration, or production-support task. Each local part should link back to the entry point and cite direct public sources near material claims. Essential facts must remain in local text when the public site is unavailable. Follow the existing 300-line maximum for each Markdown leaf; split a large part into linked local parts within `pal-found-dev/references/` if needed. A `references/` filename is an implementation detail of the bundle, not an instruction to users to copy it.

## 3. Topic and source traceability

Use the restored coverage map as a finite authoring register. Remove `utm_source` and other tracking query parameters from reader-facing URLs. Verify each retained URL and its claim against the current official page. A page that redirects, changes scope, or disappears needs an equivalent official replacement and a recorded review decision. Do not turn a source list into a skill section without explaining the development path, prerequisite, lifecycle, result, and material constraint.

| Coverage group | Local part | Representative official evidence and review focus |
| --- | --- | --- |
| 1. Tool selection and environments | `SKILL.md`, `pipelines.md` | [Developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain), [application building](https://www.palantir.com/docs/foundry/app-building/overview), [Pipeline Builder versus Code Repositories](https://www.palantir.com/docs/foundry/building-pipelines/considerations-pb-cr). Explain why to choose each path. |
| 2. Python/SQL pipelines | `pipelines.md` | [Python transforms](https://www.palantir.com/docs/foundry/transforms-python/overview), [SQL transforms](https://www.palantir.com/docs/foundry/transforms-sql/overview), [branch/release process](https://www.palantir.com/docs/foundry/building-pipelines/branching-release-process), [data branching](https://www.palantir.com/docs/foundry/data-integration/branching). Check SQL batch limitation, incremental fallback, test/build/transaction order. |
| 3. Ontology development | `ontology-compute.md` | [Core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts), [Actions](https://www.palantir.com/docs/foundry/action-types/overview), [Functions](https://www.palantir.com/docs/foundry/functions/overview). Distinguish modeling, querying, and transactional write behavior. |
| 4. Compute Modules | `ontology-compute.md` | [Compute Modules](https://www.palantir.com/docs/foundry/compute-modules/overview), [execution modes](https://www.palantir.com/docs/foundry/compute-modules/execution-modes). Explain container, source, mode, scaling, and execution limits. |
| 5. React with OSDK | `applications-branching-security.md` | [Developer Console](https://www.palantir.com/docs/foundry/developer-console/overview), [OSDK React](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/overview), [permissions](https://www.palantir.com/docs/foundry/developer-console/permissions). Explain app identity, generated SDK, lifecycle. |
| 6. Workshop widgets | `applications-branching-security.md` | [Custom Widgets](https://www.palantir.com/docs/foundry/custom-widgets/overview), [Workshop embedding](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop). Explain widget set, parameters/events, local work, publish. |
| 7. Three branch layers | `applications-branching-security.md` | [Code Repository branches](https://www.palantir.com/docs/foundry/code-repositories/branch-settings), [dataset branches](https://www.palantir.com/docs/foundry/data-integration/branching), [Global Branching](https://www.palantir.com/docs/foundry/global-branching/overview). State scope and merge/release behavior separately. |
| 8. Security and governance | `applications-branching-security.md`, `ontology-compute.md` | [Project roles](https://www.palantir.com/docs/foundry/security/projects-and-roles), [object security](https://www.palantir.com/docs/foundry/object-permissioning/overview), [application restrictions](https://www.palantir.com/docs/foundry/developer-console/application-restrictions). Do not imply OAuth scopes alone confer resource access. |
| 9. Lineage and operations | `operations.md` | [Data Lineage](https://www.palantir.com/docs/foundry/data-lineage/overview), [Observability](https://www.palantir.com/docs/foundry/observability/overview), [pipeline maintenance](https://www.palantir.com/docs/foundry/maintaining-pipelines/overview). Explain diagnosis, status, schedules, health and support. |
| Requested REST topic | `rest-api.md` | [API reference](https://www.palantir.com/docs/foundry/api/), [SDK overview](https://www.palantir.com/docs/foundry/api/v2/general/overview/sdks), local SDK v2 method docs. Verify public endpoint URL, release stage and example behavior. |

The coverage map's section 10 is reading-order advice, not a tenth platform capability. A review matrix should enumerate its substantive subsections, the exact local heading, at least one public source, and reviewer disposition. The matrix is project evidence, not distributed skill content.

## 4. REST API example contract

Use a read-only endpoint for the main example. `GET /api/v2/datasets/{datasetRid}` on the enrollment host is a suitable contract: the public [Get Dataset](https://www.palantir.com/docs/foundry/api/v2/datasets-v2-resources/datasets/get-dataset) page and checked-in SDK v2 `Datasets/Dataset.md` describe the method, RID argument, response, release stage, and permission requirements. The accompanying SDK example uses `FoundryClient`, `UserTokenAuth`, and `client.datasets.Dataset.get(dataset_rid)` only if its import, argument, and response are confirmed against the SDK source. Use an illustrative host, RID, and placeholder token. Do not publish credentials or claim a live request was run.

For each REST example or pseudocode path, review these fields: API major version and enrollment host; HTTP method and path; path/query/header/body shape; OAuth scope and Foundry resource permission; content type and return type; release stage; documented errors; and any follow-up state check. The direct HTTP example should carry a bearer token from an environment variable and a finite timeout. It should identify development user tokens versus production OAuth authorization-code or client-credentials flows. An application restriction and scope do not override the caller's Foundry resource permissions.

List examples must follow the documented `data`/`nextPageToken` contract, pass opaque `pageToken`, stop when the token is absent, and bound `pageSize` and total work as appropriate. Binary/Arrow/CSV responses must be treated as bytes or streams, not assumed to be JSON. Errors should distinguish malformed input, authentication, authorization, absent/inaccessible resource, throttling, and server failure. Retry only where the endpoint contract permits safe replay; after a timed-out write, check whether the first request committed before repeating it. A returned HTTP success may indicate request acceptance while a build or other asynchronous task still needs status inspection.

The current draft `rest-api.md` links to a broken SDK page at `/docs/foundry/api/general/overview/sdk`. Replace it with the verified [v2 SDK page](https://www.palantir.com/docs/foundry/api/v2/general/overview/sdks), and verify the other API overview links before release. The local Python SDK docs provide method-level evidence during authoring; they do not become reader-facing prerequisites. The `pal-found-*` CLI has its own parser and policy surface, so a platform SDK method existing does not imply a corresponding CLI operation.

## 5. Cleanup and migration

1. Inventory all Markdown under the 19 existing skill folders. Record every internal ADR/design/tracker/`.ept` reference and each copy-folder instruction. The current five `references/inputs.md` files in AIP Agents, Functions, Language Models, Models, and Ontologies refer to `.ept/docs/customer_input/foundry-platform-python/docs/v2/`; remove those paths from distributed text while preserving their input meanings. Search matches need context review: Foundry's own Code Repositories and ordinary words such as “design” remain valid user topics.
2. Remove the sentence beginning “Copy the entire ... folder, including `references/`” and equivalent packaging directions from each skill entry point. Keep copy instructions in the repository README. Preserve useful install and command instructions for CLI skills.
3. Author the new skill using the file map above. Resolve its draft `../pal-found/SKILL.md` cross-folder link. Verify public sources and SDK method contracts; correct unsupported or stale claims before acceptance.
4. Extend the README's canonical inventory and PowerShell copy verification from 19 to 20 folders, including `pal-found-dev`. Update POSIX and Claude Code instructions and any fixed count or list. Confirm copy replaces the new folder cleanly and includes all local parts. Stage a copy in the test harness's temporary directory, then inspect links in that copied tree.
5. Run content-boundary, topic, links, REST example, distribution, and existing 351-operation gates. Review claims manually against official pages. Record reviewer/source/date for claims that tests cannot prove. Then pin and distribute the skills repository revision with the existing parent gitlink process.
6. If the new skill or cleanup fails after distribution, return the skills repository to its last verified revision and recopy the complete skill folders. The installed CLI package needs no rollback for a documentation-only fault.

No new service, database, secret store, network runtime dependency, Foundry endpoint, or CLI entry point is required. Repository Markdown, README copy instructions, and pytest validation change. A live Foundry enrollment is optional for later safe verification, not a design prerequisite.

## 6. Nonfunctional requirements and gates

| Requirement | Verification |
| --- | --- |
| Offline usability | Each required concept is explained in local Markdown. Resolve links from every page after copying one skill folder independently; public links are optional deeper reading. |
| Source fidelity | Manual review maps each substantive topic and example to a direct official page and, for REST, the relevant local SDK contract. Record exceptions; do not infer behavior from names. |
| Maintainer clarity | Skill entry point stays short; leaf files stay at or below 300 lines; headings and navigation identify the next step. Avoid duplicated wording that can drift. |
| User-facing boundary | Static scan rejects `.ept/`, local SDK paths, ADR/ticket/design-document references, and copy-folder directions in distributed skill prose. Review false positives before changing valid platform terms. |
| CLI preservation | Existing frozen 351-operation inventory and example checks still pass. The knowledge-only `pal-found-dev` is included in generic leaf/link checks but excluded from command-operation and mandatory CLI install checks. |
| REST reliability | A focused contract review validates main HTTP/SDK examples against the public endpoint and SDK v2 docs; parser or syntax tests alone do not prove server behavior. No live secrets in tests. |
| Distribution | README and distribution tests expect 20 exact skill names, check all `SKILL.md` sentinels and required local parts, and reject missing or extra source/copied folders. |

Run `test_skill_documentation.py`, `test_offline_skill_gate.py`, `test_documented_examples.py`, `test_distribution_commands.py`, plus focused FEATURE-013 tests. Keep static checks narrow enough to report the file and offending link/text. Existing tests that iterate names starting with `pal-found-` need explicit separation of command skills from `pal-found-dev`; otherwise a knowledge skill may be mistaken for a CLI namespace.

## 7. Developer Story boundaries

| Story group | Exclusive implementation files | Acceptance focus |
| --- | --- | --- |
| Cleanup | Existing 19 `.agents/skills/pal-found*/` folders only | Internal-document and copy-direction removal without loss of operation guidance. |
| Development core | `pal-found-dev/SKILL.md`, `references/pipelines.md`, `references/operations.md` | Discoverability, groups 1–2 and 9, task path. |
| Ontology and applications | `pal-found-dev/references/ontology-compute.md`, `applications-branching-security.md` | Groups 3–8 and branch/security boundaries. |
| REST API | `pal-found-dev/references/rest-api.md` | API/SDK/CLI distinction, read-only example, auth, paging, errors, async/write guidance. |
| Integration and QA gate | `README.md`, skill tests, source-review evidence | Twenty-skill copy, self-contained links, topic/source matrix, prohibited text, regression. |

The first four groups own source-backed content and review it before integration. The fifth group owns reusable checks and the assembled-bundle audit; it does not replace subject-matter review. Content files are disjoint so stories can proceed in parallel after grooming. The integration story depends on their outputs. BA-DES-014 will register final story IDs and acceptance criteria; this table defines technical ownership before grooming. Each story must fit one sprint or be split at a local-part boundary.

## 8. Requirement traceability and review

| Requirement | Design and gate |
| --- | --- |
| BR-013-01/02; AC-013-01/02 | Sections 1, 5, 6: user-facing cleanup and negative scan. |
| BR-013-03/04/05; AC-013-03..07 | Sections 2–3, 7: entry point, nine-group map, development paths and source review. |
| BR-013-06/07; AC-013-08 | Section 4: distinct REST contract and SDK/public evidence. |
| BR-013-08/09; AC-013-09 | Sections 2, 5–6: independent copied-folder links and optional public sources. |
| BR-013-10; AC-013-10 | Sections 3–7: semantic review, test gates, distribution and CLI regression. |

Reviewers should check BA-DES-014's final content contract, lead developer feasibility of file/test ownership, and Project Owner approval of this design before FEATURE-013 moves to implementation planning. The parent feature and story workflow control that transition; this design does not authorize early implementation.

# 1. Content architecture and topic ownership

## 1.1 Distribution and navigation

Paths below are relative to `pal_found_cli_skills/.agents/skills/pal-found-dev/`. Keep `SKILL.md` and the five current reference pages as navigation overviews. Add task parts under `references/`. Every required file, anchor, fixture and example linked by this skill must resolve inside that folder. Another skill may be optional supplementary reading. The development skill must contain the explanation that its own task requires.

`SKILL.md` exposes a local capability-selection table, reading order and prerequisite boundary. Replace its public capability links with local headings. Its reading order follows customer section 10: platform, pipelines, SDLC, production, Ontology, applications, widgets, compute, branching, transactions. Each overview links its task parts; every part links its parent overview and entry point. Citations never serve as the only navigation route. No installation or folder-copy prose, project ticket IDs, ADRs, internal source checkout paths or development document links enter distributed skill content.

Each leaf has at most 300 lines. Each registered topic heading contains explicit child headings: `Concept and lifecycle`, `Prerequisites`, `Procedure`, `Worked example`, `Expected result and checks`, `Failures and recovery`. Authors may link a shared local prerequisite or schema section where it supplies the full fact. A heading with a list of URLs does not satisfy this contract. Additional parts require updating both the local navigation and maintainer register.

These six headings must carry all seven BA topic elements. `Prerequisites` explicitly includes the seventh element, access boundary: identify steps possible locally, steps requiring authorized enrollment connectivity, and administrator-controlled prerequisites. The register records a separate access-boundary evidence destination even when it points into that prerequisite heading. Missing access-boundary guidance fails topic acceptance.

## 1.2 File and topic map

Owner keys identify BA story responsibility boundaries, not agent identities. N=navigation/audit; P=Python/repository; W=SQL/workspaces; O=Ontology/Functions; C=Compute; A=apps/widgets; B=branching/security; M=operations; R=REST; V=verification. The coordinator binds these keys to actual DEV-STORY IDs before grooming. All topic titles below reproduce customer subsection identity; the last row is separate REST coverage.

BA-DES-015 created design-stage stories: N=DEV-STORY-061, P=062, W=063, O=064, C=065, A=066, B=067 and M=068. R infrastructure/shared models=069; R domain operation content=071,072,073,074,075,077,079,081,083,085,087,089,091; independent REST acceptance=093; V integration/GitHub delivery=070. BA-DES-015 section 7 binds thirteen exclusive resource predicates to all 425 operation identities. They remain New until the parent meets specific story workflow prerequisites.

| ID | Customer topic | Local file | Owning heading | Owner |
| --- | --- | --- | --- | --- |
| T01 | Platform and developer-tool overview | references/development-paths.md | Platform and tool selection | N |
| T02 | Development environments | references/development-paths.md | Environments and connectivity | N |
| T03 | 2.1 Code Repositories: authoring, Git and SDLC | references/pipelines/repositories.md | Repository authoring and review | P |
| T04 | 2.2 Python Transforms | references/pipelines/python-transforms.md | Python transform lifecycle | P |
| T05 | 2.3 Testing and data quality | references/pipelines/testing.md | Tests and expectations | P |
| T06 | 2.4 Local Python / VS Code development | references/pipelines/local-development.md | Local Python development | P |
| T07 | 2.5 SQL pipelines | references/pipelines/sql.md | SQL transforms | W |
| T08 | 2.6 Code Workspaces | references/pipelines/workspaces.md | Workspace exploration and publication | W |
| T09 | 2.7 Production SDLC and release management | references/pipelines/releases.md | Production release procedure | P |
| T10 | 2.8 Dataset transactions and internal execution semantics | references/pipelines/transactions.md | Transactions and incremental execution | P |
| T11 | 3.1 Ontology fundamentals and type system | references/ontology/modeling.md | Ontology types and backing data | O |
| T12 | 3.2 Interfaces and polymorphic Ontology design | references/ontology/interfaces.md | Interfaces and implementations | O |
| T13 | 3.3 Object sets and querying | references/ontology/queries.md | Object sets and query decisions | O |
| T14 | 3.4 Actions | references/ontology/actions.md | Action validation and writeback | O |
| T15 | 3.5 Functions | references/ontology/functions.md | Function runtimes and publication | O |
| T16 | 3.6 Ontology security | references/ontology/security.md | Object and Action authorization | O |
| T17 | Compute: Fundamentals and architecture | references/compute/lifecycle.md | Container configuration and lifecycle | C |
| T18 | Compute: Execution models and transaction/provenance behavior | references/compute/execution.md | Execution modes and provenance | C |
| T19 | Compute: SDK and integration references | references/compute/integration.md | SDK integration and Sources | C |
| T20 | 5.1 OSDK and Developer Console foundations | references/applications/osdk.md | Application registration and generated SDK | A |
| T21 | 5.2 React application lifecycle | references/applications/react.md | React query and release lifecycle | A |
| T22 | Widget lifecycle | references/widgets/lifecycle.md | Widget Set creation and releases | A |
| T23 | Widget: Local development and testing | references/widgets/testing.md | Playground and Workshop previews | A |
| T24 | Workshop ↔ React integration | references/widgets/integration.md | Parameters and events | A |
| T25 | Widget: Distribution | references/widgets/distribution.md | Widget and Marketplace distribution | A |
| T26 | 7.1 Global Branching | references/branching/global.md | Global branch lifecycle | B |
| T27 | 7.2 Git / local Code Repository branches | references/branching/git.md | Git review and branch settings | B |
| T28 | 7.3 Global branch vs Git branch | references/branching/contexts.md | Select and verify branch contexts | B |
| T29 | 7.4 Dataset/build branches | references/branching/datasets.md | Dataset branches and fallbacks | B |
| T30 | 7.5 Application-specific Global Branching | references/branching/integrations.md | Resource integration boundaries | B |
| T31 | Foundry platform security | references/security/platform.md | Projects and resource boundaries | B |
| T32 | Ontology/application security | references/security/applications.md | Application and Ontology permission checks | B |
| T33 | Compute and branch security | references/security/compute-branches.md | Execution identity and branch authorization | B |
| T34 | Lineage | references/operations/lineage.md | Trace branch and build provenance | M |
| T35 | Monitoring and alerting | references/operations/monitoring.md | Checks, monitoring and alert ownership | M |
| T36 | Pipeline support and operations | references/operations/support.md | Diagnose, recover and verify pipelines | M |
| T37 | Separate REST API development topic | references/rest-api.md and references/rest/* | Discover and author any frozen SDK REST operation | R |

The original `pipelines.md` routes T03-T10; `ontology-compute.md` routes T11-T19; `applications-branching-security.md` routes T20-T33; `operations.md` routes T34-T36. `rest-api.md` routes the complete catalog, authentication, capability indexes and operation/model contracts specified in part 2. `development-paths.md` is reached directly from the entry point.

## 1.3 Shared semantics and examples

P owns repository preview/test/release behavior; B links to that local procedure and owns comparison with dataset and Global contexts. O owns object/Action permissions; A owns OAuth registration and generated SDK authorization; C owns execution identity and Sources. B's security pages compare those already local mechanisms and provide diagnostic decision tables. P owns transaction/incremental concepts; R owns complete SDK operation/model/error contracts and links to P for transaction decisions. Every required explanation remains inside the development skill.

Each owner supplies a small worked task with complete inputs, code/configuration or recorded UI steps, output/state, and a failure case. Examples belong under `examples/<owner>/` only when a complete asset is needed; prose-only examples stay beside their procedure. Runnable code uses synthetic input. Enrollment placeholders must identify how to obtain and validate the value through authorized tenant UI or already generated artifacts. Do not invent a universal object type, function signature, branch name, scope or permission.

P's example joins synthetic orders and customers, validates null/duplicate behavior, exercises an expectation failure, and records preview versus release-build evidence. W supplies SQL syntax/limitations and notebook-to-output publication. O supplies a model/interface/query, Action validation and separate TypeScript v1, TypeScript v2 and Python Function examples where applicable. C supplies a container entrypoint, configuration, mode choice, Source identity and failure/recovery evidence. A supplies generated SDK binding, OAuth callback, a query/Action state and widget parameter/event round trip. B supplies conflicting branch/snapshot selection; M supplies a stale output investigation and post-recovery evidence.

## 1.4 Twenty-skill audit and shared defects

N records one audit row for every Markdown file in all 20 skills: public URL occurrence, surrounding reader instruction, essential dependency decision, repair/local destination, source owner and reviewer. Review every URL in context; a regular-expression directive scan is discovery evidence only. Add essential missing platform explanation to its owning skill. Preserve the current namespace/operation meaning and supported inventory.

When a gap changes a CLI operation contract or behavior, query existing FEATURE-012 tickets through the tracker and attach the gap to its responsible ticket. Create a FEATURE-012 BUG-SUB only when no existing ticket owns that defect. Link the unresolved owning ticket as `Blocks` to the affected FEATURE-015 story and final verification story; record exact unavailable task and unblock condition. Do not duplicate CLI semantics in a competing feature. Nonessential optional topics have a recorded disposition; an essential shared defect cannot be accepted as deferred.

[Back to design](../SA-DES-014-offline-development-knowledge.md)

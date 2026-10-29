# Foundry development skill source review

| Field | Value |
| --- | --- |
| Story | DEV-STORY-060 |
| Coverage register | `.ept/docs/customer_input/development-skill-coverage.md` |
| Distributed skill | `pal_found_cli_skills/.agents/skills/pal-found-dev/` |
| Review date | 2026-10-05 |
| Reviewer | Integration developer; content owners review platform claims separately |

Each row maps one substantive subsection in the coverage register to a local
heading and a public Palantir source. “Mapped” means that the local section
contains a development explanation and cites the source; it does not assert
that a live Foundry environment was used. Content owners must resolve factual
findings from their source reviews before QA signs off. Section 10 of the
register gives reading order and is represented by `SKILL.md` navigation.

| Register subsection | Local file and heading | Official source | Disposition |
| --- | --- | --- | --- |
| 1. Platform and developer-tool overview | `SKILL.md` § Choose a development path | [Developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain) | Mapped |
| 1. Development environments | `SKILL.md` § Choose a development path | [Code Workspaces](https://www.palantir.com/docs/foundry/code-workspaces) | Mapped |
| 2.1 Code Repositories: authoring, Git and SDLC | `pipelines.md` § Develop, test, and release | [Code Repositories navigation](https://www.palantir.com/docs/foundry/code-repositories/navigation) | Mapped |
| 2.2 Python Transforms | `pipelines.md` § Author Python transforms | [Python transforms](https://www.palantir.com/docs/foundry/transforms-python/overview) | Mapped |
| 2.3 Testing and data quality | `pipelines.md` § Develop, test, and release | [Python unit tests](https://www.palantir.com/docs/foundry/transforms-python/unit-tests) | Mapped |
| 2.4 Local Python / VS Code development | `pipelines.md` § Develop, test, and release | [Local development](https://www.palantir.com/docs/foundry/transforms-python/local-development) | Mapped |
| 2.5 SQL pipelines | `pipelines.md` § Author SQL transforms | [SQL transforms](https://www.palantir.com/docs/foundry/transforms-sql/overview) | Mapped |
| 2.6 Code Workspaces | `pipelines.md` § Develop, test, and release | [Code Workspaces getting started](https://www.palantir.com/docs/foundry/code-workspaces/getting-started/index.html) | Mapped |
| 2.7 Production SDLC and release management | `pipelines.md` § Develop, test, and release | [Branching and release process](https://www.palantir.com/docs/foundry/building-pipelines/branching-release-process) | Mapped |
| 2.8 Dataset transactions and internal execution semantics | `pipelines.md` § Understand builds, dataset branches, and transactions | [Data branching](https://www.palantir.com/docs/foundry/data-integration/branching) | Mapped |
| 3.1 Ontology fundamentals and type system | `ontology-compute.md` § Model the Ontology | [Core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts) | Mapped |
| 3.2 Interfaces and polymorphic Ontology design | `ontology-compute.md` § Model the Ontology | [Interfaces](https://www.palantir.com/docs/foundry/interfaces/interface-overview) | Mapped |
| 3.3 Object sets and querying | `ontology-compute.md` § Read and query objects | [Object Set basics](https://www.palantir.com/docs/foundry/api/ontologies-v2-resources/ontology-object-sets/ontology-object-set-basics) | Mapped |
| 3.4 Actions | `ontology-compute.md` § Write through Actions and Functions | [Action types](https://www.palantir.com/docs/foundry/action-types/overview) | Mapped |
| 3.5 Functions | `ontology-compute.md` § Write through Actions and Functions | [Functions getting started](https://www.palantir.com/docs/foundry/functions/getting-started) | Mapped |
| 3.6 Ontology security | `ontology-compute.md` § Secure Ontology consumers | [Ontology permissions](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions) | Mapped |
| 4. Fundamentals and architecture | `ontology-compute.md` § Run custom code with Compute Modules | [Compute Modules](https://www.palantir.com/docs/foundry/compute-modules/overview) | Mapped |
| 4. Execution models and transaction/provenance behavior | `ontology-compute.md` § Run custom code with Compute Modules | [Execution modes](https://www.palantir.com/docs/foundry/compute-modules/execution-modes) | Mapped |
| 4. SDK and integration references | `ontology-compute.md` § Run custom code with Compute Modules | [Python SDK](https://www.palantir.com/docs/foundry/compute-modules/python-sdk) | Mapped |
| 5.1 OSDK and Developer Console foundations | `applications-branching-security.md` § React applications with the Ontology SDK | [Developer Console application creation](https://www.palantir.com/docs/foundry/developer-console/create-application) | Mapped |
| 5.2 React application lifecycle | `applications-branching-security.md` § React applications with the Ontology SDK | [OSDK React applications](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/overview) | Mapped |
| 6. Widget lifecycle | `applications-branching-security.md` § Custom React widgets inside Workshop | [Create a Widget Set](https://www.palantir.com/docs/foundry/custom-widgets/create) | Mapped |
| 6. Local development and testing | `applications-branching-security.md` § Custom React widgets inside Workshop | [Widget development](https://www.palantir.com/docs/foundry/custom-widgets/development) | Mapped |
| 6. Workshop ↔ React integration | `applications-branching-security.md` § Custom React widgets inside Workshop | [Embedding in Workshop](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop) | Mapped |
| 6. Distribution | `applications-branching-security.md` § Custom React widgets inside Workshop | [Widget publication](https://www.palantir.com/docs/foundry/custom-widgets/publish) | Mapped |
| 7.1 Global Branching | `applications-branching-security.md` § Choose the right branch | [Global Branching concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | Mapped |
| 7.2 Git / local Code Repository branches | `applications-branching-security.md` § Choose the right branch | [Code Repository navigation](https://www.palantir.com/docs/foundry/code-repositories/navigation) | Mapped |
| 7.3 Global branch vs Git branch | `applications-branching-security.md` § Choose the right branch | [Global Branching concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | Mapped |
| 7.4 Dataset/build branches | `applications-branching-security.md` § Choose the right branch | [Data branching](https://www.palantir.com/docs/foundry/data-integration/branching) | Mapped |
| 7.5 Application-specific Global Branching | `applications-branching-security.md` § Choose the right branch | [Global Branching integrations](https://www.palantir.com/docs/foundry/global-branching/integrations) | Mapped |
| 8. Foundry platform security | `applications-branching-security.md` § Security and governance during development | [Projects and roles](https://www.palantir.com/docs/foundry/security/projects-and-roles) | Mapped |
| 8. Ontology/application security | `applications-branching-security.md` § Security and governance during development | [Application restrictions](https://www.palantir.com/docs/foundry/developer-console/application-restrictions) | Mapped |
| 8. Compute and branch security | `ontology-compute.md` § Run custom code with Compute Modules; `applications-branching-security.md` § Security and governance during development | [Compute Module execution modes](https://www.palantir.com/docs/foundry/compute-modules/execution-modes), [Global branch security](https://www.palantir.com/docs/foundry/global-branching/branch-security) | Mapped |
| 9. Lineage | `operations.md` § Use lineage to understand impact | [Data Lineage](https://www.palantir.com/docs/foundry/data-lineage/overview) | Mapped |
| 9. Monitoring and alerting | `operations.md` § Monitor data quality and service health | [Observability](https://www.palantir.com/docs/foundry/observability/overview) | Mapped |
| 9. Pipeline support and operations | `operations.md` § Establish a support path | [Maintaining pipelines](https://www.palantir.com/docs/foundry/maintaining-pipelines/overview) | Mapped |
| REST API development | `rest-api.md` § Host, version, and endpoint; Authentication and permissions; Requests and responses; Paging; Errors, throttling, and retries; Python SDK relationship | [API reference](https://www.palantir.com/docs/foundry/api/), [SDK overview](https://www.palantir.com/docs/foundry/api/v2/general/overview/sdks), [Get Dataset](https://www.palantir.com/docs/foundry/api/v2/datasets-v2-resources/datasets/get-dataset), [Paging](https://www.palantir.com/docs/foundry/api/general/overview/paging), [List Objects](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-objects/list-objects) | Mapped; SDK and List Objects contracts verified |

The REST check compared the official Get Dataset endpoint with the `get`
method table and example in
`.ept/docs/customer_input/foundry-platform-python/docs/v2/Datasets/Dataset.md`.
The official List Objects page limits Object Storage V1 backed objects to
10,000 results across pages and states that Object Storage V2 has no such
endpoint limit. The example uses a separate client-chosen work bound.
The Get Dataset page and local SDK method reference identify the dataset RID
argument; the SDK method table marks `get` Stable. The public Paging page
confirms the `nextPageToken` and `pageToken` contract. The
verification is recorded in DEV-059 comment
`20261005-163139-project-manager`.

## Reader journeys and gate evidence

| Journey | Entry and next step | Evidence |
| --- | --- | --- |
| Build a pipeline | `SKILL.md` → `pipelines.md` → `operations.md` | Tool choice, transform mode, test/release/build, and monitoring present. |
| Build an application | `SKILL.md` → `applications-branching-security.md` | Developer Console identity, OSDK, deployment, and permissions present. |
| Manage branches | `applications-branching-security.md` → `pipelines.md` | Git, dataset, and Global branch scopes are separate. |
| Use an API | `SKILL.md` → `rest-api.md` | Direct HTTP and Python SDK paths, auth, paging, errors, and retry guidance present. |
| Support production | `operations.md` → `pipelines.md` | Build/job status, lineage, checks, and support ownership present. |

Static gates run from `pal_found_cli_skills/tests`: exact 20-folder inventory,
all required local parts, copied-folder links, 300-line leaves, no internal
project paths or copy directions, and unchanged 351-operation CLI register.
The copied-folder gate uses an isolated pytest temporary directory.

On 2026-10-05, `python -m pytest -q tests` in `pal_found_cli_skills`
passed 31 tests. The suite ran the published PowerShell copy block against
temporary source and destination trees, including rerun and invalid-source
cases. The same command in `pal_found_cli_tool` passed 1,121 tests with six
coroutine warnings. Both suites used local files and mocks;
neither needed a Foundry token. The skill suite includes the frozen
351-operation documentation gate.

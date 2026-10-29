Below is a documentation map intended to form a reasonably complete Foundry development knowledge set across pipelines, Ontology development, Compute Modules, OSDK/React, Workshop custom widgets, SDLC, branching, security, lineage, transactions, and production operations.

A useful distinction to keep in mind is that Foundry currently has several related but separate branching layers: **Git/Code Repository branches**, **dataset/build branches**, and **Global Branching**, which coordinates changes across multiple Foundry applications. [Palantir](https://www.palantir.com/docs/foundry/data-integration/branching?utm_source=chatgpt.com)

## 1. Platform development landscape and tool selection

### Platform and developer-tool overview

- [Developer toolchain — overview of APIs, SDKs, development environments, Compute Modules and developer tooling](https://www.palantir.com/docs/foundry/dev-toolchain?utm_source=chatgpt.com)
- [Application building overview — application-building options and relationship to the Ontology/OSDK](https://www.palantir.com/docs/foundry/app-building/overview?utm_source=chatgpt.com)
- [Data integration overview — ingestion, transformation, pipeline management, security and lineage](https://www.palantir.com/docs/foundry/data-integration/overview?utm_source=chatgpt.com)
- [Building pipelines overview — lifecycle of building production data pipelines](https://www.palantir.com/docs/foundry/building-pipelines/overview?utm_source=chatgpt.com)
- [Application reference — major Foundry data-development applications and their responsibilities](https://www.palantir.com/docs/foundry/data-integration/application-reference?utm_source=chatgpt.com)
- [Considerations: Pipeline Builder vs. Code Repositories — when to use visual pipelines vs. code](https://www.palantir.com/docs/foundry/building-pipelines/considerations-pb-cr?utm_source=chatgpt.com)

### Development environments

- [Code Repositories overview — Git-based Foundry IDE for transforms, functions and other code](https://www.palantir.com/docs/foundry/code-repositories/overview?utm_source=chatgpt.com)
- [Code Workspaces overview — JupyterLab, RStudio and VS Code environments integrated with Foundry](https://www.palantir.com/docs/foundry/code-workspaces?utm_source=chatgpt.com)
- [VS Code workspaces overview — Code Repositories vs hosted VS Code vs local VS Code extension](https://www.palantir.com/docs/foundry/vs-code/overview?utm_source=chatgpt.com)
- [Ontology SDK overview — application development against the Foundry Ontology](https://www.palantir.com/docs/foundry/ontology-sdk?utm_source=chatgpt.com)
- [Compute Modules overview — containerized custom compute and services](https://www.palantir.com/docs/foundry/compute-modules/overview?utm_source=chatgpt.com)
- [Custom Widgets overview — custom React/front-end components embedded in Workshop](https://www.palantir.com/docs/foundry/custom-widgets/overview?utm_source=chatgpt.com)

---

## 2. Python and SQL data-pipeline development

### 2.1 Code Repositories: authoring, Git and SDLC

These are the foundational pages for the normal **edit → preview/test → commit → CI/checks → pull request → review → merge → tag/release/build** workflow.

- [Code Repositories overview](https://www.palantir.com/docs/foundry/code-repositories/overview?utm_source=chatgpt.com)
- [Code Repositories navigation — Code, Branches, Tags, Pull Requests, Checks and Settings](https://www.palantir.com/docs/foundry/code-repositories/navigation?utm_source=chatgpt.com)
- [Create transforms in Code Repositories](https://www.palantir.com/docs/foundry/code-repositories/create-transforms?utm_source=chatgpt.com)
- [Preview transforms](https://www.palantir.com/docs/foundry/code-repositories/preview-transforms?utm_source=chatgpt.com)
- [Code Repository unit tests](https://www.palantir.com/docs/foundry/code-repositories/unit-tests?utm_source=chatgpt.com)
- [Branch settings — default branch, merge strategies, protected branches and fallback branches](https://www.palantir.com/docs/foundry/code-repositories/branch-settings?utm_source=chatgpt.com)
- [Repository settings](https://www.palantir.com/docs/foundry/code-repositories/repository-settings?utm_source=chatgpt.com)
- [Repository upgrades — upgrade PRs and automatic merging](https://www.palantir.com/docs/foundry/code-repositories/repository-upgrades?utm_source=chatgpt.com)
- [Code Repositories administration overview](https://www.palantir.com/docs/foundry/code-repositories/admin-overview?utm_source=chatgpt.com)
- [Artifact settings](https://www.palantir.com/docs/foundry/code-repositories/artifact-settings?utm_source=chatgpt.com)
- [Code Repositories FAQ — CI, transform inputs/outputs and troubleshooting](https://www.palantir.com/docs/foundry/code-repositories/faq?utm_source=chatgpt.com)

### 2.2 Python Transforms

This is the main body of documentation for production pipeline code in Python. Python is currently the most feature-complete Foundry transform language, including batch and incremental pipelines, expectations, multiple compute engines and reusable libraries. [Palantir](https://www.palantir.com/docs/foundry/transforms-python/overview?utm_source=chatgpt.com)

- [Python Transforms overview](https://www.palantir.com/docs/foundry/transforms-python/overview?utm_source=chatgpt.com)
- [Transforms — inputs, outputs, decorators and compute logic](https://www.palantir.com/docs/foundry/transforms-python/transforms?utm_source=chatgpt.com)
- [Pipelines and transform registration](https://www.palantir.com/docs/foundry/transforms-python/pipelines?utm_source=chatgpt.com)
- [Incremental transforms — usage and semantics](https://www.palantir.com/docs/foundry/transforms-python/incremental-usage?utm_source=chatgpt.com)
- [Compute engines — selecting PySpark/single-node execution models](https://www.palantir.com/docs/foundry/transforms-python/compute-engines?utm_source=chatgpt.com)
- [Using Python libraries](https://www.palantir.com/docs/foundry/transforms-python/use-python-libraries?utm_source=chatgpt.com)
- [Python Transforms API reference](https://www.palantir.com/docs/foundry/api-reference/transforms-python-library/api-overview?utm_source=chatgpt.com)
- [Debugging Python transforms](https://www.palantir.com/docs/foundry/transforms-python/debugging?utm_source=chatgpt.com)

### 2.3 Testing and data quality

- [Python unit tests — pytest and execution as repository checks](https://www.palantir.com/docs/foundry/transforms-python/unit-tests?utm_source=chatgpt.com)
- [Data expectations — getting started](https://www.palantir.com/docs/foundry/transforms-python/data-expectations-getting-started?utm_source=chatgpt.com)
- [Data expectations reference](https://www.palantir.com/docs/foundry/transforms-python/data-expectations-reference?utm_source=chatgpt.com)
- [Development best practices — testing, project organization and health checks](https://www.palantir.com/docs/foundry/building-pipelines/development-best-practices?utm_source=chatgpt.com)
- [Building a production pipeline](https://www.palantir.com/docs/foundry/building-pipelines/building-production-pipeline?utm_source=chatgpt.com)

### 2.4 Local Python / VS Code development

- [Python local development](https://www.palantir.com/docs/foundry/transforms-python/local-development?utm_source=chatgpt.com)
- [Local transform preview](https://www.palantir.com/docs/foundry/transforms-common/local-preview?utm_source=chatgpt.com)
- [Palantir VS Code extension — transform preview](https://www.palantir.com/docs/foundry/palantir-extension-for-visual-studio-code/transforms-preview?utm_source=chatgpt.com)
- [Local VS Code vs. Foundry VS Code workspace guide](https://www.palantir.com/docs/foundry/vs-code/local-vs-workspace-guide?utm_source=chatgpt.com)
- [VS Code workspaces overview](https://www.palantir.com/docs/foundry/vs-code/overview?utm_source=chatgpt.com)

### 2.5 SQL pipelines

SQL transforms use Spark SQL inside Code Repositories. One important design constraint is that Foundry SQL transforms do **not** support incremental transforms; use Python when incremental semantics are required. [Palantir](https://www.palantir.com/docs/foundry/transforms-sql/overview?utm_source=chatgpt.com)

- [SQL Transforms overview](https://www.palantir.com/docs/foundry/transforms-sql/overview?utm_source=chatgpt.com)
- [Spark SQL reference — query form, dataset references and supported SQL functionality](https://www.palantir.com/docs/foundry/transforms-sql/spark-reference?utm_source=chatgpt.com)
- [Code Repositories batch-pipeline tutorial](https://www.palantir.com/docs/foundry/building-pipelines/create-batch-pipeline-cr/index.html?utm_source=chatgpt.com)

### 2.6 Code Workspaces

Code Workspaces are backed by repositories and provide version control while exposing JupyterLab/RStudio/VS Code-style workflows. For workspace-backed transforms, publication occurs through the workspace workflow rather than directly through its underlying repository. [Palantir](https://www.palantir.com/docs/foundry/code-workspaces/getting-started/index.html?utm_source=chatgpt.com)

- [Code Workspaces overview](https://www.palantir.com/docs/foundry/code-workspaces?utm_source=chatgpt.com)
- [Code Workspaces getting started — repository backing, branches, transforms and publishing](https://www.palantir.com/docs/foundry/code-workspaces/getting-started/index.html?utm_source=chatgpt.com)
- [Working with data in Code Workspaces — datasets, SQL access, branches and restrictions](https://www.palantir.com/docs/foundry/code-workspaces/data?utm_source=chatgpt.com)

### 2.7 Production SDLC and release management

- [Branching and release process — recommended pipeline release/branching SDLC](https://www.palantir.com/docs/foundry/building-pipelines/branching-release-process?utm_source=chatgpt.com)
- [Recommended project and team structure](https://www.palantir.com/docs/foundry/building-pipelines/recommended-project-structure?utm_source=chatgpt.com)
- [Development best practices](https://www.palantir.com/docs/foundry/building-pipelines/development-best-practices?utm_source=chatgpt.com)
- [Building a production pipeline](https://www.palantir.com/docs/foundry/building-pipelines/building-production-pipeline?utm_source=chatgpt.com)
- [Scheduling overview](https://www.palantir.com/docs/foundry/building-pipelines/scheduling-overview?utm_source=chatgpt.com)
- [Scheduling best practices](https://www.palantir.com/docs/foundry/building-pipelines/scheduling-best-practices?utm_source=chatgpt.com)
- [Builds — build graph, JobSpecs, staleness and branching behavior](https://www.palantir.com/docs/foundry/data-integration/builds?utm_source=chatgpt.com)

### 2.8 Dataset transactions and internal execution semantics

This group is especially important if you want to understand what a "build" actually means beneath the UI.

- [Datasets — transactions, dataset views and branches](https://www.palantir.com/docs/foundry/data-integration/datasets?utm_source=chatgpt.com)
- [Data branching — dataset transactions, branch pointers, parent branches, build branches and fallback resolution](https://www.palantir.com/docs/foundry/data-integration/branching?utm_source=chatgpt.com)
- [Builds — build resolution, freshness/staleness and execution](https://www.palantir.com/docs/foundry/data-integration/builds?utm_source=chatgpt.com)
- [Python Transform transactionality — output transactions are committed on successful jobs](https://www.palantir.com/docs/foundry/transforms-python/transforms?utm_source=chatgpt.com)
- [Incremental Transform semantics — added/modified data, snapshots and incremental fallback rules](https://www.palantir.com/docs/foundry/transforms-python/incremental-usage?utm_source=chatgpt.com)
- [Create dataset transaction API](https://www.palantir.com/docs/foundry/api/datasets-resources/transactions/create-transaction?utm_source=chatgpt.com)
- [Commit dataset transaction API](https://www.palantir.com/docs/foundry/api/datasets-resources/transactions/commit-transaction/?utm_source=chatgpt.com)
- [Abort dataset transaction API](https://www.palantir.com/docs/foundry/api/datasets-v2-resources/transactions/abort-transaction?utm_source=chatgpt.com)

In particular, a Python transform executes with transactions opened on its outputs and those transactions are committed after successful execution. Dataset branches themselves are transaction pointers and, unlike Git branches, dataset branches are not merged into each other. [Palantir](https://www.palantir.com/docs/foundry/transforms-python/transforms?utm_source=chatgpt.com)

---

## 3. Ontology development

### 3.1 Ontology fundamentals and type system

- [Ontology core concepts — objects, links, actions, functions, interfaces and object views](https://www.palantir.com/docs/foundry/ontology/core-concepts?utm_source=chatgpt.com)
- [Ontology types reference](https://www.palantir.com/docs/foundry/object-link-types/type-reference?utm_source=chatgpt.com)
- [Object types overview](https://www.palantir.com/docs/foundry/object-link-types/object-types-overview?utm_source=chatgpt.com)
- [Create an object type](https://www.palantir.com/docs/foundry/object-link-types/create-object-type/index.html?utm_source=chatgpt.com)
- [Properties overview](https://www.palantir.com/docs/foundry/object-link-types/properties-overview?utm_source=chatgpt.com)
- [Property/base data types](https://www.palantir.com/docs/foundry/object-link-types/base-types?utm_source=chatgpt.com)
- [Shared properties overview](https://www.palantir.com/docs/foundry/object-link-types/shared-property-overview?utm_source=chatgpt.com)
- [Link types overview](https://www.palantir.com/docs/foundry/object-link-types/link-types-overview?utm_source=chatgpt.com)
- [Link type metadata](https://www.palantir.com/docs/foundry/object-link-types/link-type-metadata?utm_source=chatgpt.com)
- [Object type groups](https://www.palantir.com/docs/foundry/object-link-types/type-groups?utm_source=chatgpt.com)
- [Type classes / metadata type classes](https://www.palantir.com/docs/foundry/object-link-types/metadata-typeclasses?utm_source=chatgpt.com)

### 3.2 Interfaces and polymorphic Ontology design

- [Interfaces overview — interface types and polymorphism](https://www.palantir.com/docs/foundry/interfaces/interface-overview?utm_source=chatgpt.com)
- [Implement an interface on an object type](https://www.palantir.com/docs/foundry/interfaces/implement-interface?utm_source=chatgpt.com)

### 3.3 Object sets and querying

- [Ontology Object Set basics — API-level object-set concept](https://www.palantir.com/docs/foundry/api/ontologies-v2-resources/ontology-object-sets/ontology-object-set-basics?utm_source=chatgpt.com)
- [Functions Object Sets API — search, filtering, links and aggregation; TSv1 reference](https://www.palantir.com/docs/foundry/functions/api-object-sets?utm_source=chatgpt.com)
- [TypeScript OSDK — modern object/object-set querying, links, filters and aggregations](https://www.palantir.com/docs/foundry/ontology-sdk/typescript-osdk?utm_source=chatgpt.com)
- [Datasets and saved Object Sets — static vs dynamic saved object sets](https://www.palantir.com/docs/foundry/analytics/datasets-object-sets?utm_source=chatgpt.com)
- [Ontology query compute — object types, object sets and query execution concepts](https://www.palantir.com/docs/foundry/ontologies/query-compute-usage?utm_source=chatgpt.com)

### 3.4 Actions

Actions are the primary transactional write primitive for operational Ontology workflows.

- [Action types overview](https://www.palantir.com/docs/foundry/action-types/overview/index.html?utm_source=chatgpt.com)
- [Action parameters](https://www.palantir.com/docs/foundry/action-types/parameter-overview?utm_source=chatgpt.com)
- [Action rules](https://www.palantir.com/docs/foundry/action-types/rules?utm_source=chatgpt.com)
- [Submission criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria?utm_source=chatgpt.com)
- [Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions?utm_source=chatgpt.com)
- [Read and write authorizations — security boundaries for Action reads/writes](https://www.palantir.com/docs/foundry/action-types/read-write-authorizations?utm_source=chatgpt.com)
- [Function-backed Actions](https://www.palantir.com/docs/foundry/action-types/function-actions-overview?utm_source=chatgpt.com)
- [Action side effects overview](https://www.palantir.com/docs/foundry/action-types/side-effects-overview?utm_source=chatgpt.com)
- [Webhooks — writeback vs side-effect transaction behavior](https://www.palantir.com/docs/foundry/action-types/webhooks?utm_source=chatgpt.com)

The webhook page is particularly useful for transaction design: a **writeback webhook runs before Ontology edits**, while a **side-effect webhook runs after the Ontology modification path**; the former gives limited coordination with the external system but does not constitute a distributed ACID transaction. [Palantir](https://www.palantir.com/docs/foundry/action-types/webhooks?utm_source=chatgpt.com)

### 3.5 Functions

- [Functions overview](https://www.palantir.com/docs/foundry/functions/overview?utm_source=chatgpt.com)
- [Functions getting started — repository, run, test and publish lifecycle](https://www.palantir.com/docs/foundry/functions/getting-started?utm_source=chatgpt.com)
- [Function language feature support — TypeScript v1/v2 and Python capability matrix](https://www.palantir.com/docs/foundry/functions/language-feature-support?utm_source=chatgpt.com)
- [Functions types reference](https://www.palantir.com/docs/foundry/functions/types-reference?utm_source=chatgpt.com)
- [Functions on Ontology objects](https://www.palantir.com/docs/foundry/functions/functions-on-objects?utm_source=chatgpt.com)
- [Object sets in Functions](https://www.palantir.com/docs/foundry/functions/api-object-sets?utm_source=chatgpt.com)
- [Python Functions on Ontology objects](https://www.palantir.com/docs/foundry/functions/python-functions-on-objects?utm_source=chatgpt.com)
- [Ontology edits from Functions — concepts](https://www.palantir.com/docs/foundry/functions/edits-overview?utm_source=chatgpt.com)
- [TypeScript v2 Ontology edits](https://www.palantir.com/docs/foundry/functions/typescript-v2-ontology-edits?utm_source=chatgpt.com)
- [Python Ontology edits](https://www.palantir.com/docs/foundry/functions/python-ontology-edits?utm_source=chatgpt.com)
- [Function unit testing — getting started](https://www.palantir.com/docs/foundry/functions/unit-test-getting-started?utm_source=chatgpt.com)
- [Testing/stubbing Object Set searches and aggregations](https://www.palantir.com/docs/foundry/functions/unit-test-object-searches?utm_source=chatgpt.com)
- [Testing Ontology edits](https://www.palantir.com/docs/foundry/functions/unit-test-ontology-edits?utm_source=chatgpt.com)
- [Creating stub Ontology objects for tests](https://www.palantir.com/docs/foundry/functions/unit-test-stub-objects?utm_source=chatgpt.com)
- [Mocking users and groups in Function tests](https://www.palantir.com/docs/foundry/functions/unit-test-users-groups?utm_source=chatgpt.com)
- [Function development in VS Code](https://www.palantir.com/docs/foundry/functions/navigating-vscode?utm_source=chatgpt.com)

### 3.6 Ontology security

For current deployments, start with the project/Compass-based model. Palantir now explicitly documents the Ontology-role and datasource-derived models as previous/legacy permission systems. [Palantir](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions?trk=public_post_comment-text\&utm_source=chatgpt.com)

- [Object permissioning overview](https://www.palantir.com/docs/foundry/object-permissioning/overview?utm_source=chatgpt.com)
- [Current Ontology permissions — project/Compass-based permissions](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions?trk=public_post_comment-text&utm_source=chatgpt.com)
- [Object security policies — object/property-level controls](https://www.palantir.com/docs/foundry/object-permissioning/object-security-policies?utm_source=chatgpt.com)
- [Legacy Ontology permissions — Ontology roles and datasource-derived model](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions-legacy?utm_source=chatgpt.com)
- [Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions?utm_source=chatgpt.com)
- [Action read/write authorizations](https://www.palantir.com/docs/foundry/action-types/read-write-authorizations?utm_source=chatgpt.com)

---

## 4. Compute Modules

### Fundamentals and architecture

- [Compute Modules overview — architecture and supported use cases](https://www.palantir.com/docs/foundry/compute-modules/overview?utm_source=chatgpt.com)
- [Getting started — local Docker development and deployment into Foundry](https://www.palantir.com/docs/foundry/compute-modules/get-started?utm_source=chatgpt.com)
- [Containers — Docker/image/container concepts for Compute Modules](https://www.palantir.com/docs/foundry/compute-modules/containers?utm_source=chatgpt.com)

### Execution models and transaction/provenance behavior

- [Execution modes — Function mode vs Pipeline mode, identity and permissions](https://www.palantir.com/docs/foundry/compute-modules/execution-modes?utm_source=chatgpt.com)
- [Compute Module sources — outbound networking, secrets and zero-trust model](https://www.palantir.com/docs/foundry/compute-modules/sources?utm_source=chatgpt.com)
- [Scaling — replicas, concurrency, autoscaling and scheduled overrides](https://www.palantir.com/docs/foundry/compute-modules/scaling?utm_source=chatgpt.com)
- [Usage and pricing / compute consumption](https://www.palantir.com/docs/foundry/compute-modules/usage?utm_source=chatgpt.com)

Pipeline-mode Compute Modules participate in the Foundry build system, so their inputs/outputs, provenance and permissions are managed as a pipeline execution rather than as an interactive service. [Palantir](https://www.palantir.com/docs/foundry/compute-modules/execution-modes?utm_source=chatgpt.com)

### SDK and integration references

- [Compute Modules Python SDK](https://www.palantir.com/docs/foundry/compute-modules/python-sdk?utm_source=chatgpt.com)
- [Compute Modules TypeScript/Node.js SDK](https://www.palantir.com/docs/foundry/compute-modules/typescript-sdk?utm_source=chatgpt.com)
- [Compute Module Functions and CLI](https://www.palantir.com/docs/foundry/compute-modules/functions?utm_source=chatgpt.com)
- [OSDK integration from Compute Modules](https://www.palantir.com/docs/foundry/compute-modules/osdk-integration?utm_source=chatgpt.com)
- [Platform Observability — includes metrics for Compute Modules](https://www.palantir.com/docs/foundry/observability/overview?utm_source=chatgpt.com)

---

## 5. React applications with the Ontology SDK

### 5.1 OSDK and Developer Console foundations

- [Ontology SDK overview](https://www.palantir.com/docs/foundry/ontology-sdk?utm_source=chatgpt.com)
- [Developer Console overview](https://www.palantir.com/docs/foundry/developer-console/overview?utm_source=chatgpt.com)
- [Create a Developer Console application — OAuth, OSDK generation and resources](https://www.palantir.com/docs/foundry/developer-console/create-application?utm_source=chatgpt.com)
- [Developer Console permissions — user vs application permissions and OAuth model](https://www.palantir.com/docs/foundry/developer-console/permissions?utm_source=chatgpt.com)
- [Application restrictions — OAuth scopes, resource restrictions and API-level security](https://www.palantir.com/docs/foundry/developer-console/application-restrictions?utm_source=chatgpt.com)
- [Bootstrap a TypeScript application](https://www.palantir.com/docs/foundry/developer-console/how-to-bootstrapping-typescript?utm_source=chatgpt.com)
- [TypeScript OSDK reference](https://www.palantir.com/docs/foundry/ontology-sdk/typescript-osdk?utm_source=chatgpt.com)
- [TypeScript OSDK subscriptions](https://www.palantir.com/docs/foundry/ontology-sdk/typescript-subscriptions?utm_source=chatgpt.com)
- [TypeScript OSDK 1.x → 2.x migration guide](https://www.palantir.com/docs/foundry/ontology-sdk/typescript-osdk-migration?utm_source=chatgpt.com)

### 5.2 React application lifecycle

- [OSDK React applications overview](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/overview?utm_source=chatgpt.com)
- [React development environment — VS Code workflow, lint/test/build, commits, tags and PR previews](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/development?utm_source=chatgpt.com)
- [@osdk/react — objects, Object Sets, links, aggregations, Actions, Functions and cache behavior](https://www.palantir.com/docs/foundry/ontology-sdk-react-applications/osdk-react?utm_source=chatgpt.com)
- [Host/deploy a custom OSDK application on Foundry](https://www.palantir.com/docs/foundry/developer-console/deploy-custom-application-on-foundry?utm_source=chatgpt.com)

The security pages should be treated as mandatory reading for custom apps: an OSDK application's effective authorization depends on user/application identity plus OAuth/application restrictions, rather than OSDK code bypassing Foundry authorization. [Palantir](https://www.palantir.com/docs/foundry/developer-console/permissions?utm_source=chatgpt.com)

---

## 6. Workshop custom React/OSDK widgets

This is the current documentation path for implementing a **native custom React widget that Workshop hosts**, rather than merely embedding an independent web application.

### Widget lifecycle

- [Custom Widgets overview](https://www.palantir.com/docs/foundry/custom-widgets/overview?utm_source=chatgpt.com)
- [Create a Widget Set — Foundry-hosted or external source repository, optional OSDK](https://www.palantir.com/docs/foundry/custom-widgets/create?utm_source=chatgpt.com)
- [Develop a Widget Set — React/Vite development and dev-mode previews](https://www.palantir.com/docs/foundry/custom-widgets/development?utm_source=chatgpt.com)
- [Publish a Widget Set — Foundry CI/CD, @osdk/cli and external CI/CD](https://www.palantir.com/docs/foundry/custom-widgets/publish?utm_source=chatgpt.com)
- [Add additional widgets to a Widget Set](https://www.palantir.com/docs/foundry/custom-widgets/additional-widget?utm_source=chatgpt.com)

### Local development and testing

- [Widget development — local machine and remote VS Code development workflow](https://www.palantir.com/docs/foundry/custom-widgets/development?utm_source=chatgpt.com)
- [Embed a Widget in Workshop — Workshop dev mode and preview unpublished changes](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop?utm_source=chatgpt.com)
- [Publish Widget Sets — lint/build/publish and Foundry tag builds](https://www.palantir.com/docs/foundry/custom-widgets/publish?utm_source=chatgpt.com)

The key local-development sequence documented by Palantir is essentially repository setup → authentication/token setup → dependency installation → local Vite/dev server, followed by dev-mode preview in the Custom Widgets playground/Workshop. A brand-new widget must have a first release before it becomes selectable in Workshop; subsequent unpublished versions can then be previewed in Workshop dev mode. [Palantir](https://www.palantir.com/docs/foundry/custom-widgets/create?utm_source=chatgpt.com)

### Workshop ↔ React integration

- [Parameters and events — Workshop variables, Object Sets and bidirectional events](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events?utm_source=chatgpt.com)
- [Use OSDK inside a Widget Set](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk?utm_source=chatgpt.com)
- [Embedding a Custom Widget in Workshop](https://www.palantir.com/docs/foundry/custom-widgets/embedding-in-workshop?utm_source=chatgpt.com)
- [Workshop widget concepts](https://www.palantir.com/docs/foundry/workshop/concepts-widgets?utm_source=chatgpt.com)

### Distribution

- [Publish a Widget Set](https://www.palantir.com/docs/foundry/custom-widgets/publish?utm_source=chatgpt.com)
- [Package Widget Sets into Marketplace products](https://www.palantir.com/docs/foundry/custom-widgets/marketplace?utm_source=chatgpt.com)

---

## 7. Branching: local/Git, dataset and Global Branching

This is the set I would consider mandatory for understanding Foundry development correctly.

### 7.1 Global Branching

- [Global Branching overview](https://www.palantir.com/docs/foundry/global-branching/overview?utm_source=chatgpt.com)
- [Global Branching core concepts — branch workflow, proposals, rebase and lifecycle](https://www.palantir.com/docs/foundry/global-branching/core-concepts?utm_source=chatgpt.com)
- [Global Branch security — roles, organizations, merge permissions and resource permissions](https://www.palantir.com/docs/foundry/global-branching/branch-security?utm_source=chatgpt.com)
- [Global Branching integrations — application/resource compatibility and limitations](https://www.palantir.com/docs/foundry/global-branching/integrations?utm_source=chatgpt.com)
- [Global Branching application](https://www.palantir.com/docs/foundry/global-branching/application?utm_source=chatgpt.com)

### 7.2 Git / local Code Repository branches

- [Code Repository navigation — sandbox branches, commits, checks and pull requests](https://www.palantir.com/docs/foundry/code-repositories/navigation?utm_source=chatgpt.com)
- [Code Repository branch settings — protection, merging and fallbacks](https://www.palantir.com/docs/foundry/code-repositories/branch-settings?utm_source=chatgpt.com)
- [Branching and release-process best practices](https://www.palantir.com/docs/foundry/building-pipelines/branching-release-process?utm_source=chatgpt.com)

### 7.3 Global branch vs Git branch

- [Global Branching in VS Code — explicit distinction between Code Repository/Git branches and Global branches](https://www.palantir.com/docs/foundry/vs-code/global-branching?utm_source=chatgpt.com)

This page is particularly valuable because Palantir explicitly states that a repository can expose **two different branch concepts**: the underlying repository/Git branch and a Global branch spanning multiple platform applications. [Palantir](https://www.palantir.com/docs/foundry/vs-code/global-branching?utm_source=chatgpt.com)

### 7.4 Dataset/build branches

- [Data branching — dataset branches, transactions, build branches and fallback branches](https://www.palantir.com/docs/foundry/data-integration/branching?utm_source=chatgpt.com)
- [Datasets — dataset transaction/view/branch model](https://www.palantir.com/docs/foundry/data-integration/datasets?utm_source=chatgpt.com)
- [Builds — build-level branching behavior](https://www.palantir.com/docs/foundry/data-integration/builds?utm_source=chatgpt.com)
- [Code Repository fallback branches](https://www.palantir.com/docs/foundry/code-repositories/branch-settings?utm_source=chatgpt.com)
- [Data Lineage branch selection and fallback behavior](https://www.palantir.com/docs/foundry/data-lineage/navigation?utm_source=chatgpt.com)

### 7.5 Application-specific Global Branching

- [Global Branching integrations index](https://www.palantir.com/docs/foundry/global-branching/integrations?utm_source=chatgpt.com)
- [Branching the Ontology](https://www.palantir.com/docs/foundry/ontologies/branching-ontology?utm_source=chatgpt.com)
- [Branching Functions](https://www.palantir.com/docs/foundry/functions/branching-functions?utm_source=chatgpt.com)
- [Pipeline Builder branch concepts](https://www.palantir.com/docs/foundry/pipeline-builder/branches-overview?utm_source=chatgpt.com)

---

## 8. Security and governance across all development

### Foundry platform security

- [Security and governance overview](https://www.palantir.com/docs/foundry/security/overview?utm_source=chatgpt.com)
- [Projects and roles — Foundry resource permission model](https://www.palantir.com/docs/foundry/security/projects-and-roles?utm_source=chatgpt.com)
- [Pipeline security overview](https://www.palantir.com/docs/foundry/building-pipelines/security-overview?utm_source=chatgpt.com)
- [Recommended Project/team structure for permission boundaries](https://www.palantir.com/docs/foundry/building-pipelines/recommended-project-structure?utm_source=chatgpt.com)

### Ontology/application security

- [Object permissioning overview](https://www.palantir.com/docs/foundry/object-permissioning/overview?utm_source=chatgpt.com)
- [Current Ontology project-based permissions](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions?trk=public_post_comment-text&utm_source=chatgpt.com)
- [Object security policies](https://www.palantir.com/docs/foundry/object-permissioning/object-security-policies?utm_source=chatgpt.com)
- [Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions?utm_source=chatgpt.com)
- [Action read/write authorization](https://www.palantir.com/docs/foundry/action-types/read-write-authorizations?utm_source=chatgpt.com)
- [Developer Console permissions](https://www.palantir.com/docs/foundry/developer-console/permissions?utm_source=chatgpt.com)
- [Developer Console application restrictions](https://www.palantir.com/docs/foundry/developer-console/application-restrictions?utm_source=chatgpt.com)

### Compute and branch security

- [Compute Module execution-mode permissions](https://www.palantir.com/docs/foundry/compute-modules/execution-modes?utm_source=chatgpt.com)
- [Compute Module zero-trust networking and Sources](https://www.palantir.com/docs/foundry/compute-modules/sources?utm_source=chatgpt.com)
- [Global Branch security](https://www.palantir.com/docs/foundry/global-branching/branch-security?utm_source=chatgpt.com)

---

## 9. Lineage, monitoring, operations and production support

### Lineage

- [Data Lineage overview](https://www.palantir.com/docs/foundry/data-lineage/overview?utm_source=chatgpt.com)
- [Data Lineage navigation — graph, branches, build history, code, health and schedules](https://www.palantir.com/docs/foundry/data-lineage/navigation?utm_source=chatgpt.com)
- [Data Lifetime — lineage-aware retention/deletion](https://www.palantir.com/docs/foundry/data-lifetime/overview?utm_source=chatgpt.com)

### Monitoring and alerting

- [Observability overview — monitoring, logs, traces and metrics](https://www.palantir.com/docs/foundry/observability/overview?utm_source=chatgpt.com)
- [Data Health — resource monitoring and alerting](https://www.palantir.com/docs/foundry/observability/data-health?utm_source=chatgpt.com)
- [Monitoring Views — scalable monitoring rules across resource scopes](https://www.palantir.com/docs/foundry/monitoring-views/overview?utm_source=chatgpt.com)
- [Health Checks overview](https://www.palantir.com/docs/foundry/health-checks/overview?utm_source=chatgpt.com)
- [Health Checks reference — status, duration, freshness, schema, content and size checks](https://www.palantir.com/docs/foundry/health-checks/checks-reference?utm_source=chatgpt.com)

### Pipeline support and operations

- [Maintaining pipelines overview](https://www.palantir.com/docs/foundry/maintaining-pipelines/overview?utm_source=chatgpt.com)
- [Recommended health checks](https://www.palantir.com/docs/foundry/maintaining-pipelines/recommended-health-checks?utm_source=chatgpt.com)
- [Defining data expectations for maintained pipelines](https://www.palantir.com/docs/foundry/maintaining-pipelines/define-data-expectations?utm_source=chatgpt.com)
- [Recommended support processes](https://www.palantir.com/docs/foundry/maintaining-pipelines/support-processes?utm_source=chatgpt.com)
- [Scheduling overview](https://www.palantir.com/docs/foundry/building-pipelines/scheduling-overview?utm_source=chatgpt.com)
- [Scheduling best practices](https://www.palantir.com/docs/foundry/building-pipelines/scheduling-best-practices?utm_source=chatgpt.com)
- [Build execution and debugging concepts](https://www.palantir.com/docs/foundry/data-integration/builds?utm_source=chatgpt.com)

---

## 10. Minimal recommended reading order

If the goal is to turn the material above into a **structured training/knowledge corpus**, I would sequence it as follows:

1. **Platform model:** Developer Toolchain → Data Integration → App Building.
2. **Pipeline fundamentals:** Code Repositories → Python Transforms → SQL Transforms → Builds → Datasets → Data Branching.
3. **SDLC:** Code Repository navigation → Branch Settings → Branching and Release Process → Tests → Expectations.
4. **Production:** Project Structure → Pipeline Security → Scheduling → Lineage → Data Health → Observability.
5. **Ontology:** Core Concepts → Types → Objects/Links/Interfaces → Object Sets → Actions → Functions → Permissioning.
6. **Application development:** OSDK → Developer Console → TypeScript OSDK → React OSDK → security/restrictions.
7. **Workshop extension:** Custom Widgets Create → Development → Parameters/Events → OSDK → Workshop embedding → Publish.
8. **Compute Modules:** Overview → Get Started → Execution Modes → Sources → Scaling → SDK.
9. **Branching deep dive:** Dataset Branching → Code Repository Branching → Global Branching → VS Code distinction → application-specific integrations.
10. **Transaction semantics:** datasets/transactions → builds → transform transactionality → incremental transforms → Actions/writeback → Compute Module pipeline execution.

The resulting corpus covers not only how to **write code**, but the surrounding execution model: Git/CI, data transactions, branch isolation, release control, application authorization, object/action security, provenance/lineage, scheduling, data quality, operational monitoring and production support. [Palantir](https://www.palantir.com/docs/foundry/code-repositories/overview?utm_source=chatgpt.com)
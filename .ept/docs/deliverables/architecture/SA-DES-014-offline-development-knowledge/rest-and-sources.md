# 2. REST contracts and source fidelity

## 2.1 Full SDK coverage

T37 covers every canonical REST operation exposed by released `foundry-platform-sdk==1.101.0`: 425 operations, 113 resource clients and 20 API-version/service namespaces (18 v2 services and two v1 services). This target matches the installed authoring runtime. [Frozen inventory and provenance](sdk-baseline.md) records identities, hashes, stages and compatibility evidence. The 351 CLI operation records remain a separate preservation requirement.

All v1/v2 operations and Stable, Public Beta and Private Beta stages in this baseline are included. Deprecated or compatibility-only methods retain local contracts and source guidance for choosing alternatives. Enrollment enablement and permissions determine execution availability. They do not remove operations from offline authoring coverage. Future SDK versions require explicit inventory refresh before claiming coverage.

`references/rest/catalog.md` indexes operations by task, version, service, resource and method. Every operation resolves to its full local contract, request/result/error models, worked SDK example and expected result. Authentication and client-behavior pages explain identity, token/OAuth lifecycle, scopes, resource permissions, transport modes, timeouts, retries, pagination, streams and uncertain writes. Service indexes link resource parts under `references/rest/<version>/<service>/`; model parts use qualified identities under `references/rest/models/<version>/<service>/`. Split leaves at 300 lines.

Each service index explains capability selection and lifecycle before listing methods. Filesystem guidance covers project/folder discovery, traversal and modifications supported by the frozen SDK, including resource access effects. AIP guidance covers Agents, versions, sessions, continuation/cancellation, RAG context and traces, language model operations and Models lifecycle. Functions guidance includes every Query method, including `execute` and streaming alternatives, with actual stage and compatibility notes. An operation absent from the frozen SDK must not be invented.

## 2.2 Complete local method/model contract

Every operation includes purpose/lifecycle; HTTP method/path; API version/stage; exact SDK signature; required/default/nullable path/query/header/body fields; serialization/content types; documented authorization and resource effects; response status/fields; documented errors; timeout/retry behavior; success checks; and failure/recovery. Required model descriptions include every transitive alias, field, enum value, union alternative/discriminator, list/map member, recursive reference, validation constraint and error envelope. SDK TypedDict request shapes and Pydantic response shapes both remain discoverable.

Source silence about scopes, permissions or retry guarantees is labeled explicitly. Reader guidance identifies tenant verification steps. Do not invent scope strings, universal privileges, idempotency keys or recovery endpoints. Document administrator/preview prerequisites and distinguish offline authoring from authorized enrollment execution.

Every operation has an adapted SDK example with complete synthetic inputs or precisely described tenant values, response/error fixtures and observable assertions. HTTP examples cover each wire-shape family and link to complete per-operation wire contracts. Review generated snippets for missing values, unbounded iterators and misleading output. Batch limits, byte encodings, stream formats and write effects match source.

Frozen extraction traverses request/response/error references across ordinary, asynchronous, raw and streaming methods. It identifies 3,242 reachable contract symbols: 2,278 model symbols and 964 error symbols. Symbols include aliases, classes and error parameter classes; these are extraction evidence awaiting independent reconciliation, not counts of business entities. Traversal terminates at a locally explained primitive or intentional tenant-defined schema. Unresolved symbols fail acceptance.

Transport wrappers are modes of one operation. Sync calls, async calls, ordinary iterators, raw pages and streaming responses have distinct return/lifetime rules. Ordinary async paged methods may return async iterators directly. Verify whether each example awaits, iterates or enters a context manager. Preserve finite page/object/retry/poll budgets, empty intermediate pages, repeated-token rejection, partial-result reporting and stream closure. Include OSv1/OSv2 differences where relevant.

Tenant-generated Ontology/Function/Agent/model types require a synthetic schema and local instructions for obtaining permitted metadata or generated bindings. Generic JSON containers still need documented structural constraints.

## 2.3 Maintenance and source fidelity

Implementation adds a deterministic maintainer extractor and validator outside distributed skills. Inputs are frozen release source/docs and pinned runtime. It emits indexes, contract scaffolds and reconciliation reports. Authors complete capability explanations, intent, prerequisites, effects, examples and recovery; independent reviewers check every completed contract. Generated and human-authored sections have explicit ownership so refreshes preserve guidance.

The maintainer manifest records release/commit/OpenAPI version, input hashes, operation identity/hash, local destinations, transitive symbols, contract/example reviews, author/reviewer and changes. Identical inputs produce identical IDs, edges and hashes. Refresh reports added/removed/changed records; changed signatures/models/stages/errors invalidate associated reviews and examples. Exact identity equality is required; equal counts alone cannot pass.

All 37 topic rows retain official source review and all 20 skills retain dependency audits. Reader citations are optional attribution after complete local explanations. No ticket, ADR, development document, internal checkout path or maintainer tool becomes a distributed dependency. Explain official website material in original prose; excerpts stay short. SDK adaptations retain applicable Apache-2.0 copyright, license and NOTICE obligations. Record adaptation provenance outside skills.

Customer checkout is release tag 1.79.0 at `2da67907be429c35f747eef565867ce81dd2cafc`, despite publishing-placeholder metadata `0.0.0`. Its 397 operations are compared with primary 1.101.0; retaining that comparison adds no second runtime support promise. Historical 1.79-only operations receive explicit historical labels. Current contracts/examples use 1.101.0 without mixing release signatures.

Unresolved task-critical conflicts/extraction gaps become QUESTION blockers. Grooming verifies frozen runtime and exact story operation sets. Project Owner approved revised architecture on 2026-10-06 in Closed QUESTION-179. Grooming and implementation proceed through story workflow before publication.

[Back to design](../SA-DES-014-offline-development-knowledge.md)

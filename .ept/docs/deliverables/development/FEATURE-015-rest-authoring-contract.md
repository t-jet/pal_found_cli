# REST authoring handoff

This document defines file and data ownership for DEV-STORY-069 and the thirteen REST domain stories. Approved requirements remain BA-DES-015 revision 2 and SA-DES-014 revision 2. Execution plans and estimates are recorded in tracker comments.

## Frozen operation ownership

[Exact operation partitions](FEATURE-015-rest-operation-partitions.json) assigns all 425 SDK 1.101.0 operation identities to thirteen exclusive domain owners. Its union has SHA-256 `a6542de72e2fd73a6197ddb6063cf76617b1c8c1bad95f53547dbbce87760bcd`. Each operation belongs to one domain story; API versions remain distinct. Shared schema ownership does not transfer operation ownership.

## Core ownership: DEV-STORY-069

Within `pal_found_cli_skills`, core owns `scripts/offline_rest_catalog.py`, `tests/test_offline_rest_catalog.py`, `maintainer/rest-contract-register.json`, and provenance/reconciliation files under `maintainer/rest/`. Distributed files owned by core are existing `references/rest-api.md`, `references/rest/catalog.md`, service `index.md` files, `references/rest/authentication.md`, `references/rest/client-behavior.md`, structural resource contracts under `references/rest/contracts/<version>/<service>/`, and the qualified definitions under `references/rest/models/`. These reader paths are relative to `.agents/skills/pal-found-dev/`. DEV-STORY-061 owns navigation links in SKILL.md; it does not rewrite the REST overview.

Core records exact signatures, HTTP paths/methods, serialization, required/default/nullable fields, response/error definitions, stages, transport wrappers and their source hashes. It renders original, readable explanations of model fields, aliases, enum members, union discriminators/alternatives, maps, lists, recursive links and constraints. Full source reconciliation includes indirect and compound forward references. The initial 3,242-symbol inventory is not an upper limit.

The register uses canonical `version.service.Resource.method` keys. Each entry records source release/commit/OpenAPI version, source/document hashes, structural contract destination and anchor, shared model/error references, available sync/async/raw/stream modes, domain owner, behavior destination, runnable example and fixture paths, and distinct author/reviewer identities and review disposition. Changed source signatures, models, stages or errors invalidate the associated review. Regeneration preserves human-owned behavior files.

Independent structural review compares every emitted definition and source constraint against a separately derived AST/runtime ledger, including descriptions, serialization aliases, nullability, defaults, enum/union alternatives and error parameters. The report lists every symbol and finding; aggregate totals or samples cannot replace it. Human review covers authored semantic annotations and every changed or unresolved source interpretation. Domain reviews check model meanings in every operation example. The first ten diverse contracts and recursive/compound models form a measured effort checkpoint. If complete review and corrected closure exceed the estimated capacity, split the remaining explicit deliverables before scaling; retain the full operation union and keep incomplete review gates open.

Core also owns shared transport examples under `examples/rest/common/`, with fake-transport request/response/error assertions and finite pagination, polling, retry and stream-lifetime demonstrations. They explain ordinary iterator returns and async iterator versus awaitable wrapper distinctions. Source silence about permissions or retry guarantees is explicit.

## Domain ownership

Each domain owns resource behavior parts under `references/rest/<version>/<service>/`, excluding `index.md`. Use stable resource names, split numbered parts before 300 lines, and retain exact operation anchors. Shared admin and Ontology namespaces have exclusive resource owners in the partition manifest. The resource page supplies lifecycle, prerequisites, effects, exact invocation, restrictions, validation and recovery for every operation. Structural definitions link locally to core-owned contracts and complete shared models.

Runnable examples and fixture data required by readers live inside the standalone skill at `examples/rest/<story-number>/`. Every operation exposes an adaptable SDK-backed example, synthetic input or explicitly described tenant value, serialized-request assertion, expected response and documented error assertion. Examples execute against a fake transport using prepared SDK 1.101.0 and a fake credential. They declare the difference between offline fixture execution and authorized enrollment execution. They cannot require a source checkout, another skill or a test-only file.

Domain-specific unit tests live at `tests/test_offline_rest_<story-number>.py`. Independent acceptance belongs to DEV-STORY-093 and `tests/test_offline_rest_acceptance.py`; its independent fixtures must not copy generator expectations. Every operation receives source and semantic review, including transport modes and all transitive model constraints. Public references supply optional attribution after complete local guidance.

## Acceptance and delivery boundaries

Catalog scaffolds alone do not satisfy an operation. Acceptance requires complete behavior and examples, corrected model/error closure, exact identity equality, independent source review, and fixture evidence for every operation. Preserve applicable SDK Apache-2.0 copyright, license and NOTICE obligations. Add no installation/copy prose or internal development links to distributed content. Independent QA uses only the skill and declared prepared tools while public access is blocked. GitHub publication and parent pin updates belong to DEV-STORY-070 after integrated acceptance.

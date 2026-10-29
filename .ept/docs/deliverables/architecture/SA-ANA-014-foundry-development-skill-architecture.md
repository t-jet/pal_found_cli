# Architecture analysis: Foundry development skill

| Field | Value |
| --- | --- |
| Document ID | SA-ANA-014 |
| Feature | FEATURE-013 |
| Status | Closed; BA approved in QUESTION-166 and Project Owner approved in QUESTION-167 |
| Date | 2026-10-04 |
| Sources | FEATURE-013, BA-ANA-014, `development-skill-coverage.md`, Foundry Platform Python SDK docs, existing skill and test trees |

## Scope and affected interfaces

FEATURE-013 changes the distributed Markdown skills, not the installed `pal-found-*` commands or Foundry APIs. Existing skills contain development artifacts and copy-folder instructions that are useful to maintainers but irrelevant to agents using Foundry. The new `pal-found-dev` skill must teach development choices and behavior across pipelines, Ontology, Compute Modules, applications, security, branching, and production operations. It also needs a separate REST API development guide. Its source map is `.ept/docs/customer_input/development-skill-coverage.md`.

| Component | Change |
| --- | --- |
| Existing `pal-found` and 18 namespace skills | Remove internal development-document references and the instruction to copy an entire folder. Keep user-facing Foundry and CLI facts. Check all entry points and local reference parts, including `inputs.md`. |
| `pal-found-dev/SKILL.md` | Add a short orientation and task-based navigation. It is the entry point for conceptual development guidance. |
| `pal-found-dev/references/*.md` | Keep categorized, substantive guides inside the skill folder. Include a distinct REST API guide. |
| Skills repository tests and distribution checks | Check content boundaries, coverage, links, and the copied offline bundle. Existing operation coverage tests remain applicable. |
| Installed `pal_found_cli` package | No command change required. Examples that mention a CLI operation must match the installed interface. |

The implementation already has a draft `pal-found-dev` entry point and five local topic guides. Treat them as draft material: review every claim and example against current public documentation and the Python SDK contract before acceptance. A topic heading alone does not satisfy coverage.

## Information architecture

Use one skill folder at `.agents/skills/pal-found-dev/`. Keep the entry point concise and route by task to local Markdown parts. The current five-part outline can work if each guide has clear sections and enough detail for the relevant task:

| Guide | Coverage-map sections |
| --- | --- |
| `pipelines.md` | 1–2: tool selection; Code Repositories and workspaces; Python/SQL transforms; tests, local development, release, builds, transactions. |
| `ontology-compute.md` | 3–4: Ontology types, interfaces, object sets, Actions, Functions, security; Compute Module execution and integration. |
| `applications-branching-security.md` | 5–8: Developer Console, OSDK/React, Workshop widgets, three branching layers, application and platform security. |
| `operations.md` | 9: lineage, observability, health, scheduling, production support. |
| `rest-api.md` | Additional requested topic: direct HTTP development and Python platform SDK relationship. |

Section 10 of the coverage map provides a reading path, which the entry point can adapt to task-based navigation. Every substantive subsection of sections 1–9 needs a traceable explanation, not only a link. The source map is an authoring checklist; readers of distributed skills should receive the needed concept and a public Palantir source link, not a path into `.ept` or a project ADR.

Existing skills use local `references/` parts for offline knowledge. Keep each `pal-found-dev` local link within its own folder. The current draft `../pal-found/SKILL.md` link crosses the folder boundary and fails the copied-skill contract enforced by `test_relative_links_resolve_within_skill_folder`. It should become plain text naming the separately installed `pal-found` and namespace skills. Do not make understanding a topic depend on those other folders being present. Public `www.palantir.com` links can support verification and deeper reading, while essential guidance remains in the local part.

The delivery stack is Markdown skill folders in `pal_found_cli_skills`, Python and pytest for repository checks, and the existing Python `pal_found_cli` package for any CLI examples. Foundry SDK documentation and the public Foundry API are evidence sources. They are not packaged runtime dependencies of the new skill.

## Source hierarchy and REST boundary

Use official Palantir documentation to explain platform behavior and supported development workflows. Verify each source URL in the coverage map, remove tracking query parameters from published links, and resolve moved or deprecated pages before writing a claim. Use the checked-in Python SDK documentation under `.ept/docs/customer_input/foundry-platform-python/docs/` as authoring evidence for endpoint paths, HTTP methods, request and response types, release stages, errors, and SDK method examples. The SDK source tree is internal to this repository and must not appear as a dependency or link in distributed skills. Where local SDK docs and current public API documentation differ, investigate and document the version or release-stage boundary; do not silently combine contracts. For example, the local v2 Dataset and Transaction method pages show per-method paths and release stages, including private-beta operations. The public endpoint page is the citation a skill reader can follow.

Keep REST API development separate from the 18 CLI operation catalogs and from OSDK app development. The REST guide should explain enrollment host and versioned endpoint selection; user token versus production OAuth client setup; scopes plus Foundry permissions; path/query/body/header and response contracts; JSON versus streaming or binary responses; cursor pagination; error handling, rate limits, timeout and write-retry uncertainty; SDK equivalents; and an end-to-end read-only example. It should explain that the platform SDK wraps platform API endpoints while generated OSDK targets application-specific Ontology resources. A method example must match a documented endpoint and credential model. It must not promise that an HTTP success proves an asynchronous build or Action has completed. Public [developer toolchain](https://www.palantir.com/docs/foundry/dev-toolchain), [API overview](https://www.palantir.com/docs/foundry/api/general/overview), and [Developer Console permissions](https://www.palantir.com/docs/foundry/developer-console/permissions) are starting references.

## Verification and migration

1. Inventory every distributed `SKILL.md` and local part. Search for ADR, design, tracker, internal `.ept` source paths, and the copy-folder instruction. Review search matches in context so user-facing references to Foundry Code Repositories remain.
2. Build a traceability table from the coverage map's sections and subtopics to specific `pal-found-dev` headings and public source links. Check meaning and examples manually against those sources; a heading or URL count is insufficient.
3. Validate every relative link from each skill entry point and reference part, both in the repository and in a staged copy of each independent skill folder. No cross-folder relative links. Preserve existing 300-line part limit unless an approved design changes it.
4. Check REST snippets against public endpoint documentation and local Python SDK method docs. Check imports, token handling, versioned paths, pagination termination, and response type. Tests should use no live credentials or Foundry calls.
5. Run existing skill documentation, offline-content, and distribution tests plus new coverage and content-boundary tests. Preserve the 351-operation inventory gate. Review changed prose for clarity and source-supported claims.
6. Distribute the new folder through the skills repository's existing clone/copy workflow. Release notes should state that `pal-found-dev` is a separate, documentation-only skill. Existing skill folders can be restored from repository history if a documentation regression is found; CLI package rollback is unnecessary for this change.

Static tests can prove file presence, link resolution, source-domain constraints, topic mapping, and prohibited text removal. They cannot prove Foundry semantics. A human review needs to compare representative claims and examples with official pages, especially branching, transaction commit, OAuth permissions, and asynchronous work.

## Constraints and open review

No new Foundry permissions, requests, or data volume arise from installing documentation. Agents following examples may make requests, so examples should use clearly illustrative identifiers and safe read-only calls where possible. Documentation must describe permission prerequisites without implying a bypass. The existing CLI keeps its separate policy and install guidance.

BA-ANA-014 owns the finite business requirements and acceptance criteria. The BA approved this architecture against those requirements in QUESTION-166, and the Project Owner approved it in QUESTION-167. No unresolved technical question requires a separate Question ticket; the source and packaging boundaries follow the stated feature and the existing offline-skill contract.

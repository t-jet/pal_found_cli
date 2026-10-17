# Business design: Offline Foundry skill guidance

| Field | Value |
| --- | --- |
| Document ID | BA-DES-013 |
| Feature and epic | FEATURE-012; EPIC-012 |
| Status | Resolved for design review; Project Owner approval pending in QUESTION-163 |
| Date | 2026-10-03 |
| Approved sources | BA-ANA-013 (BR-012-01..11, AC-012-01..13); SA-ANA-013; QUESTION-152 |

## 1. Business outcome and boundary

An agent new to Palantir Foundry receives a task, reads the distributed skills offline, chooses a supported operation, supplies Foundry-specific inputs, anticipates its effect, invokes the installed command, and interprets the result or failure. Each documented operation must give enough context for this path. The current scope is one general skill, 18 namespace skills, and the 351 operations supported by the installed CLI inventory. The installed command, rather than an older design catalogue, determines whether an operation is in scope. `geo` and `core` have no supported command operations; four older Widgets catalogue entries must not appear callable.

FEATURE-008 supplies brief platform and capability descriptions. FEATURE-009 supplies JSON formats and parameter variants. FEATURE-011 keeps command execution in the installed `pal-found-*` tool. FEATURE-012 adds the Foundry meaning of each capability, operation, input, and result. QUESTION-152 permits `SKILL.md` to link to packaged local Markdown parts. Every required part must travel with the skill folder and resolve offline. This decision supersedes the earlier single-file wording for this feature, while preserving documentation-only skills.

## 2. Agent journey and content responsibilities

1. The agent opens the general `pal-found` entry point. It learns what Foundry is, the relevant resource types and identifiers, shared authorization and output concepts, and how to find a capability skill.
2. The agent selects a namespace skill from the task's Foundry resource and desired outcome. The skill explains the capability's purpose, resource lifecycle, prerequisites, and links to related capabilities.
3. The agent selects a supported operation by its effect. The operation entry states which resource it reads, creates, changes, deletes, executes, or starts; it names material persistent or external effects and any permission boundary.
4. The agent prepares positional identifiers, JSON fields, operation options, and shared options using their Foundry meaning. Each entry states required status, accepted form or unit, and how different values change the operation or output.
5. The agent invokes the installed `pal-found-*` command. The skill explains how to distinguish local validation or access-control rejection from Foundry authorization failure and from an accepted request.
6. The agent interprets success, empty or partial results, page tokens, asynchronous status, and errors. The skill identifies the returned identifier or follow-up operation and avoids claiming a final state after timeout or pending work.
7. The agent can repeat this path using only the copied skill folder and installed CLI. Source links may help maintainers validate claims, but no web page is needed during use.

The skill entry point must provide clear navigation to every local part it requires. A namespace part may hold operation details, but the entry point must tell the agent which part to read before it invokes the command. Each copied namespace folder must carry all context required to use that namespace on its own. The general skill may offer broader context, but it cannot be a required external dependency for a namespace skill. Repeat concise shared explanations inside a namespace where needed and review them for consistency.

## 3. Required content record per operation

| Field | Business meaning and review rule |
| --- | --- |
| Identity | Installed command, resource, and operation name; supported or explicitly unsupported status. The record identifies the Foundry resource and its relationship to the capability. |
| Preconditions | Required existing resources, prior operations, permissions, or state. The record distinguishes CLI access controls from Foundry authorization. |
| Effect | Observable read or state change, material side effects, persistence, and what a successful request does or does not prove. |
| Inputs | Every positional identifier, JSON field, operation-specific option, and shared option that changes Foundry behavior or output; required status, Foundry meaning, allowed form or unit, default where applicable, and difference between meaningful values. |
| Success | Returned data or fields, identifier meaning, state change, empty and partial results, pagination, pending work, and the next check when applicable. |
| Failure | Relevant invalid-input, missing-resource, authentication, permission, CLI policy, rate-limit, timeout, and server outcomes. State whether the intended Foundry effect is known to have occurred. |
| Example | Clearly illustrative inputs tied to the intended resource, expected Foundry effect, and interpretation of the returned result. It does not imply that example identifiers exist. |
| Evidence | A reference to supported CLI behavior and authoritative Foundry material for each substantive claim; review date and command version or commit for maintainers. |

The record is complete only when a novice agent can explain the input, effect, and result without inferring Foundry behavior from a command name. Reviewers check every supported operation, including read-only and uncommon operations. The coverage register has one row for each of the 351 supported operations. Each row identifies its resource, effects and side effects, every applicable input meaning, success/empty/page/pending/error interpretation, example, source evidence, reviewer decision, and later QA test-case IDs. Parser checks can prove accepted syntax, but a reviewer must sign off on Foundry meaning using authoritative evidence. Existing skill checks that only find headings or flags do not meet this criterion. Examples cover relevant happy, empty or pending, and error outcomes across the operation's applicable cases. Destructive operations can be checked with source evidence and mocked results; no live destructive call is required for offline proof.

## 4. Capability workflow design

Each namespace skill must explain how its resources move through a useful task. It identifies the starting resource, the operation that advances or reads it, and the returned state or identifier needed next. Where a call only starts work, the skill names the status or result operation and explains that request acceptance is not final completion. Where results are paged, it explains when another page is needed. Where an input can expand data transfer or request count, it explains that effect before invocation.

The general skill holds common vocabulary for projects, folders, datasets, branches, transactions, ontology objects and actions, models, sessions, streams, media, and administration. Namespace skills explain their own workflows and exceptions. Cross-capability examples connect these concepts without pretending that a single operation performs a larger workflow. Existing auth, access-control, retry, output-format, and binary-limit guidance remains consistent with the operation records.

## 5. Abstract user, interface, and data design

There is no graphical UI or new application API in FEATURE-012. The agent-facing interface is the distributed skill text and the existing installed commands. The intended user experience is a clear path from the general skill to the right namespace and operation, with local part links that work offline. The design changes no CLI argument, Foundry endpoint, credential, or permission.

The business information structure is: a capability description contains resource concepts and operation records; an operation record contains the fields in section 3; an example connects inputs to effect and outcome; a coverage record links the operation to the installed command and review evidence. The skill bundle contains its entry point and any required local Markdown parts. A copied bundle is complete only if those parts remain present and readable without network access.

## 6. Acceptance criteria for the design

| ID | Source | Given / When / Then |
| --- | --- | --- |
| AC-D-013-01 | BR-012-01, 02; AC-012-01, 02 | Given a novice agent and the general skill, when it reads the primer and one capability entry, then it can identify the relevant Foundry resource, lifecycle, prerequisite, and appropriate namespace. |
| AC-D-013-02 | BR-012-03; AC-012-03 | Given any supported operation, when a reviewer reads its record, then the affected resource, observable effect, material side effect, and persistent state are stated. |
| AC-D-013-03 | BR-012-04; AC-012-04 | Given any positional input, JSON field, operation option, or shared option that affects behavior or output, when a reviewer reads its entry, then required status, Foundry meaning, allowed form or unit, and value-dependent effect are stated. |
| AC-D-013-04 | BR-012-05; AC-012-05, 06 | Given a success, empty result, next page, or pending job, when an agent reads the operation record, then it can distinguish the outcome and identify the returned identifier or next status check. |
| AC-D-013-05 | BR-012-06, 11; AC-012-07, 08, 13 | Given a rejected, rate-limited, timed-out, or unfinished invocation, when the agent reads the skill and CLI result, then it can identify the failure or uncertainty and does not claim an unproven Foundry change. |
| AC-D-013-06 | BR-012-07, 08; AC-012-09 | Given a documented capability task, when the agent follows its example, then it can state prerequisites, input meaning, effect, result meaning, and next operation without outside guidance. |
| AC-D-013-07 | BR-012-09; AC-012-10 | Given a copied skill folder and installed CLI without network access, when a reviewer checks all operation records and exercises representative calls with mocks or recorded responses, then every documented path is understandable and every required local part resolves. |
| AC-D-013-08 | BR-012-10; AC-012-11, 12 | Given the supported CLI inventory, when a reviewer compares it with the skill bundle and its evidence, then every supported operation has one complete record, unsupported entries are not callable, and shared claims do not conflict. |
| AC-D-013-09 | BR-012-11; AC-012-13 | Given an operation with permission, request-volume, or data-volume limits, when the agent reads its entry, then it can identify those limits before choosing the operation or interpreting its result. |

## 7. Migration and distribution procedure

1. Baseline the installed command inventory and existing 19 skill entry points. Keep implemented operations separate from old catalogue entries.
2. Preserve the brief sourced descriptions from FEATURE-008 and the JSON formats and variants from FEATURE-009. Reconcile the FEATURE-011 single-file wording with QUESTION-152 before changing a skill bundle.
3. Add general vocabulary and navigation. Add per-capability workflow descriptions and per-operation records. Place local Markdown parts beside their skill entry point when needed; keep each linked part in the copied bundle.
4. Compare each operation record with the installed CLI and authoritative Foundry source material. Resolve unknown semantics through review instead of inventing them. Check common concepts and exceptions across skills.
5. Verify every supported operation, input meaning, effect, result, and relevant failure. Check copied local links without network access and exercise representative agent paths using mocks or recorded responses. Do not require live destructive calls.
6. Ship the revised documentation with the normal skill copy process. A command or Foundry behavior change triggers an affected-skill review. If verification fails, restore the prior skill content from version control; installed command behavior remains unchanged.

## 8. Developer Story boundaries and dependencies

Stories should fit one sprint and deliver a usable capability or review gate. Each namespace story owns its skill content and per-operation evidence. Large Admin and Ontologies namespaces are split by disjoint resource clients and separate local reference parts. The first story in each split pair owns that namespace `SKILL.md` navigation; the second owns only its own part and checks its link with the first owner. Small related capabilities share a story. The general primer and shared rules story precedes namespace work; the final copied-bundle review follows all content stories. All stories belong to FEATURE-012 and EPIC-012. Grooming must freeze exact parser and dispatch operation keys for each owner's scope and confirm one-sprint fit, splitting oversized stories before Development. Each namespace story includes at least one offline agent exercise for every namespace it owns.

| Group | Intended outcome | Approximate supported operations |
| --- | --- | ---: |
| DEV-STORY-041: General skill | Platform primer, common concepts, navigation, shared result and failure rules | Shared |
| DEV-STORY-042: Admin identity/access | `admin` authentication_provider, enrollment, enrollment_role_assignment, group, group_member, group_membership, group_membership_expiration_policy, group_provider_info, role, user, user_provider_info. Owns Admin `SKILL.md` navigation and identity local part. | 38 |
| DEV-STORY-043: Admin governance and audit | All other `admin` resource clients (CBAC, host, markings, organizations) and `audit` log_file. Owns separate governance local part and Audit skill. | 28 + 2 |
| DEV-STORY-044: Datasets | Datasets, branches, files, transactions, and views | 33 |
| DEV-STORY-045: Filesystem | Projects, spaces, folders, resources, roles | 31 |
| DEV-STORY-046: Ontology discovery | `ontologies` action_type, action_type_full_metadata, linked_object, object_type, ontology, ontology_object, ontology_value_type, query_type. Owns Ontologies `SKILL.md` navigation and discovery local part. | 28 |
| DEV-STORY-047: Ontology actions and rich properties | All other `ontologies` resource clients, including ontology_interface, ontology_object_set, action, edits, attachments, queries, media, and time series. Owns separate action/property local part. | 39 |
| DEV-STORY-048: Data integration and health | Connectivity, checkpoints, data health | 29 |
| DEV-STORY-049: Agent and function use | AIP agents, functions, language models | 24 |
| DEV-STORY-050: Models | Models, versions, experiments, deployments, studios | 23 |
| DEV-STORY-051: Orchestration and SQL | Builds, schedules, jobs, SQL query lifecycle | 25 |
| DEV-STORY-052: Streams | Streams, subscribers, offsets, publication | 15 |
| DEV-STORY-053: Media sets | Media lifecycle and transactions | 19 |
| DEV-STORY-054: Applications and widgets | Third-party applications and Widgets | 17 |
| DEV-STORY-055: Offline integration review | Owns reusable coverage, local-link, and offline exercise checks plus the final copied-bundle gate; audits signed semantic rows from content stories. | All 351 |

Dependencies: DEV-STORY-042..054 depend on DEV-STORY-041 for the shared content contract. DEV-STORY-043 depends on DEV-STORY-042 for Admin navigation; DEV-STORY-047 depends on DEV-STORY-046 for Ontologies navigation. DEV-STORY-055 depends on DEV-STORY-041..054. These dependencies are tracker `DependsOn` links. The final review checks a signed 351-row semantic register from the content owners, bidirectional inventory coverage, copied local links, and mocked agent paths across all 18 namespaces. It also confirms that the four unsupported Widgets design rows are not presented as callable. No story implements a new CLI or Foundry operation. Detailed effort and technical sequencing belong to story grooming and SA design. Stories remain New while FEATURE-012 is In Design; their New-to-Open DoD requires the feature to reach Waiting for Implementation.

## 9. Traceability and review

The source-to-design mapping is in section 6. Each Developer Story must cite its covered BR-012 and AC-D-013 identifiers and identify its supported operation set. The final review story must cover AC-D-013-07..09 across all 351 operations. QA test cases will be linked to those story criteria during implementation. Architect approval is recorded in QUESTION-161 and lead developer approval in QUESTION-162; both are Closed. Project Owner approval is requested in QUESTION-163 and remains required before BA-DES-013 closes. SA-DES-012 owns technical layout and verification mechanism decisions; BA-DES-013 defines the information an agent must receive and the outcomes reviewers must check.

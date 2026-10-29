# Business analysis: Offline Foundry skill knowledge

| Field | Value |
| --- | --- |
| Document ID | BA-ANA-013 |
| Feature | FEATURE-012 |
| Epic | EPIC-012 |
| Status | Closed; approved by architect and Project Owner |
| Date | 2026-10-03 |
| Requirement source | FEATURE-012; Project Owner request recorded 2026-10-03 |

## 1. Business case and scope

An agent unfamiliar with Palantir Foundry needs to understand what it will read or change before it invokes a supported operation. The distributed skills currently provide brief platform and capability descriptions (FEATURE-008) and JSON formats and parameter variants (FEATURE-009). The new requirement adds Foundry meaning to those instructions: how capabilities work, what each operation does, how input values affect its behavior, and how to interpret success or failure. The agent must be able to complete this path with the installed skills and CLI while offline.

This analysis covers the general Foundry knowledge skill and every distributed namespace skill for an operation supported by the installed CLI. It covers documentation and verification. It does not authorize new Foundry operations, change CLI behavior, change platform permissions, or alter models used by agents. Unsupported operations must be identified as unsupported rather than explained as if callable. The documented operation inventory must follow the supported CLI surface at the time of review.

## 2. Business requirements

| ID | Requirement |
| --- | --- |
| BR-012-01 | The skill set must explain Palantir Foundry, its relevant resource types, and how those resources relate, in terms an agent with no Foundry knowledge can use. |
| BR-012-02 | Each covered capability must explain its purpose, common workflow, prerequisites, and how its resources relate to other covered capabilities. |
| BR-012-03 | Every supported operation must explain its Foundry purpose, the resource it acts on, the effect of invocation, and any material side effect or persistent state change. Read, create, update, delete, execute, and asynchronous actions must be distinguishable where applicable. |
| BR-012-04 | Every operation input, including positional identifiers, JSON fields, operation options, and common CLI options that affect Foundry behavior or output, must explain the meaning of its value, required or optional status, applicable form or unit, and how changing it affects the operation or result. Existing JSON format and variant coverage from FEATURE-009 remains required. |
| BR-012-05 | Every supported operation must explain the meaning of its successful result, including returned identifiers, resource state, empty or partial results, pagination, and asynchronous status or follow-up steps where applicable. |
| BR-012-06 | Every supported operation must explain relevant failure outcomes, including invalid input, absent resources, authentication, permission, access restriction, rate limiting, and timeout where applicable. The guidance must distinguish a failed request from an operation whose final Foundry outcome is still pending or unknown. |
| BR-012-07 | Skills must describe material prerequisites, ordering, and relationships between operations needed to complete a covered end-to-end Foundry task. |
| BR-012-08 | Each operation must have at least one coherent example that connects Foundry input meaning, expected Foundry effect, and result interpretation. Examples must not imply that illustrative identifiers are real resources. |
| BR-012-09 | An agent must be able to select, prepare, and interpret each supported operation using only the distributed skill files and installed CLI, without opening a web page or asking for platform guidance. Source references may support maintenance, but they must not be required for use. |
| BR-012-10 | Documentation must match the supported CLI behavior and authoritative Foundry source material. Shared Foundry concepts must have consistent meanings across skills, and changes to supported operations must trigger a documentation review. |
| BR-012-11 | Skills must make existing access restrictions, permission prerequisites, request-volume effects, and data-volume or transfer limits clear where they affect operation choice or result interpretation. Documentation must not claim to grant access that the agent lacks. |

## 3. Acceptance criteria

Each criterion applies to the currently supported operation inventory. A reviewer can check an operation against the installed CLI and its authoritative source material.

| ID | Requirement | Given / When / Then |
| --- | --- | --- |
| AC-012-01 | BR-012-01 | Given an agent with no Foundry knowledge and the general skill, when it reads the platform introduction, then it can identify the Foundry resources used by the covered skills and explain how those resources relate without another guide. |
| AC-012-02 | BR-012-02, BR-012-07 | Given a covered capability, when the agent reads its skill, then it can state the capability purpose, required starting conditions, main resource lifecycle, and related capability used in a covered task. |
| AC-012-03 | BR-012-03 | Given any supported operation, when a reviewer reads its skill entry, then the entry names the affected Foundry resource, describes its observable effect, and identifies any persistent or externally visible side effect. |
| AC-012-04 | BR-012-04 | Given any positional input, JSON field, operation option, or common CLI option that affects Foundry behavior or output, when a reviewer compares the skill with the supported operation, then the skill states whether the input is required, what its value identifies or controls, its applicable form or unit, and the difference caused by changing it. |
| AC-012-05 | BR-012-05 | Given a successful invocation, when the agent reads the operation entry, then it can identify what the returned fields or content represent, whether the Foundry state changed, and which identifier or status to use next. |
| AC-012-06 | BR-012-05 | Given an operation that returns no items, a page token, or a pending result, when the agent reads its skill, then it can distinguish an empty result from incomplete retrieval and identify the documented next step. |
| AC-012-07 | BR-012-06, BR-012-11 | Given an invocation rejected by credentials, permission, access restriction, invalid input, or a missing resource, when the agent reads its skill and CLI result, then it can identify the failure category and does not claim the intended Foundry effect occurred. |
| AC-012-08 | BR-012-06, BR-012-11 | Given a rate limit, timeout, or pending asynchronous result, when the agent reads its skill and CLI result, then it can distinguish a known failure from an unknown or unfinished outcome and identify a safe documented way to check status. |
| AC-012-09 | BR-012-07, BR-012-08 | Given a supported end-to-end task, when the agent follows a skill example, then it can state the prerequisite, input meaning, expected Foundry effect, result meaning, and next operation without external guidance. |
| AC-012-10 | BR-012-09 | Given a network-isolated environment with installed skills and CLI, when a reviewer checks every supported operation's guidance and exercises representative CLI calls from each capability against mocks or recorded responses, then each documented path has enough Foundry concept, input, effect, and result meaning to use it without external guidance. If a skill references local parts, those parts must be distributed and readable offline. Live Foundry invocation is optional and is not required for destructive operations. |
| AC-012-11 | BR-012-10 | Given the supported CLI operation inventory, when a reviewer compares it with the distributed skill set, then every supported operation has an entry and no unsupported operation is presented as callable. |
| AC-012-12 | BR-012-10 | Given a skill claim about Foundry behavior, when a reviewer traces it to supported CLI behavior and authoritative Foundry material, then the claim is supported and does not conflict with another skill. |
| AC-012-13 | BR-012-11 | Given an operation affected by a permission, access restriction, request limit, or data-size limit, when the agent reads its skill, then it can identify the restriction and how it changes possible outcomes before invocation. |

## 4. End-to-end process impact

| Process | Impact |
| --- | --- |
| Agent onboarding | General skill must give enough vocabulary to understand namespace skills without prior Foundry training. |
| Operation selection | Capability and operation entries must distinguish similar actions and identify their resource scope and effects. |
| Input preparation | An agent must map each identifier, value, and option to a Foundry concept, not merely copy a valid JSON shape. |
| Invocation and follow-up | Guidance must tell the agent when an operation changes state and when a later status check, page, or related operation is needed. |
| Result handling | The agent must interpret returned data, empty results, failures, and unfinished outcomes without asserting success prematurely. |
| Review and maintenance | Skill authors must verify full operation coverage and update affected explanations when CLI or Foundry behavior changes. |
| Distribution | The explanation must travel with the distributed skills so an offline agent has the same guidance as an online agent. |

## 5. Access restrictions, rates, and data size

This is a documentation change. It grants no new Foundry permission and changes no existing credential or access-control setting. The skill must explain that both CLI policy and Foundry authorization can prevent an operation. It must identify actions that write, delete, publish, execute, or expose data so an agent can check authority before acting. An error must not be described as a successful Foundry change.

The documentation adds no Foundry requests by itself. Better guidance may change which operations agents choose, but no request-rate increase can be quantified from the requirement alone. Skills must describe pagination, retries, rate limits, and status checks where they affect request volume or the interpretation of an incomplete result. Examples must not encourage unnecessary repeated calls.

The skills will grow because every supported operation needs semantic detail. Foundry data size and transfer limits do not change. Skills must explain data-volume limits, truncation, paging, binary transfer, or local output handling where those limits affect an operation's observable result. File growth and offline readability are review concerns; document composition rules apply to the deliverable and should inform later skill design.

## 6. Assumptions, risks, and dependencies

| Type | Item | Response |
| --- | --- | --- |
| Assumption | The supported installed CLI inventory is the boundary for operation coverage. | Review inventory at design and verification time; avoid promising unsupported SDK functions. |
| Assumption | Official Foundry material and supported CLI behavior can substantiate operation meaning. | Mark unresolved behavior for review instead of inventing an effect. |
| Risk | A syntactically correct example may still change the wrong Foundry resource. | Require resource and side-effect explanation beside inputs and results. |
| Risk | Duplicate concept explanations may conflict between general and namespace skills. | Review shared meanings across the distributed set. |
| Risk | CLI or Foundry changes may make offline guidance stale. | Make operation and source traceability part of change review. |
| Risk | Large files may make guidance hard to locate. | Require navigable, complete distributed content at design review. |
| Approved decision | FEATURE-011 design specifies one `SKILL.md` per skill, while FEATURE-009 design permits local parts for long skills. | QUESTION-152 approved packaged local Markdown parts linked from `SKILL.md`. Every part must ship and resolve offline; complete operation coverage and installed CLI execution remain required. |
| Dependency | FEATURE-008 supplies brief platform and capability descriptions; FEATURE-012 expands them into usable context. | Retain the prior descriptions and source traceability. |
| Dependency | FEATURE-009 supplies JSON formats and parameter variants; FEATURE-012 adds Foundry meaning and outcome semantics. | Preserve format and variant coverage in the combined guidance. |
| Dependency | FEATURE-011 defines skills as documentation for installed `pal-found-*` commands. | Keep explanations tied to the installed commands, without changing agent model definitions. |
| Dependency | SA-ANA-013 must review affected skill and CLI surfaces and source-of-truth constraints. | Request architecture review of these requirements. |

## 7. Traceability and review

| Source | Requirement coverage | Review evidence |
| --- | --- | --- |
| FEATURE-012 acceptance criteria 1 and 5 | BR-012-01, 02, 07, 08 | AC-012-01, 02, 09 |
| FEATURE-012 acceptance criteria 2 and 3 | BR-012-03, 04 | AC-012-03, 04 |
| FEATURE-012 acceptance criteria 4 | BR-012-05, 06, 11 | AC-012-05 through 08, 13 |
| FEATURE-012 acceptance criteria 6 and 7 | BR-012-09, 10 | AC-012-10 through 12 |
| BA-ANA-008 / FEATURE-008 | BR-012-01, 02, 10 | AC-012-01, 02, 12 |
| BA-ANA-009 / FEATURE-009 | BR-012-04, 10 | AC-012-04, 11 |
| BA-ANA-012 / FEATURE-011 | BR-012-09, 10 | AC-012-10, 11 |

Architect approved BR-012-01..11 and AC-012-01..13 in QUESTION-153. Project Owner approved the same requirements in QUESTION-155. QUESTION-152 approved the content model described above. Detailed business design, implementation stories, and test-case IDs will be linked in later workflow stages.

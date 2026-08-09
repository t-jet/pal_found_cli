# Architect Improvement Memory

## Improvement History

## Improvement: tracker CLI comment syntax

Condition:
- When adding a comment via `.ept/skills/tracking-system/tracker/tracker_cli.py`

Action:
- Do use the `comment create` subcommand (not `comment <ticket_id>`); required flags are `--subject` and `--text` (the CLI decodes literal two-character `\n` sequences into newlines, so pass `\n` not actual line breaks inside `--text`). Don't use `--text-file` for comments — it is NOT a documented option and `ticket-helper` will abort at validation. For long Markdown comment bodies on Windows PowerShell: (1) replace backticks with plain text or single-quotes because PowerShell treats backtick as its escape char inside double quotes; (2) pass the whole body as a single `--text` value with `\n` escapes. If the body is truly large, split it or put the artifact in the ticket body via `update --description-file` (which IS documented and reads a file) and post a short pointer comment. `update --description-file` replaces the ticket body; it does not append, so reserve it for body updates not for audit-trail comments.

## Improvement: exhaust all ADRs before claiming a requirement is absent

Condition:
- When deciding an AC-vs-implementation conflict and justifying the decision with "the requirement is not in any upstream contract"

Action:
- Do grep/read ALL relevant ADRs (not just the SRS and the directly-named ADR) for the keyword before making the absence claim. ADRs cross-reference each other and a decision clause in a sibling ADR (e.g. ADR-005 §Consequences) can mandate the very behavior under dispute. List the ADRs actually consulted in the decision comment so the reviewer can verify coverage.

## Improvement: post a visible correction when a prior decision was wrong

Condition:
- When a prior decision comment is discovered to be based on incomplete research after the ticket has already transitioned to Resolved (and the workflow forbids reopening)

Action:
- Do post a new comment titled "CORRECTION: supersedes prior decision" that explicitly names the prior comment ID, states what was wrong, cites the missed evidence, and gives the revised decision. Do not silently leave the wrong decision standing and do not edit/hide the prior comment — transparency lets the requester and implementer trace the reasoning.

## Improvement: memory read before any user-facing update

Condition:
- When starting any architect task or user request, including cases where a higher-priority instruction first requires loading `.ept/agents/architect.md` or another local preflight file

Action:
- Do complete required local preflight reads in strict order before any acknowledgement, progress update, planning, skill announcement, repository/task read, or efficiency batching. If `.ept/agents/architect.md` must be loaded first, the first tool call may read only that file; the next single-purpose tool call must read `.ept/skills/self-improvement/SKILL.md` plus `.ept/self-improvement/architect.md`. Don't batch architect preflight with skill index, workflow docs, tracker context, or other repo reads. The first visible assistant text may appear only after both mandatory reads are complete. If you catch a preflight-order miss, recover at once with the missing memory read, state the gap plainly if needed, and keep all later actions within protocol.

## Improvement: ticket tracker boundary

Condition:
- When gathering ticket context under a workflow that requires `ticket-helper` or tracking-system CLI use

Action:
- Don't use `rg`, `Get-Content`, or other filesystem reads against `.ept/tracker`; use only the allowed ticket interface for ticket state, links, comments, and workflow data. If `ticket-helper` is required but no subagent tool is exposed, say the limitation before using the documented tracking CLI as the only available ticket interface.

## Improvement: tracker storage exclusion when searching helper docs

Condition:
- When searching repository docs for ticket-helper or workflow instructions and direct tracker storage access is forbidden

Action:
- Do use exact ripgrep excludes with no stray spaces, for example `rg "ticket-helper" .ept -g "!.ept/tracker/**"`. Don't trust a malformed glob like `-g '! .ept/tracker/**'`, because it can list tracker files and break the ticket-helper-only rule.

## Improvement: no callable ticket-helper tool

Condition:
- When workflow requires `ticket-helper` subagent but the current host exposes no callable subagent tool (note: availability varies by host — some expose `ticket-helper` as a real subagent, others do not)

Action:
- Do state tool gap, read `.ept/agents/ticket-helper.md`, then use only documented tracker CLI commands through that protocol; don't read or write `.ept/tracker` files directly. If the subagent IS exposed, delegate all get/list/comment/link/update/workflow calls to it and verify its reported normalization of undocumented command forms.

## Improvement: DEV-STORY AC body template source

Condition:
- When writing Given/When/Then AC + operation catalog + technical scope for a DEV-STORY body, and a brief names DEV-STORY-00X as the "reference pattern"

Action:
- Do GET both DEV-STORY-008 (functions) AND the named reference sibling's FULL body before copying any pattern. DEV-STORY-008 currently holds the canonical AC/catalog/scope template (operation-catalog table + numbered Given/When/Then AC + Related Documentation links + Technical Scope bullets). Some sibling bodies (DEV-STORY-009 admin) are still TODO placeholders because their ACs live in comments, not the body — don't copy those. Template the author. dev_story body order: Description -> Authoritative operation catalog table -> Acceptance Criteria (Given/When/Then, numbered) -> Related Documentation (concrete doc links) -> Technical Scope -> Notes.

## Improvement: enumerate SDK namespace operations via nested cached_property traversal

Condition:
- When enumerating operations for a foundry_sdk v2 namespace (DEV-STORY triage / New->Open DoD), the operation count must be authoritative

Action:
- Do cross-validate the count against THREE independent sources and state all three in the DoD comment: (1) SDK source `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/<ns>/` — read `<ns>/_client.py` for `@cached_property` sub-client accessors, then each sub-client `.py` for public methods; (2) canonical-env-var-reference.md namespace table rows; (3) metadata-allow-list.md namespace block rows. For nested clients (audit.Organization.LogFile, filesystem.Resource.Role), enumerate the leaf client methods only — the intermediate client has no ops itself. Flag `bytes`-returning methods (need BinaryDownloadHandler, tier-3 BLOCKED) and paged/`ResourceIterator`-returning methods (need PaginationHelper). Check FR-ATTR-4 scope to confirm whether attribution applies (audit/admin/filesystem are excluded). When placeholder ticket prose claims operations absent from all three sources, call out the conflict and replace that prose with the concordant SDK contract; don't open a clarification question when primary sources fully resolve it.

## Improvement: tracker update optional named fields use --field key=value

Condition:
- When setting a non-standard optional field on a ticket via `tracker_cli.py update` (e.g. release_notes, epic, feature_request)

Action:
- Do use `--field key=value` form; don't assume a `--<field-name>` flag exists. The documented `update` flags are limited to `--status`, `--assignee`, `--priority`, `--author`, `--description` plus `--field key=value` for any other named field. A `--release-notes` flag is NOT recognized and silently degrades; the release_notes field is required by the dev_story Analysis→Grooming DoD, so verify with a follow-up `get` that the field actually populated before transitioning.

## Improvement: serialize tracker writes

Condition:
- When creating or updating tracker links, comments, or ticket fields through the tracker CLI

Action:
- Do run write operations sequentially and verify the resulting ticket/link state after batches; don't parallelize tracker writes because ID allocation can race and silently drop or overwrite intended links.

## Improvement: consult the workflow transition map before any status change

Condition:
- When a ticket update, auto-transition rule, or stakeholder instruction requires moving a ticket to a new status (including cases where an auto-transition rule like AT-x 'should have fired' but did not)

Action:
- Do call `tracker_cli.py workflow transitions <type> <status-name>` (via ticket-helper) — NO `get` prefix; `get` is only for ticket bodies — and only transition to a status in the returned allowed list. If the rule's intended target is not reachable, do NOT force an invalid transition; instead document the rule-handler / transition-map gap in a comment on the affected ticket, escalate to `workflow-mgr`, and leave the ticket in a non-terminal status. Cite the verbatim transition-map output as the refusal evidence so the reviewer can verify.

## Improvement: epic Blocked status does not automatically block child story pre-Development transitions

Condition:
- When a parent epic is in Blocked status and a child DEV-STORY needs to advance through any pre-Development status (New → Open → Analysis → Grooming)

Action:
- Do check whether a formal `Blocks` link from the epic to the story exists. If no Blocks link exists, the epic's Blocked status does not block the story's transition. Document the epic anomaly in the triage comment and note that the epic/DEV-STORY-001..004 upstream dependency applies to the Development phase (implementation), not to New/Open/Analysis/Grooming (registration, triage, scope definition, decomposition). Re-evaluate the epic block only when the story approaches Development. This has now been confirmed for both New → Open (DEV-STORY-006 / EPIC-002) and Open → Analysis.

## Improvement: preserve safety bounds when exact metadata is unknowable

Condition:
- When a contract requires exact response metadata but the transport may omit it and learning it would cross a configured safety limit

Action:
- Do preserve the safety limit, expose exact values only when verified, and represent unknown values with nullable fields plus proven lower bounds. Don't consume an unbounded response or invent an exact value to satisfy wording.

## Improvement: pass explicit author to ticket-helper writes

Condition:
- When delegating tracker write ops to `ticket-helper`, including comments, updates, links, or ticket creation

Action:
- Do name explicit tracker actor in first delegation, usually current role such as `architect`. Don't rely on helper to infer `--author`; it will fail validation before running tracker CLI.

## Improvement: default checklist placeholder is not fatal when description has real AC

Condition:
- When a sub-task body has a generated `## Acceptance Criteria` TODO section but the `## Description` contains specific, actionable acceptance criteria

Action:
- Do treat the detailed Description criteria as usable scope evidence for triage if required workflow fields and links are valid. Don't block New -> Open solely because the placeholder checklist remains, but document this explicitly in the triage comment for implementer visibility.

## Improvement: spawn typed subagents without full-history fork

Condition:
- When spawning a specific subagent type such as `ticket-helper`

Action:
- Don't set `fork_context: true` with `agent_type`; this host rejects that combination. Do pass all needed context in the message and spawn isolated typed subagent.

## Improvement: prove tracing at outbound transport

Condition:
- When an acceptance criterion claims distributed trace propagation from logs or SDK context values

Action:
- Do distinguish correlation logging from outbound propagation. Trace SDK ContextVars through client construction to transport headers, require client creation and retries inside one trace scope, and test emitted headers. When SDK resolves headers during HTTP-client construction, verify scope entry precedes client creation and assert exact transport headers (`X-B3-TraceId`, `X-B3-SpanId`, `X-B3-Sampled`) with tracing both enabled and disabled. Don't treat scope-entry mocks or stderr fields as propagation proof, and don't claim W3C when contract supports only B3.

## Improvement: readiness authorization needs complete direct-source cross-check

Condition:
- When asked for DEV-STORY New-to-Open readiness and an early stop interrupts the required SDK, environment-variable, metadata, SRS, SAD, and ADR review

Action:
- Do return proven evidence as partial, name each unverified contract, and fail transition authorization. Don't infer ACL classes, target paths, or acceptance criteria from operation names alone.

## Improvement: source-only readiness handoff

Condition:
- When a manager requests one readiness package and explicitly forbids tracker access, file delivery, and subagents

Action:
- Do treat supplied ticket facts as fixed, verify technical claims from SDK and project documents only, and return the full catalog, contracts, acceptance criteria, replacement body, DoD comment, and verdict in one response. Don't invoke the normal ticket gate or mutate delivery files.

## Improvement: classify local destructive commands beside SDK operations

Condition:
- When a namespace story adds a local destructive command outside its authoritative SDK operation catalog, such as session cache purge

Action:
- Do keep the local command outside SDK operation counts, then cross-check access-control write verbs, operation-level env mapping, metadata-only behavior, and documentation. Require access control before filesystem mutation; don't let an unrecognized verb bypass read-only mode.

## Improvement: verify ACL semantics and transport mode independently of generated method names

Condition:
- When a generated SDK catalog includes POST reads, mutating verbs absent from `AccessControlGuard`, or decoded byte/TableResponse methods that also expose `with_streaming_response`

Action:
- Do classify access from operation semantics and approved policy, not HTTP verb alone: preserve read classification for search-style POSTs, and add missing mutating verbs such as `launch` or `promote_version` to the shared guard with full regressions. For content downloads, inspect the generated response mode and require `with_streaming_response` plus `BinaryDownloadHandler` when available; don't call the eager decoded method and then claim bounded response memory.

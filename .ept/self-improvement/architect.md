# Architect Improvement Memory

## Improvement History

## Improvement: story-title operation counts must be re-verified against the vendored SDK before grooming

Condition:
- When a DEV-STORY title or an ADR/SAD entry claims a namespace operation count (e.g. streams "17 operations") and grooming scope must be defined

Action:
- Do enumerate the leaf client methods from the vendored SDK source (`foundry_sdk/v2/<ns>/`), then cross-check the canonical env-var reference and metadata allow-list row counts. When all three concord on a different number than the title/ADR/SAD, correct the count in the scope comment and DESIGN deliverable (flagged as stale), rather than silently implementing the claimed number. Confirmed on DEV-STORY-016 2026-08-10: title/ADR-003/SAD-001 say 17, SDK exposes exactly 15 (Dataset 1, Stream 7, Subscriber 7); sql_queries stays 5 across all three sources. Confirmed again on DEV-STORY-017 2026-08-10: title/SAD-001 say 15, SDK exposes exactly 20 (Connection 7, FileImport 6, TableImport 6, VirtualTable 1) with env-ref and allow-list concordant at 20; DEV-STORY-018 media_sets 19 was confirmed accurate across all three sources. Confirmed a third time on DEV-STORY-019/020 2026-08-10: checkpoints "3" CONFIRMED (Record get/get_batch/search, env-ref 3, allow-list 3 all PERMITTED); data_health title/SAD-001 say 4, SDK exposes exactly 6 (Check 4: create/delete/get/replace + CheckReport 2: get/get_latest) with env-ref and allow-list concordant at 6 (3 PERMITTED / 3 BLOCKED). Confirmed a fourth time on DEV-STORY-021/022 2026-08-10: third_party_applications "9" CONFIRMED (ThirdPartyApplication 1 + Website 3 + Version 5; env-ref 9, allow-list 9 with 4 PERMITTED / 5 BLOCKED) and widgets "12" CONFIRMED (DevModeSettings 6 + Release 3 + Repository 2 + WidgetSet 1; env-ref 12, allow-list 12 with 5 PERMITTED / 7 BLOCKED) — run the full three-source validation even when the title is accurate, because the cross-check also yields the metadata-only policy and write set that the DESIGN deliverable needs. Confirmed a fifth time on DEV-STORY-023 2026-08-11 (knowledge-skill documentation story): for the 20-namespace overview table, use the test-asserted OP_SPECS counts for the 18 implemented namespaces (admin 66, aip_agents 15, audit 2, checkpoints 3, connectivity 20, data_health 6, datasets 33, filesystem 31, functions 7, language_models 2, media_sets 19, models 23, ontologies 67, orchestration 20, sql_queries 5, streams 15, third_party_applications 9, widgets 12) with geo and core explicitly documented at 0 public operations (SDK source has only errors.py + models.py, SAD-001 AA-3); total 355 concordant across SAD-001, ENV-REF-001, META-ALLOW-001. For a knowledge skill, record the widgets runtime drift (12 design vs 8 installed per QUESTION-043) as a known limitation in the content and DESIGN rather than correcting the count.

## Improvement: verify ticket ID when create output omits it

Condition:
- When a tracker `create` command's YAML output lacks the `ticket_id` field (e.g. codereview/devops create returned only `current_status` onwards)

Action:
- Do run `get <expected-ticket-id> --author <role>` to confirm the ticket exists and carries the expected fields (priority, assignee, parent, estimated_hours) before reporting success; confirmed on CODEREVIEW-015, DEVOPS-016 on 2026-08-10, and again on the DEV-STORY-017/018 sub-task batches 2026-08-10 (design/development/unittest/codereview/devops creates all omit `ticket_id`; testcase/testexec include it). NOTE 2026-08-11 (DEV-STORY-023 batch): all seven sub-task creates (design/development/unittest/codereview/testcase/testexec/devops) DID include `ticket_id` — the omission behavior is run/version-specific, so always read the actual output and only fall back to `get` verification when the id line is genuinely absent.

## Improvement: tracker CLI comment syntax

Condition:
- When adding a comment via `.ept/skills/tracking-system/tracker/tracker_cli.py`

Action:
- Do use the `comment create` subcommand (not `comment <ticket_id>`); required flags are `--subject` and `--text` (the CLI decodes literal two-character `\n` sequences into newlines, so pass `\n` not actual line breaks inside `--text`). Don't use `--text-file` for comments — it is NOT a documented option and `ticket-helper` will abort at validation. For long Markdown comment bodies on Windows PowerShell: (1) replace backticks with plain text or single-quotes because PowerShell treats backtick as its escape char inside double quotes; (2) pass the whole body as a single `--text` value with `\n` escapes; (3) single-quoted inner text (e.g. quoted ticket titles) needs no escaping inside the double-quoted `--text` value — confirmed on DEV-STORY-013 comments 20260809-193823/195044/195048/195052. If the body is truly large, split it or put the artifact in the ticket body via `update --description-file` (which IS documented and reads a file) and post a short pointer comment. `update --description-file` replaces the ticket body; it does not append, so reserve it for body updates not for audit-trail comments.

## Improvement: groom a DEV-STORY end-to-end in one handoff

Condition:
- When a dev_story ticket is in Analysis with its Analysis DoD met and the Grooming stage is next

Action:
- Do drive the full Grooming in one session: (1) validate `workflow transitions dev_story <status>` before each move; (2) create ALL grooming sub-tasks together (DESIGN required first, then DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, DEVOPS if applicable) with per-role assignees, `addressed_to`, `estimated_hours`, checked acceptance criteria in `--description-file` bodies, and parent DEV-STORY links (Contains + ParentChild; CODEREVIEW gets bidirectional RelatesTo to DEV plus a Blocks link so the review stays blocked until DEV Resolved); (3) produce the DESIGN deliverable under `.ept/docs/deliverables/architecture/DESIGN-<n>-<ns>-cli.md` mirroring DESIGN-012, register it in `.ept/docs/document_index.md`, keep markdown tables lint-clean (space-padded separators satisfy MD060); (4) walk DESIGN to Closed (New→Open→In Progress→Resolved→Closed) with evidence comments at each stage; (5) post "DESIGN sub-task created", "Execution plan", and "Grooming complete" (DoD checklist) comments; (6) transition to Development. Use one sibling story (e.g. DEV-STORY-008) as the field/title/body convention reference. Confirmed twice: DEV-STORY-013 and DEV-STORY-014 (batch 1 and 2, 2026-08-09).

## Improvement: new deliverable docs must match sibling lint conventions

Condition:
- When creating a new markdown deliverable that mirrors an existing sibling document (e.g. a new DESIGN-XXX doc)

Action:
- Do run `get_errors` on the new file before committing; MD060/table-column-style flags compact separator rows, so use space-padded separator rows (`| --- | --- |`) matching clean siblings, and confirm the sibling file itself passes lint before copying its table style. Also update `.ept/docs/document_index.md` (deliverable entry plus Last Updated and Major Change footer) and re-check lint on the index.

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
- Do run write operations sequentially and verify the resulting ticket/link state after batches; don't parallelize tracker writes because ID allocation can race and silently drop or overwrite intended links. Refinement 2026-08-12 (SA-ANA-010): parallel `comment create` calls via separate ticket-helper subagent invocations each succeeded with distinct IDs (20260812-135354-architect, 20260812-135404-architect). The race risk applies to multiple writes inside one CLI process, not to one write per isolated subagent invocation. Keep one tracking operation per invocation; use hyphens in subjects and compact bodies (em-dash subjects caused a provider 400 on the BA-ANA-005 batch).

## Improvement: consult the workflow transition map before any status change

Condition:
- When a ticket update, auto-transition rule, or stakeholder instruction requires moving a ticket to a new status (including cases where an auto-transition rule like AT-x 'should have fired' but did not)

Action:
- Do call `tracker_cli.py workflow transitions <type> <status-name>` (via ticket-helper) — NO `get` prefix; `get` is only for ticket bodies — and only transition to a status in the returned allowed list. If the rule's intended target is not reachable, do NOT force an invalid transition; instead document the rule-handler / transition-map gap in a comment on the affected ticket, escalate to `workflow-mgr`, and leave the ticket in a non-terminal status. Cite the verbatim transition-map output as the refusal evidence so the reviewer can verify.
- Do re-`get` the ticket immediately before each planned follow-up transition: epic auto-transitions fire right after a manual status move when all EpicLink children are already terminal (confirmed on EPIC-007 2026-08-11: manual New→Open then AT-2 + AT-1×2 fired instantly, landing the epic in terminal Done before the planned Open→In Progress update; the transition call then failed exit 2 with 'Done is a terminal status'). A transition map validated earlier can go stale the moment auto-rules run, so verify actual current status rather than trusting the last known value.
- Do set the epic `resolution` field (`update --field resolution=Done`) BEFORE the manual In Progress→Resolved transition; the AT-1 Resolved→Done auto-transition then lands the epic in Done already carrying the resolution. Confirmed on the epic-closure batch 2026-08-11 (EPIC-005/006/008): all three were In Progress with all EpicLink DEV-STORYs Closed; each `update --status Resolved` exited 0 reporting pre-auto context `Resolved`, then the immediately-following `get` showed `Done` with `allowed_transitions: []` and `resolution: Done` present in Ticket Details — so the manual Resolved→Done step was skipped every time. When auto-rules can reach the target first, sequence: set resolution → post evidence comment → manual transition → re-get → skip redundant manual transition if terminal already landed.

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

## Improvement: drive SA-ANA analysis sub-tasks end-to-end in one batch

Condition:

- When executing the analysis phase for a set of SA-ANA sub-tasks (sa_subtask_analysis, New) that have dependency QUESTIONS addressed to architect

Action:

- Do run the full lifecycle per sub-task in this order and keep it repeatable: (1) post the New→Open DoD evidence comment, then `update --status Open`; (2) post the architecture plan + Open→In Progress DoD comment (business requirements, acceptance criteria, plan, related docs, deliverables list), then `update --status In Progress`; (3) close the dependency QUESTION: verify parent mapping via `get` and check `list links` for a Blocks link first, post the answer comment, walk New→Open→In Progress, set `time_spent_hours=0.5`, then Resolved→Closed (skip `--field resolution` — the question type has NO resolution field and exits 2); (4) create the deliverable under `.ept/docs/deliverables/architecture/SA-ANA-<n>-architecture-analysis.md` (<300 lines, lint-clean), register it in document_index.md; (5) post the architecture approach + In Progress→Resolved DoD comment (14 criteria incl. time reported, affected services, implementation approach, technology stack, migration approach, BA-ANA In Progress+), set `time_spent_hours=1.0`, then `update --status Resolved`; (6) create the PO approval QUESTION under the sub-task addressed to project-owner WITHOUT a Blocks link so the parent stays Resolved. Confirmed on the full 8-sub-task batch SA-ANA-002..009 on 2026-08-12 (deliverables 85–95 lines each; all 8 dependency QUESTIONS-048..055 closed; approval QUESTIONS-056..063 created; all SA-ANA left at Resolved awaiting PO approval, not Closed, because BA-ANA counterparts are not yet terminal).

## Improvement: em-dash comment subjects under user mandate - honor, fall back on 400

Condition:
- When a user explicitly mandates a comment subject containing an em dash (e.g. "SA cross-review - BA-ANA-XXX (2026-08-12)") or a tracked deliverable pattern uses one

Action:
- Do use the mandated subject verbatim and keep the body compact; em-dash subjects succeeded 9/9 in the 2026-08-12 SA cross-review batch (BA-ANA-002..010) plus the SA-ANA-010 naming-update comment. Only on a provider 400 invalid_request_error retry once with hyphens in the subject.

## Improvement: after PO naming decisions land, sweep analysis deliverables and flag design-phase naming updates

Condition:
- When the PO confirms naming decisions (e.g. pal_found_ rename via QUESTION-072..075) after analysis deliverables were written with assumed or PROPOSED names

Action:
- Do update the owning SA-ANA deliverable mapping rows to CONFIRMED values (repos/package underscore pal_found_, entry-point and skill folder hyphen pal-found-), mark still-open rows (env vars, historical doc filenames), update migration/risks/coordination sections, post an update comment on the SA-ANA ticket, and include a per-ticket naming-impact note in the SA cross-review comments on the BA-ANA counterparts so the design phase picks them up. Don't approve silently or leave superseded proposals in the mapping table. Confirmed 2026-08-12: SA-ANA-010 rows 2,3,4,6,7,8,9,10 corrected; 9 cross-reviews on BA-ANA-002..010 all APPROVED with naming notes.

## Improvement: close SA-ANA sub-tasks Resolved-to-Closed after PO approval, matching BA counterpart by parent feature

Condition:
- When a batch of SA-ANA analysis sub-tasks sits at Resolved with PO approval QUESTIONS closed and BA-ANA counterparts terminal, and the manager directs Resolved -> Closed

Action:
- Do follow per-ticket: get SA-ANA (confirm Resolved, not Blocked; Closed is in allowed_transitions) -> get the BA-ANA counterpart and confirm terminal -> comment create DoD evidence (author architect; subject "Resolved-to-Closed DoD evidence - SA-ANA-00X"; body cites not blocked, no dependents blocked, BA-SUB/UX-SUB N/A, BA-ANA Closed verified via get, approval QUESTION Closed verified via list, deliverable finalized) -> update --status Closed --author architect -> verify get shows Closed with allowed_transitions []. Batch efficiencies that are compliant: match the BA counterpart by PARENT FEATURE, not by number (BA-ANA/SA-ANA IDs can be shifted across features: SA-ANA-003<->BA-ANA-004 on FEATURE-003, SA-ANA-004<->BA-ANA-003 on FEATURE-004); verify all approval QUESTIONS with ONE `list --status Closed --type question`; run `workflow transitions sa_subtask_analysis Resolved` ONCE and reuse for the whole batch (skill sanctions run-or-reuse); run up to two ticket-helper operations in parallel (1 op per invocation). Expect occasional transient KeyboardInterrupt on update/get; retry the exact command once per stored rule. Confirmed 2026-08-12 on the full 9-sub-task batch SA-ANA-002..010 (all exit 0; approval QUESTIONS-056..063 and QUESTION-077 Closed; BA-ANA-002..010 all Closed).

## Improvement: create after post-persist abnormal exit duplicates - treat emitted ticket_id as authoritative

Condition:
- When a tracker `create` process exits abnormally (KeyboardInterrupt / Ctrl+C, e.g. Windows STATUS_CONTROL_C_EXIT) AFTER printing the full success YAML that includes `ticket_id`

Action:
- Do NOT retry. The ticket was already persisted; retrying the exact command creates a second identical ticket (confirmed 2026-08-13: SA-DES-004 approval create aborted after persist with exit 1, retry created a duplicate pair QUESTION-089 + QUESTION-090). Treat the emitted `ticket_id` as authoritative proof of success, report the abnormal exit code with that explanation, and verify existence only via a read-only `list`/`get` if needed. If a duplicate still exists, clean it up: mark the non-canonical one `Duplicated` with a RelatesTo link to the canonical ticket plus a reason comment (confirmed: RelatesTo LINK-00760 QUESTION-089->QUESTION-090, comment 20260813-124407-architect, QUESTION-089 Duplicated). This extends the existing 'verify ticket ID when create output omits it' improvement: output WITH ticket_id + abnormal exit = exists, no retry; output WITHOUT ticket_id + clean exit = get to verify.

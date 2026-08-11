# Ticket Helper Improvement Memory

## Improvement: Memory preflight must be first

Condition:
- When a new ticket-helper task arrives

Action:
- Do make the first assistant action and first tool call a single-purpose read of the self-improvement skill and `.ept/self-improvement/ticket-helper.md`; only afterward read role, repository, tracker, or workflow instructions.

## Improvement: Inspect executable queue head

Condition:
- When asked to identify current workflow point from `build-queue all`

Action:
- Do skip monitoring-only Feature/Epic queue containers, then inspect the first executable ticket's full state, direct children, latest blocker/readiness comments, links, current transition, and type DoD; recheck stale comments against current parent and blocker status before naming the next action.

## Improvement: Preserve title-body mismatch

Condition:
- When tracker title and ticket body state different scope or counts

Action:
- Do report both exact values and preserve comments explaining which source is authoritative; don't silently normalize immutable title text.

## Improvement: Recheck DoD after evidence writes

Condition:
- When comments or fields are written to satisfy a status-transition DoD, or when a caller asserts a transition DoD is already met by prior-session evidence

Action:
- Do verify every DoD criterion via CLI — evidence comments, prerequisite ticket terminal statuses, child question checks, blocker links, and same-batch sibling precedent — then run current-status transitions immediately before the status update. For New-to-Open on sub-task types whose DoD lists "Assignee set to creator", when assignee differs from reporter, confirm the assignee-handoff pattern against prior sibling evidence before transitioning; treat a matching precedent as DoD met (confirmed on TESTCASE-022 20260811: assignee qa-engineer, reporter architect, precedent TESTCASE-016).

## Improvement: Validate creator-assignee DoD before create

Condition:
- When creating sub-tasks whose New-to-Open DoD requires assignee to equal creator

Action:
- Do resolve author and requested assignee before creation; if they differ, preflight standard creator handoff: assign reporter for New validation, document New DoD, transition to Open, then assign delivery role. Stop when later type-specific gates, such as CodeReview file and compile checks, are unmet.

## Improvement: Clear resolved outgoing blockers before close

Condition:
- When a resolved prerequisite still has active outgoing Blocks links and its instructions require that it no longer block other tickets before closure

Action:
- Do remove only the verified outgoing blocker links, confirm the prerequisite has no remaining links, recheck every dependent blocker flag and remaining blocker source, then validate the Resolved-to-Closed transition.

## Improvement: Replace full ticket body cleanly

Condition:
- When correcting a ticket description or acceptance criteria with `update --description`

Action:
- Do stage one complete Markdown body in a temporary file, update through `--description-file`, remove the temporary file, then verify the saved body has one Description, Acceptance Criteria, Related Documentation, and Notes structure with no stale placeholders or control characters. Never pass Markdown backticks inline through PowerShell because escape sequences can corrupt identifiers.

## Improvement: Recheck parent contract after child corrections

Condition:
- When child scope is corrected before a parent story transition

Action:
- Do compare the corrected child contract with the parent body and comments; report any stale parent acceptance criterion explicitly instead of assuming comments silently replace it.

## Improvement: Normalize multiline description input

Condition:
- When passing a CLI-retrieved CRLF body back through PowerShell `update --description`

Action:
- Do convert the command argument to LF-only before update, then re-get and verify paragraph and table spacing; raw CRLF input may duplicate blank lines.

## Improvement: Keep commit evidence distinct from test evidence

Condition:
- When In Progress DoD requires code or tests committed but supplied evidence covers only files, compilation, tests, lint, security, or packaging

Action:
- Don't infer commit completion from green technical gates; record the evidence, set time, and keep ticket In Progress until commit evidence is explicit.

## Improvement: Respect type-specific transition states

Condition:
- When a caller requests an intermediate status that is absent from the ticket type's transition map, such as CodeReview In Progress or Resolved

Action:
- Do follow the exact configured path, using Open as active review and Open-to-Closed for approval when configured; require the configured file/line/snippet evidence before approval, then clear only verified review blockers. Report missing states instead of inventing or forcing transitions.

## Improvement: Record canonical quality gates precisely

Condition:
- When QA evidence distinguishes the configured lint or security scope from a broader noncanonical command

Action:
- Do record the configured command scope and its passing result exactly; label broader checks as noncanonical without treating vendored or excluded content as a release defect.

## Improvement: Verify deliverable index separately

Condition:
- When a completion report or other deliverable is committed and the ticket DoD requires `.ept/docs/document_index.md` registration

Action:
- Do verify the index contains the new deliverable link independently of the report commit; record evidence and time but keep the ticket active when the index entry is missing.

## Improvement: Separate referenced paths from inferred paths

Condition:
- When packaging a ticket for another role and the request asks for referenced documentation or SDK paths

Action:
- Do list only paths present in ticket bodies, comments, or linked-ticket context as tracker references; state when no exact SDK path is recorded instead of inferring one from repository naming.

## Improvement: Resolve parent design gates by exact ticket

Condition:
- When Analysis-to-Grooming requires the parent Feature's BA and SA design subtasks to be terminal

Action:
- Do retrieve the exact BA-DES and SA-DES tickets, confirm their configured terminal statuses, and include that evidence in the final DoD recheck before transitioning.

## Improvement: Normalize created child bodies before activation

Condition:
- When `create --description` or `create --description-file` wraps supplied Markdown in the ticket template and leaves duplicate headings or TODO sections

Action:
- Do re-get each new child, replace the full body with one clean Description, Acceptance Criteria, Related Documentation, and Notes structure, verify the saved body has exactly one of each section and no TODO placeholders, then proceed to any Open-to-active transition. Inline `--description` bodies wrap the same as `--description-file`.

## Improvement: Keep QA design behind implementation gate

Condition:
- When a TESTCASE Open-to-In Progress DoD requires accessible, runnable implementation

Action:
- Do verify the scoped source and tests physically exist and the DEV/UNITTEST evidence supports runnable work; if not, record the exact gap and keep TESTCASE Open without treating expected pre-implementation absence as a defect.

## Improvement: Reverse development dependency at review handoff

Condition:
- When a Development ticket reaches Resolved and its instructions require review approval before closure

Action:
- Do remove verified DEV-to-review and DEV-to-test outgoing blockers, preserve bidirectional review relations, then create the configured CodeReview-to-DEV Blocks link and recheck that DEV is Resolved-but-blocked while CodeReview can open.

## Improvement: Preserve QA defect blocker through verification

Condition:
- When a BUG-SUB fix is implemented but the blocked QA execution has not independently verified the original failure

Action:
- Do record commit and regression evidence without removing the BUG-SUB-to-TESTEXEC blocker; report any missing time field or QA evidence separately and keep the defect active until independent QA verifies the original failure. After verification, resolve the defect, remove only its outgoing QA blocker, preserve the parent relation, then close and recheck the downstream ticket.

## Improvement: Full-dev-story grooming batch pattern

Condition:
- When a dev_story Grooming request includes creating all sub-tasks and closing DESIGN, and the caller provides `--description-file` bodies plus a validated link plan

Action:
- Do create DESIGN, DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, and DEVOPS sequentially with per-role `--assignee`/`--addressed-to` and `estimated_hours`; then register Contains + ParentChild for every child, bidirectional RelatesTo and Blocks between CODEREVIEW and DEV, and RelatesTo from CODEREVIEW to the story; then run DESIGN through New→Open→In Progress→Resolved→Closed with evidence comments at each step (validating every transition via `workflow transitions design <status>`); then post story comments (DESIGN sub-task created, Execution plan, Grooming complete) and transition the story Grooming→Development. Confirmed on DEV-STORY-013: sub-tasks DESIGN-013..DEVOPS-013, links LINK-00473..00491, DESIGN comments 20260809-194858/194907/194917, story comments 20260809-195044/195048/195052.

## Improvement: Verify caller-asserted absence of blockers before close

Condition:
- When a caller asserts a Resolved ticket has only non-blocking links (no active is-blocked-by links) and requests a Resolved-to-Closed move

Action:
- Do run `link list <ticket-id>` and confirm the returned links contain no Blocks/blocking inbound entries before executing the status update; don't rely on caller context alone. Pre-verify the move with `workflow transitions <type> Resolved`, execute `update --status Closed`, then re-run `get` to confirm the persisted status is Closed before returning the Result block. If the caller reports an intermediate status absent from the transition map, follow the configured path instead. Confirmed on TESTEXEC-016 close (20260810): link list showed exactly the caller-expected inbound Contains LINK-00546 and ParentChild LINK-00547 from DEV-STORY-016 with no Blocks entries; update --status Closed exited 0 with current_status: Closed; fresh get confirmed persisted status Closed. Also confirmed on DEV-STORY-015 close (20260810): closure batch (resolution=Done field update, evidence comment, Resolved->Closed) executed after link list confirmed 19 links with no Blocks/Question/DependsOn entries; fresh get confirmed status Closed and resolution Done. Reconfirmed on TESTCASE-021 close (20260811): link list showed exactly the caller-expected inbound Contains LINK-00647 and ParentChild LINK-00648 from DEV-STORY-021 with no Blocks entries; workflow transitions testcase Resolved confirmed -> Closed [TERMINAL]; update --status Closed exited 0 with current_status: Closed; fresh get confirmed persisted status Closed. Reconfirmed on DEVOPS-021 close (20260811): link list showed exactly inbound Contains LINK-00651 and ParentChild LINK-00652 from DEV-STORY-021 with no Blocks entries; workflow transitions devops Resolved confirmed -> Closed [T]; update --status Closed exited 0 with current_status: Closed; evidence comment 20260811-034731-devops-engineer confirmed via comment list. Reconfirmed on TESTCASE-022 close (20260811): link list showed exactly the caller-expected inbound Contains LINK-00666 and ParentChild LINK-00667 from DEV-STORY-022 with no Blocks entries; workflow transitions testcase Resolved confirmed -> Closed [TERMINAL]; update --status Closed exited 0 with current_status: Closed; fresh get confirmed persisted status Closed. Reconfirmed on UNITTEST-023 close (20260811): link list showed exactly the caller-expected inbound Contains LINK-00683 and ParentChild LINK-00684 from DEV-STORY-023 with no Blocks entries; workflow transitions unittest Resolved confirmed -> Closed [TERMINAL]; update --status Closed exited 0 with current_status: Closed; fresh get confirmed persisted status Closed with time_spent_hours=12 and closure comment 20260811-042354-python-developer.

## Improvement: Validate update field names against type optional_fields

Condition:
- When an update request specifies a field name absent from the ticket type's optional_fields (e.g. author when only reporter exists)

Action:
- Do run type-info first and abort with corrective action listing valid field names; don't guess the caller intended a different field, and don't execute `update --field <invalid>`.

## Improvement: Multiline comment body via text escapes

Condition:
- When creating or updating a tracker comment whose body is multiline Markdown

Action:
- Do pass the full body inline to `comment create --text` using \n escapes; the CLI decodes them, PowerShell passes \n literally so no corruption occurs; verify with `comment get` afterward. Wrap the whole --text argument in single quotes so Markdown backticks are not interpreted as PowerShell escape characters; confirmed byte-for-byte on 35-line, 40+ line, and 44-line Markdown bodies (TESTCASE-012/013/014), a 12-line Answer comment (QUESTION-037), and a 44-line codereview evidence body (CODEREVIEW-014) and a 15-line execution-plan comment (TESTEXEC-014), and the 37-line gate re-verification comment (TESTCASE-015, comment 20260810-031251), and the 9-line closure comment on TESTEXEC-015 (comment 20260810-044434-qa-engineer, subject 'TESTEXEC-015 closed'), and the 27-line execution-plan comment on TESTEXEC-018 (comment 20260810-133557-qa-engineer, subject 'Test execution plan + implementation-existence gate verified (TESTEXEC-018)'); never omit single quotes around the --text argument. IMPORTANT: when the body contains a literal apostrophe, double it ('' inside the single-quoted argument) so PowerShell does not close the string early — an unescaped apostrophe drops the shell into the '>>' continuation prompt and the command never executes. Confirmed on CODEREVIEW-017 P1 comment (20260810): first attempt with 'operations' dispatch path' stalled at '>>' with no write, then the retry with 'operations'' dispatch path' committed comment 20260810-130004-python-developer byte-for-byte. Reconfirmed on DEV-019/DEV-020 evidence comments (20260810): two 30+ line OWASP self-review bodies committed as 20260810-180549-python-developer and 20260810-180555-python-developer via single-quoted --text with \n escapes and no apostrophe doubling needed. Reconfirmed on UNITTEST-019/UNITTEST-020 results comments (20260810): two multiline Markdown bodies with backticks committed as 20260810-180744-python-developer and 20260810-180750-python-developer via single-quoted --text with \\n escapes; Reconfirmed on UNITTEST-023 (20260811): the 46-check verification comment 20260811-041928-python-developer committed byte-for-byte via single-quoted --text with \n escapes (no apostrophes in body); comment get reconfirmed the full body. both verified byte-for-byte with comment get. Reconfirmed on DESIGN-023 closure comment (20260811): 8-line body committed as 20260811-014226-architect via single-quoted --text with \n escapes (em-dash in subject and body, no backticks, no apostrophes); verified byte-for-byte with comment get. Reconfirmed on TESTCASE-022 implementation-gate comment (20260811): 28-line body with backticks and em-dashes committed as 20260811-022006-qa-engineer via single-quoted --text with \n escapes, no apostrophes so no doubling needed; comment list confirmed the commit.

## Improvement: Verify inline create body fidelity before transition

Condition:
- When a create request passes a full Markdown body inline via --description with backticks and apostrophes, and no transition is requested

Action:
- Do single-quote wrap the --description argument in PowerShell so backticks and apostrophes pass byte-for-byte; re-get the ticket and confirm the stored Description matches the caller body; leave template TODO sections intact until the caller requests activation-time normalization.


## Improvement: Verify field persistence after update

Condition:
- When executing a field-only update via `--field` or a first-class option (`--assignee`, `--priority`) on a ticket

Action:
- Do re-run `get` after the update and confirm the new value appears in the ticket frontmatter before returning the Result block; do not rely on the brief update confirmation line alone. Field-only updates print only a brief confirmation line, so the persisted frontmatter value is the authoritative check for DoD criteria such as "Time reported in subtask frontmatter"; confirmed on UNITTEST-014 time_spent_hours=12 and on CODEREVIEW-017 assignee=tech-lead (20260810): update --assignee tech-lead exited 0 printing only the brief one-line confirmation; fresh get confirmed assignee=tech-lead in frontmatter. Reconfirmed on DEV-023 time_spent_hours=16 (20260811): update --field time_spent_hours=16 exited 0 printing only the brief one-line confirmation; fresh get confirmed time_spent_hours=16 in frontmatter with status still In Progress; the subsequent In Progress -> Resolved transition printed the full YAML status context. Reconfirmed on UNITTEST-023 time_spent_hours=12 (20260811): update --field time_spent_hours=12 exited 0 printing only the brief one-line confirmation; fresh get confirmed time_spent_hours=12 in frontmatter with status still In Progress; the subsequent In Progress -> Resolved transition exited 0 and the fresh get confirmed current_status Resolved with time_spent_hours=12 still in frontmatter.


## Improvement: Retry transient CLI KeyboardInterrupt once

Condition:
- When a tracker CLI command aborts with KeyboardInterrupt during YAML load/import (PyYAML regex compile or scanner), no user input pending, and other CLI commands succeed

Action:
- Do treat it as a transient environment failure, not a validation error; retry the exact same command once, then continue the protocol. Applies to read (get, link list) and write (update --status) commands; confirmed on UNITTEST-014 close, on CODEREVIEW-014 comment get, on CODEREVIEW-014->DEV-014 closure chain link list DEV-014, and on CODEREVIEW-013 update --status Closed (first attempt interrupted during YAML load; retry succeeded), and on TESTEXEC-016 update --field time_spent_hours (first attempt interrupted before any output; single retry succeeded with exit 0), and on TESTEXEC-016 update --status Resolved (preflight workflow transitions + get confirmed the In Progress -> Resolved move was allowed; single update exited 0 without interruption). Confirm the active python interpreter first only if consecutive commands keep failing. Reconfirmed on the DESIGN-022 get (20260810): two consecutive KeyboardInterrupts (first during site-module import, second during YAML safe_load) before the third identical retry returned the full get output with exit 0; retry the exact same read up to three times before suspecting an interpreter issue. Reconfirmed on UNITTEST-019/UNITTEST-020 link list (20260810): each interrupted once during YAML load; single retry succeeded with exit 0. Reconfirmed on DEVOPS-022 comment list (20260811): first attempt aborted KeyboardInterrupt during comments.py utf-8-sig file open; single retry returned all 9 comments with exit 0. Reconfirmed on UNITTEST-023 comment get (20260811): first attempt aborted KeyboardInterrupt during YAML load; single retry returned the full comment body with exit 0.


## Improvement: Never batch tracker CLI commands

Condition:
- When multiple tracker CLI commands (get, list, comment list, link list, workflow transitions, workflow status, type-info) are needed in the same validation step

Action:
- Do run them sequentially, one command per terminal call; never batch two tracker CLI invocations in parallel, whether read or workflow-inspection commands. Parallel calls share one terminal and interleave outputs, which corrupts verbatim output fidelity; re-run any corrupted result sequentially.


## Improvement: Enrich search results with get for type and parent

Condition:
- When a search request report must include type and parent fields that the search output table does not print

Action:
- Do run ``search <query>`` for the match table, then run ``get <ticket-id>`` sequentially for each returned ID to capture type and parent from the Ticket Details block; return the full search output and the ticket type, status, priority, assignee, and parent per match, and say explicitly when no tickets match.

## Improvement: Enrich comment reports with get for full bodies

Condition:
- When a comment report must include full body text that the comment list output table does not print

Action:
- Do run ``comment list <ticket-id>`` for the summary table, then run ``comment get <ticket-id> <comment-id>`` sequentially for each returned comment ID to capture the full body; return the list output and each comment id, author, created, updated, subject, and body verbatim, one command per terminal call. Compare the number of comments fetched with the comment-list count and state explicitly that no comment was omitted (confirmed on DEV-STORY-013: 23 of 23 comments retrieved, DEV-STORY-018: 8 of 8 comments retrieved, and DEV-STORY-017: 8 of 8 comments retrieved (20260810)). Reconfirmed on UNITTEST-023 (20260811): 11 of 11 comments fetched verbatim.

## Improvement: Verify write commit before retrying interrupted commands

Condition:
- When a tracker CLI write command (comment create, update --status) aborts with KeyboardInterrupt (^C) and shows no result output

Action:
- Do verify via a read command (comment list, get) whether the write was committed before retrying; the interrupt can mask a successful write and blind retries create duplicate comments. Confirmed on TESTEXEC-013: two interrupted `comment create` runs both committed, producing duplicate comments 20260810-010207-qa-engineer and 20260810-010214-qa-engineer; no CLI delete-comment command exists to remove the duplicate.


## Improvement: Never batch tracker CLI commands — preflight reads included

Condition:
- When multiple tracker CLI commands (get, list, comment list, link list, workflow transitions, workflow status, type-info) are needed in the same validation step, including preflight reads before the first write

Action:
- Do run them sequentially, one command per terminal call, in every phase of the protocol: preflight validation, DoD checks, and post-write verification. Never batch two tracker CLI invocations in parallel, even when the calls are independent and depend on no prior output. Parallel calls share one terminal and interleave outputs, which corrupts verbatim output fidelity; re-run any corrupted result sequentially. Confirmed on DEV-STORY-015 grooming batch: three parallel preflight reads (get story, workflow transitions, get DESIGN-015) still interleaved their YAML blocks despite each being independent. Reconfirmed on the 8-operation read batch for EPIC-007/DEV-STORY-021/DEV-STORY-022 (20260810): 2 gets + 2 link lists + 2 list --parent + 2 list --parent --status New executed sequentially, one command per terminal call, exit 0, no interleaving.

## Improvement: Quote --field values containing parentheses in PowerShell

Condition:
- When an update request passes an optional field value via --field key=value and that value contains parentheses, commas, or other PowerShell metacharacters (e.g. release_notes with an operation list like (Dataset, Stream, Subscriber))

Action:
- Do single-quote the whole --field key=value argument so PowerShell does not parse parentheses as subexpression syntax; an unquoted value raised ParserError "Missing argument in parameter list" and no write was executed, then the single-quoted retry succeeded. Confirmed on DEV-STORY-016 release_notes update (20260810). This complements the existing --text and --description quoting guidance which does not cover --field values.

## Improvement: Verify create via get when ticket_id omitted

Condition:
- When a multi-step batch creates sub-task tickets and a create output YAML omits the ticket_id line (confirmed for codereview and devops create outputs; their YAML lacks ticket_id while other types include it)

Action:
- Do run a sequential get on the expected ticket id and confirm id, type, title, status, priority, assignee, estimated_hours, and parent before proceeding to the next dependent create step; the get Ticket Details block is the authoritative persistence check, and the caller's multi-step rule requires each step to succeed before the next runs.

## Improvement: Preflight-verify all tickets before link batches

Condition:
- When a multi-step link batch references multiple tickets (e.g. a dev story and its seven sub-tasks)

Action:
- Do run a sequential get on every referenced ticket to confirm id, type, status, and parent before the first link create; then execute each link create one command per terminal call and stop on the first failure. Confirmed on the DEV-STORY-016 19-link batch (LINK-00536..00554): all eight tickets preflight-verified, all links created sequentially with exit code 0.

## Improvement: Don't enrich beyond explicit operation limit

Condition:
- When a caller requests a single operation (e.g. `list`) and explicitly forbids any other operation, but the report must include a field the command output does not print (e.g. parent column absent from the list table); also when a caller enumerates an exact ordered list of read operations (e.g. get, link list, comment list) and requires the raw outputs exactly as printed

Action:
- Do execute exactly the one permitted command (or exactly the enumerated operations, one per terminal call, in order), return their full verbatim outputs, and state explicitly which requested fields are not available from those outputs without extra operations (e.g. `comment list` prints no body text — `comment get` per comment would be needed); don't run additional commands against the caller's constraint and don't infer missing field values from titles or context. Confirmed on DEV-STORY-017 read batch (20260810): get/link list/comment list executed sequentially exit 0; comment text column absent from comment list output; no comment get enrichment run because the caller scoped exactly three operations and required output as printed. Reconfirmed on DEV-017/DEV-018/UNITTEST-017/UNITTEST-018 read batch (20260810): eight sequential read-only commands (4 get + 4 comment list) executed one per terminal call with exit 0; comment list printed no body text and no comment get enrichment was run because the caller scoped exactly eight operations and required outputs verbatim. Reconfirmed on the 9-operation read batch (20260810): 4 gets + workflow types + 2 workflow status + 2 workflow transitions executed one per terminal call, exit 0, no mutation and no enrichment run because the caller enumerated exactly nine read-only operations (get, workflow types, workflow status, workflow transitions) and required outputs verbatim. Reconfirmed on the 8-operation read batch (20260810): 4 gets + 4 link lists executed one per terminal call, exit 0, no mutation and no enrichment run because the caller enumerated exactly eight read-only operations (get, link list) and required outputs verbatim; the get outputs printed ticket bodies in full with no truncation, so no code-block body re-print was needed. Reconfirmed on the 4-get read batch (20260810): 4 gets executed one per terminal call, exit 0, no mutation and no enrichment run because the caller enumerated exactly four read-only operations (get) and required outputs verbatim; the get outputs printed each ticket body in full with no truncation, and the final report reproduced the description bodies verbatim in fenced code blocks. Reconfirmed on the 10-operation read batch (20260810): 6 workflow status + 2 workflow transitions + 2 type-info executed one per terminal call, exit 0, no mutation and no enrichment run because the caller enumerated exactly ten read-only operations (workflow status, workflow transitions, type-info) and required outputs verbatim; workflow status printed the full status detail fields (Description, Stage Goal, Responsible Roles, Allowed Transitions) for each requested status, workflow transitions printed the complete transition table, and type-info printed full YAML including statuses, allowed_transitions, automatic_transitions, and ticket_instructions with transition_dods verbatim.

## Improvement: Confirm large get output via fresh filtered re-run

Condition:
- When a tracker get output is large, the tool saves it to a session-resource file, and that file may hold stale output from an unrelated earlier command

Action:
- Do re-run the same command with a narrow Select-String filter (ticket_id, current_status, status) to capture fresh authoritative values; if the filtered re-run returns empty, run the full command unfiltered. Never paste session-resource file content that contradicts the expected command.

## Improvement: Verify each step and preflight DoD before transition

Condition:
- When a multi-step request sets a field, creates a comment, and transitions status

Action:
- Do validate the workflow transition map and all DoD criteria via CLI (links, comments, question sub-task terminal statuses, time-reported field persistence) before the status write; then verify each write's persistence with a fresh get and report every step's full verbatim output separately, never rolling forward after a failure.


## Improvement: Verify cwd via Get-Location when Set-Location is simplified

Condition:
- When a caller mandates Set-Location to the workspace root inside the same command chain as each tracker CLI call, and the terminal tool echoes a simplified command that omits the leading Set-Location

Action:
- Do confirm the Get-Location output printed by the executed chain reports the workspace root before consuming the CLI result; treat the simplified echo as a display artifact, not a skipped instruction, and never assume cwd correctness without that confirmation line. Reconfirmed on DEV-STORY-018 list (20260810): Get-Location printed E:\learn\GenAI_Foundations_DA\git\foundry_cli and the CLI found 7 child tickets. Reconfirmed on TESTEXEC-017 comment create (20260810): Get-Location printed E:\learn\GenAI_Foundations_DA\git\foundry_cli and the comment create exited 0.


## Improvement: Normalize --field to key=value when caller passes space-separated

Condition:
- When a caller requests a field update with `--field key value` (space-separated) instead of the CLI documented `--field key=value` form

Action:
- Do inspect `update --help` and the `--field` parser (parse_extra_fields requires an `=` separator and raises ValidationError otherwise), then run the write as `--field key=value`; never execute the space-separated form. Confirm persistence with a post-update `get`. Confirmed on TESTCASE-015/016 time_spent_hours=8 (20260810).


## Improvement: Stage inline create bodies when description-file path is unavailable

Condition:
- When a create request supplies a Markdown body inline (no file path) and the caller has not provided a staging file location

Action:
- Do write the exact body to a temp file via a single-quoted PowerShell here-string with LF-only UTF-8 encoding (byte-verified via read_file), then use create --description-file; never point --description-file at a nonexistent guessed path and never pass multiline Markdown inline. Confirmed on QUESTION-038 creation (20260810): first attempt used a nonexistent staged path and exited 4, retry with a temp file succeeded with exit 0. Reconfirmed on QUESTION-039 (20260810): staged body verified byte-perfect via read_file; create exited 0 and get confirmed all fields (id/type/priority/assignee/reporter/parent/addressed_to).

## Improvement: Preflight transition validation via get allowed_transitions for simple status writes

Condition:
- When a request is a two-step comment-create plus single status update, the caller forbids extra tracker commands, and the get status-context block already lists allowed_transitions plus the full target DoD

Action:
- Do run the preflight get once, verify the target status is listed in its allowed_transitions, then proceed directly to comment create and update --status; the get YAML status-context is authoritative and avoids a redundant workflow transitions call when the caller restricts extra operations. Confirm each write's persistence with a fresh get or comment list afterwards. Confirmed on TESTEXEC-015 (20260810): get showed allowed_transitions In Progress; comment create 20260810-042050-qa-engineer exited 0; update --status In Progress exited 0; fresh get and comment list confirmed persistence (5 comments). For a single status write when the caller bans every other tracker command, the update --status output YAML status-context block itself is authoritative persistence proof (current_status shows the target status); do not run a fresh get. Confirmed on TESTEXEC-015 (20260810): update --status Resolved exited 0 with current_status: Resolved in the output.

## Improvement: Field-only update verify when caller bans extra commands

Condition:
- When caller allows exactly two writes (comment create + --field update) and bans every other tracker command, so post-write get persistence verify is impossible

Action:
- Do treat the field-only update confirmation line "Updated ticket: <id>" as authoritative persistence proof, skip get, and state the caller constraint in Result. If first update attempt aborts with KeyboardInterrupt (^C), retry once exact same command per transient-interrupt rule. Confirmed on TESTEXEC-015 (20260810): comment create 20260810-042318-qa-engineer exit 0; update --field time_spent_hours=8 exit 0 (first attempt ^C, retry success).

## Improvement: Abort when comment create lacks required --subject

Condition:
- When a caller requests `comment create <ticket-id> --text <body>` and omits the required `--subject`, while REFERENCE.md and the CLI parser (argument_parser.py `--subject required=True` and comments.py non-empty check) both make the subject mandatory for comment create; also when the same request combines comment create with other tracker writes

Action:
- Do abort per validation protocol before any CLI execution and return an error with reason, description, and corrective action: supply `--subject 'Short summary'`; don't invent a subject from the body, don't run comment create without it, and don't substitute another command. In multi-step requests, validate EVERY step (including the comment's --subject) before executing ANY write; one invalid step aborts the entire request so no earlier step changes ticket state. When the same request also forbids the mandatory preflight reads (workflow transitions / link list DoD verification), report that concern too and keep the ticket state unchanged. Confirmed on TESTEXEC-015 close (20260810): step 1 update --status Closed ran exit 0 before step 2's missing --subject was caught; the terminal status could not be rolled back.

## Improvement: Interpret Blocked flag on Closed siblings during DoD preflight

Condition:
- When preflight-checking a status-transition DoD and a sibling sub-task (e.g. CODEREVIEW) shows Blocked=Yes in `list --parent` output while already Closed

Action:
- Do run `link list` on that sibling and confirm the Blocked flag comes from an inbound Blocks link of an already-terminal ticket (closed DEV); treat it as a terminal-status artifact that does not block the transition DoD; verify no open QUESTION sub-tasks or active blockers exist before executing the status update. Confirmed on DEVOPS-015 Open->In Progress (20260810): CODEREVIEW-015 Blocked=Yes from LINK-00534 (DEV-015 -> CODEREVIEW-015 Blocks) with DEV-015 Closed; DEVOPS-015 transitioned to In Progress with exit 0.





## Improvement: Comment list --author does not filter rows

Condition:
- When a caller requests all comments for a ticket authored by a specific role and the plan uses ``comment list <ticket-id> --author <role>``

Action:
- Do treat ``--author`` on comment list as acting-author annotation, not a filter; the table prints all comments regardless. Enumerate via unfiltered ``comment list``, then filter by the author field in each ``comment get`` output. Confirmed on DEVOPS-016 (20260810): ``comment list DEVOPS-016 --author devops-engineer`` still printed all 11 comments including architect's "Ticket created"; 11 of 11 bodies fetched verbatim, 10 authored by devops-engineer. Reconfirmed on UNITTEST-023 (20260811): ``comment list UNITTEST-023 --author tech-lead`` printed all 11 comments including architect's "Ticket created"; 11 of 11 bodies fetched verbatim.

## Improvement: Link-list confirmation scope for cross-ticket batches

Condition:
- When a caller requests a multi-link batch and confirms it with ``link list <ticket-id>`` where that ticket is not a party to every created link

Action:
- Do report that ``link list <ticket>`` prints only links where that ticket is source or target; cross-links between other batch tickets are absent from that output and need their own ``link list`` on those tickets. Confirm the full batch across the involved tickets. Confirmed on the DEV-STORY-020 19-link batch (20260810): link list DEV-STORY-020 showed 15 of the 19 created links (LINK-00620..00633, 00636); the four CODEREVIEW-020 <-> DEV-020 links (00634, 00635, 00637, 00638) were correctly absent because DEV-STORY-020 is not party to them.

## Improvement: Verify create via get when output is anomalous

Condition:
- When a multi-step batch creates sub-task tickets and a create command stdout is anomalous (omits ticket_id and/or the YAML status-context block, or prints unrelated SDK introspection JSON instead of status context; confirmed for codereview/devops create outputs and for DEVOPS-022 create printing checkpoints/data_health signature JSON on 20260810)

Action:
- Do run a sequential get on the expected ticket id and confirm id, type, title, status, priority, assignee, estimated_hours, and parent before proceeding to the next dependent create step; the get Ticket Details block is the authoritative persistence check, and the caller's multi-step rule requires each step to succeed before the next runs. Don't retry the create blindly on anomalous output.

## Improvement: Link-list confirmation scope for cross-ticket batches (strengthened 20260810)

Condition:
- When a caller requests a multi-link batch and confirms it with ``link list <ticket-id>`` where that ticket is not a party to every created link, and expects the story link count to equal pre-existing + all new links

Action:
- Do report that ``link list <ticket>`` prints only links where that ticket is source or target; cross-links between other batch tickets are absent from that output and need their own ``link list`` on those tickets. Confirm the full batch across the involved tickets. Confirmed on DEV-STORY-020 and reconfirmed on the DEV-STORY-021/022 38-link batch (20260810): each story link list shows 19 links = 4 pre-existing + 15 story-party new links (7 Contains + 7 ParentChild + 1 CODEREVIEW->story RelatesTo); the other 4 cross-links (CODEREVIEW<->DEV RelatesTo bidirectional + DEV->CODEREVIEW Blocks + CODEREVIEW->DEV Blocks) are absent because the story is not party to them. All 38 ``link create`` commands printed "Created link: LINK-xxxxx" with exit 0; transient KeyboardInterrupt on link 7 and link 24 retried once per transient rule and succeeded.

## Improvement: Redirect comment-create output when a long body makes terminal echo unwieldy

Condition:
- When executing a tracker CLI comment create whose --text body is long multiline Markdown (30+ lines) and the PowerShell terminal echo of the full command risks truncating the confirmation line

Action:
- Do append `2>&1 | Out-File -FilePath <log>.log -Encoding utf8; Write-Output "OP_EXIT:$LASTEXITCODE"` to the command so the created-comment confirmation is captured to a file and verified via read_file; the CLI exit code remains authoritative via $LASTEXITCODE. Keep the single-quoted --text argument unchanged. Confirmed on TESTCASE-020 tech-lead approval comments (20260810): op1-comment.log captured `Created comment: 20260810-194021-tech-lead`, op2-comment.log captured `Created comment: 20260810-194028-tech-lead`, both with OP_EXIT:0; comment list and get confirmed persistence and unchanged status.

## Improvement: Confirm verbatim get output capture for single read-only retrieval

Condition:
- When a caller requests exactly one tracker operation (a single get) and the terminal tool returns full inline output without saving to a session-resource file

Action:
- Do paste the complete CLI output verbatim into the Result Output block, including the YAML status-context block, Ticket Details, and content body; don't summarize or omit fields. Confirmed on DEV-STORY-019 get (20260810): exit 0, full output captured inline with no session-resource file.

## Improvement: Question create does not auto-link

Condition:
- When a create question request supplies --parent and the caller expects auto-created Blocks/Question links on creation

Action:
- Do report that create question --parent registers no links (link list returns 0 on the new ticket); the Blocks link must be created explicitly via link create <question> <parent> Blocks per the question Open instructions; the parent stays non-Blocked until that link exists and AT-4 (child_blocker_created) fires. Confirm with link list and get <parent>. Confirmed on QUESTION-042 (20260810): link list QUESTION-042 printed 0 links and get DEV-022 stayed New.

## Improvement: Follow allowed path for blocked question transitions

Condition:
- When a caller requests a question status sequence that includes a status not reachable from the current status (e.g. New to In Progress when the question transition map only allows New to [Open, Blocked, Canceled, Rejected, Duplicated]), and also supplies a --field resolution value on a type whose optional_fields do not include resolution

Action:
- Do preflight `workflow transitions question` and `type-info question`; on the direct New-to-In-Progress failure (ValidationError 2 naming allowed statuses), execute the allowed path New to Open to In Progress sequentially and report the exact error verbatim; use a single `--status Closed` to reach the terminal status and state that resolution is not an optional field of type question; remove each Blocks link in its own `link remove` call, then verify final state with get + link list on every ticket, one command per terminal call. Confirmed on the QUESTION-043 close batch (20260811): direct New->In Progress exited 1 with ValidationError [2]; allowed path exited 0 at each step; link remove LINK-00677 and LINK-00678 both exited 0; final get/link list confirmed QUESTION-043 Closed with 0 links and DEV-022/UNITTEST-022 New with no inbound Blocks.
## Improvement: Note addressed_to outside question type

Condition:
- When a create request passes --addressed-to for a type whose optional_fields exclude addressed_to (e.g. testcase, testexec) and the caller bans post-create verification commands

Action:
- Do note in the Result that addressed_to is documented as a question-type field and absent from the type optional_fields, and that persistence was not verified because the caller constrained operations to the single create; don't claim the value persisted in frontmatter. Create exit 0 only confirms the CLI accepted the argument.
## Improvement: Note addressed_to outside question type (reconfirmed DEVOPS-023)

Condition:
- When a create request passes --addressed-to for a type whose optional_fields exclude addressed_to (e.g. testcase, devops) and the caller constrains operations to the single create

Action:
- Do note in the Result that addressed_to is documented as a question-type field and absent from the type optional_fields, and that persistence was not verified because the caller constrained operations to the single create; don't claim the value persisted in frontmatter. Create exit 0 only confirms the CLI accepted the argument. Reconfirmed on DEVOPS-023 (20260811): devops optional_fields [priority, resolution, assignee, reporter, component, labels, estimated_hours, time_spent_hours, due_date] exclude addressed_to; the create --addressed-to devops-engineer exited 0. Note also that this devops create output DID include ticket_id (DEVOPS-023), so ticket_id omission is not universal for devops creates — check the actual output before deciding a get is needed.

## Improvement: Confirm large get output via fresh filtered re-run

Condition:
- When a tracker get output is large, the tool saves it to a session-resource file, and that file may hold stale output from an unrelated earlier command

Action:
- Do re-run the same command with a narrow Select-String filter (ticket_id, current_status, status) to capture fresh authoritative values; if the filtered re-run returns empty, run the full command unfiltered. Never paste session-resource file content that contradicts the expected command. When the tool returns a unique per-call path (call_00_<session-token>_...) written by the just-executed command, read it via read_file and paste the content verbatim — that file is fresh and authoritative, so no filtered re-run is needed. Confirmed on type-info development (20260811): 10KB output saved to a unique call_00_ path in the same tool result, read verbatim with no re-run.


## Improvement: Redirect comment-create output for long bodies - verify commit before retry

Condition:
- When a comment create with a long multiline --text body is redirected to a log file (Out-File) and the run is interrupted (^C) before the confirmation line prints

Action:
- Do first check the log file and run comment list/get on the target ticket to confirm whether the write committed; only retry if no comment with the exact subject exists. The interrupt can mask a successful write; a blind retry duplicates the comment. Confirmed on UNITTEST-022 (20260811): the interrupted create had committed comment 20260811-022140-python-developer and the log file already held the confirmation line.


## Improvement: Invoke tracker CLI via venv python, never bare python

Condition:
- When running tracker CLI commands and bare `python` resolves to a system interpreter (e.g. D:\app\Python\python.exe) instead of the project venv, or when capturing tracker CLI output to a log file with `2>&1 | Out-File` and the command invokes the CLI through the call operator (`& "path\tracker_cli.py"`)

Action:
- Do invoke through the venv python executable (`& ".venv\Scripts\python.exe" ".ept\skills\tracking-system\tracker\tracker_cli.py"`) when piping to Out-File; PowerShell raises InvalidOperation "Cannot run a document in the middle of a pipeline" for `& script.py | Out-File`. Confirmed on TESTCASE-021 get (20260811): call-operator pipeline failed; python-interpreter redirect captured full get output with GET_EXIT:0. Reconfirmed on link list DEV-023 (20260811): bare python first attempt aborted with KeyboardInterrupt inside yaml.safe_load (system D:\app\Python), retry with `.venv\Scripts\python.exe` succeeded exit 0; full-link-list output then captured verbatim via `*> link-list-DEV-023.log` + read_file when the shared terminal returned a stale scrollback fragment (type-info dev_story echo) instead of the fresh command result.

## Improvement: Split update-with-comment request into two CLI ops

Condition:
- When caller asks `update <id> --status <s> --subject <t> --text <b>` (mixes a status transition with comment subject/body in one update call)

Action:
- Do preflight `update --help` first; run the status transition with `update --status` alone, then post the exact subject/body via `comment create`; never pass `--subject`/`--text` to `update` (exit 1 unrecognized arguments). Confirmed on TESTCASE-022 gate (20260811): split into `update --status "In Progress"` plus `comment create` 20260811-025129-tech-lead.

## Improvement: Set resolution via --field resolution=Done

Condition:
- When caller requests `update <id> --status Closed --resolution Done` but the `update` CLI exposes no `--resolution` option

Action:
- Do set `--field resolution=Done` after confirming `resolution` is listed in the type optional_fields (codereview/development/testcase all include it); verify persistence with a fresh `get` showing `resolution: Done` in Ticket Details. Confirmed on CODEREVIEW-022 and DEV-022 close (20260811).


## Improvement: Approval-gate evidence may live on TESTCASE sibling

Condition:
- When preflight-verifying a TESTEXEC In Progress->Resolved move whose DoD requires approval comments, and the caller states approval comments exist

Action:
- Do locate approval comments on the paired TESTCASE sibling ticket (tech-lead "Tech lead approval — TESTCASE-xxx" and "Approval gate for TESTEXEC-xxx: PASS"), not on the TESTEXEC itself; verify via comment list on the TESTCASE before the status write. Confirmed on TESTEXEC-021/022 (20260811): both approval comments found on TESTCASE-021/022; both Resolved transitions exited 0 and fresh gets confirmed status Resolved with time_spent_hours=8 in frontmatter.

## Improvement: Verify caller-asserted absence of blockers before close (reconfirmed TESTEXEC-021/022)

Condition:
- When a caller asserts Resolved TESTEXEC tickets have only non-blocking links and requests Resolved->Closed moves

Action:
- Do preflight link list on each ticket (confirm only Contains/ParentChild inbound, no Blocks entries), reuse the get allowed_transitions (Closed listed), post closure evidence comment via single-quoted --text with \n escapes, update --status Closed, then fresh filtered get confirming current_status: Closed and time_spent_hours=8 before moving to the next ticket. Confirmed on TESTEXEC-021/022 (20260811): comments 20260811-031517-qa-engineer and 20260811-031530-qa-engineer, both updates exited 0, both fresh gets confirmed Closed with time_spent_hours=8.

## Improvement: Delegate New-to-Open DoD assignee-creator check to sibling precedent

Condition:
- When a New-to-Open devops sub-task (or other creator-assignee DoD type) shows assignee differing from reporter and the caller records that evidence in a pre-transition comment

Action:
- Do rely on the caller-asserted assignee-handoff evidence plus a prior-sibling (Closed devops ticket) precedent instead of aborting; confirm no Question sub-tasks/blocks exist via link list, then run workflow transitions, comment create, and update --status Open. Confirmed on DEVOPS-021/DEVOPS-022 (20260811): assignee devops-engineer, reporter architect; prior sibling DEVOPS-020 (Closed, same handoff) served as precedent; transitions exited 0.

## Improvement: Don't depend on type-info when get already carries New DoD

Condition:
- When preflight-verifying a sub-task New-to-Open DoD and `type-info <type>` repeatedly aborts with KeyboardInterrupt during YAML safe_load (two consecutive attempts), while the ticket's own `get` status-context block already lists the full New-status DoD criteria and allowed_transitions

Action:
- Do reuse the `get` YAML status-context as the authoritative DoD source, pre-verify the move with `workflow transitions <type> New`, and confirm the assignee-handoff precedent against a prior sibling that has already completed the lifecycle (e.g. DEVOPS-016 Closed) rather than a sibling still in New (DEVOPS-021). Don't block the preflight on type-info when its content is already present in the get output. Confirmed on DEVOPS-022 New->Open (20260811): type-info devops interrupted twice; get DEVOPS-022 + workflow transitions devops New + get DEVOPS-016/DEVOPS-021 precedent fully satisfied the DoD; comment create 20260811-032402-devops-engineer and update --status Open exited 0.
## Improvement: Verify write commit before retrying interrupted commands (strengthened 20260811)

Condition:
- When a tracker CLI write command (update --status) aborts with KeyboardInterrupt (^C) during automatic-transition evaluation (evaluate_automatic_transitions) after the ticket status was already written, and no result output is shown

Action:
- Do run a read (get) first to check whether the status was persisted before retrying; the ticket write commits before auto-transition evaluation, so the ticket can show the new status even though the command exited 1 with a traceback. Retry only if the read shows the target status was NOT persisted. Confirmed on TESTCASE-021 In Progress->Resolved (20260811): attempt 1 interrupted during YAML load (get showed In Progress, retried); attempt 2 interrupted during evaluate_automatic_transitions after commit (fresh get showed current_status: Resolved); no further retry and no duplicate write.

## Improvement: Re-pin cwd when tracker commands report false "Ticket not found"

Condition:
- When the persistent terminal cwd drifts away from the workspace root (e.g. to a candidate copy folder or a smoke-empty temp folder) mid-session and tracker CLI commands that resolve tickets by top-level path (update, comment get, list --parent) report ValidationError [2] "Ticket <id> not found" even though get from the root succeeds, or a tracker CLI invocation using a RELATIVE script path fails with Python "can't open file '<drifted-cwd>\.ept\skills\tracking-system\tracker\tracker_cli.py': No such file or directory" exit 1

Action:
- Do re-pin Set-Location to the workspace root and confirm Get-Location before consuming CLI results; use the ABSOLUTE script path (e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\skills\tracking-system\tracker\tracker_cli.py) inside the same command chain so a drifted terminal cwd cannot redirect the script lookup, and pin the working directory for every tracker command rather than once per session. Chained commands in one terminal call inherit the drifted cwd; read (get) resolves the nested full path while the drifted copy's index lacks the ticket, causing the misleading "not found" on update/comment get. Confirmed on TESTCASE-021 transition (20260811): terminal cwd had drifted to T:\tmp\foundry-devops021-022-20260811\candidate; update TESTCASE-021 --status Resolved returned ValidationError [2] Ticket TESTCASE-021 not found; re-pinning to E:\learn\GenAI_Foundations_DA\git\foundry_cli and re-running the same update progressed into handle_update. Reconfirmed on TESTCASE-022 comment create (20260811): first attempt used the relative script path and the terminal cwd had drifted to T:\tmp\foundry-devops021-022-20260811\smoke-empty, so python failed with "can't open file '<drifted-cwd>\.ept\skills\tracking-system\tracker\tracker_cli.py'"; the retry pinned Set-Location to E:\learn\GenAI_Foundations_DA\git\foundry_cli and used the absolute script path, created comment 20260811-034113-qa-engineer with exit 0.

## Improvement: Verify caller-asserted current status before update --status

Condition:
- When a caller requests an `update --status` transition and asserts a current status (e.g. Open) that may differ from the ticket's actual status

Action:
- Do run `workflow transitions <type> "<asserted-status>"` as preflight, then attempt the update; when the CLI rejects it with a ValidationError naming a different status (including a terminal one), do not retry or override — run `get <ticket-id>` to confirm the real persisted current_status and report the caller's assertion mismatch as the reason. Don't rely on caller context alone for status. Confirmed on EPIC-007 (20260811): caller asserted Open, update exited 2 with "Invalid status transition for 'epic': 'Done' -> 'In Progress'. 'Done' is a terminal status and cannot be transitioned"; fresh get confirmed current_status: Done, status_description "All linked Developer Stories Closed; deployed.", type epic.
## Improvement: CODEREVIEW approval closure chain

Condition:
- When a caller requests the full review-approval closure: close a CODEREVIEW ticket after approval, remove its inbound Blocks link to the DEV sub-task, and close the Resolved DEV sub-task

Action:
- Do preflight the CODEREVIEW approval evidence comment (specific files/lines cited + decision made) and verify Open->Closed is allowed; run `link remove` on the inbound Blocks link; close CODEREVIEW; then run `link list DEV` to confirm no is-blocked-by rows remain (only expected Contains/ParentChild/RelatesTo/outbound Blocks); post the closure comment with \n escapes; set resolution via `--field resolution=Done` after confirming it is in the development optional_fields; run `update --status Closed`; confirm persistence with a fresh get showing current_status Closed and resolution Done. Confirmed on CODEREVIEW-023/DEV-023 (20260811): LINK-00697 removed exit 0, CODEREVIEW-023 Open->Closed exit 0 (evidence comment 20260811-044953-tech-lead), link list DEV-023 showed exactly 5 links (00681/00682 Contains+ParentChild, 00693/00694 RelatesTo, 00696 outbound Blocks) with no inbound Blocks, closure comment 20260811-045630-tech-lead, resolution=Done update exit 0, DEV-023 Resolved->Closed exit 0, fresh get confirmed Closed with resolution Done.

## Improvement: Verify before retry on interrupted terminal output

Condition:
- When a sync tracker write returns no output and a ^C/interrupt marker, or when a retry could duplicate a possibly-committed mutation

Action:
- Do run a read-only verification (comment list / get) before any retry; if the target comment or write already exists, treat the operation as committed (exit 0) and do not re-execute. Don't assume ^C means the command never ran. Confirmed on TESTCASE-023 (20260811): Operation 2 comment create printed no output with a ^C marker, but comment list showed 20260811-054233-tech-lead already committed; comment get confirmed a byte-identical body.

## Improvement: Epic closure batch - set resolution before AT-1 auto-transitions (confirmed EPIC-006)

Condition:
- When closing an epic whose linked Dev Stories are all terminal and AT-1 auto-transitions (all_children_reach_status In Progress->Resolved, Resolved->Done) may fire instantly after any update

Action:
- Do set resolution first via `update --field resolution=Done` (validate against epic optional_fields via type-info), post the verification comment, then `update --status Resolved`; re-run get and accept the auto-fired terminal status without attempting a further transition (Done is terminal and rejects it). Verify both comments byte-for-byte via comment get. Confirmed on EPIC-006 (20260811): resolution=Done update exited 0, verification comment 20260811-094111-architect, Resolved transition exited 0, fresh get showed current_status Done with resolution Done in Ticket Details (AT-1 fired), closure comment 20260811-094121-architect, no manual Done transition attempted.

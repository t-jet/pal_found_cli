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
- Do verify every DoD criterion via CLI — evidence comments, prerequisite ticket terminal statuses, child question checks, blocker links, and same-batch sibling precedent — then run current-status transitions immediately before the status update.

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
- Do run `link list <ticket-id>` and confirm the returned links contain no Blocks/blocking inbound entries before executing the status update; don't rely on caller context alone. Pre-verify the move with `workflow transitions <type> Resolved`, execute `update --status Closed`, then re-run `get` to confirm the persisted status is Closed before returning the Result block. If the caller reports an intermediate status absent from the transition map, follow the configured path instead. Confirmed on TESTEXEC-016 close (20260810): link list showed exactly the caller-expected inbound Contains LINK-00546 and ParentChild LINK-00547 from DEV-STORY-016 with no Blocks entries; update --status Closed exited 0 with current_status: Closed; fresh get confirmed persisted status Closed. Also confirmed on DEV-STORY-015 close (20260810): closure batch (resolution=Done field update, evidence comment, Resolved->Closed) executed after link list confirmed 19 links with no Blocks/Question/DependsOn entries; fresh get confirmed status Closed and resolution Done.

## Improvement: Validate update field names against type optional_fields

Condition:
- When an update request specifies a field name absent from the ticket type's optional_fields (e.g. author when only reporter exists)

Action:
- Do run type-info first and abort with corrective action listing valid field names; don't guess the caller intended a different field, and don't execute `update --field <invalid>`.

## Improvement: Multiline comment body via text escapes

Condition:
- When creating or updating a tracker comment whose body is multiline Markdown

Action:
- Do pass the full body inline to `comment create --text` using \n escapes; the CLI decodes them, PowerShell passes \n literally so no corruption occurs; verify with `comment get` afterward. Wrap the whole --text argument in single quotes so Markdown backticks are not interpreted as PowerShell escape characters; confirmed byte-for-byte on 35-line, 40+ line, and 44-line Markdown bodies (TESTCASE-012/013/014), a 12-line Answer comment (QUESTION-037), and a 44-line codereview evidence body (CODEREVIEW-014) and a 15-line execution-plan comment (TESTEXEC-014), and the 37-line gate re-verification comment (TESTCASE-015, comment 20260810-031251), and the 9-line closure comment on TESTEXEC-015 (comment 20260810-044434-qa-engineer, subject 'TESTEXEC-015 closed'), and the 27-line execution-plan comment on TESTEXEC-018 (comment 20260810-133557-qa-engineer, subject 'Test execution plan + implementation-existence gate verified (TESTEXEC-018)'); never omit single quotes around the --text argument. IMPORTANT: when the body contains a literal apostrophe, double it ('' inside the single-quoted argument) so PowerShell does not close the string early — an unescaped apostrophe drops the shell into the '>>' continuation prompt and the command never executes. Confirmed on CODEREVIEW-017 P1 comment (20260810): first attempt with 'operations' dispatch path' stalled at '>>' with no write, then the retry with 'operations'' dispatch path' committed comment 20260810-130004-python-developer byte-for-byte.

## Improvement: Verify inline create body fidelity before transition

Condition:
- When a create request passes a full Markdown body inline via --description with backticks and apostrophes, and no transition is requested

Action:
- Do single-quote wrap the --description argument in PowerShell so backticks and apostrophes pass byte-for-byte; re-get the ticket and confirm the stored Description matches the caller body; leave template TODO sections intact until the caller requests activation-time normalization.


## Improvement: Verify field persistence after update

Condition:
- When executing a field-only update via `--field` or a first-class option (`--assignee`, `--priority`) on a ticket

Action:
- Do re-run `get` after the update and confirm the new value appears in the ticket frontmatter before returning the Result block; do not rely on the brief update confirmation line alone. Field-only updates print only a brief confirmation line, so the persisted frontmatter value is the authoritative check for DoD criteria such as "Time reported in subtask frontmatter"; confirmed on UNITTEST-014 time_spent_hours=12 and on CODEREVIEW-017 assignee=tech-lead (20260810): update --assignee tech-lead exited 0 printing only the brief one-line confirmation; fresh get confirmed assignee=tech-lead in frontmatter.


## Improvement: Retry transient CLI KeyboardInterrupt once

Condition:
- When a tracker CLI command aborts with KeyboardInterrupt during YAML load/import (PyYAML regex compile or scanner), no user input pending, and other CLI commands succeed

Action:
- Do treat it as a transient environment failure, not a validation error; retry the exact same command once, then continue the protocol. Applies to read (get, link list) and write (update --status) commands; confirmed on UNITTEST-014 close, on CODEREVIEW-014 comment get, on CODEREVIEW-014->DEV-014 closure chain link list DEV-014, and on CODEREVIEW-013 update --status Closed (first attempt interrupted during YAML load; retry succeeded), and on TESTEXEC-016 update --field time_spent_hours (first attempt interrupted before any output; single retry succeeded with exit 0), and on TESTEXEC-016 update --status Resolved (preflight workflow transitions + get confirmed the In Progress -> Resolved move was allowed; single update exited 0 without interruption). Confirm the active python interpreter first only if consecutive commands keep failing.


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
- Do run ``comment list <ticket-id>`` for the summary table, then run ``comment get <ticket-id> <comment-id>`` sequentially for each returned comment ID to capture the full body; return the list output and each comment id, author, created, updated, subject, and body verbatim, one command per terminal call. Compare the number of comments fetched with the comment-list count and state explicitly that no comment was omitted (confirmed on DEV-STORY-013: 23 of 23 comments retrieved, DEV-STORY-018: 8 of 8 comments retrieved, and DEV-STORY-017: 8 of 8 comments retrieved (20260810)).

## Improvement: Verify write commit before retrying interrupted commands

Condition:
- When a tracker CLI write command (comment create, update --status) aborts with KeyboardInterrupt (^C) and shows no result output

Action:
- Do verify via a read command (comment list, get) whether the write was committed before retrying; the interrupt can mask a successful write and blind retries create duplicate comments. Confirmed on TESTEXEC-013: two interrupted `comment create` runs both committed, producing duplicate comments 20260810-010207-qa-engineer and 20260810-010214-qa-engineer; no CLI delete-comment command exists to remove the duplicate.


## Improvement: Never batch tracker CLI commands — preflight reads included

Condition:
- When multiple tracker CLI commands (get, list, comment list, link list, workflow transitions, workflow status, type-info) are needed in the same validation step, including preflight reads before the first write

Action:
- Do run them sequentially, one command per terminal call, in every phase of the protocol: preflight validation, DoD checks, and post-write verification. Never batch two tracker CLI invocations in parallel, even when the calls are independent and depend on no prior output. Parallel calls share one terminal and interleave outputs, which corrupts verbatim output fidelity; re-run any corrupted result sequentially. Confirmed on DEV-STORY-015 grooming batch: three parallel preflight reads (get story, workflow transitions, get DESIGN-015) still interleaved their YAML blocks despite each being independent.

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
- Do treat ``--author`` on comment list as acting-author annotation, not a filter; the table prints all comments regardless. Enumerate via unfiltered ``comment list``, then filter by the author field in each ``comment get`` output. Confirmed on DEVOPS-016 (20260810): ``comment list DEVOPS-016 --author devops-engineer`` still printed all 11 comments including architect's "Ticket created"; 11 of 11 bodies fetched verbatim, 10 authored by devops-engineer.

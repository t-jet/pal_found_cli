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
- When comments or fields are written to satisfy a status-transition DoD

Action:
- Do re-get ticket, verify evidence comment and prerequisite tickets, check child questions and blocker links, then run current-status transitions immediately before status update.

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
- When `create --description` wraps supplied Markdown in the ticket template and leaves duplicate headings or TODO sections

Action:
- Do re-get each new child, replace the full body with one clean Description, Acceptance Criteria, Related Documentation, and Notes structure, and verify it before any Open-to-active transition.

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

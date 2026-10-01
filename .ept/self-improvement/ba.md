# BA Improvement Memory

Improvement entries recorded after task completion.

## Improvement: compact prompts for batch comment creation; retry provider 400 with trimmed body

Condition:

- When delegating a batch of evidence/DoD comments to the ticket-helper subagent and a subagent invocation returns a provider error (`400 invalid_request_error`, no CLI output)

Action:

- Do retry the failed invocation once with a compacted prompt: shorter body, plain hyphens instead of em dashes, minimal markdown
- Do keep the per-ticket evidence table but trim evidence wording to the minimum that stays concrete (IDs, line counts, statuses)
- Do not change the tracker command itself; only the prompt payload
- Do record the retry and its outcome in the final report (observed 2026-08-12: BA-ANA-005 evidence comment succeeded on second retry after two provider 400s; same day 9 cross-review comments with em-dash subjects and short bodies all succeeded first try — the failure driver was body length, not the em dash character; keep bodies short)
- Reconfirmed 2026-08-13 while closing BA-DES-002..011: provider 400s hit single calls too (BA-DES-011 get, SA-DES-005/006 get pair, BA-DES-007 comment create), each fixed by one compact retry. When BOTH calls in a parallel pair return 400, retry them ONE at a time (sequential), not as a new pair — parallel pairs keep tripping the provider

## Improvement: resolve BA/SA analysis mutual closure when SA is Resolved

Condition:

- When closing the BA-ANA + SA-ANA pair for a FEATURE Analysis→In Design transition, and SA-ANA is already Resolved while BA-ANA is at In Progress

Action:

- Do advance BA-ANA In Progress→Resolved→Closed first: SA-ANA at Resolved satisfies BA-ANA's "SA Analysis Sub-Task in In Progress or later" Resolved DoD; BA-ANA Closed then satisfies SA-ANA's Resolved→Closed "BA-ANA terminal" DoD
- Do attempt `update SA-ANA-XXX --status Closed --author ba` for the SA-ANA Close — the CLI permits a non-creator role author to transition SA sub-task status when all DoD dependencies are met (verified exit 0, 2026-09-30)
- Do create BA-DES + SA-DES under the FEATURE then set both design sub-tasks New→Open before advancing FEATURE Analysis→In Design
- Do confirm the EPIC FeatureContains link (e.g. LINK-01052) is present before advancing the Feature

## Improvement: hold BA-ANA at In Progress until SA-ANA counterpart reaches In Progress

Condition:

- When BA-ANA In Progress→Resolved DoD requires the SA-ANA counterpart to be at least In Progress, and SA-ANA is still New after repeated polls (verified via `list --type sa_subtask_analysis`)

Action:

- Do NOT transition BA-ANA to Resolved while SA-ANA is New; the DoD criterion is explicitly unmet
- Do create one QUESTION ticket per BA-ANA addressed to architect (addressed_to=architect, parent=BA-ANA, priority High, assignee ba, author ba) noting the specific SA-ANA dependency, then leave BA-ANA at In Progress
- Do report in the final report that BA-ANA await SA-ANA progression; do not fabricate Resolved status

## Improvement: treat transient KeyboardInterrupt at CLI startup as infra retry, not tracker failure

Condition:

- When a tracker CLI command exits 1 with `KeyboardInterrupt` during Python startup/config parse (before any mutation), on an otherwise-identical command that previously exited 0

Action:

- Do retry the exact same command once in a fresh invocation; do not inspect .ept/tracker internals; do not treat the failed attempt as a tracker defect
- Do record the retry and its outcome in the final report (observed 2026-08-12: FEATURE-007 Open→Analysis succeeded on retry)

## Improvement: self-improvement read must come first

Condition:

- When starting any incoming task as BA agent, including when the role file (ticket-helper.md) itself mandates the memory read and when the mode wrapper says to load the role file before anything else

Action:

- Do make the first tool call a single-purpose read of .ept/self-improvement/ba.md (self-improvement skill + memory) only — no role file, skill-index, caveman, humanizer, or any other read before or alongside it
- Do not batch or delay the memory read even when the role instructions or the mode wrapper repeat the same requirement
- Do read ticket-helper.md and skill-index.md only after the memory read completes

## Improvement: verify tracker state before DoD documentation

Condition:

- When a request describes ticket statuses that may be stale (e.g. "all at New") or asks to document DoD evidence for transitions

Action:

- Do `get` each ticket first; compare stated status to actual status; record discrepancies honestly in comments and in the final report; never fabricate evidence for a status the tracker does not show

## Improvement: collect concrete evidence before writing DoD comments

Condition:

- When creating DoD evidence comments for a batch of tickets

Action:

- Do gather per-ticket `get`, `link list`, `comment list`, and `list --parent` before commenting; cite concrete IDs (links, comment IDs, child counts) in the evidence table; mark a criterion NOT MET (with reason) when evidence cannot be produced

## Improvement: respect subagent and operation limits

Condition:

- When delegating tracker operations to the ticket-helper subagent

Action:

- Do run one operation per invocation and at most 2 subagent invocations in parallel; instruct each spawned subagent to follow the same rule

## Improvement: stage long ticket descriptions via .ept/tmp description-file

Condition:

- When creating a ticket whose description is long or multi-line markdown

Action:

- Do write description text verbatim to a temp file under `.ept/tmp` and pass `--description-file <path>` to `create`; don't inline large markdown bodies through shell quoting

## Improvement: skip post-write verification when caller scopes one operation

Condition:

- When caller scopes exactly one tracker operation (e.g. "perform ONE operation only", "do not run any additional operations")

Action:

- Do run only the requested operation and stop; skip get/comment-get/list verification the caller did not request
- Do report the single command's verbatim output and exit code; no extra CLI calls
- Do capture the authoritative exit code via `$LASTEXITCODE` in the persistent terminal after the command and include it in the report; a successful `update --field` prints `Updated ticket: <id>` and exits 0

## Improvement: long comment bodies via quoted variable with \n escapes

Condition:

- When creating a comment whose body is long or multi-line via `comment create --text` in PowerShell

Action:

- Do build the full body in a single-quoted PowerShell variable using literal `\n` escape sequences (no raw newlines, no here-strings) and pass it as `--text <var>`; avoids shell quoting issues with embedded double quotes
- Do remember `comment create` has no `--text-file` option; `--description-file` exists only for `create`/`update`
- Do escape apostrophes as `''` inside the single-quoted variable and keep the full body in the variable; inline single-quoted `--text '...'` breaks with an argparse unrecognized-arguments error (exit 1) when the body contains an apostrophe

## Improvement: verify every evidence-comment update persists

Condition:

- When correcting/updating tracker evidence comments in a batch

Action:

- Do run `comment get <ticket> <comment-id>` per comment after each `comment update` and confirm subject + text persisted before reporting success
- Do retry failed updates immediately; transient infra errors (e.g. "Response contained no choices") need one retry before flagging failure
- Do record the retry and its outcome in the final report
- Do not report "corrected" for a comment whose `comment get` was not run or did not show the new subject

## Improvement: verify parent restore after closing blocking QUESTION

Condition:

- When closing blocking QUESTION tickets whose Resolved→Closed DoD requires removing the Blocks link, and relying on AT-6 auto-restore or AT-5 all-blockers-cleared

Action:

- Do `get <parent>` after the questions close; NEITHER AT-6 (`this_ticket_reaches_status`) NOR AT-5 (`all_blockers_cleared`) is reliable — observed 2026-08-11 (QUESTION-044..047: four parents stayed `Blocked`) and again 2026-08-12 (BA-ANA-010 stayed `Blocked` after all four Blocks links LINK-00713..00716 removed and QUESTION-072..075 Closed)
- Do restore each parent manually per its Blocked-status instruction "IF all blocking links removed THEN return this ticket to prior status": `update <parent> --status <prior> --author ba` (prior status from history; BA-ANA-010 prior = In Progress), verify exit 0 and `get` shows prior status; confirm `link list <parent>` shows zero links
- Do run `reconcile-index` (check mode) to confirm no frontmatter/index drift before reporting parent status

## Improvement: derive SA-ANA counterpart from dependency QUESTION titles, not ticket number

Condition:

- When closing BA-ANA sub-tasks and needing the SA-ANA counterpart status for the Resolved-to-Closed DoD evidence comment

Action:

- Do map the counterpart from the dependency QUESTION titles (QUESTION-048..055 pattern "SA-ANA-XXX dependency for BA-ANA-YYY resolution"), not from equal ticket numbers — BA-ANA-003 <-> SA-ANA-004 and BA-ANA-004 <-> SA-ANA-003 are crossed because feature numbering differs (BA-ANA-003 lives under FEATURE-004, BA-ANA-004 under FEATURE-003). Reconfirmed 2026-08-12 while closing BA-ANA-002..010: all 9 counterpart pairs verified by title/parent match.
- Do confirm the match by comparing parent and title of the SA-ANA get output with the BA-ANA being closed.

## Improvement: task (top-level) type rejects time_spent_hours; record time in comments

Condition:

- When a caller asks to report time via time_spent_hours on a `task` (top-level) ticket, or any top-level ticket type

Action:

- Do attempt the `update --field time_spent_hours=...` exactly once, expect `ValidationError [2]: Field(s) not allowed for type 'task': time_spent_hours` (optional_fields for task are only parent, component, labels, due_date), do NOT retry, and record the rejection verbatim in the ticket comment and final report with the work time stated there instead
- Do note workflow rule 9 limits time reporting to sub-task types; top-level types (task, feature, epic, dev_story) have no time field. Observed 2026-08-12 on TASK-003 closure.

## Improvement: use exact user-mandated subject strings verbatim (em dash fidelity)

Condition:

- When the user specifies an exact comment subject format (e.g. `"In Progress->Resolved DoD evidence — <BA-DES-XXX> (2026-08-13)"`) for DoD evidence comments

Action:

- Do pass the subject string verbatim including the em dash character; em-dash subjects are safe when bodies stay compact (reinforced 2026-08-13: 9/9 BA-DES DoD evidence comments created, all exit 0; the 2026-08-12 provider-400 failures were body-length driven, NOT the em dash character — a compact body with em-dash subject succeeds first try). Do NOT substitute a plain hyphen for the mandated em dash: I repeated this deviation on 2026-08-13 (9 BA-DES comments) after doing the same on 2026-08-12 (FEATURE Analysis->In Design comments). If a hyphen was used anyway, flag the deviation in the final report and offer to correct.

## Improvement: re-run verification once when ticket-helper report omits verbatim CLI output

Condition:

- When a ticket-helper subagent returns a report for a scoped read-only operation (e.g. verify `get`) that omits the CLI output (e.g. only "exit 0, output returned above" with no content)

Action:

- Do re-run the exact same operation once in a fresh invocation with an explicit "include the full raw CLI output verbatim, do not summarize" instruction; do not treat the omission as a tracker failure (tracker exit was 0). Observed 2026-08-12 on FEATURE-009 verification get.
- Refined 2026-08-13: a summary-only report is ACCEPTABLE without re-run when it states the needed facts explicitly and unambiguously (status + exit code, e.g. SA-DES-005 get summary: "status Resolved, exit 0"); re-run only when status or exit code is missing or ambiguous.

## Improvement: duplicate design sub-task handling via Duplicated status

Condition:

- When a user scope list omits a ticket that shares title and parent with an in-scope ticket (e.g. BA-DES-003 vs BA-DES-004, both under FEATURE-003)

Action:

- Do `get` the out-of-scope ticket to confirm exact duplication; then `link create <dup> <canonical> RelatesTo`, `comment create` the duplication rationale, and `update <dup> --status Duplicated --author ba` (exit 0, terminal). Do not run any design work under the duplicate. Observed 2026-08-13: BA-DES-003 marked Duplicated (LINK-00729, comment 20260813-100953-ba).

## Improvement: dev_story creation requires feature_request and epic fields plus two link types

Condition:

- When creating DEV-STORY tickets under a FEATURE during BA-DES work

Action:

- Do pass `--parent FEATURE-XXX --field feature_request=FEATURE-XXX --field epic=EPIC-XXX --field release_notes=<placeholder> --assignee tech-lead --author ba` at `create dev_story` (feature_request and epic are in dev_story required_fields; release_notes is pre_grooming_required)
- Do create `Contains` link (source=FEATURE, target=DEV-STORY) and `EpicLink` link (source=DEV-STORY, target=EPIC) right after creation; for a feature linked to two EPICs (FEATURE-010 → EPIC-009 + EPIC-010), create two EpicLink links per story
- Do record all assigned LINK IDs for the DoD evidence table. Observed 2026-08-13: 14 DEV-STORYs (024..037), Contains LINK-00730..00743, EpicLink LINK-00744..00759, all exit 0.

## Improvement: verify tool-side entry-point parity before claiming net-new tool work (CLI-only skills features)

Condition:
- When a FEATURE mandates "skills must use CLI only / no python scripts in skills / move implementations to tool"

Action:
- Do first grep the tool `pyproject.toml` for the `pal-found-*` console entries and inspect `pal_found_cli_tool/src/pal_found_cli/<ns>/` before claiming the skills scripts are the sole implementation or that new tool commands are needed. Tool already exposes all 18 `pal-found-*` entry points incl. datasets/ontologies (verified 2026-09-30). The requirement is primarily a skills-repo doc refactor plus datasets/ontologies parity migration, not net-new tool commands.
- Do classify each skills script (16 thin wrappers vs 2 full standalone datasets/ontologies) in the work-plan comment with line counts from direct file reads.

## Improvement: create BA-ANA and SA-ANA sub-tasks sequentially; link Contains source=subtask, target=feature

Condition:
- When creating the BA Analysis and SA Analysis sub-tasks under a FEATURE during Open->Analysis promotion and linking them

Action:
- Do run the two `create` commands as separate sequential CLI invocations, not one paired `;`-joined line (the paired one-liner was interrupted with ^C once; one-at-a-time each exited 0). Verify each ticket ID and exit code, then `link create <sub> <feature> Contains --author ba` (source=subtask, target=feature) for each, then `link list FEATURE-XXX` to confirm, then `update FEATURE-XXX --status Analysis --author ba`.

## Improvement: new Epic warranted decision for doc-only skills model

Condition:
- When analyzing a requirement that changes the delivered skill-content model (e.g. skills become documentation-only, launcher scripts removed, impl moved into tool) and related EPICs are already Done/archived

Action:
- Do treat it as a NEW Epic (BA/Architect creates at design start), not a standalone feature and not a relink to archived EPICs. Do NOT fabricate an Epic link when no Epic exists; record the decision in the work-plan comment and note the Epic-for-creation. Verify via `list --type epic` that no in-flight Epic fits.

## Improvement: hold BA-DES at In Progress with dependency QUESTION when SA-DES is New

Condition:

- When BA-DES In Progress→Resolved DoD requires the SA-DES counterpart to be at least In Progress, and all SA-DES are still New after polling

Action:

- Do complete all In Progress deliverables (business design doc, DEV-STORYs + links, time_spent_hours, document_index update, requirements comment), then create one QUESTION per BA-DES addressed to architect (addressed_to=architect, parent=BA-DES, priority High, assignee ba, NO Blocks link so the parent stays In Progress, not Blocked), then leave BA-DES at In Progress
- Refinement 2026-09-30 (BA-ANA-012): the BA-ANA/SA-ANA analysis sub-task instructions explicitly FORBID advancing a BA-ANA to Resolved while SA-ANA is below In Progress AND the BA-ANA Open/analysis instructions say to create a QUESTION with a Blocks link and set status Blocked until resolved. So for analysis sub-tasks a Blocks link + at-Blocked is the documented holding state (prior status In Progress recorded for restore). Distinguish the design-phase BA-DES convention (no Blocks link, stay In Progress) from the analysis-phase BA-ANA convention (Blocks link, hold Blocked). Do not fabricate Resolved/Closed while the cross-role counterpart is below In Progress.
- Do poll `list --type sa_subtask_design` before deciding on promotion; do not fabricate Resolved. Same pattern as BA-ANA phase (QUESTION-048..055). Observed 2026-08-13: QUESTIONS-078..086 created, all 9 BA-DES stay In Progress.

## Improvement: BA-DES design deliverable + DEV-STORY creation pattern

Condition:

- When designing a feature (Phase 3 Design) and creating DEV-STORYs under it

Action:

- Do produce the design deliverable under .ept/docs/deliverables/business_design/BA-DES-XXX-*.md under 300 lines (composition rule), register it in document_index.md under Business Design, and mirror the Status field in the index.
- Do create DEV-STORYs via 'create dev_story --parent <FEATURE> --assignee <role> --field component=skills --field story_points=N --field feature_request=<FEATURE> --field epic=<EPIC> --field release_notes=... --field priority=High --author ba'. --parent does NOT auto-create links; manually create Contains (FEATURE->STORY) and EpicLink (STORY->EPIC).
- Do promote stories New->Open immediately and set release_notes (pre-grooming) + assignee (pre-development).
- Do check Resolved->Closed DoD requires SA-SUB terminal status; do NOT fabricate Close when SA-DES sibling still In Progress. Hold at Resolved, document the dependency, no QUESTION (not ambiguity).

## Improvement: cross-review approval QUESTION creation and terminal-parent behavior

Condition:

- When remediating a workflow-probe violation by creating cross-review approval QUESTIONs (SA-ANA/BA-DES approvals) with a Blocks + Question link to a parent sub-task

Action:

- Do use 'create question --parent <subtask> --addressed-to <role> --assignee <role> --priority High'; then 'link create <QUESTION> <parent> Blocks' and 'link create <QUESTION> <parent> Question' (both required by BA _Standards cross-review).
- Do expect the auto-block to fire on the FIRST Blocks link when the parent is non-terminal (ba_subtask_design Resolved -> Blocked); later Blocks/Question links warn "Blocked -> Blocked" harmlessly.
- Do NOT expect auto-block on a terminal parent: sa_subtask_analysis Closed is terminal with NO outgoing transitions, so the "[automations warning] ... terminal status and cannot be transitioned" is expected and SAFE. The parent stays Closed; holding is conceptual, not enforced by state.
- Do report terminal parents honestly (Closed, not Blocked); never claim a Blocked state the tracker does not show. Addressed_to/assignee per available_resources.md: sa_subtask approval reviewer = ba; ba_subtask_design approvers = architect (SA) + tech-lead (Lead Developers); PO approval handled separately.
- Do record exact IDs (QUESTION-XXX, LINK-XXXXX) in the final report (observed 2026-09-30: FEATURE-011 approvals QUESTION-142/143/144, links LINK-01063..01068).

Condition:

- When designing a feature (Phase 3 Design) and creating DEV-STORYs under it

Action:

- Do produce the design deliverable under .ept/docs/deliverables/business_design/BA-DES-XXX-*.md under 300 lines (composition rule), register it in document_index.md under Business Design, and mirror the Status field in the index.
- Do create DEV-STORYs via 'create dev_story --parent <FEATURE> --assignee <role> --field component=skills --field story_points=N --field feature_request=<FEATURE> --field epic=<EPIC> --field release_notes=... --field priority=High --author ba'. --parent does NOT auto-create links; manually create Contains (FEATURE->STORY) and EpicLink (STORY->EPIC).
- Do promote stories New->Open immediately and set release_notes (pre-grooming) + assignee (pre-development).
- Do check Resolved->Closed DoD requires SA-SUB terminal status; do NOT fabricate Close when SA-DES sibling still In Progress. Hold at Resolved, document the dependency, no QUESTION (not ambiguity).


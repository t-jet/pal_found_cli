## Improvement: Immediate memory preflight after role bootstrap

Condition:
- When authoritative role instructions must be loaded before their preflight requirements are known, or a new delegated task arrives after an earlier task finished in the same session

Action:
- Do treat every new delegated task as a fresh preflight boundary and load the self-improvement skill and agent memory before commentary, planning, or any other project read, even when the memory was read for an earlier task in the same session

## Improvement: Read blocker evidence chain end to end

Condition:
- When deciding whether an unblocked ticket or open question is actionable

Action:
- Do retrieve parent children, ticket links, and linked question comments; status alone does not prove prerequisites or DoD
- When multiple question blockers are identified together, document the full blocker set and prior status before activating links; verify every link afterward, and treat a `Blocked -> Blocked` automation warning as non-fatal only when the command exit is 0 and fresh state confirms the parent remains correctly Blocked

## Improvement: Never infer actual time from estimates

Condition:
- When transition DoD requires time reported but ticket only has estimated hours

Action:
- Don't copy estimates into time_spent_hours; stop before transition and request actual time evidence
- When multiple contributors report actual effort, retrieve the current value and write the verified cumulative total rather than replacing it with only the latest contribution

## Improvement: Revalidate every status hop

Condition:
- When one request may advance a ticket through multiple statuses

Action:
- Do use each transition result as fresh context, verify new-status DoD and links, then run workflow transitions again before the next hop

## Improvement: Audit created-ticket links before Open

Condition:
- When a new subtask is created with a parent argument

Action:
- Do run link list before New to Open; physical nesting may not create required Contains and ParentChild links

## Improvement: Resolve configured type keys before dependent preflight

Condition:
- When a request uses a display name or ticket prefix that may differ from the configured CLI type key

Action:
- Do run `workflow types`, read its result, and only then construct type-info, transition, and create commands; don't batch type discovery with commands that depend on the unresolved key

## Improvement: Avoid no-match exits during strict retries

Condition:
- When a retry instruction requires stopping on any nonzero exit and optional evidence discovery may find nothing

Action:
- Do use a read-only command that explicitly reports found or not found with exit 0; don't use raw search-tool exit status as control flow

## Improvement: Clear verified defect blocks before closure

Condition:
- When a Resolved defect has an outgoing Blocks link and closure DoD forbids active blocks

Action:
- Do record QA verification, remove the exact Blocks link, verify remaining links, then close and restore the target ticket to its documented prior status

## Improvement: Respect chained automatic transitions

Condition:
- When closing a child may trigger one or more parent automatic transitions

Action:
- Do retrieve the parent fresh before any write; never replay an assumed intermediate status or DoD
- When an automatic transition filters for a child type that does not exist, don't treat the empty child set as proof of completion; inspect the parent's explicit deployment evidence and target-environment DoD before any manual advance

## Improvement: Separate objective evidence from addressee acceptance

Condition:
- When durable evidence appears to answer or supersede a question addressed to another role

Action:
- Do document research and advance only to In Progress; don't resolve, close, or mark duplicate without the configured addressee review and requester acceptance

## Improvement: Keep artifact completion separate from review approval

Condition:
- When a completed artifact is ready but the workflow DoD requires named reviewer approval

Action:
- Do record the artifact, validation evidence, and actual time, then advance only to the review-capable status; never infer approval from artifact completeness

## Improvement: Reopen QA-rejected resolved defects through valid states

Condition:
- When independent QA rejects a Resolved defect and the workflow has no direct transition back to In Progress

Action:
- Do document the failed QA, cumulative time, prior status, and preserved blocker links; preflight and use the configured nonterminal bridge such as Resolved to Blocked, then refresh context and preflight Blocked to In Progress
- Don't remove downstream Blocks links or close the defect while rework remains

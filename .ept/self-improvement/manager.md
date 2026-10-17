## Improvement: preflight agent slots

Condition:
- When running workflow batch through subagents and ticket-helper also needed

Action:
- Do preflight available agent capacity; keep slots free for ticket-helper before spawning execution batch.

## Improvement: enforce manager execution boundary

Condition:
- When delegated task asks manager-role agent to author, test, or review implementation artifacts

Action:
- Do hand off execution to appropriate specialist before touching artifacts; keep manager work to coordination and ticket audit.

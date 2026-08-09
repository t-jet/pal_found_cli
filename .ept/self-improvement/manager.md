## Improvement: preflight agent slots

Condition:
- When running workflow batch through subagents and ticket-helper also needed

Action:
- Do preflight available agent capacity; keep slots free for ticket-helper before spawning execution batch.

## Improvement: preflight and correct tracker CLI command syntax before executing

Condition:
- When a caller-supplied tracker CLI command string deviates from REFERENCE.md syntax - an undocumented alias (e.g. "list comments"/"list links" instead of "comment list"/"link list"), named options where the CLI only accepts positional arguments, or an option value the CLI does not accept

Action:
- Do preflight the command string and option values against REFERENCE.md and the CLI's own --help output before executing. Correct the command to the documented form and documented values before running it, and report the corrected command actually executed. Treat CLI runtime validation as authoritative once syntax is confirmed correct.

## Improvement: quote comment/subject text safely based on content

Condition:
- When building a PowerShell --text/--subject argument for comment create (or similar) whose body contains single quotes/apostrophes

Action:
- Do use a double-quoted variable instead of single-quoted (safe only when the text has no $, backtick, or double-quote characters). When the text has no single quotes, the single-quoted form is safe and literal \n escapes pass through unmodified for the CLI to decode. Verify quoting safety against the actual text before executing.

## Improvement: preserve open status when review evidence misses mandatory citations

Condition:
- When a code-review or DoD-verification transition requires file/line citations, timestamps, environment, or test-data evidence before closing

Action:
- Do inspect each cited artifact and record exact path:line range, timestamp, environment, test data, per-case result, and a short verbatim code/design snippet before closing. If supplied evidence has only aggregate results or vague citations, document the missing proof and leave the ticket in its current status; do not claim approval or transition it to a terminal status.

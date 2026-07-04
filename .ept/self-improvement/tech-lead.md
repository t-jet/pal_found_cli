# Tech Lead — Improvement Memory

## Improvement: verify reviewer ADR claims against code before fixing

Condition:
- When addressing a code-review finding that cites an ADR (e.g. "ADR-004 says errors go to stderr")

Action:
- Do read the cited ADR section directly before applying the fix; reviewers occasionally cite the wrong ADR number or invert the rule, and blindly matching their wording propagates the error.

## Improvement: flip tests asserting the bug when fixing correctness findings

Condition:
- When a code-review finding flags a correctness bug (e.g. wrong stream, wrong exit code) and the existing unit test asserts the buggy behaviour

Action:
- Do update the test in the same commit so it asserts the ADR-correct behaviour; do not leave the test enforcing the bug and creating a regression trap for the next reviewer.

## Improvement: prefer best-effort optional imports for SDK exception mapping

Condition:
- When mapping third-party SDK exception types to project exit codes and the SDK may not be installed in every environment (CI, unit tests, lightweight runners)

Action:
- Do wrap the SDK import in try/except inside a registration helper that returns a base mapping plus SDK additions; document HTTP status classification as the primary fallback so reviewers understand the layered design.

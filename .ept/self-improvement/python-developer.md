# python-developer — improvement memory

## Improvement: circular-import when registering cross-module exception mappings

Condition:
- When adding an exception-class → exit-code (or similar) mapping inside `error_serializer` (or any low-level module) for an exception defined in a module that imports FROM that low-level module (e.g. `access_control_guard` imports `EXIT_ACCESS_CONTROL` from `error_serializer`).

Action:
- Do the import lazily inside the registration function (`_register_sdk_exceptions`) wrapped in try/except, never at module top level. This breaks the cycle because the function runs at import time only after the constants it depends on are already defined. Place the registration BEFORE any early `return mapping` in the same function so it always executes.

## Improvement: BUG-SUB-004 exit-code 8 gap pattern

Condition:
- When an exception type is documented in an exit-code taxonomy (ADR-001) with a constant (`EXIT_ACCESS_CONTROL = 8`) but `serialize()` returns the default code instead.

Action:
- Check `_EXCEPTION_TO_EXIT_CODE` map population and whether HTTP-classification fallback applies. No-HTTP-status exceptions (AccessControlError) must have an explicit map entry; the HTTP path cannot rescue them. Add a regression test that asserts BOTH the code AND the full stdout envelope (type, exit_code_name, message, call_id).

## Improvement: stdout-capture fixture is fragile for print_to_stdout=True

Condition:
- When writing an envelope test that uses the suite's `stdout_capture` autouse fixture with `print_to_stdout=True`.

Action:
- Do inline stdout capture (io.StringIO + try/finally restore) inside the test instead of relying on the shared fixture, which may be reset/ordered unpredictably across tests in the same class.

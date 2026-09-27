## Improvement: build-queue all needs no author flag

Condition:
- When executing build-queue all on tracking system

Action:
- Do run exact command python .ept/tools/tracker/tracker_cli.py build-queue all from workspace root; don't add flags; return full output verbatim; exit 0 = success.

## Improvement: read-only retrieval needs no author flag

Condition:
- When running read-only tracker CLI retrieval (for example, get <ticket-id>)

Action:
- Do run the exact documented command from workspace root without --author or extra flags; capture terminal exit code; return complete CLI output verbatim; exit 0 = success.

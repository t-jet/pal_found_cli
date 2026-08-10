## Improvement: build-queue all read-only, no author flag

Condition:
- When executing build-queue all on tracking system

Action:
- Do run exact command python .ept/skills/tracking-system/tracker/tracker_cli.py build-queue all from workspace root; don't add flags; return full output verbatim; exit 0 = success.

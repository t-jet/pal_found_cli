---
id: QUESTION-013
type: question
title: 'QUESTION: TC3.R3 metadata separator in OutputFormatter.emit_to_stderr (AC conflict)'
status: Resolved
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: Critical
reporter: qa-engineer
---

# QUESTION-013: QUESTION: TC3.R3 metadata separator in OutputFormatter.emit_to_stderr (AC conflict)

## Description

AC for DEV-STORY-002 OutputFormatter.emit_to_stderr requires a # ---metadata-start--- separator between payload and metadata, but implementation omits it. Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Need decision: (a) add the separator to emit_to_stderr, (b) drop the separator from AC, or (c) make separator conditional on a flag. Affects structured-output consumers that parse stderr.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

---
id: DEV-011
type: development
title: Implement Foundry AIP Agents CLI, session lifecycle, and Claude skill
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: workflow-mgr
estimated_hours: 26
time_spent_hours: 26
---

# DEV-011: Implement Foundry AIP Agents CLI, session lifecycle, and Claude skill

## Description

Implement the AIP Agents package, 16-command parser and registry, nested SDK routing, validated JSON inputs, pagination, aliases and history, cleanup, eager-byte persistence, Claude skill, launcher, and console entry. Session cancel accepts optional --response as an AgentMarkdownResponse scalar string and forwards it to the SDK unchanged. It must not expose response-json or apply JSON/object validation to this value. Classify purge as a write, run access control before filesystem or SDK work, and exclude attribution.

## Acceptance Criteria

- Parser and registry expose 15 SDK operations plus local session purge.
- Nested routing, structured JSON inputs, pagination, aliases, history, cleanup, and eager-byte persistence follow DESIGN-011.
- Session cancel exposes optional --response <markdown-string> and forwards the scalar string unchanged.
- No response-json option or JSON/object validation exists for session cancel response.
- Purge uses the write classification and every guard runs before filesystem or SDK effects.
- B3 tracing and attribution exclusion match the approved contract.
- Claude skill, launcher, package allow-list, and console entry are included.
- Ruff and mypy pass.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-011-aip-agents-cli.md
- DEV-STORY-011

## Notes

The source SDK defines AgentMarkdownResponse as str.

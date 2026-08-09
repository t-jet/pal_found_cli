---
id: DEV-007
type: development
title: 'DEV-STORY-006 DEV: foundry-filesystem CLI (31 ops, ontologies OP_SPECS pattern)'
status: Closed
created: 2026-07-29
updated: 2026-07-29
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 4
---

# DEV-007: DEV-STORY-006 DEV: foundry-filesystem CLI (31 ops, ontologies OP_SPECS pattern)

## Description

**Scope**: Implement `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py` using the DEV-STORY-007 ontologies refined pattern (`OP_SPECS` table + `_get_client` nested-sub-client dispatcher + `async def main()` + `def console_main()`). Wire all 31 ops: folder(5), project(7), resource(11), resource-role(3, via `client.filesystem.Resource.Role`), space(5) through the shared common layer (ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, PaginationHelper, TracingProvider). Register `foundry-filesystem` console entry point in pyproject.toml. Add `.claude/skills/foundry-filesystem/` skill package (SKILL.md + scripts/foundry_filesystem_cli.py launcher).

**Acceptance Criteria**: Given/When/Then for AC-FS-PKG-1, AC-FS-PKG-2, AC-FS-PKG-3, AC-FS-OP-ALL, AC-FS-OP-FOLDER, AC-FS-OP-PROJECT, AC-FS-OP-RESOURCE, AC-FS-OP-RESOURCE-ROLE, AC-FS-OP-SPACE, AC-FS-INFRA-COMMON, AC-FS-INFRA-RETRY, AC-FS-INFRA-ERROR (NO new error mapping — rely on common ErrorSerializer; filesystem exceptions subclass NotFoundError/PermissionDeniedError/BadRequestError already), AC-FS-INFRA-OUTPUT, AC-FS-INFRA-ACL, AC-FS-INFRA-PAGINATION (5 ops), AC-FS-INFRA-TRACING, AC-FS-EXIT-SUCCESS, AC-FS-EXIT-AUTH, AC-FS-EXIT-NOTFOUND, AC-FS-EXIT-CONFIG, AC-FS-QUALITY-LINT-TYPE, AC-FS-QUALITY-PATTERN-CONSISTENCY. Estimated 16h.

**Deliverables**: foundry_filesystem_cli.py, __init__.py files, SKILL.md, launcher, pyproject.toml changes.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

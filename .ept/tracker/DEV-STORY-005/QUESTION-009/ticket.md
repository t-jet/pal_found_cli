---
id: QUESTION-009
type: question
title: 'QUESTION: DEVOPS-004 deployment prerequisites — DEV-STORY-001/003/004 incomplete,
  CLI code not in package directory'
status: Closed
addressed_to: architect
created: 2026-05-20
updated: 2026-05-20
priority: High
assignee: architect
reporter: devops-engineer
---

## Context
DEVOPS-004 (Deploy foundry-datasets skill) was blocked on deployment prerequisite questions.

## Questions
1. Should DEVOPS-004 be blocked until DEV-STORY-001 through DEV-STORY-004 are Closed?
2. Should the CLI script be moved into src/foundry_cli/datasets/scripts/ or is .claude/skills/ the canonical deployment target?
3. Is the .claude/skills/foundry-datasets/ structure the final deployment artifact, or should files also be installed as a Python package?

## Answer (Architect + DevOps Engineer)

### Q1: Dependency blocking
**DEVOPS-004 may proceed — DEV-STORY-004 is NOT a prerequisite.**

The foundry-datasets CLI imports 7 components, all from DEV-STORY-001/002/003, all present in src/foundry_cli/common/:
- ConfigLoader, AuthProvider, AsyncClientFactory (DEV-STORY-001)
- RetryHandler, ErrorSerializer, OutputFormatter, LogSetup (DEV-STORY-002)
- AccessControlGuard, PaginationHelper (DEV-STORY-003)

BinaryDownloadHandler, SessionManager, TracingProvider (DEV-STORY-004) are NOT used by the datasets CLI. They serve file download, session persistence, and tracing — none relevant to the Datasets API v2.

### Q2: Code location
**.claude/skills/foundry-datasets/ IS the canonical deployment target.** Per SAD-001 §8.2, deployment is file copy to .claude/skills/ — no pip package installation.

### Q3: Final deployment artifact
Per SAD-001 §8.2 and SRS-001 FR-SKILL-2, each skill package SHALL contain:
`
foundry-{namespace}/
├── SKILL.md
└── scripts/
    ├── foundry_{namespace}_cli.py
    └── _foundry_cli_common.py
`

### Deployment prerequisites identified
1. Assemble _foundry_cli_common.py from src/foundry_cli/common/ components and copy to .claude/skills/foundry-datasets/scripts/
2. Validate the CLI entry point works with the assembled common module
3. The pyproject.toml entry point references the wrong location — document this discrepancy

## Research Done
- Reviewed document_index.md, SAD-001 §8, SRS-001 FR-SKILL-2/NFR-DIST-2
- Examined pyproject.toml, CI workflows, source tree structure
- Verified src/foundry_cli/common/ component availability
- Verified .claude/skills/foundry-datasets/ current contents

Subject: DoD evidence: implementation and verification (2026-08-13)
Created: 2026-08-13T20:06:50
Updated: 2026-08-13T20:06:50
---
Implementation plan:
- Keep the change limited to the static main skill.
- Retain the existing frontmatter and instructions.
- Record the final path, official source, and review date.

Evidence:
- .agents/skills/pal-found/SKILL.md:10-17 contains the platform description, source URL https://www.palantir.com/docs/foundry/architecture-center/platforms, and review date 2026-08-13.
- Source URL check returned HTTP 200.
- Targeted migration/release pytest: 8 passed.
- Latest focused suite: 1,092 passed, 5 warnings.
- Launcher, ruff, mypy, and compileall checks passed.

Acceptance criteria and deliverable: one concise official-source-backed platform section in the cited file; source URL and review date recorded; existing frontmatter and instructions preserved; final path and source recorded.

Related documentation: .ept/docs/deliverables/business_design/BA-DES-009-business-design.md; .ept/docs/deliverables/architecture/SA-DES-008-technical-design.md.

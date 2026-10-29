Subject: Focused static and semantic checks: pass
Created: 2026-10-05T10:28:17
Updated: 2026-10-05T10:28:17
---
Checked both owned pages: 48 and 170 lines (<300), 92 official www.palantir.com/docs/foundry links with no query tracking, topic markers for coverage groups 3-8, local return links resolve, no .ept/ or ADR- paths, no copy-folder instructions, no trailing whitespace. rg --files verified both physical files. Representative semantic claims checked against official Ontology permissions, Compute execution modes, Developer Console permissions, Custom Widget create/embedding, data branching, VS Code Global Branching, and Action webhooks. Documentation-only; no executable code or build artifact to compile. Central commit pending with shared submodule.

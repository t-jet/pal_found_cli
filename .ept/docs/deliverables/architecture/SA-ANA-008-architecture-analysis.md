# Architecture Analysis — SA-ANA-008

## Add Palantir Foundry Platform and Capability Descriptions to Skills

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-008 |
| **Feature** | FEATURE-008 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| Main foundry skill | no platform description | brief Palantir Foundry platform description (BR-008-01) |
| 18 namespace skills | no capability description | short capability description per skill (BR-008-02) |
| Official Palantir Foundry web pages | external source | cited as description sources (BR-008-03) |
| Skill documentation | content only | content plus source citation |

This is a content-only change to static markdown skill files. No executable
code, no packaging, and no access-control change is involved.

## 2. Architecture Approach

Two description layers are added:

- Platform layer: the main `foundry` skill carries a brief description of what
  Palantir Foundry is, so a user opening the general skill understands the
  platform context before any namespace skill.
- Capability layer: each namespace skill carries a short description of the
  Foundry capability its tool covers (for example, datasets, ontology, admin).

Both layers follow the same rules:

- Text is sourced from official Palantir Foundry web pages and each description
  cites its source page (BR-008-03).
- Descriptions stay brief and readable by a non-expert (BR-008-04).
- Facts are consistent across all skills; a review pass checks that no two
  skills state conflicting facts (BR-008-05, AC-008-04).

The citation makes the source traceable (AC-008-03) and gives maintainers a
known place to re-check when official pages change.

## 3. Technology Stack

- Markdown content in skill files
- Source citations as links to official Palantir Foundry pages
- No code, no dependencies, no build step

## 4. General Implementation Approach

1. Write the platform description for the main skill (AC-008-01), sourced and
   cited.
2. Write a capability description for each of the 18 namespace skills
   (AC-008-02), each sourced and cited (AC-008-03).
3. Run a consistency review across all descriptions (AC-008-04).
4. Update documentation references to the new sections.

## 5. General Migration Approach

- Phase 1 (author): draft platform and capability text from official pages.
- Phase 2 (insert): add the sections to the 19 skill files.
- Phase 3 (verify): consistency and citation review.
- Phase 4 (maintain): re-check descriptions when official pages change.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Source drift | Official pages change after copying | Cite source page; re-check on page changes |
| Fact drift | Descriptions diverge from the actual capability | Match description to the skill's operation set at review |
| Licensing | Quoting beyond allowed scope | Paraphrase briefly with attribution (BA-ANA-008 assumption) |
| Inconsistency | Skills state conflicting facts | AC-008-04 consistency review |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-008 (Analysis) |
| Epic | EPIC-009 |
| BA sub-task | BA-ANA-008 |
| SA sub-task | SA-ANA-008 |
| BA deliverable | BA-ANA-008-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |

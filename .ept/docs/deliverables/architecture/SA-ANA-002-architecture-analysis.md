# Architecture Analysis — SA-ANA-002

## Host All Three Repositories Publicly on GitHub

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-002 |
| **Feature** | FEATURE-002 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| foundry_cli repository (design, docs, tracking) | private single repo | public GitHub repo |
| foundry_cli_tool repository (CLI source) | nested repo, empty | public GitHub repo |
| foundry_cli_skills repository (agent skills) | nested repo, LICENSE only | public GitHub repo |
| GitHub web UI and git protocol | restricted | open read, restricted write |
| Issues and pull requests | internal only | open to external contributors |
| Releases and tags | internal | publicly reachable |
| GitHub Actions (ci.yml, publish.yml) | existing | unchanged; secrets scoped per repo |

## 2. Architecture Approach

Publish each of the three repositories as a public GitHub repository. Read access
is open to everyone; write access stays limited to maintainers. Each repo keeps
its own branch protection and its own secret set.

The design repo stays the home of the tracker and deliverables. The tool repo
holds the Python package and its CI/CD. The skills repo holds the agent skill
files. Public visibility is set at the repository level in GitHub settings; no
code change is required.

Prerequisite: FEATURE-003 (repository split) must land first, because three
separate repositories must exist before they can be made public.

## 3. Technology Stack

- GitHub for hosting, issues, pull requests, and releases
- git for cloning and version control
- Existing GitHub Actions workflows (ci.yml, publish.yml) unchanged
- GitHub repository settings and secrets management

No new runtime dependencies.

## 4. General Implementation Approach

1. Audit every file that will be public for secrets, tokens, or internal data;
   scrub anything found and confirm `.env` stays gitignored.
2. Set repository visibility to public on each of the three repositories.
3. Verify anonymous access: clone each repo without credentials and open a
   release URL without login.
4. Confirm write access is still limited to maintainers and branch protection
   remains active.
5. Open issues and pull requests to external contributors.

## 5. General Migration Approach

- Phase 1 (pre-flight): secret audit and content review per repository.
- Phase 2 (flip): change visibility; keep write restrictions unchanged.
- Phase 3 (verify): anonymous clone and release download checks against
  AC-002-01..05.
- Phase 4 (operate): monitoring, contribution guidelines, and secret scanning
  stay on.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Secret exposure | Internal data or tokens become public | Pre-publication audit; secret scanning; `.env` gitignored |
| Unwanted contributions | Low-quality issues or PRs | Contribution guidelines and maintainer controls |
| Split dependency | Public hosting cannot complete before the split | Sequence: FEATURE-003 first, then publish |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-002 (Analysis) |
| Epic | EPIC-010 |
| BA sub-task | BA-ANA-002 |
| SA sub-task | SA-ANA-002 |
| BA deliverable | BA-ANA-002-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |

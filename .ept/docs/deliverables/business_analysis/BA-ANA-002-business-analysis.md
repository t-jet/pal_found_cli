# Business Analysis — BA-ANA-002

## Host All Three Repositories Publicly on GitHub

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-002 |
| **Feature** | FEATURE-002 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

The project currently lives in a single repository that is not publicly reachable.
Hosting the three repositories — design and documentation, the CLI tool, and the
agent skills — publicly on GitHub lets any user view, clone, and contribute without
authentication. Public hosting is the prerequisite for every downstream distribution
feature: pip and conda installation (FEATURE-004, FEATURE-005), git-based skill
distribution (FEATURE-007), and harness-agnostic skill access (FEATURE-006).

Without public hosting, users cannot reach the tool or the skills through the
channels the Project Owner wants to support, and community contribution is blocked.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-002-01 | All three repositories must be publicly visible on GitHub so any user can view content without authentication. |
| BR-002-02 | Any user must be able to clone all three repositories without credentials. |
| BR-002-03 | The public contribution path must be open: users can raise issues and open pull requests. |
| BR-002-04 | Repository access must be revoked and no longer possible once content is removed or the repository is taken private. |
| BR-002-05 | Released artifacts (tags, releases) must be publicly reachable without login. |
| BR-002-06 | Repository owners must be able to restrict who can write to each repository independently. |

## 3. Acceptance Criteria

- AC-002-01: Given a user without a GitHub account, when they open any of the three repository URLs, then they can read all repository content without authentication.
- AC-002-02: Given a user with git installed, when they run `git clone` on any of the three repositories, then the clone succeeds without credentials.
- AC-002-03: Given a user, when they browse a repository, then they can see and open issues and pull requests.
- AC-002-04: Given a repository owner, when they publish a release, then any user can view and download the release artifacts without login.
- AC-002-05: Given a repository that is later made private, when a user without access retries to clone it, then the operation fails and no content is exposed.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Installation and distribution | Public hosting unblocks pip, conda, and git-clone distribution paths. |
| Contribution | External contributors gain a standard GitHub workflow (issues, pull requests, reviews). |
| Release management | Public releases become a visible, verifiable artifact for every consumer. |
| Documentation | Users can read design and usage documentation directly from the repository. |
| Access management | Owners must manage per-repository write permissions instead of one project-wide setting. |

## 5. Changes in Access Restrictions

- Read access for anonymous users: from restricted to open on all three repositories.
- Write access: remains restricted to maintainers and approved collaborators.
- No Foundry credentials are exposed by making the repositories public; the tool and skills must not embed secrets.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | No repository content contains secrets, API tokens, or private customer data. |
| Assumption | Public hosting does not conflict with organizational policy. |
| Risk | Accidental exposure of secrets or internal details in public repositories. |
| Risk | Public visibility attracts unwanted issues or low-quality contributions. |
| Mitigation | Secret scanning and review before publishing; contribution guidelines; maintainer controls. |

## 7. Request Rate Changes

Public hosting increases read traffic (clone and download volume) versus a private
repository. Expected audience is individual developers and AI agents cloning the
skills; the volume is low and within standard GitHub hosting limits. No rate-limit
or quota changes are required by consumers.

## 8. Data Size Changes

Repository content is documentation, Python source code, and markdown skill files.
All three repositories together are small (well under GitHub's per-repository size
limits). Cloning the skills repository is expected to be a one-time lightweight
operation for consumers.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-002 (Open) |
| Epic | EPIC-010 — Public repositories and distribution of the Foundry CLI tool |
| BA sub-task | BA-ANA-002 |
| SA counterpart | SA-ANA-002 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |

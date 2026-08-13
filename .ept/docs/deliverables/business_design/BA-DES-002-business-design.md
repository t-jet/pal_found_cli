# Business Design — BA-DES-002

## Host All Three Repositories Publicly on GitHub

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-002 |
| **Feature** | FEATURE-002 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-002, SA-ANA-002 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design covers making the three repositories publicly visible and cloneable
on GitHub. The repositories are named per ND-010-01: `pal_found_cli` (design,
documentation, tracking), `pal_found_cli_tool` (CLI source), and
`pal_found_cli_skills` (agent skills). Public hosting is the foundation for
every distribution channel in the programme, so the design defines one set of
business rules that applies to all three repositories and a repeatable
publication procedure per repository.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-002-01 | All three repositories must be publicly visible so any user can view content without authentication. |
| BR-D-002-02 | Any user must be able to clone all three repositories without credentials. |
| BR-D-002-03 | Visitors must be able to raise issues and open pull requests on all three repositories. |
| BR-D-002-04 | Released artifacts (tags, releases) must be publicly reachable without login. |
| BR-D-002-05 | Write access must remain restricted to maintainers per repository. |
| BR-D-002-06 | Repository content must be free of secrets, credentials, and private customer data before publication. |
| BR-D-002-07 | Publication must be reversible: taking a repository private must stop all public access immediately. |

## 3. Logical Flow (business terms)

1. A maintainer prepares a repository for publication: reviews content,
   runs a secret scan, and confirms no internal-only material remains.
2. The maintainer switches the repository visibility setting from private
   to public and records the decision.
3. GitHub applies the visibility change: content, clone access, issues,
   pull requests, and releases become available to unauthenticated users.
4. A verification pass checks the public state: browse a URL without
   logging in, clone without credentials, open an issue, and download a
   release artifact.
5. If a problem is found, the maintainer takes the repository private again;
   public access stops on the visibility change, before any further fixes.

## 4. UI/UX (abstract)

The design assumes standard GitHub web and git interfaces; no custom
interface is built. The business-relevant user experience is described at an
abstract level:

- An unauthenticated visitor can open any repository landing page and read
  the README, file tree, issues list, and release list.
- A visitor can run a clone command against the repository URL without being
  asked for credentials.
- A maintainer sees the repository visibility setting and write-permission
  list in the repository settings and can change either.
- Error experience: a visitor who follows a removed or made-private
  repository receives a not-found or access-denied response and no content.

## 5. API Specification (abstract)

No new application interfaces are introduced. The design relies on the
following abstract behaviours of the hosting service:

- A visibility-change action that takes a repository from private to public
  (and back), effective immediately.
- A public read path for repository content, clone operations, issues,
  pull requests, and release downloads.
- A restricted write path limited to maintainers and approved collaborators.
- A permission model that can be configured independently for each
  repository.

## 6. Data Structures (business terms)

- Repository record: name, visibility state (private/public), description,
  default branch, write-permission list.
- Release record: version tag, release notes, downloadable artifacts,
  visibility inherited from the repository.
- Publication checklist record: content review done, secret scan done,
  internal-only material removed, visibility set, verification passed.

## 7. Acceptance Criteria

- AC-D-002-01: Given a user without a GitHub account, when they open any of
  the three repository URLs, then all content is readable without
  authentication.
- AC-D-002-02: Given a user with git installed, when they clone any of the
  three repositories, then the clone succeeds without credentials.
- AC-D-002-03: Given a visitor, when they browse a repository, then they can
  see and open issues and pull requests.
- AC-D-002-04: Given a release published by an owner, when a visitor follows
  the release link, then artifacts are downloadable without login.
- AC-D-002-05: Given a repository that is later made private, when a user
  without access retries a clone, then the operation fails and no content is
  exposed.
- AC-D-002-06: Given a repository prepared for publication, when its content
  is scanned, then no secrets or credentials are found.

## 8. Migration Procedure

1. Freeze content changes in each repository one day before publication to
   give the review a stable snapshot.
2. Run the secret scan and content review on all three repositories; record
   results in the publication checklist. Fix and re-scan until clean.
3. Publish one repository at a time in dependency order: first
   `pal_found_cli_skills` (no internal dependencies), then
   `pal_found_cli_tool`, then `pal_found_cli` (design and documentation
   repository, referenced by the others).
4. After each publication, run the verification pass (AC-D-002-01..04) and
   record the outcome.
5. Confirm write permissions per repository remain restricted to maintainers.
6. Announce the publication and point users at the canonical URLs used by
   the distribution channels (FEATURE-004, FEATURE-005, FEATURE-007).
7. Rollback: if any verification fails, switch the repository back to
   private, document the reason, and resume after the fix.

## 9. Developer Story Scope

One story covers the full publication run across the three repositories
including the checklist, verification, and rollback steps.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-002 |
| Epic | EPIC-010 |
| BA design sub-task | BA-DES-002 |
| SA counterpart | SA-DES-002 |
| Analysis | BA-ANA-002, SA-ANA-002 (Closed, PO-approved) |
| Naming decisions | ND-010-01 (QUESTION-072, Closed) |

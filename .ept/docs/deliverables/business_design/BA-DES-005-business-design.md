# Business Design — BA-DES-005

## Publish the CLI Tool to PyPI for pip Installation

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-005 |
| **Feature** | FEATURE-004 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-003, SA-ANA-004 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines how the CLI tool is published to PyPI so any user can
install it with pip. The package is published under the confirmed name
`pal_found_cli` (ND-010-02) with console commands under the `pal-found-`
prefix (ND-010-03). The design covers the publication procedure, release
verification, package metadata, and the user-facing install experience.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-005-01 | The tool must be published to PyPI under the confirmed package name so it can be installed with pip. |
| BR-D-005-02 | Installing the package must not require manual configuration beyond standard environment setup. |
| BR-D-005-03 | Versioned releases must be published and users must be able to upgrade. |
| BR-D-005-04 | Each release must be verified as installable before it is announced as stable. |
| BR-D-005-05 | Runtime dependencies must be declared so pip installs them automatically. |
| BR-D-005-06 | The package page must describe what the tool does and how to use it. |
| BR-D-005-07 | The published artifact must contain no embedded credentials. |
| BR-D-005-08 | Console commands installed by the package must use the `pal-found-` prefix. |

## 3. Logical Flow (business terms)

1. A maintainer prepares a release from a versioned source state: metadata
   is checked, a version number is assigned, and the change summary is
   written.
2. The package is built and installed into a clean environment; a smoke run
   verifies the tool starts and executes a basic command.
3. The artifact is uploaded to PyPI under the confirmed package name.
4. A release verification pass installs the published version in a second
   clean environment and runs the documented commands.
5. The release is announced as stable only after verification passes.
6. Users install or upgrade with pip and receive the dependencies
   automatically.

## 4. UI/UX (abstract)

The design assumes the standard PyPI web interface; no custom interface is
built. Abstract user experience:

- A user runs the install command and the tool becomes available in their
  environment.
- A user opens the package page on PyPI and sees the description, install
  command, usage summary, and version list.
- A user upgrades and receives the new version through the standard pip
  flow.
- Error experience: a user with an unsupported environment receives a clear
  failure message from pip without any manual configuration being required.

## 5. API Specification (abstract)

No new tool interfaces are introduced. The design relies on the package
registry behaviour:

- A publish action that uploads a versioned artifact under a package name.
- A download action that serves the artifact to pip during install or
  upgrade.
- A metadata record (description, dependencies, command entry points) shown
  on the package page and honoured by pip.
- An authentication token used only by maintainers at publish time; never
  embedded in the artifact.

## 6. Data Structures (business terms)

- Package metadata record: name, version, description, author, licence,
  runtime dependency list, command entry points.
- Release record: version number, change summary, artifact, verification
  result, publication timestamp.
- Verification checklist record: clean-install result, smoke-run result,
  secret scan result, upgrade result.

## 7. Acceptance Criteria

- AC-D-005-01: Given a user with Python and pip, when they install the
  published package, then the tool installs successfully.
- AC-D-005-02: Given an installed release, when the user runs a tool
  command, then it works as documented.
- AC-D-005-03: Given a published new version, when a user upgrades via pip,
  then they receive the new version.
- AC-D-005-04: Given a release candidate, when it is published, then a
  clean install is verified before it is marked stable.
- AC-D-005-05: Given the package page, when a user opens it, then it
  explains what the tool does and how to install and use it.
- AC-D-005-06: Given the published artifact, when it is scanned, then it
  contains no embedded credentials.
- AC-D-005-07: Given the installed package, when command availability is
  checked, then commands use the `pal-found-` prefix.

## 8. Migration Procedure

1. Confirm the package name `pal_found_cli` is available on PyPI; if a
  squatter holds it, open a naming question to the Project Owner before
  continuing.
2. Prepare the first release from the renamed repository
  (`pal_found_cli_tool`): align metadata with the confirmed name and
  `pal-found-` command prefix.
3. Publish the first stable release following the release verification flow;
  record the verification checklist.
4. Update installation documentation across the programme (skills,
  README, distribution guides) to use the confirmed package name and
  command prefix.
5. Announce the first stable release and the upgrade path.
6. Rollback: keep the previous published version available; if a release
  fails verification, do not announce it and fix forward from the versioned
  source.

## 9. Developer Story Scope

Two stories: (1) build and publish the first PyPI release with verification;
(2) package page content and installation documentation with the confirmed
names.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-004 |
| Epic | EPIC-010 |
| BA design sub-task | BA-DES-005 |
| SA counterpart | SA-DES-004 |
| Analysis | BA-ANA-003, SA-ANA-004 (Closed, PO-approved) |
| Naming decisions | ND-010-02, ND-010-03 (QUESTION-073, QUESTION-074, Closed) |

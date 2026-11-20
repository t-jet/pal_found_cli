---
id: BUG-051
type: bug
title: CI Security Scan fails on filelock advisories for reviewed tool release candidate
status: In Progress
affected_version: 54dfbdefe54820d0722474b7bd2b0095f2eb232e
created: 2026-11-18
updated: 2026-11-18
priority: High
assignee: devops-engineer
reporter: project-manager
component: ci-security
---

## Observed defect

UAT/release-candidate CI run 44247425711 fails Security Scan on tool PR https://github.com/t-jet/pal_found_cli_tool/pull/4 at exact head 54dfbdefe54820d0722474b7bd2b0095f2eb232e. Ruff, mypy and four test jobs pass. Bandit is clean. Safety exits 64 after reporting three filelock 3.32.7 advisories: CVE-2026-112910, CVE-2026-112908 and CVE-2026-112938. Build Package is skipped. Expected: supported dependency resolution passes security scanning and all eight CI checks, including package build.

## Reproduction and evidence

Inspect the exact run at https://github.com/t-jet/pal_found_cli_tool/actions/runs/44247425711 and reproduce its workflow installation commands, Python/runner environment and package resolution before choosing a fix. Exact dependency parent and constraints have not been established; no remediation has been selected.

- Retained failure log: .ept/tmp/task022_tool_bug050_corrected_security_failure_20261118.log; SHA256 c9775c20f3675bcc89073d24dfb5b3b5b5f8de2d6903987d108c69aa7cd7ba0a.
- Retained exact-head CI proof: .ept/tmp/feature015_tool_bug050_corrected_ci_20261118.json; SHA256 a74b8cfddc129464cfe70db2bfcc154a692ba3917ddec49b4195a0f3578a87c8.
- First-party filelock advisories: https://github.com/tox-dev/filelock/security/advisories/GHSA-8mx5-7m5m-r77g ; https://github.com/tox-dev/filelock/security/advisories/GHSA-6627-m3xw-93mp ; https://github.com/tox-dev/filelock/security/advisories/GHSA-m462-7rxw-wvpg . All list 4.2.1 as patched. Version selection still requires dependency and compatibility checks.

## Acceptance criteria

- Reproduce the failing CI install and record exact dependency parent, resolver constraints, Python version and installed package graph. Explain why filelock 3.32.7 is selected before implementing remediation.
- Prefer supported nonvulnerable dependencies and demonstrate successful resolution plus pip check. Preserve existing supported runtime/SDK compatibility and packaging behavior. Where no supported patched Safety dependency resolution exists, permit a proposal through the existing reviewed, time-bound scanner-only exception process solely for Safety IDs 72390, 54654 and 57659 in filelock 3.32.7 pulled by Safety 3.8.1. Proposed expiry is 2026-12-02, with earlier removal when patched supported Safety ships. This is permission to propose, not implementation approval or a package-patch claim. No wildcard or permanent ignore, forced filelock 4.x, downgrade, fork, scanner weakening or new global policy.
- Obtain independent security, compatibility and risk review before any implementation approval. A proposed exception must retain the full installed-environment scan including scanner dependencies, Bandit's gate, continue-on-vulnerability-error: False and all lint/type/test gates. New unrelated vulnerabilities and expired entries must block. Record exact scope, reason, expiry/removal trigger and reachability limits; scanner-only does not mean zero risk.
- Publish reviewed changes through the normal tool workflow. Record fresh all-eight-check CI success at the exact candidate and exact merged main revision, ancestry/tree evidence, and paired parent source/pin proof. Independent QA must verify before closure; retain immutable evidence and hashes.

## Scope and relationships

Related: FEATURE-015, TASK-022, BUG-050 and historical Closed BUG-006. BUG-006 concerned a different nltk advisory and remains archived. This defect blocks BUG-050 release acceptance. TASK-022 publication work must continue and is related without a blocking link. No cyclic dependencies, scanner waiver or FEATURE-015 acceptance is implied.

## Related Documentation

.ept/docs/document_index.md; .ept/docs/deliverables/qa/WORK-007-release-pin-plan.md; TASK-022 publication criteria; tool .github/workflows/ci.yml and pyproject.toml; tracking-system and workflow skills.

---
id: BUG-052
type: bug
title: Honor proxy environment variables in SDK clients and release urgently
status: Closed
affected_version: 0.1.5
created: 2026-11-19
updated: 2026-11-20
priority: High
resolution: Done
assignee: tech-lead
reporter: project-manager
component: shared-http
fix_version: 0.1.6
---

# Honor standard proxy environment variables in SDK clients

## Priority and scope

High priority. The Project Owner explicitly requires this fix before FEATURE-015 work, followed by a new PyPI and Conda release containing the fix and all other changes already on the CLI tool's main branch. This publication instruction supersedes the earlier GitHub-only delivery restriction for this urgent CLI release.

## Reported environment and reproduction

- pal-found-cli 0.1.5, foundry-platform-sdk 1.111.0, httpx 0.28.1, Windows.
- HTTP_PROXY=http://proxy.mycompany.net:2011 and HTTPS_PROXY=http://proxy.mycompany.net:2010.
- Set FOUNDRY_HOSTNAME=foundry-us.mycompany.com and provide the existing valid FOUNDRY_TOKEN, then run `pal-found-admin user get-current --format json`.
- Reported result: retries, exit 6, and `ConnectionError: [Errno 11001] getaddrinfo failed` because the Foundry host is resolved directly.
- Ordinary httpx requests and the SDK with explicit Config(proxies={"https": ...}) succeed through the configured proxy. The corporate hostname, token and proxy are user-reported evidence; do not request or expose credentials.

## Root-cause hypothesis

AsyncClientFactory.create constructs AsyncFoundryClient without SDK Config. The SDK supplies a custom httpx transport with no proxy, bypassing normal environment-proxy discovery. Confirm this against released SDK source and reproduce it with controlled local proxy fixtures before implementing a fix.

## Acceptance criteria

- The shared client factory honors HTTP_PROXY/HTTPS_PROXY and lowercase equivalents with documented, standard precedence and scheme selection. Preserve existing direct-client behavior when no proxy applies.
- NO_PROXY/no_proxy bypass behavior is supported and tested for the applicable hostname rules; handle wildcard, exact host, domain boundary, port and IP cases according to a documented standard. Any deliberately unsupported rule must be identified before acceptance. Consider ALL_PROXY only where consistent with the selected standard and SDK capabilities.
- Requests for a proxy-only, locally unresolvable target reach a controlled proxy without attempting direct target DNS. Test actual transport routing, not only the presence of Config arguments. Verify bypassed targets use the direct path.
- Preserve authentication, hostname normalization, preview, timeouts, retries, access guards, binary/stream behavior and existing supported SDK compatibility. Never log proxy credentials or token values.
- Independent QA verifies the regression, lowercase/uppercase behavior, bypass and no-proxy cases on appropriate Windows/Linux and admitted SDK controls. Existing meaningful checks remain green.
- Release a new consistent package version to PyPI and the configured Conda channel, including current tool main changes and this fix. Verify published versions, artifacts and clean-install smoke tests. Record exact source commit, tag, CI, artifact hashes, registry URLs and limits in ticket comments.

## Ownership and references

Tech Lead owns the shared client-factory implementation and focused regression tests. Independent QA owns verification; DevOps owns packaging and publication. Current tool main observed by GitHub ls-remote is 01cd9e91e98dc27ca03bfbf0031ee7807684a7ba. Use isolated worktrees; preserve the dirty parent workspace and all unrelated FEATURE-015 changes.

References: `.ept/docs/document_index.md`, `.ept/docs/deliverables/qa/WORK-007-release-pin-plan.md`, shared AsyncClientFactory source, frozen SDK source/runtime, tool CI and release workflows, and the Project Owner's proxy incident report in this session.

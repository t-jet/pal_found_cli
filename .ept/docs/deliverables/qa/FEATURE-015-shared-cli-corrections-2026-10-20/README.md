# Shared CLI correction evidence

Reviewed tool: `657215f37a242889c8b36d104e15bff49587ffb4`.
This bundle records verification of BUG-036 through BUG-042. FEATURE-015
acceptance and release remain separate gates.

Follow-up candidate `2feb1fed64406ddc987d036ce7ae667d3bd11d9d` corrects
three parser return annotations after GitHub mypy rejected their broader
base type. Independent [annotation continuity review](annotation-continuity.json)
verified the exact three-line change, six compilations, three normalized AST
comparisons and 24 parser input comparisons. Runtime behavior, package
configuration and tests are unchanged. The reports below retain their original
`657215f` execution scope; they are not package rebuild results for `2feb1fe`.
Local mypy 2.4 passed all 72 source files; Ruff and 411 focused tests passed.
All eight [GitHub CI checks](github-ci-2feb1fe.json) passed at `2feb1fe`:
Ruff, mypy, Python 3.11 and 3.12 tests on Windows and Linux, security scan,
and package build. The recorded check links and timestamps identify the run.
Independent QA subsequently [closed BUG-036 through BUG-042](bug-closure.json)
through the tracker CLI and removed their seven verified blocking links.
DEV-STORY-070 remains in Development with its separate BUG-034 blocker.

| Evidence | Result |
| --- | --- |
| [Independent QA](independent-qa.json) | 1,684 regression tests and 330 contract checks passed; no failures or skips. Includes real SDK pagination/filter verification. |
| [Package verification](packaging-qa.json) | Six clean installs, six `pip check` results and twelve real console TOON round trips passed across wheel, sdist and Conda on Python 3.11 and 3.12. Exact package/source hashes are recorded. |
| [Guidance review](guidance-qa.json) | Eight whole pages accepted at their recorded hashes against the corrected tool and SDK 1.101.0. |
| [Initial QA findings](initial-qa-findings.json) | Historical 109-failure regression result, classification and limits retained. Subsequent test corrections preserved cases and strengthened source-derived oracles. |

Independent QA covers environment format defaults, genuine TOON encoding,
sanitized JSON parser errors, matching SDK/outer timeouts, four total calls by
default, seven preview query selectors, and required build-search filters on
every page. The tests use synthetic data and mocked transport; no live tenant
access or production deployment is claimed.

Execution paths in the reports identify the original temporary workspace.
Artifact and source hashes bind those observations to the reviewed commit.
Runtime QA used SDK 1.101.0; clean dependency resolution selected SDK 1.111.0
for pip installations and 1.110.0 for Conda. Package probes establish the
reported installation and output behavior, not every API operation on those
later SDK versions. The TOON dependency remained exactly 1.2.0 throughout.

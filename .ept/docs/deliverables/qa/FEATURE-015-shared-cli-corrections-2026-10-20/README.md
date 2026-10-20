# Shared CLI correction evidence

Reviewed tool: `657215f37a242889c8b36d104e15bff49587ffb4`.
This bundle records verification of BUG-036 through BUG-042. FEATURE-015
acceptance and release remain separate gates.

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

Subject: Fix commit, hashes and regression checks
Created: 2026-10-18T17:33:52
Updated: 2026-10-18T17:33:52
---
Fix: `pal_found_cli_skills` commit `03a1304f15519547b4487624cd168a68f5613d64`, based on integration `691107e896b74edd7569bf03084820ebf368be90`. Seven OntologyObject/LinkedObject REST-081 fixtures now check decoded identities, search predicate, aggregate accuracy/group/metric and count. Object and link list fixtures issue a second real SDK request with the decoded `nextPageToken`; applicable fixtures still check declared named errors. Both behavior pages contain adaptable SDK worked calls. No ledger or tracker data was changed in the skills commit.

SHA-256 of changed files under `.agents/skills/pal-found-dev/`:
- `examples/rest/081/v2/ontologies/LinkedObject/invoke_get_linked_object.py`: `e1c90d87f5ce1a882679b72563c8c0ab8cbd8ef6cdc8c14fc4a6b0e642c9de9f`
- `examples/rest/081/v2/ontologies/LinkedObject/invoke_list_linked_objects.py`: `2fc206687aac16d0ec1f424ce8212e80f8acdf4e5a47df58c4322d754fbf14bf`
- `examples/rest/081/v2/ontologies/OntologyObject/invoke_aggregate.py`: `ab29779974f7cf7056e7c388c8871ce1975e9969adedc407558e2b4b78e9888b`
- `examples/rest/081/v2/ontologies/OntologyObject/invoke_count.py`: `4642a16ac8583cb7b16f9b8be963fd83dc1b96ef32f8c7b997d458253f28654a`
- `examples/rest/081/v2/ontologies/OntologyObject/invoke_get.py`: `19e46c42df3d4ce70630aab9b21851b1854ce1b0ed3bb1fa84d3d8a023d6a9b9`
- `examples/rest/081/v2/ontologies/OntologyObject/invoke_list.py`: `6be0b60991f6f6120f4e2f54ea54d8ab421731ed2e00eaa44299cf6a6686295e`
- `examples/rest/081/v2/ontologies/OntologyObject/invoke_search.py`: `a5dc57d367fe91589523e4307714cd932cb0b66aafb8b310673e165e8749070b`
- `references/rest/v2/ontologies/LinkedObject.md`: `c83272d5ee49a860c8f082b54191f8c7c7fa1cb34a92fd30f3e711f1d2c55545`
- `references/rest/v2/ontologies/OntologyObject.md`: `b378e3222e4b6e859e612f54768a0a9af9094bb64a0dc6cd71abb437ad350bf2`

Regression checks at this commit: all seven fixture scripts passed against SDK 1.101.0/httpx MockTransport; `python -m pytest -q tests/test_offline_rest_wave1.py tests/test_documented_examples.py` returned 519 passed; Ruff and `git -c core.whitespace=cr-at-eol diff --check` passed. Independent QA reports seven fixtures and both worked snippets passing via real SDK MockTransport. QA will record its own evidence before closure. Keep `LINK-01974` until QA verifies release readiness.

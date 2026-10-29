Subject: Fix plan and root cause
Created: 2026-10-18T17:33:30
Updated: 2026-10-18T17:33:30
---
Root cause: seven REST-081 OntologyObject and LinkedObject fixtures originally accepted placeholder response bodies and omitted documented named failures. Their worked-example pages had no executable SDK calls. Prior changes added concrete records and errors, but list fixtures still checked only one page. The remaining gap was no SDK request using a returned page token.

Plan: keep SDK 1.101.0 MockTransport requests offline; assert decoded object identities, the requested search predicate, aggregate metric and count. Make object and link lists return two pages and verify the second request carries the decoded next-page token. Add complete, adaptable SDK calls to the two behavior pages. Run each fixture directly, the focused REST and documentation tests, Ruff and diff checks. Leave formal TESTEXEC-080 and the blocking link for independent QA.

Reproduction: run the seven `examples/rest/081/v2/ontologies/{OntologyObject,LinkedObject}/invoke_*.py` files and inspect their corresponding `references/rest/v2/ontologies/{OntologyObject,LinkedObject}.md` pages at candidate 4ab4e6f. Expected: representative result/error assertions and usable calls. Actual at that candidate: empty result placeholders, omitted named errors and prose-only worked examples. No application log exists because this defect is in offline documentation fixtures.

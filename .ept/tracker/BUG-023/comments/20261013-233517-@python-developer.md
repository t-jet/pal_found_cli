Subject: Implementation and developer verification
Created: 2026-10-13T23:35:17
Updated: 2026-10-13T23:35:17
---
## Implementation (2026-10-13)
- Compared OP_SPECS against the local SDK 1.101.0 source signatures. Exactly 18 operations have 37 required keyword inputs that the CLI previously treated as optional; attachment uploads infer or validate their three required values and remain unchanged.
- Marked these flags required in the Ontology parser. Missing flags fail before client creation with input exit code 1. _invoke still JSON-decodes supplied values and preserves empty objects or lists.
- Corrected the CLI inputs line in each of the 18 offline skill records. Existing examples still supply the required flags.
- Added regression cases for all 37 omissions and representative object/list payloads; updated the existing search pagination case with its required --select.

## Verification
- pytest tests/test_pal_found_ontologies_cli.py: 50 passed.
- Skills gate and documentation checks: 19 passed. Independent QA parsed all 67 Ontology examples with no failures.
- git diff --check: passed. Ruff check reports one unused EXIT_SERVER_ERROR import in the shared CLI file, outside this patch's parser/spec scope; parent agent owns concurrent error-handler work.

## Security review
No shell or dynamic Python evaluation added. Missing-input errors name flags only, without input values. Existing access-control guard and SDK invocation ordering remain intact. No credentials, network-on-import, or logging changes. Independent QA of omission matrix is pending.

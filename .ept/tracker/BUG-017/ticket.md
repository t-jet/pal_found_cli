---
id: BUG-017
type: bug
title: Ontology query attribution CLI incorrectly requires JSON string
status: Closed
affected_version: pal_found_cli_tool-worktree
created: 2026-10-12
updated: 2026-10-14
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
component: ontologies
---

# BUG-017: Ontology query attribution CLI incorrectly requires JSON string

## Description

# Ontology query attribution is parsed as JSON instead of a string

## Reproduction

In the current worktree, parse and invoke:

```bash
pal-found-ontologies query execute palantir myQuery --parameters '{}' --attribution my-app
```

`query.execute` lists `attribution` in `json_args`. `_invoke` calls `json.loads("my-app")` before the SDK method. The result is `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`, mapped by `main` to exit code 1. A parser and SDK-like invocation probe reproduces this without a Foundry connection: `.ept/tmp/ontology_input_probe.py` (temporary probe; command and result are stated here).

The local SDK defines `core_models.Attribution = str` and `Query.execute(... attribution: Optional[Attribution])`. A plain attribution value must pass as a string. JSON quoting can currently bypass the failure, but the CLI and record do not require that unusual encoding.

## Expected

Remove `attribution` from `query.execute` JSON arguments. Keep `parameters` JSON-decoded. Pass `--attribution my-app` to the SDK as `"my-app"`. Update the Ontology input guide and operation record to identify attribution as a scalar string, and test valid and malformed values through parser and invocation.

## Evidence

- `pal_found_cli_tool/src/pal_found_cli/ontologies/scripts/pal_found_ontologies_cli.py`: `query.execute` spec, `_coerce_arg`, `_invoke`, `main` error mapping.
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/core/models.py`: `Attribution = str`.
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/ontologies/query.py`: `execute` signature.
- Independent QA probe result: `JSONDecodeError`, exit code 1.

Related: TASK-006, FEATURE-012, DEV-STORY-053, WORK-005.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes

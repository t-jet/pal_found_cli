# ADR-004: Format Auto-Selection Algorithm

| Field | Value |
|---|---|
| **ID** | ADR-004 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The `--format auto` (and `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT=auto`) setting must select between JSON and TOON output without user specification. The formal rule from the requirements is:

> Use TOON when the top-level result is a list/array AND all items share a uniform field set. Use JSON in all other cases.

This ADR defines the precise algorithm implementing that rule, including all edge cases.

## Decision

The format auto-selection algorithm is as follows (evaluated in this order):

```
function select_format(data, format_setting):

  # 1. Explicit format always wins
  if format_setting in ("json", "toon"):
      return format_setting

  # format_setting == "auto" from here

  # 2. Errors always use JSON
  if data is an error envelope:
      return "json"

  # 3. Non-list top-level always uses JSON
  if data is not a list:
      return "json"

  # 4. Empty list uses JSON (cannot determine uniformity)
  if len(data) == 0:
      return "json"

  # 5. Extract field sets from all items
  field_sets = [frozenset(item.keys()) for item in data if isinstance(item, dict)]

  # 6. Any non-dict item in the list → use JSON
  if len(field_sets) != len(data):
      return "json"

  # 7. All items must share an identical field set
  if len(set(field_sets)) == 1:
      return "toon"
  else:
      return "json"
```

**Special cases:**

| Scenario | Format |
|---|---|
| Error envelope | Always JSON |
| Single object (dict) | JSON |
| Empty list `[]` | JSON |
| Uniform array of dicts | TOON |
| Mixed-type array `[dict, str, ...]` | JSON |
| Heterogeneous-field array `[{a,b}, {a,c}]` | JSON |
| Nested array of arrays | JSON |
| Binary download metadata envelope | Always JSON (never TOON) |
| Pagination metadata on stderr | Always JSON (never TOON, always stderr) |

## Rationale

- **Errors always JSON:** Errors have a well-defined schema agents rely on for error handling; TOON would disrupt existing error parsing logic
- **Empty list → JSON:** Cannot determine field uniformity without items; `[]` in JSON is unambiguous and trivially parseable
- **Strict key-set equality:** Partial uniformity (shared subset of keys) still results in variable-width TOON columns in practice; strict equality ensures TOON is always readable
- **Non-dict list items:** TOON is defined for tabular (dict) data only; lists containing scalars or nested lists are not candidates
- **Binary download → JSON:** These envelopes contain mixed types (path string, size int, checksum string, truncated bool) and are always single objects

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Select TOON if any items are dicts | Too permissive; would produce malformed TOON for mixed arrays |
| Select TOON if >50% of items are uniform | Partial uniformity confuses column alignment; strict equality is simpler and more predictable |
| Always request TOON from the TOON library and fall back | TOON library raises on non-uniform input; brittle; adds exception handling overhead |

## Consequences

- `_foundry_cli_common.py` output formatter must implement this algorithm before dispatching to `toon.from_list()` or `json.dumps()`
- The `toon-python` library must be called only with pre-validated uniform arrays
- Test suite must cover all 9 special cases in the table above
- Knowledge skill must document this algorithm so agents understand when to expect TOON vs JSON

## References

- SRS FR-OUT-5 through FR-OUT-7
- Q&A R3: A(Q3(R3).2-A, Q3(R3).2-B)
- `toon-python` library documentation

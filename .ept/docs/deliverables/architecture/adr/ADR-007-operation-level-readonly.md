# ADR-007: Operation-Level READONLY — No Independent Setting

| Field | Value |
|---|---|
| **ID** | ADR-007 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The access control model (SRS Section 4) defines namespace-level `READONLY` and an override mechanism (`{NS}_READONLY=false` overrides global `READONLY=true`). The question is: should individual operations also be independently settable to `READONLY=true`?

**Two interpretations of "operation-level READONLY":**

1. **Override only (current spec):** `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=false` overrides a parent `READONLY=true`. This is supported.

2. **Independent setting:** `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=true` blocks writes for *only* this operation even when global READONLY is `false`. This would be a new capability not currently in spec.

This ADR decides whether to support interpretation 2.

## Decision

**Operation-level `READONLY=true` as an independent setting is NOT supported.**

Only the following operation-level access control variables are supported:
- `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_ENABLED=true/false` — enable or disable the operation entirely
- `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=false` — override parent READONLY=true (grants write permission for this operation only)

An `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=true` setting where global/namespace READONLY is not already true SHALL be ignored (treated as the default, which is full access).

## Rationale

- **Complexity vs value:** Supporting independent operation-level READONLY requires classifying every operation as "read" or "write" — 355 operations @ ~3 env vars each = 1,065+ config entries. This classification must be maintained as the SDK evolves
- **Sufficient granularity at namespace level:** Namespace-level READONLY is the right granularity for access control. If an operator needs to block writes only to `datasets.dataset.put_schema`, they can set `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_ENABLED=false` instead, which is more explicit
- **Prevents accidental security gaps:** An operator who sets `datasets.dataset.put_schema` READONLY=true but forgets that `datasets.dataset.create` is also a write operation has a false sense of security. The `ENABLED=false` mechanism is more explicit and harder to misconfigure
- **Consistency with 8-step precedence model:** The model only defines operation-level READONLY as an *override* of a parent READONLY setting. Adding independent operation-level READONLY would require adding a Step 3.5 that doesn't exist in the agreed model

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Support independent operation-level READONLY=true | High complexity, low marginal value; `ENABLED=false` achieves the same result more clearly |
| Auto-classify operations as read/write using method name heuristics | Heuristics (`get_`, `list_`, `create_`, `delete_`) would misclassify ambiguous methods; maintenance burden |
| Support READONLY at operation level only as a future enhancement | Accepted — if demand emerges, add it then; explicitly deferring avoids premature complexity |

## Consequences

- The access control guard in `_foundry_cli_common.py` does NOT need to evaluate `{NS}_{CLASS}_{OP}_READONLY=true`
- The canonical env var reference table includes READONLY flags only at the namespace level (not operation level)
- Documentation must clearly state that operation-level write blocking is done via `ENABLED=false`
- If an `ENABLED=false` approach creates confusion (e.g., blocking read access to avoid writes), revisit this decision in a future sprint

## Status Review

This decision should be revisited after the first production deployment if operator feedback indicates a need for fine-grained write-blocking at the operation level without disabling reads.

## References

- SRS Section 4.2 — 8-Step Precedence Model
- SRS FR-ACL-5
- Q&A R3: A(Q3(R3).3, Q3(R3).4)

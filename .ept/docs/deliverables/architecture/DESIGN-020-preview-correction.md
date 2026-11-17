# Data Health preview parameter correction

| Field | Value |
| --- | --- |
| Scope | Six Data Health Check and CheckReport CLI operations |
| Original design | DESIGN-020, DEV-STORY-020 |
| Defect | BUG-034 |
| Baseline | Released tool `b9c5f8a`; `foundry-platform-sdk` 1.101.0 |
| Status | Design correction; implementation and independent QA pending |

## Decision

Pass `preview=True` to the SDK on every Data Health CLI operation: Check create, delete, get, replace; CheckReport get and get_latest. Keep the six existing commands and their inputs. Do not expose a user flag or forward `_sdk_internal`.

DESIGN-020 says to exclude preview parameters. This correction supersedes that instruction for the six operations above. Other DESIGN-020 contracts remain in force, including access control, write classification, the metadata-only policy, retry behavior, timeout, JSON input validation and result formatting.

The Palantir API reference identifies each endpoint as preview and instructs callers to add `preview=true` to the query string. The SDK 1.101.0 signatures expose `preview: Optional[bool]` on all six methods. The released CLI omits that argument. A mock transport captured a Check GET request without the query parameter and the same SDK call with `preview=True` serialized `?preview=true`. No enrolled tenant was called, so server rejection has not been observed directly.

The API schema labels the parameter optional, but its endpoint warning states how to use the preview endpoint. This design supplies the required value internally for the current API baseline. Reassess this decision when the pinned SDK or endpoint status changes.

## Verification

- Assert the URL of each of the six CLI requests contains `preview=true`, including calls with optional `intent` or `limit`.
- Assert existing argument validation, access controls, write set and metadata-only restrictions remain effective.
- Correct the Data Health skill guidance and examples so offline users can tell that the CLI opts into preview.
- Update TESTCASE-020, which currently forbids passing preview, and run independent QA against the tool and skill candidate before accepting BUG-034 or the affected FEATURE-015 work.

## Source and traceability

The six Palantir API references are [Create Check](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/checks/create-check), [Delete Check](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/checks/delete-check), [Get Check](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/checks/get-check), [Replace Check](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/checks/replace-check), [Get Check Report](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/check-reports/get-check-report), and [Get Latest Check Reports](https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/check-reports/get-latest-check-reports).

BUG-034 links this correction to historical DESIGN-020 and DEV-STORY-020, offline skill story DEV-STORY-048, and FEATURE-012/FEATURE-015. Closed tickets retain their historical decisions; BUG-034 carries the remediation and retest evidence.

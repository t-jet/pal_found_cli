# python-developer — improvement memory

## Improvement: circular-import when registering cross-module exception mappings

Condition:
- When adding an exception-class → exit-code (or similar) mapping inside `error_serializer` (or any low-level module) for an exception defined in a module that imports FROM that low-level module (e.g. `access_control_guard` imports `EXIT_ACCESS_CONTROL` from `error_serializer`).

Action:
- Do the import lazily inside the registration function (`_register_sdk_exceptions`) wrapped in try/except, never at module top level. This breaks the cycle because the function runs at import time only after the constants it depends on are already defined. Place the registration BEFORE any early `return mapping` in the same function so it always executes.

## Improvement: BUG-SUB-004 exit-code 8 gap pattern

Condition:
- When an exception type is documented in an exit-code taxonomy (ADR-001) with a constant (`EXIT_ACCESS_CONTROL = 8`) but `serialize()` returns the default code instead.

Action:
- Check `_EXCEPTION_TO_EXIT_CODE` map population and whether HTTP-classification fallback applies. No-HTTP-status exceptions (AccessControlError) must have an explicit map entry; the HTTP path cannot rescue them. Add a regression test that asserts BOTH the code AND the full stdout envelope (type, exit_code_name, message, call_id).

## Improvement: stdout-capture fixture is fragile for print_to_stdout=True

Condition:
- When writing an envelope test that uses the suite's `stdout_capture` autouse fixture with `print_to_stdout=True`.

Action:
- Do inline stdout capture (io.StringIO + try/finally restore) inside the test instead of relying on the shared fixture, which may be reset/ordered unpredictably across tests in the same class.

## Improvement: tests using a non-production calling convention can mask spec bugs

Condition:
- When a shared component has a canonical env-var transformation rule documented in the spec (e.g. SRS §5.2 `{NS}_{CLASS}_{OP}` kept verbatim) but existing unit tests call the component with a synthetic/humanised convention (e.g. `check("datasets", "create_dataset")` instead of `check("dataset", "create")`).

Action:
- Do align unit-test call arguments to the production calling convention that matches the env vars the tests set; don't let tests rely on internal verb-parsing heuristics to bridge the gap. When fixing a transformation bug, grep the test suite for ALL call sites of the affected method and verify each one matches its asserted env keys under the corrected code, because the old buggy behaviour may have made mismatched conventions pass by accident.

## Improvement: check isinstance(dict) before hasattr for dict-key extraction

Condition:
- When extracting a value from a response that can be either a dict or a Pydantic-style object, and the key name (e.g. "items", "next_page_token") could shadow a built-in dict method or vice versa.

Action:
- Do branch on `isinstance(response, dict)` (and `isinstance(response, list)`) BEFORE any `hasattr(response, <key>)` check, because every dict satisfies `hasattr(response, "items")` via its bound `.items()` method, returning the method object instead of the keyed value.

## Improvement: verify artifact/glob fixes against real build output, isolate with diff -w

Condition:
- When fixing a defect in a tracked config/workflow file (e.g. a publish.yml artifact glob), especially when the working tree already carries uncommitted whitespace or line-ending drift from earlier sessions.

Action:
- Do confirm the artifact format against real on-disk build evidence (e.g. `.ept/tmp/conda-channel` output) before editing, and confirm the change is content-only with `git diff -w` so pre-existing whitespace noise is not mis-attributed to your edit or accidentally broadened.

## Improvement: git diff --check flags CR at EOL when cr-at-eol not set

Condition:
- When fixing a trailing-whitespace gate failure (git diff --check) in a repo with mixed line endings (core.autocrlf=false, no .gitattributes, no cr-at-eol), where added lines end with CRLF while unchanged lines stay CRLF.

Action:
- Do strip trailing whitespace including the CR from the flagged added lines only (keep unchanged line endings intact), then re-verify with the exact gate command. Tools that append to project files (self-improvement memory appends, subagent memory updates) can re-introduce flagged lines, so re-run the strip and the gate after all such appends, as the last step.

## Improvement: hygiene test forbids `_cli.py`/`scripts/` in SKILL.md, not in references

Condition:
- When authoring doc-only skill content that splits operation detail into `references/*.md` and cites the CLI parser path (e.g. `.../scripts/pal_found_<ns>_cli.py`) as a source locator.

Action:
- Do keep parser/`scripts/` source locators OUT of `SKILL.md` (the repository-hygiene test scans only `pal-found-*/SKILL.md` for `python ..._cli.py` / `scripts/`) and place those source pins only in `references/*.md` parts, which the test does not scan.

## Improvement: batch `update --status` commands can ^C after already completing server-side

Condition:
- When running two chained tracker commands in one terminal call (e.g. `update --status Open; update --status "In Progress"`), the second can render as `^C` while the server already applied both transitions.

Action:
- Do verify actual current status with `get <id>` after a ^C in a chained batch before retrying; do not assume a failed transition. Re-running a now-invalid transition (`In Progress -> Open`) is the tell that the batch already succeeded.

## Improvement: validate CLI create arguments against SDK signature

Condition:
- When a CLI operation wraps an SDK create method and fails because a required SDK argument is absent.

Action:
- Do compare the local SDK docs and installed method signature, then test both parser requirement and exact async SDK call arguments.

## Improvement: preserve cursor semantics for SDK async iterators

Condition:
- When a CLI exposes page tokens for an SDK method returning `AsyncResourceIterator`.

Action:
- Do use the SDK's public raw-response wrapper to fetch and decode one page per request; test an empty page with continuation, the initial cursor, page bounds, and the returned next cursor across affected operations.

## Improvement: isolated SDK reader acceptance

Condition:
- When source-blind SDK reader task requires independent namespace acceptance

Action:
- Do copy owning skill into isolated snapshot, hash snapshot and prepared SDK, run public composed FoundryClient routes through denied-network fake transport, and label detached resource fixtures as smoke only.

## Improvement: inspect iterator API before rejecting page access

Condition:
- When SDK method annotation says `ResourceIterator` but guide reads `.data` or `.next_page_token`.

Action:
- Do inspect iterator class properties and page-fetch timing, then run guide call through composed client MockTransport before filing route defect. Return annotation alone insufficient.

## Improvement: measure example coverage without test files

Condition:
- When docs examples need unit coverage but hosted runtime modules unavailable.

Action:
- Do measure non-test modules with `coverage report --omit '*test*.py'`; invoke actual entry points through narrow dependency stubs and assert rows, modes, and failures. Label hosted runtime unexecuted.

## Improvement: semantic schema checks before example writes

Condition:
- When prepared-runtime example groups or sums pandas values before a dataset write.

Action:
- Do test nonnumeric input and output values against actual example code; reject wrong types before write with a check that still runs under optimized Python. Coverage percent alone cannot prove valid output schema.

## Improvement: SDK source fences versus offline reader prose

Condition:
- When generating offline API model pages from SDK definitions containing public links or placeholder comments

Action:
- Do keep exact SDK source in fenced blocks, add complete local meaning in reader prose, and record per-symbol source/page hashes with independent review pending. When a Python alias is `Any`, check pinned SDK documentation for type/encoding tables and emit source-backed valid JSON examples plus documentation hash. Do check source fidelity separately from prose tests that normalize optional attribution links.


## Improvement: root SDK mock transport must cover lazy clients

Condition:
- When testing an operation through public FoundryClient with a patched HTTP-client constructor

Action:
- Do keep constructor patch active through nested resource access and request; root client constructs resource clients lazily. Assert fake transport handled request before claiming offline success.

## Improvement: compare inventories to distributed records

Condition:
- When testing preservation of documented operation IDs against frozen baseline

Action:
- Do extract IDs from actual distributed operation headings and compare exact sorted hash; don't hash another frozen constant as the "actual" result.

## Improvement: uncertain REST write fixture

Condition:
- When offline SDK guidance handles a lost upload or commit reply

Action:
- Do mutate fake server state before raising transport timeout, reconcile through known RID and staged or branch reads, and assert exactly one mutation; never let a passing fixture hide automatic replay.

## Improvement: unmeasured ticket time

Condition:
- When subtask DoD requires time in frontmatter but actual contributor hours were not measured

Action:
- Do record time as untracked in ticket comment and ask manager for workflow treatment before Resolved; don't invent hours or set numeric zero.

## Improvement: integer request timeout cannot certify wall deadline

Condition:
- When SDK request timeout accepts positive whole seconds and app promises a shorter elapsed-time budget.

Action:
- Do stop before call if fewer than one whole second remains; pass integer timeout no greater than remaining whole seconds; recheck clock after response before claiming complete. Preserve partial result on overrun and test slow or noncooperative transport. Don't promise hard preemption of a blocking call.


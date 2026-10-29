# WORK-006 offline reader exercise

Date: 2026-10-12. Scope: FEATURE-012, with a focused retest of BUG-009.

## Setup and limits

Copied all 20 folders from `pal_found_cli_skills/.agents/skills` to `.ept/tmp/work006_skills_copy`. Read the copy and the installed `pal-found-* --help` output. Public web and Foundry tenant access were not used. The probe at `.ept/tmp/work006_probe.py` calls actual installed CLI parsers, argument validation, pagination, dispatch, and error serialization with mocked SDK responses. This is a temporary probe; the inputs, responses, and assertions below are the durable record. No live platform change occurred.

SHA-256 matches between copy and source: general output guide `78CF60CE830EF2E64DCF0DC821B77CAC03A4E17F0C425D99D7564F2CB6593A9B`; dataset file guide `A638ADE43371FBB9A842D6EC16F975CEA41D2F2D0173F3E3B333D5B35B4E1BAD`; orchestration build guide `5D617CC702605048416666BDE559EC068B414B4CB881A38F3911C1416AB5034A`.

Commands: `python .ept/tmp/work006_probe.py` exited 0; `python -m pytest pal_found_cli_tool/tests/test_pagination_helper.py -q` returned 27 passed; `python -m pytest pal_found_cli_skills/tests/test_offline_skill_gate.py -q` returned 9 passed. Installed help for the selected datasets, orchestration, AIP Agents, Data Health, and Streams operations exited 0 and confirmed the flags used below. A `requests` dependency warning appeared on stderr; it did not change command exit status.

## Cases

Each prompt below is the task presented to the reviewer. The interpretation is the recorded answer after reading copied guidance and installed help. Synthetic RIDs identify mocked resources.

### W006-01: Empty first page with continuation

Prompt: "List `reports/` files in dataset `ri.foundry.main.dataset.11111111-1111-4111-8111-111111111111`. First response has no items but a continuation token. Is the folder empty?"

Selected command: `pal-found-datasets file list <dataset-rid> --path-prefix reports/ --page-size 1`. Mocked SDK page 1: `{"data":[],"next_page_token":"cursor-2"}`. Next command adds `--page-token cursor-2`; mocked page 2: `{"data":[{"path":"reports/oct.csv"}],"next_page_token":null}`. Actual parser and `_invoke_paginated` sent `path_prefix="reports/"`, `page_size=1`, and page tokens `null` then `cursor-2` to SDK mock. CLI helper returned `[]` with `cursor-2`, then one file with no continuation.

Predicted effect: read file metadata only; no dataset change. Interpretation: first page is inconclusive; after page 2, at least one matching file exists and pagination is exhausted. Expected and observed match. **PASS.** This retests BUG-009 using the copied corrected primer and `PaginationHelper`.

### W006-02: Start a one-time build

Prompt: "Start a build for the dataset on `master`. Tell me whether computation finished."

Selected command: `pal-found-orchestration build create --target-json '{"type":"manual","targetRids":["ri.foundry.main.dataset.11111111-1111-4111-8111-111111111111"]}' --fallback-branches-json '[]' --branch-name master`. The actual parser and `_validate_inputs` converted JSON to an object and list. SDK mock received `target`, `fallback_branches=[]`, `branch_name="master"`, and `request_timeout=30`. Mocked response: `{"rid":"ri.foundry.main.build.22222222-2222-4222-8222-222222222222","status":"RUNNING"}`.

Predicted effect: Foundry accepts a one-time build request and may run jobs; this response does not prove completion. Interpretation: build is running; use `pal-found-orchestration build get <build-rid>` and `build jobs <build-rid>` to check completion and failures. Expected and observed match. **PASS.**

Follow-up probe: `build get <build-rid>` called the mocked SDK with that RID and returned `{"rid":"ri.foundry.main.build.22222222-2222-4222-8222-222222222222","status":"FAILED"}`. The correct final statement is that this build failed; inspect `build jobs` for job-level cause. This follow-up passed the parser and dispatch assertions. **PASS.**

### W006-03: Foundry permission failure

Prompt: "A file upload returns `PermissionDeniedError`, exit 3, message `Forbidden`. Did the upload succeed and what should change?"

Mocked exception: `PermissionError("Forbidden")`. Actual `ErrorSerializer` produced `{"error":true,"exit_code":3,"exit_code_name":"PermissionDeniedError","message":"Forbidden","exception_type":"PermissionError"}`. Predicted effect: request denied; no successful upload is established. Interpretation: ask for Foundry resource permission, then retry and verify the file/transaction state. Expected and observed match. **PASS.** This uses a local permission exception, not a live HTTP 403 response.

### W006-04: Local access-control block

Prompt: "A `file upload` attempt returns `AccessControlError`, exit 8, message `Read-only mode blocked file.upload`. Should I request Foundry access?"

Mocked exception: `AccessControlError(..., step=4)`. Actual serializer produced `{"error":true,"exit_code":8,"exit_code_name":"AccessControlError","message":"Read-only mode blocked file.upload"}`. Predicted effect: local policy prevents the call before a successful Foundry write. Interpretation: inspect local read-only/access-control configuration; changing Foundry permissions alone would not remove this block. Expected and observed match. **PASS.** The full `AccessControlGuard` decision path was not invoked in this case.

### W006-05: Invalid JSON input

Prompt: "`build create` receives `--target-json '{bad'`. Is the build queued?"

Actual parser accepted the string, then `_validate_inputs` rejected it before SDK dispatch. Actual serializer produced `{"error":true,"exit_code":1,"exit_code_name":"UserInputError","message":"target must contain valid JSON"}`. Predicted effect: no build request. Interpretation: correct JSON syntax and rerun; only a returned Build RID can establish acceptance. Expected and observed match. **PASS.**

### W006-06: HTTP status distinctions

Prompt: "An SDK response carries HTTP 403, 404, or 429. What can I conclude?" A local exception stub carried `response.status_code` through the real error serializer. Actual classifications were 403 to exit 3 `PermissionDeniedError`, 404 to exit 4 `NotFoundError`, and 429 to exit 7 `RateLimitExhausted`. Interpretation: 403 requires Foundry access review; 404 requires RID/path check; 429 requires backoff after retries. None proves a write succeeded. Each exact exit assertion passed. **PASS.** This validates status classification, not live retry timing.

### W006-07: Read-only guard decision

Prompt: "The local CLI has `FOUNDRY_AGENTIC_CLI_READONLY=true`. Can `datasets.file.upload` reach Foundry?" The actual `AccessControlGuard.check("file", "upload")` raised `AccessControlError` with exit 8 and precedence step 5. The expected interpretation is local rejection before a write. **PASS.** This covers the global read-only path; other precedence branches still rely on existing guard tests.

### W006-08: Created Data Health check without a report

Prompt: "`check create` returned a Check RID. `check-report get-latest CHECK_RID --limit 5` returned an empty collection. Did the check pass?" The actual installed parser and validation accepted `--limit 5`; SDK mock received the Check RID and `limit=5`, then returned `{"data":[]}`. Predicted effect: rule creation saves a check, while `get-latest` reads prior evaluations and causes none. Interpretation: no report establishes either healthy or unhealthy status; wait for evaluation and inspect its result. The isolated reader made that distinction and suggested `check get` to inspect the saved rule. **PASS.**

### W006-09: Commit a processed Streams offset

Prompt: "A subscriber read partition 0 record at offset 50 without `--auto-commit`. Processing succeeded. How does the caller advance its stored position?" The actual installed parser and validation accepted `subscriber commit-offsets DATASET_RID master worker-1 --offsets-json '{"0":50}'`. SDK mock received `offsets={"0":50}` and returned `{"0":51}`. Predicted effect: subscriber checkpoint advances; stream records remain. Interpretation: JSON value is last processed offset; next read starts at 51. The isolated reader also warned that committing 50 while earlier records remain unprocessed would skip them and advised matching `--view-rid` if the read pinned a view. **PASS.**

## Isolated novice reader

A separate agent received no prior conversation. Its allowed task sources were the copied skill folders and installed CLI help. It could not read the original skill tree, CLI source, tests, tracker, project documents, public web, or a live Foundry tenant. It reported consulting the copied general, datasets, orchestration, and AIP Agents skills and their linked local parts, plus installed help for the selected operations. The following records its answers against the six prompts sent to it; names and sample RIDs remain synthetic.

| Prompt | Recorded reader answer | Expected decision | Verdict |
| --- | --- | --- | --- |
| List `reports/` files; first page `[]` with `cursor-2`, next page `reports/oct.csv` without token. | Chose `pal-found-datasets file list DATASET_RID --path-prefix reports/`, then `--page-token cursor-2`; first empty page is inconclusive, second closes listing with one match. | Continue until token exhausted; read only. | PASS |
| `build create` returns RID and `RUNNING`; later `build get` returns `FAILED`. | Chose `pal-found-orchestration build create` with `--target-json` and `--fallback-branches-json`, then `build get`; start response is not completion, later response establishes failed build; inspect `build jobs`. | Separate accepted start from final failure. | PASS |
| Dataset `file upload` gives `PermissionDeniedError`, exit 3. | Chose `file upload` with local path, identified Foundry permission denial, asked for dataset/branch access and file-state verification. | Do not claim upload; distinguish service permission. | PASS |
| Same upload gives `AccessControlError`, exit 8. | Identified local CLI enabled/readonly/metadata-only controls and stated that this call made no Foundry write. | Distinguish local guard from HTTP 403. | PASS |
| `build create` has malformed `--target-json`, exit 1. | Identified user input failure before a build starts; correct JSON and check returned Build RID after rerun. | Do not claim queued build. | PASS |
| AIP `session blocking-continue` succeeds; `session-trace get` returns 403. | Used alias and JSON user input; concluded exchange completed, but trace steps remain unknown. Chose `content get --alias` for permitted conversation content and requested trace access only if needed. | Trace denial does not negate exchange or reveal trace internals. | PASS |
| Data Health `check create` returns RID; latest report list is empty. | Chose `check create --config-json` then `check-report get-latest CHECK_RID --limit 5`; empty reports mean no evaluation result, not a passing check. | Rule saved; health unknown until evaluation. | PASS |
| Streams read offset 50 without auto commit; processing succeeded. | Chose `subscriber commit-offsets ... --offsets-json '{"0":50}'`; expected next read offset 51 and recommended `get-read-position` verification. | Commit last processed offset after processing. | PASS |

Reader also checked that installed `session-trace` uses a hyphen; `session_trace` was rejected by help. It supplied `--parameter-inputs-json '{}'` for AIP only when the agent has no required application variables. Those are correct conditional input choices. The reader did not execute a tenant operation. This is an independent task-choice and interpretation check across five namespace skills, not a 351-operation semantic audit.

## TESTEXEC-055 reconciliation and scope

TESTEXEC-055's closed result comment says `record completeness sample | PASS | checked None/None`, `300-line leaf limit | PASS | max leaf 0 lines`, and `examples=-` in every namespace. Those values do not substantiate its recorded offline reader PASS. The nine tests in `test_offline_skill_gate.py` are structural; they do not run these five interpretation cases. This report supplies five narrow independent cases and does not retroactively validate the full TESTEXEC-055 claim.

Nine of nine executable case groups and eight of eight isolated reader answers pass. The sample spans datasets, orchestration, AIP Agents, Data Health, and Streams. The independent 351-operation semantic audit belongs to other TASK-006 work items. This report does not validate all FEATURE-012 operations.

## Reproduction probe

Copy the skill folders to `.ept/tmp/work006_skills_copy`, save this code as `.ept/tmp/work006_probe.py`, then run `python .ept/tmp/work006_probe.py`. It uses only local CLI modules and SDK mocks.

```python
"""Temporary offline probe for WORK-006; durable outcomes go in QA evidence."""

import asyncio
import contextlib
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pal_found_cli_tool" / "src"))

from pal_found_cli.common.pagination_helper import PaginationHelper
from pal_found_cli.common.error_serializer import ErrorSerializer
from pal_found_cli.common.access_control_guard import AccessControlError, AccessControlGuard
from pal_found_cli.datasets.scripts import pal_found_datasets_cli as datasets
from pal_found_cli.orchestration.scripts import pal_found_orchestration_cli as orchestration
from pal_found_cli.data_health.scripts import pal_found_data_health_cli as data_health
from pal_found_cli.streams.scripts import pal_found_streams_cli as streams

COPY = ROOT / ".ept" / "tmp" / "work006_skills_copy"


async def main():
    primer = (COPY / "pal-found" / "references" / "03-output-success-failure.md").read_text(encoding="utf-8")
    file_record = (COPY / "pal-found-datasets" / "references" / "03-file.md").read_text(encoding="utf-8")
    build_record = (COPY / "pal-found-orchestration" / "references" / "01-build-job.md").read_text(encoding="utf-8")
    assert "An empty page is valid, even when a next-page" in primer
    assert "Continue until no token remains" in primer
    assert "An empty page is not proof there are no more results" in file_record
    assert "The returned Build is a start response" in build_record

    pages = [
        SimpleNamespace(decode=lambda: SimpleNamespace(data=[], next_page_token="cursor-2")),
        SimpleNamespace(decode=lambda: SimpleNamespace(data=[{"path": "reports/oct.csv"}], next_page_token=None)),
    ]
    sdk_list = AsyncMock(side_effect=pages)
    client = SimpleNamespace(with_raw_response=SimpleNamespace(list=sdk_list))
    rid = "ri.foundry.main.dataset.11111111-1111-4111-8111-111111111111"
    args1 = datasets.build_parser().parse_args(["file", "list", rid, "--path-prefix", "reports/", "--page-size", "1"])
    helper1 = PaginationHelper(page_size=1, batch_pages=1)
    first = await datasets._invoke_paginated("file", "list", client, args1, 30, helper1)
    assert first == [] and helper1.next_page_token == "cursor-2"
    args2 = datasets.build_parser().parse_args(["file", "list", rid, "--path-prefix", "reports/", "--page-size", "1", "--page-token", helper1.next_page_token])
    helper2 = PaginationHelper(page_size=1, page_token=helper1.next_page_token, batch_pages=1)
    second = await datasets._invoke_paginated("file", "list", client, args2, 30, helper2)
    assert second == [{"path": "reports/oct.csv"}] and helper2.next_page_token is None
    assert sdk_list.await_args_list[0].kwargs["page_token"] is None
    assert sdk_list.await_args_list[1].kwargs["page_token"] == "cursor-2"

    target = {"type": "manual", "targetRids": [rid]}
    bargs = orchestration.build_parser().parse_args(["build", "create", "--target-json", json.dumps(target), "--fallback-branches-json", "[]", "--branch-name", "master"])
    build_rid = "ri.foundry.main.build.22222222-2222-4222-8222-222222222222"
    create_client = SimpleNamespace(create=AsyncMock(return_value={"rid": build_rid, "status": "RUNNING"}))
    spec = orchestration.OPERATION_BY_RESOURCE["build"]["create"]
    orchestration._validate_inputs(spec, bargs)
    started = await orchestration._invoke(spec, create_client, bargs, 30)
    assert started["status"] == "RUNNING"
    assert create_client.create.await_args.kwargs["target"] == target
    assert create_client.create.await_args.kwargs["fallback_branches"] == []
    assert create_client.create.await_args.kwargs["branch_name"] == "master"
    assert create_client.create.await_args.kwargs["request_timeout"] == 30

    get_args = orchestration.build_parser().parse_args(["build", "get", build_rid])
    get_spec = orchestration.OPERATION_BY_RESOURCE["build"]["get"]
    orchestration._validate_inputs(get_spec, get_args)
    get_client = SimpleNamespace(get=AsyncMock(return_value={"rid": build_rid, "status": "FAILED"}))
    final_build = await orchestration._invoke(get_spec, get_client, get_args, 30)
    assert final_build["status"] == "FAILED"
    assert get_client.get.await_args.args == (build_rid,)

    check_rid = "ri.data-health.main.check.33333333-3333-4333-8333-333333333333"
    hargs = data_health.build_parser().parse_args(["check-report", "get-latest", check_rid, "--limit", "5"])
    hspec = data_health.OPERATION_BY_RESOURCE["check_report"]["get_latest"]
    data_health._validate_inputs(hspec, hargs)
    hclient = SimpleNamespace(get_latest=AsyncMock(return_value={"data": []}))
    empty_reports = await data_health._invoke(hspec, hclient, hargs, 30)
    assert empty_reports == {"data": []}
    assert hclient.get_latest.await_args.args == (check_rid,)
    assert hclient.get_latest.await_args.kwargs == {"limit": 5, "request_timeout": 30}

    sargs = streams.build_parser().parse_args(["subscriber", "commit-offsets", rid, "master", "worker-1", "--offsets-json", '{"0":50}'])
    sspec = streams.OPERATION_BY_RESOURCE["subscriber"]["commit_offsets"]
    streams._validate_inputs(sspec, sargs)
    sclient = SimpleNamespace(commit_offsets=AsyncMock(return_value={"0": 51}))
    committed = await streams._invoke(sspec, sclient, sargs, 120)
    assert committed == {"0": 51}
    assert sclient.commit_offsets.await_args.args == (rid, "master", "worker-1")
    assert sclient.commit_offsets.await_args.kwargs == {"offsets": {"0": 50}, "request_timeout": 120}

    cfg = SimpleNamespace(global_readonly=False, global_metadata_only=False, global_enabled=True)
    with patch.dict(os.environ, {"FOUNDRY_AGENTIC_CLI_READONLY": "true", "FOUNDRY_AGENTIC_CLI_ENABLED": "true"}):
        guard = AccessControlGuard(cfg, "DATASETS")
        try:
            guard.check("file", "upload")
        except AccessControlError as exc:
            guard_step = exc.step
            assert exc.exit_code == 8 and guard_step == 5
        else:
            raise AssertionError("Read-only guard allowed upload")

    class HttpError(Exception):
        def __init__(self, status):
            super().__init__(f"HTTP {status}")
            self.response = SimpleNamespace(status_code=status)

    failures = []
    for label, exc, expected in (
        ("foundry_permission", PermissionError("Forbidden"), 3),
        ("local_acl", AccessControlError("Read-only mode blocked file.upload", step=4), 8),
        ("sdk_http_403", HttpError(403), 3),
        ("sdk_http_404", HttpError(404), 4),
        ("sdk_http_429", HttpError(429), 7),
    ):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = ErrorSerializer(call_id="work006").serialize(exc)
        envelope = json.loads(output.getvalue())
        assert code == expected and envelope["exit_code"] == expected
        failures.append({"case": label, "exit_code": code, "error": {key: envelope[key] for key in ("exit_code_name", "message", "exception_type")}})

    invalid = orchestration.build_parser().parse_args(["build", "create", "--target-json", "{bad", "--fallback-branches-json", "[]"])
    try:
        orchestration._validate_inputs(spec, invalid)
    except ValueError as exc:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = ErrorSerializer(call_id="work006").serialize(exc)
        assert code == 1
        envelope = json.loads(output.getvalue())
        failures.append({"case": "bad_json", "exit_code": code, "error": {key: envelope[key] for key in ("exit_code_name", "message", "exception_type")}})
    else:
        raise AssertionError("Invalid JSON was accepted")

    print(json.dumps({
        "copy_guidance": "pass",
        "pagination": {"first_items": first, "first_next_page_token": helper1.next_page_token, "second_items": second, "second_next_page_token": helper2.next_page_token, "sdk_calls": [call.kwargs for call in sdk_list.await_args_list]},
        "build": {"response": started, "final_response": final_build, "sdk_kwargs": create_client.create.await_args.kwargs},
        "guard_step": guard_step,
        "data_health": {"response": empty_reports, "sdk_kwargs": hclient.get_latest.await_args.kwargs},
        "streams": {"response": committed, "sdk_kwargs": sclient.commit_offsets.await_args.kwargs},
        "failures": failures,
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

```

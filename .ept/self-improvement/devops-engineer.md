# DevOps Engineer Improvement Memory

## Improvement: create venvs without pip bootstrap to survive terminal displacement

Condition:
- When creating scratch virtual environments for packaging verification on a shared Windows PowerShell host where parallel agents displace the terminal (KeyboardInterrupt during `python -m venv` ensurepip)

Action:
- Do create with `python -m venv --without-pip <env>` then `python -m ensurepip --upgrade` in a separate call, and verify `pip --version` before installing. Reconfirmed on DEVOPS-023 (2026-08-11): three sequential `python -m venv` calls were interrupted mid-ensurepip, leaving a venv whose pip was missing/corrupted (wheel env had to be recreated). Don't chain venv creation with installs in one command.

## Improvement: isolate multi-step verification from shared-terminal ^C churn

Condition:
- When running sequential verification steps (secret scans, hash compares, env diffs) on a shared PowerShell terminal where parallel agents keep interrupting commands with ^C

Action:
- Do wrap multi-step checks in a single `python -c`/script file executed in one call, or capture with `*> log` + Start-Process, rather than long PowerShell pipelines. Reconfirmed on DEVOPS-023 (2026-08-11): a 3-check PowerShell command was interrupted three times; the equivalent `secret_scan.py` ran in one shot.

## Improvement: verify CI pipeline actually enforces security scans

Condition:
- When reviewing or wiring a CI/CD pipeline for new code

Action:
- Do check that security scan steps (bandit, safety, SAST) actually fail the build on HIGH+ severity findings. Treat `|| true`, non-blocking scan settings, or missing severity enforcement as readiness blockers; don't report a security stage as passing when findings cannot fail CI.

## Improvement: distinguish DevOps scope from Developer scope during pipeline verification

Condition:
- When CI pipeline verification reveals lint/type errors in application code

Action:
- Do NOT patch the application code inline. Do flag the issues, transition the DevOps ticket to Blocked (with a Blocks link to the Developer's ticket), and document the specific file:line failures so the Developer can fix them. Do complete and document the DevOps-owned deliverables (workflow file, env templates, packaging config) before transitioning.

## Improvement: confirm bandit flag semantics before committing CI changes

Condition:
- When changing bandit invocation flags in a CI workflow

Action:
- Do verify flag syntax locally before committing (`bandit --help` shows `-l` is severity alias but `--severity-level high` is the explicit form). Don't assume `-ll` means "HIGH only" — it actually means "LOW or higher" (reports everything). Test the command locally and confirm exit codes.

## Improvement: obey first-call memory preflight

Condition:
- When starting any devops-engineer task

Action:
- Do make first assistant action and first tool call a single-purpose read of self-improvement skill and devops memory only, even when a parent task or another instruction says to load an agent file first. Don't send commentary, read agent files, or batch repo, workflow, or skill reads before memory load finishes. If missed, read memory immediately and follow it before any more task work.

## Improvement: handle user ticket constraints over default ticket gate

Condition:
- When user explicitly says no ticket writes or no subagents during DevOps validation

Action:
- Do state conflict after memory preflight, then perform local repo validation only. Don't call ticket-helper or mutate tracker state.

## Improvement: fallback when ticket-helper unavailable for read-only readiness

Condition:
- When a DevOps readiness task needs ticket context but ticket-helper cannot be spawned due agent/thread limits and user forbids tracker mutation

Action:
- Do use documented read-only tracker CLI commands only, state the fallback, and avoid tracker writes. Don't inspect tracker internals or create comments/links/status changes.

## Improvement: include author on tracker writes

Condition:
- When asking ticket-helper to update, comment, transition, or otherwise write tracker state

Action:
- Do include `author=devops-engineer` in the ticket-helper request. Don't send tracker write requests without author; they fail validation and waste a round trip.

## Improvement: pick DependsOn vs Blocks when recording New→Open blockers

Condition:
- When satisfying the New→Open DoD item "blockers identified and recorded" for a DEVOPS sub-task whose downstream work depends on a QA sibling

Action:
- Do use a DependsOn link (not Blocks) when parallel triage work (wheel/sdist inspection, CI workflow audit, dependency-scan strictness check, packaging config review) can start now and only the final CI matrix + coverage evidence is downstream-gated. Do reserve Blocks for cases where no triage work can proceed until the target resolves. Don't transition to Blocked; precede the link with "DependsOn records execution-order only, not a hard stop."

## Improvement: smoke installed console scripts

Condition:
- When validating Python package release readiness for CLI entry points

Action:
- Do install the built wheel into a clean venv and run each console script smoke command. Treat wrappers that depend on repo-only paths, missing runtime dependencies, or async entry points wired directly in `[project.scripts]` as release blockers.

## Improvement: prune stale dependency links before closure

Condition:
- When a DependsOn or Blocks link was created at New/Open triage to satisfy "blockers identified" and its target has since closed or otherwise reached terminal status, and the current ticket is approaching Resolved or Closed (Closed DoD = no active blocking links)

Action:
- Do re-query `link list <ticket>` before each closure-side transition and check the status of each DependedOn/BlockedBy target, not just the link's existence. Link output does not auto-flag a closed target as stale. Do remove stale outbound DependsOn / resolved inbound Blocks links before claiming the Closed DoD "no active is-blocked-by links" is met — a stale DependsOn does not literally satisfy "is-blocked-by" but leaks stale gating evidence into the record. Don't leave a closed-target DependsOn in place hoping the DoD check ignores it.

## Improvement: reproduce CI bootstrap before dependency scan

Condition:
- When local dependency scan results differ from expected CI readiness

Action:
- Do apply CI's package-tool bootstrap order first, then rescan. Record both results. Don't attribute vulnerabilities in stale venv `pip` or `setuptools` to project dependencies when CI upgrades those tools before scanning.

## Improvement: provision dependencies for nested venv tests

Condition:
- When a test creates a nested venv with `--system-site-packages` and installs a wheel with `--no-deps`

Action:
- Do remember nested venv reads base interpreter system/user sites, not parent venv packages. Use an isolated temporary `PYTHONUSERBASE` for required dependencies when repository edits and global installs are forbidden; verify imports from that path before rerunning. For uv-managed Python (PEP 668) add `--break-system-packages --user` to the pip install; confirmed on Python 3.12.9 (DEVOPS-013/014) and Python 3.12.0 (DEVOPS-017/018, `d:/app/Python-3.12`): nested-venv test failed with `ModuleNotFoundError: dotenv`, passed after provisioning `python-dotenv`+`requests` into `PYTHONUSERBASE`.

## Improvement: verify venv interpreter version before per-version gates

Condition:
- When running Python version-specific gates (3.11/3.12 matrix) from a scratch venv

Action:
- Do run `<venv>/Scripts/python.exe --version` and confirm the actual interpreter before executing gates. Don't assume a venv created from the repo venv base is the intended version; on DEVOPS-017/018 (2026-08-10) the "env312" venv was built from the 3.11 repo venv and ran 3.11.9, silently invalidating the first 3.12 gate until recreated from the real `d:/app/Python-3.12` binary. Also record the real interpreter version in reports (3.12.0, not "3.12.9").

## Improvement: isolate release candidate from dirty worktree

Condition:
- When release verification names a final commit but shared worktree contains unrelated changes

Action:
- Do build and test a clean `git archive` of final commit, confirm required precursor commits are ancestors, and use parent before first feature commit as rollback baseline. Don't copy dirty worktree files into candidate unless scope explicitly names them as release artifacts.

## Improvement: handle parent story auto-transition on DEVOPS close

Condition:
- When closing the last DEVOPS sub-task and the parent DEV-STORY is in Deployment status with all sibling sub-tasks already terminal

Action:
- Do expect the parent to auto-transition Deployment→Resolved after the DEVOPS close, and treat Resolved→Closed of the parent as a separate validated step (all sub-tasks Closed, no blockers, release notes present) before executing it. Don't pre-close the parent before the DEVOPS sub-task reaches terminal; confirmed on DEV-STORY-014/DEVOPS-014 (2026-08-10): story went Deployment→Resolved→Closed only after DEVOPS-014 Closed.

## Improvement: pass all evidence in one evidence comment per DEVOPS ticket

Condition:
- When documenting deployment evidence on a DEVOPS ticket per the DEVOPS-010/011/012 pattern

Action:
- Do record build/install/smoke/gates/rollback + deployment steps + DoD confirmation in a single evidence comment (with \n-escaped markdown) and then chain Resolved→Closed; the evidence comment ID is the DoD proof. Confirmed on DEVOPS-013/014/015/016 (2026-08-10) with evidence comments 20260810-011301/011251/052508/052414-devops-engineer; all closed with time_spent_hours=1.0 and stale DependsOn links removed first.

## Improvement: use forward slashes for Windows paths in ticket comment bodies

Condition:
- When asking ticket-helper to create a comment whose body contains a Windows filesystem path (e.g. T:\tmp\...)

Action:
- Do write the path with forward slashes (T:/tmp/...) in the comment body text. The tracker CLI decodes escape sequences, so \t becomes a TAB and the stored path is corrupted; double backslashes leave a stray backslash. Confirmed on DEVOPS-015 plan comment (aborted, path corrupt) and DEVOPS-016 plan/steps/evidence comments (forward slashes stored byte-perfect).

## Improvement: scrub FOUNDRY* env vars before test runs after ACL verification

Condition:
- When ACL metadata-only verification sets FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true in the shared PowerShell session and a subsequent pytest run follows in the same session

Action:
- Do remove FOUNDRY_AGENTIC_CLI_METADATA_ONLY (and FOUNDRY_HOSTNAME, FOUNDRY_TOKEN, FOUNDRY_INCLUDE_TRACEBACK) before running tests. The leaked flag caused 16 focused-suite failures (exit 8 AccessControlError on write ops) until scrubbed; after scrubbing all 57 tests passed.

## Improvement: verify launchers exist after fresh-venv wheel install

Condition:
- When installing a built wheel into a brand-new venv and the install output shows dependencies resolving but no foundry-* console launchers appear in Scripts/

Action:
- Do force-reinstall the wheel (pip install --force-reinstall with the wheel path) and re-check Scripts/ before smoke testing. A silent partial install (deps only, no package, no launchers) occurred on DEVOPS-015/016; force-reinstall fixed it. Never trust "Successfully installed" from a cached/partial resolution without checking launcher files exist. On DEVOPS-021/022 (2026-08-11) the silent partial install recurred via a DIFFERENT trigger — terminal displacement between the pip install command and the verification step; the tell was `pip list` showing no `foundry-cli` row. Always confirm `pip list` contains foundry-cli and launchers exist after any editable/wheel install before running tests or smoke.

## Improvement: provision PYTHONUSERBASE deps into the same userbase the harness will use

Condition:
- When a nested-venv harness test (--system-site-packages, wheel --no-deps) must import dotenv/requests and the run sets PYTHONUSERBASE to an isolated directory

Action:
- Do pip install --break-system-packages --user with the SAME `PYTHONUSERBASE` env var exported, and verify the packages land under `<userbase>/Python<ver>/site-packages`, not the default Roaming user site. On DEVOPS-021/022 (2026-08-11) provisioning into the default user site did not help the nested venv, because the run exported a different PYTHONUSERBASE; the failure was `ModuleNotFoundError: dotenv` in `foundry-audit.exe --help` until the isolated userbase itself was provisioned.

## Improvement: use subprocess for JSON-arg CLI probes instead of PowerShell direct invocation

Condition:
- When probing a CLI that takes structured JSON arguments (--config-json, --where-json, --records-json) from a PowerShell terminal, or when piping launcher output through Select-Object

Action:
- Do run the installed launcher via `python -c`/a probe script using `subprocess.run([...], capture_output=True)` so JSON values pass verbatim and exit codes are exact. Don't pass JSON as a PowerShell positional argument (quotes get stripped -> local validation exits 1 instead of the expected ACL/network code) and don't pipe the exe through Select-Object (it corrupts $LASTEXITCODE). Confirmed on DEVOPS-019/020 (2026-08-10): `check create --config-json {...}` gave exit 1 instead of 8 until run via subprocess; first ACL probe exits were misread through pipes.

## Improvement: SearchCheckpointRecordsRequest wraps filter under "filter"

Condition:
- When invoking foundry-checkpoints `record search --where-json` with an eq filter

Action:
- Do pass the request object, not the bare filter: `{"filter": {"type": "eq", "field": "recordRid", "value": "ri.checks.main.record.xxx"}}`. The SDK `search(where=SearchCheckpointRecordsRequest)` builds `SearchRecordsRequest(where=where)` from it; a bare `{"type":"eq",...}` fails SDK validation with exit 1. Valid eq fields: recordRid, configRid, checkpointType, actingUserId, delegateUserId, organizationRid, namespaceRid, interactionRid, checkpointedItemType (DEVOPS-019 probe, 2026-08-10).

## Improvement: diagnose missing-submodule-mapping by checking gitlinks vs .gitmodules

Condition:

- When `git submodule status` fails with `fatal: no submodule mapping found in .gitmodules for path '<path>'` (exit 128) on a repo whose working tree contains the submodule directory

Action:

- Do compare `git ls-files --stage | Select-String 160000` (gitlink entries) against `.gitmodules` sections; a gitlink without a `.gitmodules` entry is the mapping gap. Fix by adding the `[submodule "<name>"]` block (path + url from the submodule's own `git -C <dir> remote -v`) to `.gitmodules`, then `git submodule init` + `git submodule update --init <path>` and re-run `git submodule status` (expect exit 0, no leading `-`/`+`). Confirmed on QUESTION-117 (2026-08-14): gitlink `2da67907` at `.ept/docs/customer_input/foundry-platform-python` (palantir/foundry-platform-python, tag 1.79.0) was registered but unmapped.

## Improvement: verify conda build/render gates with log-file redirect, not inline pipes

Condition:

- When verifying `conda build`/`conda render` exit codes from PowerShell (e.g., a QA gate expecting exit 0 after installing conda-build)

Action:

- Do run `conda render conda.recipe *> <log> 2>&1; echo "EXIT:$LASTEXITCODE"` and read the log tail; don't pipe through `Select-Object -First N` inline (PowerShell closes the pipe early and reports a false exit 2). Note `conda render` in conda-build 26.7.0 does NOT accept `--json` (exit 2, unrecognized arguments) — use plain `conda render conda.recipe` or `conda build conda.recipe --json`. The tooling prerequisite is `conda install -n base -y conda-build` (mirrors `.github/workflows/publish.yml`). Confirmed on QUESTION-118/119 (2026-08-14): after install, `conda build --version` exit 0, `conda render conda.recipe` exit 0, `conda build conda.recipe --output-folder <dir>` produced `pal_found_cli-0.1.0-py_0.conda`; local noarch install needs explicit runtime deps (`conda install -n <env> -y foundry-platform-sdk python-dotenv requests`) before console-script smoke tests pass.

# DevOps Engineer Improvement Memory

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
- Do remember nested venv reads base interpreter system/user sites, not parent venv packages. Use an isolated temporary `PYTHONUSERBASE` for required dependencies when repository edits and global installs are forbidden; verify imports from that path before rerunning.

## Improvement: isolate release candidate from dirty worktree

Condition:
- When release verification names a final commit but shared worktree contains unrelated changes

Action:
- Do build and test a clean `git archive` of final commit, confirm required precursor commits are ancestors, and use parent before first feature commit as rollback baseline. Don't copy dirty worktree files into candidate unless scope explicitly names them as release artifacts.

Subject: CI typing failure and bounded one-file correction plan
Created: 2026-11-18T01:31:49
Updated: 2026-11-18T01:31:49
---
CI run 44199067392 failed mypy src/ on four no-any-return errors in _geotemporal_compat.py; Ruff passed and later jobs were skipped. Failed log .ept/tmp/task022_tool_bug050_mypy_failure_20261118.log and approved tree b3fc47374ad27d05a01639ef4e9d87d92a39f697 remain retained.

Correct only dynamic return annotations using typing.cast: existing native/fallback callable results and precise latest/historic awaitables. Preserve native method identity, RequestInfo contents and runtime behavior. Other six approved files stay byte-identical.

Run exact CI mypy command, Ruff and native SDK 1.101/1.111/1.79 wire tests. Freeze new one-file diff, hashes and tree for independent review. No commit, push, main/parent change, status transition or blocker removal.

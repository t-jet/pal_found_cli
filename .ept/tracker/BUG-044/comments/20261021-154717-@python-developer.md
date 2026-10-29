Subject: Root cause and implementation in progress
Created: 2026-10-21T15:47:17
Updated: 2026-10-21T15:47:17
---
Positional argparse values bypass JSON coercion and remain str at SDK list validation. Fix author /root/filesystem_batch_fix owns minimal positional _coerce_arg reuse and real-SDK regressions. Root reports 19 new regression cases and 144 runtime passes per SDK 1.101.0/1.111.0, plus Ruff and mypy for 72 source files. Tracker agent reviewed original three-failure JSON evidence but did not execute these implementation checks. No published candidate, independent QA or CI acceptance is recorded yet. Remain In Progress pending those gates.

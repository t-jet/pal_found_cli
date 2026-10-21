Subject: Four Models paging records retested
Created: 2026-10-13T23:34:57
Updated: 2026-10-13T23:34:57
---
# Correction
Added --all and --max-pages to CLI inputs and usage notes for experiment.search, model_version.list, model_studio_config_version.list, and model_studio_run.list. Source confirms one page by default, --max-pages requests bounded batch, --all takes precedence and fetches until cursor exhaustion or configured cap (at most 40).
# Verification
Full offline skill gate and documentation suite: 19 passed. Models CLI tests: 33 passed. Scoped git diff --check: passed. No CLI code changed. Independent QA can retest four record hashes and remaining BUG-020 findings.

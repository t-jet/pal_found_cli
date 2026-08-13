---
name: pal-found-models
description: Run Foundry Models API v2 operations across live deployments, models, versions, experiments, experiment content, Model Studio, config versions, runs, and trainers.
---

# Foundry Models

Run `pal-found-models --help` for syntax. The CLI exposes exactly 23 Models v2 operations: `live-deployment transform-json`; `model create|get|promote-version`; `model-version create|get|list`; `experiment get|search`; `experiment-series json|parquet`; `experiment-artifact-table json|parquet`; `model-studio create|get|launch`; `model-studio-config-version create|get|latest|list`; `model-studio-run list`; `model-studio-trainer get|list`.

Structured public options use a `-json` suffix and are validated locally before any client is created. Four cursor-paged commands (`experiment search`, `model-version list`, `model-studio-config-version list`, `model-studio-run list`) accept `--page-size`, `--page-token`, `--all`, and `--max-pages` (at most 40 actual pages). `--offset`/`--page-size` on series and artifact-table JSON are service-side slicing only. Streamed downloads (series parquet, artifact-table json/parquet) write bounded content atomically under the configured download path and emit a metadata envelope; they never print content bytes.

Access control runs before client and filesystem effects. The write set is `transform_json`, all creates, `promote_version`, and `launch`; read-only mode blocks them before any work. Metadata-only policy is fail closed: exactly 12 reads are permitted and the other 11 operations are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying inference, creates, promotion, or launch can duplicate work or cost. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results or metadata envelopes go only to stdout. Logs and errors must not contain prompts, inputs, model content, downloaded bytes, credentials, tokens, or attribution RIDs.

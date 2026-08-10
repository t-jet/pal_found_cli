Subject: P1 fix applied - file_import_filters dispatch (CODEREVIEW-017)
Created: 2026-08-10T13:00:04
Updated: 2026-08-10T13:00:04
---
## P1 corrective action — `file_import_filters` dispatch (2026-08-10)

### Root cause
`file-import create`/`file-import replace` in `src/foundry_cli/connectivity/scripts/foundry_connectivity_cli.py` registered the catalog argument as `filters` and dispatched `filters=` to the SDK, but the installed SDK (foundry_platform_sdk **1.102.0**) exposes the filters input as a **keyword-only** argument named `file_import_filters`. Runtime consequence: `pydantic.ValidationError: file_import_filters — Missing required keyword only argument`, i.e. both operations could never succeed.

### SDK signature evidence (verified via `inspect.signature`/source on installed SDK)
`foundry_sdk/v2/connectivity/file_import.py` → `AsyncFileImportClient`:

```python
def create(self, connection_rid, *, dataset_rid, display_name,
           file_import_filters: List[FileImportFilter], import_mode,
           branch_name=None, subfolder=None, request_timeout=None, ...)
def replace(self, connection_rid, file_import_rid, *, display_name,
            file_import_filters: List[FileImportFilter], import_mode,
            subfolder=None, request_timeout=None, ...)
```

### Fix applied
- `src/foundry_cli/connectivity/scripts/foundry_connectivity_cli.py`
  - OP_SPECS `file_import.create` (L186, L188) and `file_import.replace` (L225, L227): catalog argument renamed `filters` → `file_import_filters` in `required` and `list_json_args`.
  - Added `_FLAG_NAME_OVERRIDES = {"file_import_filters": "filters"}` (L311) so the public CLI flag stays **`--filters-json`** (unchanged surface) while the argparse dest and dispatch kwarg use the SDK name. `_add_kwarg` reads the override for the flag and keeps `dest=arg_name`.
  - Dispatch (`_validate_inputs`, `_build_kwargs`) needed no changes: they already operate on spec arg names, which are now the exact SDK kwarg names.
- `tests/test_foundry_connectivity_cli.py`
  - `test_file_import_create_dispatches_with_filters_json` (L504): assertion corrected from `filters=` to `file_import_filters=`.
  - Added `test_file_import_replace_dispatches_with_filters_json` — replace-dispatch regression coverage asserting `file_import_filters=`.

### Verification (all green)
- Targeted tests: 4 passed (create/replace dispatch, filters-json array validation, parser surface).
- Focused suite `tests/test_foundry_connectivity_cli.py`: **34 passed**; with `test_access_control_guard.py`: **110 passed**.
- Full suite minus connectivity: 1181 passed → project total **1215 passed, 0 failed**.
- `compileall src` exit 0; `ruff check` clean on both files. `mypy`: source file 0 errors; the 2 test-file errors (L37 `_Scope.__exit__` bool, L976 `_Cfg` arg-type) are **pre-existing** — confirmed identical on the pristine baseline via `git stash`.
- Runtime probe (`misc_dos/probe_codereview_017_fix.py`): `--filters-json` accepted, decoded into `args.file_import_filters`, dispatched kwargs contain `file_import_filters=[...]` (no `filters` key) for both create and replace. PROBE PASSED.

### Impact
No CLI surface change (flag `--filters-json` unchanged); no skill-doc changes needed (`.claude/skills/foundry-connectivity` references `--filters-json` only). Only the two previously-failing operations' dispatch path was corrected.

Requesting re-review. CODEREVIEW-017 moving Correction → Corrected, reassigned to tech-lead.

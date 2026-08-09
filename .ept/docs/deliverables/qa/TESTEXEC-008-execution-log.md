# TESTEXEC-008 - Foundry Functions CLI execution log

Date: 2026-07-29
Story: DEV-STORY-008
Test design: TESTCASE-008

## Scope

Executed QA coverage for the `foundry-functions` CLI, including the seven Functions namespace operations, parser/help behavior, SDK dispatch, JSON argument parsing, boolean flags, `FUNCTIONS` ACL checks, output formatting, byte response handling, console entry point wiring, and the `.claude` skill launcher.

## Commands

| Command | Result |
|---|---|
| `python -m pytest tests/test_foundry_functions_cli.py tests/test_functions_console_wrapper.py -q` | Passed, 36 tests |
| `python -m ruff check pyproject.toml src/foundry_cli/functions tests/test_foundry_functions_cli.py tests/test_functions_console_wrapper.py` | Passed |
| `python -m mypy src/foundry_cli/functions tests/test_foundry_functions_cli.py tests/test_functions_console_wrapper.py` | Passed |
| `python -m foundry_cli.functions.scripts.foundry_functions_cli --help` | Passed, exit 0 |
| `python .claude/skills/foundry-functions/scripts/foundry_functions_cli.py --help` | Passed, exit 0 |
| `python -m compileall -q src/foundry_cli/functions .claude/skills/foundry-functions/scripts` | Passed |
| `python -m pip install -e .` | Passed, `foundry-cli 0.1.0` installed editable |
| `foundry-functions --help` | Passed, exit 0 |
| `python -m pytest -q --cov=src/foundry_cli --cov-report=term-missing` | Passed, 622 tests, 81.75% total coverage |

## Coverage against TESTCASE-008

The automated suite covers catalog completeness, parser coverage for all seven operations, operation help, query execution dispatch, `get`, `get-by-rid`, `get-by-rid-batch`, `streaming-execute`, `value-type get`, nested `version-id get`, JSON decoding for structured arguments, boolean defaults, empty pagination catalog, ACL namespace behavior, access control denial, ADR-001 exit-code mapping, retry wrapping, B3 invocation scope, output conversion, bytes envelope handling, packaged module execution, console wrapper, and `.claude` launcher behavior.

Editable package installation and `foundry-functions --help` verified the project script entry point after the `pyproject.toml` update.

## Notes

Warnings observed:

- `RequestsDependencyWarning` for installed `urllib3`, `chardet`, and `charset_normalizer` versions.
- `pytest_asyncio` deprecation warning for unset default fixture loop scope.

Both warnings are environment-level and did not fail tests.

## Result

QA passed. No defects opened for DEV-STORY-008.

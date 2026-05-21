Subject: Test Plan — Open to In Progress
Created: 2026-05-18T19:08:51
Updated: 2026-05-18T19:08:51
---
## Test Plan — Open → In Progress

### Overview
Unit tests for all 26 datasets namespace operations achieving >=80% code coverage.

### Test Framework
- pytest with pytest-asyncio for async operations
- pytest-mock for mocking external dependencies

### Test Structure
`
tests/
├── test_foundry_datasets_cli.py      # CLI entry point tests
├── test_dataset_operations.py         # Dataset CRUD (7 operations)
├── test_branch_operations.py          # Branch management
├── test_transaction_operations.py     # Transaction management
├── test_file_operations.py            # File upload/download
├── test_view_operations.py            # View operations
├── test_access_control.py             # Access control guard integration
└── conftest.py                        # Shared fixtures and mocks
`

### Test Categories

1. **Happy Path Tests** — Each operation with valid inputs returning expected results
2. **Error Path Tests** — SDK exceptions mapped to exit codes per ADR-001
3. **Access Control Tests** — Enabled/disabled/readonly/metadata-only scenarios
4. **Edge Case Tests** — Empty responses, pagination, timeouts
5. **Format Tests** — JSON vs TOON output per ADR-004

### Mocking Strategy
- Mock AsyncDatasetsClient and all sub-clients
- Mock _foundry_cli_common.py shared components
- No real network calls

### Coverage Target
>=80% line coverage across all 26 operations

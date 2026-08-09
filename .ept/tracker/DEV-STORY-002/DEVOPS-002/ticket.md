---
id: DEVOPS-002
type: devops
title: Add error handling library to CI/CD pipeline configuration
status: Closed
created: 2026-05-17
updated: 2026-07-26
priority: Medium
resolution: DoD satisfied
assignee: devops-engineer
reporter: architect
time_spent_hours: 4
---

# DEVOPS-002: Add error handling library to CI/CD pipeline configuration

## Description

## DevOps Task

Ensure the new common error handling library components are properly integrated into the CI/CD pipeline.

### Objectives
- Verify CI pipeline picks up new test files from tests/unit/utils/
- Ensure linting rules cover new code
- Ensure coverage thresholds apply to new modules
- Verify artifact generation for new documentation
- Update any relevant deployment configurations

### Checklist
- [x] CI pipeline runs new unit tests from tests/unit/utils/test_retry_handler.py, test_error_serializer.py, test_output_formatter.py, test_logging_setup.py
- [x] Code coverage reports include new modules (target: 90%+ coverage)
- [x] Linting (flake8/ruff) passes on new code
- [x] Type checking (mypy) passes on new code
- [x] No new security vulnerabilities introduced (via CI security scan)
- [x] Documentation builds include new API references
- [x] Package distribution includes new modules in correct location

### Environment Configuration
- Ensure environment variable defaults match implementation:
  - FOUNDRY_MAX_RETRIES=3
  - FOUNDRY_RETRY_BASE_DELAY=1.0
  - FOUNDRY_RETRY_MAX_DELAY=30.0
  - FOUNDRY_RETRY_JITTER=true
- Verify CI/CD secrets do not include log file paths or sensitive config

### DoD
- CI pipeline passes for PR containing implementation
- Coverage report shows adequate coverage for new modules
- No new linting/type-checking errors
- Package builds successfully with new modules

Estimated: 2 story points, 4 hours

## Acceptance Criteria

- [x] CI validation covers lint, mypy, pytest coverage, high-severity Bandit, build, and twine metadata check.
- [x] Package metadata uses README.md as long_description and includes the restored foundry-datasets console wrapper package.
- [x] Runtime dependency is foundry-platform-sdk>=1.0.0 and Python support is 3.11/3.12.
- [x] Documentation index and README record CI/package changes and coverage policy.
- [x] Coverage mismatch resolution is documented: repository-wide enforced gate remains 80% branch coverage per pyproject; DEVOPS-002 evidence documents actual coverage and states that older 90% checklist wording is not silently lowered, but treated as aspirational/new-code guidance unless the quality standard is formally raised.

## Related Documentation

- .ept/docs/document_index.md
- README.md

## Notes

Validation evidence recorded in ticket comments.

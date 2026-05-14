# Adhoc Modifications requirements

## Overview

New commands should be added to the tracker CLI utility to improve ticket handling process.
New features are:

1. For the `list` command add reporter (author) and blocked status to the output.
2. For the `list` command add possibility to specify a list of values for the `--status`, `--type` and `--priority` filters.
3. For the `list` command add a new `--non-terminal-only` option wich should exclude all tickets in the terminal statuses.
4. Implement additional `build-queue` command to generate a prioritized list of non-terminal tickets based on their blocking relationships and priorities.

Implementation to be modified located in `.ept/skills/tracking-system/tracker` folder.

## Detailed Requirements

Priority ordering should be based on the order of values in the list of values for the `priority` field (name: priority, type: enum) in the `.workflow.yaml` configuration file. Priorities listed here from the lowest to highest.

### 1. `list` command enhancements

#### 1.1 Include Reporter and Blocked Status in Output

- Modify the `list` command to include the reporter (author) of each ticket in the output.
  - The reporter value should be read from the `reporter` field in the ticket index (`.config/.index.csv`).
  - This field contains the same value as the `author` parameter used when creating the ticket.
- Add a new column to indicate whether the ticket is currently blocked by another ticket (Yes/No).
  - A ticket is considered "blocked" if there exists any link where:
    - The ticket is the target of a link, AND
    - The link type has `is_blocking: true` in its `.workflow.yaml` definition
  - For the current configuration, only the "Blocks" link type should have this flag set to true.
- Update the `format_ticket()` function in `formatters.py` to include these new columns in the output.

#### 1.2 Support Multiple Values for Filters

- Update the `list` command to allow users to specify multiple values for the `--status`, `--type`, and `--priority` filters.
- Example usage: `tracker list --status "Open,In Progress" --type "Bug,Feature" --priority "High,Medium"`
- Ensure that the command correctly filters tickets based on any of the specified values for each filter.

#### 1.3 Add `--non-terminal-only` Option

- Implement a new option `--non-terminal-only` for the `list` command.
- When this option is used, the command should exclude all tickets that are in terminal statuses based on the ticket type descriptions in workflow.

### 2. `build-queue` command

The `build-queue` command should implement the following algorithm:

#### Stage 1 - Get a list of non-terminal tickets to work on

- For each ticket type, identify terminal statuses from the ticket types definition.
- Form a list of tickets that are not in terminal statuses.
- All subsequent steps will only consider this filtered list of non-terminal tickets.

#### Stage 2 - Priority cleanup

- For each ticket in the list find all child tickets which also are in the list and verify that that all child ticket have priority not less then a parent ticket. If not, update the priority of the child ticket to match the parent ticket's priority. This should be done recursively until all child tickets have priority not less than their parent ticket.
- For each ticket in the list find all tickets which blocks the ticket and verify that all blocking tickets have priority not less than the blocked ticket. If not, update the priority of the blocking ticket to match the blocked ticket's priority. This should be done recursively until all blocking tickets have priority not less than the blocked ticket.

#### Stage 3 - Build the queue

- Sort the list of non-terminal tickets based on the following criteria:
  - Tickets that are blocking tickets with the highest priority
  - Critical with highest priority
  - Tickets that are blocking tickets with the next highest priority
  - Tickets with the next highest priority
  - Repeat the blocking/non-blocking pattern for all remaining priorities in order from highest to lowest.

The priority values are defined in the `.workflow.yaml` `priority_values` field, ordered from lowest to highest. The sorting therefore produces: blocking/Critical, Critical, blocking/High, High, blocking/Medium, Medium, blocking/Low, Low (and so on for any additional priorities).

### Stage 4 - Output the queue

- Output the sorted list of tickets in the same format as the `list` command, prepending the output with the position in the queue (1, 2, 3, ...) and listing the blocking tickets for each ticket in the queue.

## Clarifications

Q: Should --non-terminal-only calculate blocked/terminal states on-demand from links and index, or persist a blocked field in the ticket index?
A: They should be calculated on-demand from the links and index. This ensures that the information is always up-to-date and reflects the current state of the tickets without needing to maintain additional fields in the index.

Q: What are "terminal statuses" per ticket type? Should I extract this from automatic_transitions rules in the workflow configuration, or define separately?
A: They are defined in the workflow configuration and reported already by the `workflow` `types` command. Check it's implementation to figure out a right way to extract this information.

Q: Should multi-value filters (--status "Open,In Progress") require at least one match (OR) or all matches (AND)? Requirements say "based on any of the specified values" → OR is correct.
A: Yes, the multi-value filters should require at least one match (OR). This means that if a ticket matches any of the specified values for a filter, it should be included in the results. A ticket always have only one status, type and priority, so AND logic is not applicable here.

Q: The priority cleanup in Stage 2 modifies ticket priorities permanently. Should this be applied to a copy of the queue only, or mutate the index directly? The tracker's update_ticket function will write changes to disk.
A: It should mutate tickets directly in the index. This ensures that the priority adjustments are persistent and reflect the current state of the tickets for all users. The `build-queue` command is responsible for ensuring that the priorities are consistent before generating the queue, so it's appropriate to update the tickets in the index as part of this process.

Q: Stage 3 sorting criteria are cut off. Should I defer that section until you provide the complete priorities list?
A: Complete priorities list is provided in the requirements. Information is added, check it.

Q: How should the system identify "blocking" links? Should it check for specific link types or use a configuration flag?
A: Add an `is_blocking` boolean flag to each link type definition in the `.workflow.yaml` file under the `link_types` section. For the current configuration, only the "Blocks" link type should have `is_blocking: true`. Other link types should have `is_blocking: false` or omit the field (defaults to false). This makes the system flexible and configuration-driven.

Q: For the "Reporter" column in the list output, should this be extracted from ticket metadata or from the index?
A: Use the `reporter` field directly from the ticket index (`.config/.index.csv`). This field already contains the author identifier and is readily available without needing to read individual ticket files. The reporter value is the same as the `author` parameter used when the ticket was created.

Q: Should the `format_ticket()` function be extended to handle the new columns, or should a new formatter be created?
A: Extend the existing `format_ticket()` function in `formatters.py` to include the Reporter and Blocked columns. This maintains consistency with the existing output format and avoids code duplication.

## Code Quality Requirements

### Refactoring

The CLI module (`cli.py`) has grown large and should be refactored to improve maintainability:

- Split the single large source file into multiple modules organized by function:
  - Command handlers (create, list, update, etc.) should be moved to separate handler modules
  - Workflow-related functions should be grouped together
  - Build-queue functionality should remain in its own module (`build_queue.py`)
- Maintain backward compatibility with existing CLI behavior
- Preserve all existing functionality during refactoring
- Follow the existing code style and conventions

### Test Coverage

All new and modified functionality must be covered by automated tests:

- Add unit tests for:
  - Multi-value filter parsing and application
  - Non-terminal status filtering
  - Blocked status detection using `is_blocking` flag
  - Reporter column inclusion
  - Build-queue algorithm stages (1-4)
  - Priority cleanup logic
  - Queue sorting algorithm
- Add integration tests for:
  - End-to-end `list` command with new options
  - End-to-end `build-queue` command execution
- All tests must pass before considering the implementation complete
- Use the existing test infrastructure in the `tests/` directory
- Follow the existing test patterns and naming conventions

### Acceptance Criteria

- All existing tests continue to pass
- New tests provide adequate coverage (aim for >90% of new code)
- CLI refactoring does not break any existing functionality
- Code follows existing style guidelines and conventions
- Documentation (docstrings) is updated for all modified functions

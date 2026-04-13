# Issue Tracking System - User Guide

**Version**: 2.5
**Created**: 2026-01-04
**Updated**: 2026-02-22
**Purpose**: File-based issue tracking system for LLM agent collaboration implementing 16-stage workflow

---

## Overview

This tracker uses a file-system-based approach compatible with Jira T&R workflows, optimized for LLM agent operations.

### Hierarchy

```text
Physical Nesting:
  Feature Request → Developer Story → Sub-Tasks
  Feature Request → BA/SA/UX Sub-Tasks (Analysis/Design stages)
  Developer Story → DESIGN/DEV/UNITTEST/CODEREVIEW/TESTCASE/TESTEXEC/DEVOPS/BUG-SUB
  Task → Work Item Sub-Tasks (WORK-XXX)
  Any Ticket → Question Sub-Tasks (QUESTION-XXX)

Logical Linking:
  Feature Request ↔ Epic (organizational grouping via Epic Link)
  Developer Story ↔ Epic (Epic Link field inherited from Feature)
  
Root Level Tickets:
  - Feature Requests (FEATURE-XXX/) - Business capability containers
  - Epics (EPIC-XXX/) - End-to-end business scenarios (use cases)
  - Tasks (TASK-XXX/) - General-purpose ad-hoc work
  - Bugs (BUG-XXX/) - Production/UAT defects
  - Resource Requests (RESOURCE-REQ-XXX/) - New agent/resource requests
```

### Key Principles

1. **16-Stage Workflow**: From backlog (Stage 0) to production deployment (Stage 16)
2. **Developer Stories in Features**: Physical nesting under Feature Request folders (NOT under Epics)
3. **Epics at Root Level**: Logical organization units linked to Features and Stories via Epic Link
4. **Task Ticket Type**: General-purpose catch-all for ad-hoc work not fitting other types; no time reporting
5. **Resource Requests**: Special ticket type for requesting new agents/resources
6. **Knowledge Base**: All resolved questions stored in `project_qa.md`
7. **Documentation-in-Comments**: All execution plans, summaries, reports MUST be in ticket comments, NOT separate files
8. **User Activity Tracking**: All User/Project Owner activities must be documented in tickets
9. **Mandatory Process Algorithms**: All agents MUST follow `.instructions/` workflows for each ticket type
10. **No Stage Skipping**: Tickets must progress through all statuses in order (no shortcuts)
11. **Centralized Link Storage**: All relationship links stored in `tracker/.config/.link-index.csv` (single source of truth)
12. **Question-Driven Approach**: Create Question sub-tasks instead of making assumptions
13. **CLI-First Rule**: Use `.ept/tools/tracker_cli.py` for all ticket, link, and comment operations; direct file edits are only permitted when repairing the CLI itself

---

## Quick Start for Agents

### Mandatory Pre-Work Checklist

Before executing ANY activity:

1. **Search for Existing Ticket**: Check `.ept/tracker/.config/.index.csv` for related work
2. **Consult Process Instructions**: Read `.ept/tracker/.instructions/index.md` for ticket type algorithm
3. **Research Before Asking**: Check `project_qa.md`, documentation, and code before creating Questions
4. **Document Research**: Always document research done in Question tickets
5. **Follow Status Workflow**: Never skip stages - progress through all statuses in order
6. **Manage Links**: Add links to `.ept/tracker/.config/.link-index.csv` when creating relationships

### Process Algorithm Reference

All ticket types have detailed handling algorithms in `.ept/tracker/.instructions/`:

**Core Tickets**:

- [Epic (Use Case)](.ept/tracker/.instructions/epic.md) - End-to-end business scenarios
- [Feature Request](.ept/tracker/.instructions/feature-request.md) - Business capabilities
- [Developer Story](.ept/tracker/.instructions/developer-story.md) - Technical implementation work
- [Task](.ept/tracker/.instructions/task.md) - General ad-hoc work
- [Bug (Production/UAT)](.ept/tracker/.instructions/bug.md) - Production defects
- [Resource Request](.ept/tracker/.instructions/resource-request.md) - New agent requests

**Analysis & Design Sub-Tasks**:

- [BA Sub-Task](.ept/tracker/.instructions/ba-subtask.md) - Business analysis (ANALYSIS/DESIGN stages)
- [SA Sub-Task](.ept/tracker/.instructions/sa-subtask.md) - Solution architecture (ANALYSIS/DESIGN stages)
- [UX Sub-Task](.ept/tracker/.instructions/ux-subtask.md) - UX design (optional, ANALYSIS/DESIGN stages)

**Implementation Sub-Tasks** (for Developer Stories):

- [Design Sub-Task](.ept/tracker/.instructions/design-subtask.md) - Grooming/estimation (Stage 8)
- [Development Sub-Task](.ept/tracker/.instructions/development-subtask.md) - Code implementation
- [UnitTest Sub-Task](.ept/tracker/.instructions/unittest-subtask.md) - Unit test creation
- [CodeReview Sub-Task](.ept/tracker/.instructions/codereview-subtask.md) - Code review (required per DEV)
- [TestCase Sub-Task](.ept/tracker/.instructions/testcase-subtask.md) - QA test case design
- [TestExec Sub-Task](.ept/tracker/.instructions/testexec-subtask.md) - QA test execution
- [DevOps Sub-Task](.ept/tracker/.instructions/devops-subtask.md) - Deployment tasks
- [Bug Sub-Task](.ept/tracker/.instructions/bug-subtask.md) - Bugs found during QA

**Universal Sub-Tasks**:

- [Work Item Sub-Task](.ept/tracker/.instructions/workitem-subtask.md) - Task decomposition
- [Question Sub-Task](.ept/tracker/.instructions/question-subtask.md) - Clarification requests (any parent)

### Before Creating a Question

**MANDATORY CHECKS**:

1. Search `project_qa.md` for similar questions
2. Check open `QUESTION-*` folders for duplicates
3. Review `.ept/docs/` documentation
4. Check relevant code files
5. Document research in "Research Done" section

### Using the CLI

**Preferred for all tracker operations** — use `.ept/tools/tracker_cli.py` instead of direct file edits:

```bash
# Create a ticket
python .ept/tools/tracker_cli.py create task --title "My task" --assignee agent --author agent

# List tickets (with optional filters)
python .ept/tools/tracker_cli.py list --type task --status "In Progress"

# Get a single ticket
python .ept/tools/tracker_cli.py get TASK-001

# Update status / any field
python .ept/tools/tracker_cli.py update TASK-001 --status "In Progress" --author agent

# Add a comment
python .ept/tools/tracker_cli.py comment create TASK-001 --text "Work started" --author agent

# List comments
python .ept/tools/tracker_cli.py comment list TASK-001

# Create a link between tickets
python .ept/tools/tracker_cli.py link TASK-001 TASK-002 --type Blocks --author agent

# Search tickets by keyword
python .ept/tools/tracker_cli.py search "refactor"
```

Direct file edits to ticket frontmatter or `comments/` are **only** permitted when the CLI itself is being repaired or tested.

### Creating Tickets

**Feature Request**:

```bash
mkdir tracker/FEATURE-XXX
# Create ticket.md with YAML frontmatter (type: feature)
# See tracker/.instructions/feature-request.md for full workflow
```

**Epic** (at root level, linked to Feature):

```bash
mkdir tracker/EPIC-YYY
# Create ticket.md with feature_request field (type: epic)
# Add link to tracker/.config/.link-index.csv:
#   LINK-XXXXX,FEATURE-XXX,EPIC-YYY,FeatureContains,Feature Contains,Is Contained In Feature,<timestamp>,<agent>,<comment>
# Update link counter in tracker/.config/.id-counters.yaml
# See tracker/.instructions/epic.md for full workflow
```

**Developer Story under Feature Request**:

```bash
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ
# Create ticket.md (type: dev_story) with:
#   parent: FEATURE-XXX (physical location)
#   feature_request: FEATURE-XXX (same as parent)
#   epic: EPIC-YYY (Epic Link field for logical grouping)
# Add links to tracker/.config/.link-index.csv:
#   LINK-XXXXX,FEATURE-XXX,DEV-STORY-ZZZ,Contains,Contains,Contained In,<timestamp>,<agent>,Story nested in Feature
#   LINK-YYYYY,EPIC-YYY,DEV-STORY-ZZZ,EpicLink,Epic Link,Epic Link,<timestamp>,<agent>,Story associated with Epic
# Update link counter in tracker/.config/.id-counters.yaml
# See tracker/.instructions/developer-story.md for full workflow
```

**Task** (general-purpose, any level):

```bash
# Root level (no specific parent)
mkdir tracker/TASK-XXX

# Under Feature Request (if related to Feature analysis/design work)
mkdir tracker/FEATURE-XXX/TASK-YYY

# Under Epic (if related to Epic planning)
mkdir tracker/EPIC-XXX/TASK-YYY

# Under Developer Story (if related to Story implementation)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/TASK-YYY

# Create ticket.md (type: task) with:
#   type: task
#   parent: {PARENT-ID or null for root}
#   assignee: {agent-name}
#   reporter: {who-created-it}
# Use for: ad-hoc activities, documentation updates, research, admin tasks
# NO time reporting in Tasks (use Work Item sub-tasks for decomposition)
# See tracker/.instructions/task.md for full workflow
```

**Question** (nested under ANY parent task/sub-task):

```bash
# Can be child of ANY ticket or sub-task
mkdir tracker/{PARENT-PATH}/QUESTION-NNN

# Examples:
mkdir tracker/FEATURE-XXX/QUESTION-001
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/QUESTION-002
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/DEV-001/QUESTION-003
mkdir tracker/TASK-XXX/QUESTION-004

# Create ticket.md (type: question) with:
#   parent: {PARENT-ID}
#   addressed_to: {architect|business-analyst|project-owner|specific-agent}
# Parent AUTOMATICALLY blocked until question answered
# MANDATORY: Document research done before asking
# See tracker/.instructions/question-subtask.md for full workflow
```

**Resource Request** (at root level, for requesting new agents):

```bash
mkdir tracker/RESOURCE-REQ-001
# Create ticket.md (type: resource_req) using RESOURCE-REQ-TEMPLATE.md as content guide
# Include: role definition, responsibilities, required skills, deliverables
# Status workflow: New → Under Review → Approved → In Progress → Resolved → Closed
# See tracker/.instructions/resource-request.md for full workflow
```

**Analysis & Design Sub-Tasks** (for Feature Request):

```bash
# Business Analysis (ANALYSIS and DESIGN stages of Feature)
mkdir tracker/FEATURE-XXX/BA-SUB-001
mkdir tracker/FEATURE-XXX/BA-SUB-002

# Solution Architecture (ANALYSIS and DESIGN stages of Feature)
mkdir tracker/FEATURE-XXX/SA-SUB-001
mkdir tracker/FEATURE-XXX/SA-SUB-002

# UX Design (optional, ANALYSIS and DESIGN stages of Feature)
# Created only when Feature includes UI/UX work
mkdir tracker/FEATURE-XXX/UX-SUB-001
mkdir tracker/FEATURE-XXX/UX-SUB-002

# These sub-tasks are created in pairs during Feature stages:
# - BA-SUB-001 + SA-SUB-001 (+ UX-SUB-001) for ANALYSIS stage
# - BA-SUB-002 + SA-SUB-002 (+ UX-SUB-002) for DESIGN stage
# See respective .instructions/*.md files for full workflows
```

**Implementation Sub-Tasks** (for Developer Story):

```bash
# Design/Grooming (Stage 8)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/DESIGN-001

# Development (Stage 10)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/DEV-001

# Unit Testing (Stage 10)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/UNITTEST-001

# Code Review (Stage 10 - REQUIRED for each DEV sub-task)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/CODEREVIEW-001

# QA Test Case Design (Stage 11)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/TESTCASE-001

# QA Test Execution (Stage 11)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/TESTEXEC-001

# DevOps Deployment (Stage 12)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/DEVOPS-001

# Bugs Found During QA (Stage 11)
mkdir tracker/FEATURE-XXX/DEV-STORY-ZZZ/BUG-SUB-001

# See respective .instructions/*.md files for full workflows
```

**Production/UAT Bug** (standalone at root level):

```bash
mkdir tracker/BUG-XXX
# Create bug.md with type: bug, affected_version
# Optional link to Feature Request if enhancement needed (goes-to/comes-from)
# See tracker/.instructions/bug.md for full workflow
```

**Work Item Sub-Task** (for Task decomposition):

```bash
# Decompose Tasks into Work Items for better tracking
mkdir tracker/TASK-XXX/WORK-001

# Create workitem-subtask.md with:
#   parent: TASK-XXX
#   estimated_hours: {hours}
# TIME REPORTING REQUIRED in Work Items
# See tracker/.instructions/workitem-subtask.md for full workflow
```

---

### Fast Search

Use `.ept/tracker/.config/.index.csv` for quick lookups:

```python
import pandas as pd
index = pd.read_csv('.ept/tracker/.config/.index.csv')

# Find by assignee
my_tickets = index[index['assignee'] == 'python-dev']

# High priority blocked items
blocked = index[(index['status'] == 'Blocked') & (index['priority'] == 'High')]

# Questions for me
questions = index[(index['type'] == 'question') & (index['addressed_to'] == 'architect')]
```

Or use shell:

```bash
# Find all your assignments
grep ',python-dev,' tracker/.config/.index.csv

# High priority questions
grep ',question,' tracker/.config/.index.csv | grep ',High,'
```

---

## File Formats

### Ticket Files

All tickets use YAML frontmatter + Markdown body:

```yaml
---
id: DEV-STORY-001
type: developer-story
title: Implement database connection pooling
status: Development
priority: High
created: 2026-01-04T10:00:00Z
updated: 2026-01-04T15:00:00Z
assignee: python-dev
reporter: architect
parent: EPIC-001
feature_request: FEATURE-001
labels: [backend, database]
---

## Description

Detailed explanation...

## Acceptance Criteria

- [ ] Connection pool created with configurable size
- [ ] Pool supports min/max connections
- [ ] Timeout handling implemented

## Technical Notes

...
```

### Comments

Comments are stored as individual files inside a `comments/` subfolder within each ticket folder.

**File naming format**: `yyyymmdd-hhmmss-author.md`  
**Example**: `20260222-143000-solution-architect.md`

Each comment file contains the comment text with optional frontmatter, for example:

```markdown
# TASK-001 status update

**Status**: Open → In Progress
**Author**: solution-architect

Started implementation of connection pool.
```

Multiple comments appear as separate files in the `comments/` directory, sorted by filename (chronologically by timestamp).

**To add a new comment**: Use `python .ept/tools/tracker_cli.py comment create <TICKET-ID> --text "..." --author <author>` (preferred), or create a file manually in `comments/` with the `yyyymmdd-hhmmss-author.md` naming format.

**Example directory structure**:
```
TASK-001/
  ticket.md
  comments/
    20260214-000000-solution-architect.md
    20260215-143022-developer.md
    20260220-091500-solution-architect.md
```

### Links Storage

**Current (v2.4+)**: All links stored in centralized `.ept/tracker/.config/.link-index.csv`.

See [Link Management](#link-management) section for query examples.

**Historical Note**: Prior to v2.4, links were stored in distributed `links.md` files within each ticket folder. This was replaced with centralized CSV storage for better consistency (TASK-028).

---

## Common Operations

### Update Ticket Status

1. Update `status` field in frontmatter
2. Update `updated` timestamp
3. Add comment explaining change

### Create Links (Centralized Storage)

**Creating a New Link**:

1. **Validate Prerequisites**:
   - Both source and target tickets exist
   - Link type is valid
   - No duplicate link exists (same source, target, type)
   
2. **Generate Link ID**:
   - Get next counter from `.id-counters.yaml`: `counters.link`
   - Format: `LINK-{counter:05d}` (e.g., LINK-00042)
   
3. **Determine Roles**:
   - Look up `source_role` and `target_role` from link_type mapping
   - See `.workflow.yaml` for complete role mapping
   
4. **Append to CSV**:
   - Open `.ept/tracker/.config/.link-index.csv`
   - Append new row:
   ```csv
   LINK-00042,DEV-STORY-001,DEV-STORY-005,Blocks,Blocks,Is Blocked By,2026-01-18T20:00:00Z,architect,Requires database setup first
   ```
   
5. **Update Counter**:
   - Increment `counters.link` in `.id-counters.yaml`
   
6. **Update Timestamps**:
   - Update `updated` field in both source and target ticket frontmatter
   
7. **Add Comments** (optional):
   - Add comment to both tickets explaining link creation

**Deleting a Link**:

1. Find link by `link_id` in `.ept/tracker/.config/.link-index.csv`
2. Remove row from CSV (rewrite file without that line)
3. Update `updated` timestamps on both tickets
4. Add comments explaining deletion (if significant)

**Updating a Link**:

1. Delete old link (remove row by link_id)
2. Create new link (append row with new link_id)
3. Optionally preserve original `created` timestamp if updating same relationship
4. Add comment explaining update

**Querying Links**:

```python
import csv

def get_links_for_ticket(ticket_id, direction='all'):
    """Get all links for a ticket.
    
    Args:
        ticket_id: Ticket ID to search for
        direction: 'outgoing' (source), 'incoming' (target), or 'all'
    """
    with open('.ept/tracker/.config/.link-index.csv') as f:
        reader = csv.DictReader(f)
        links = []
        for row in reader:
            if direction in ['all', 'outgoing'] and row['source_ticket'] == ticket_id:
                links.append(row)
            if direction in ['all', 'incoming'] and row['target_ticket'] == ticket_id:
                links.append(row)
        return links

# Example: Find all tickets blocked by this ticket
def get_blocked_tickets(ticket_id):
    with open('tracker/.config/.link-index.csv') as f:
        reader = csv.DictReader(f)
        return [row for row in reader 
                if row['source_ticket'] == ticket_id and row['link_type'] == 'Blocks']
```

**PowerShell Examples**:

```powershell
# Find all links for a ticket
Select-String -Path \"tracker\\.link-index.csv\" -Pattern \"FEATURE-001\"

# Find all blocking relationships
Select-String -Path \"tracker\\.link-index.csv\" -Pattern \",Blocks,\"

# Count links by type
Import-Csv \"tracker\\.link-index.csv\" | Group-Object link_type | Select-Object Name, Count
```

**Link Type to Role Mapping**:

| Link Type | Source Role | Target Role | Description |
|-----------|-------------|-------------|-------------|
| Blocks | Blocks | Is Blocked By | Blocker relationship |
| DependsOn | Depends On | Is Dependency For | Dependency relationship |
| RelatesTo | Relates To | Relates To | General relationship (symmetric) |
| Contains | Contains | Contained In | Hierarchical containment |
| EpicLink | Epic Link | Epic Link | Epic association (symmetric) |
| FeatureContains | Feature Contains | Is Contained In Feature | Feature-Epic relationship |
| BugFeature | Comes From | Goes To | Bug to Feature relationship |
| Question | Asks About | Has Question | Question relationship |
| ParentChild | Is Parent Of | Is Child Of | Parent-child (also in frontmatter) |

---

## Link Consistency Management

### Centralized Storage Benefits

With `tracker/.config/.link-index.csv`, consistency is inherently simpler:

- **Single file**: No synchronization between multiple files needed
- **Atomic operations**: CSV updates are atomic (write to temp, rename)
- **Foreign key validation**: Check all referenced tickets exist
- **No bidirectional sync**: Each relationship stored once with explicit roles

### Validation

**Regular Validation**:

```python
import csv
import os

def validate_links():
    \"\"\"Validate all links in .link-index.csv\"\"\"
    issues = []
    
    with open('tracker/.config/.link-index.csv') as f:
        reader = csv.DictReader(f)
        link_ids = set()
        
        for row in reader:
            # Check link_id uniqueness
            if row['link_id'] in link_ids:
                issues.append(f\"Duplicate link_id: {row['link_id']}\")
            link_ids.add(row['link_id'])
            
            # Check tickets exist
            if not ticket_exists(row['source_ticket']):
                issues.append(f\"Broken link {row['link_id']}: source {row['source_ticket']} not found\")
            if not ticket_exists(row['target_ticket']):
                issues.append(f\"Broken link {row['link_id']}: target {row['target_ticket']} not found\")
            
            # Validate link_type
            if row['link_type'] not in VALID_LINK_TYPES:
                issues.append(f\"Invalid link_type in {row['link_id']}: {row['link_type']}\")
    
    return issues

def ticket_exists(ticket_id):
    \"\"\"Check if ticket folder exists\"\"\"
    # Implementation depends on ticket type
    # Check tracker/{ticket_id}/ or parent paths
    pass
```

**Auto-Repair**:

- Remove links where both tickets don't exist (orphaned)
- Fix malformed link_ids
- Remove duplicate links (same source, target, type)
- Report issues for manual review

### Backup Strategy

Before bulk operations:
```bash
cp tracker/.config/.link-index.csv tracker/.config/.link-index.csv.backup
```

After validation:
```bash
# If valid
rm tracker/.config/.link-index.csv.backup
# If issues found
mv tracker/.config/.link-index.csv.backup tracker/.config/.link-index.csv
```

---

## Fast Search

Use `tracker/.config/.index.csv` for tickets and `tracker/.config/.link-index.csv` for relationships:

**Ticket Search**:

```python
import pandas as pd
index = pd.read_csv('tracker/.config/.index.csv')

# Find by assignee
my_tickets = index[index['assignee'] == 'python-dev']

# High priority blocked items
blocked = index[(index['status'] == 'Blocked') & (index['priority'] == 'High')]

# Questions for me
questions = index[(index['type'] == 'question') & (index['addressed_to'] == 'architect')]
```

**Link Search**:

```python
import pandas as pd
links = pd.read_csv('tracker/.config/.link-index.csv')

# Find all links for a ticket
ticket_links = links[(links['source_ticket'] == 'FEATURE-001') | 
                     (links['target_ticket'] == 'FEATURE-001')]

# Find blocking relationships
blockers = links[links['link_type'] == 'Blocks']

# Find what blocks a specific ticket
what_blocks_me = links[(links['target_ticket'] == 'DEV-STORY-001') & 
                       (links['link_type'] == 'Blocks')]
```

**Shell Examples**:

```bash
# Find all your assignments
grep ',python-dev,' tracker/.config/.index.csv

# High priority questions
grep ',question,' tracker/.config/.index.csv | grep ',High,'

# Find all links involving a ticket
grep 'FEATURE-001' tracker/.config/.link-index.csv

# Count links by type
cut -d',' -f4 tracker/.config/.link-index.csv | sort | uniq -c
```

**PowerShell Examples**:

```powershell
# Find tickets assigned to you
Import-Csv tracker\\.index.csv | Where-Object { $_.assignee -eq 'architect' }

# Find all blocking relationships
Import-Csv tracker\\.link-index.csv | Where-Object { $_.link_type -eq 'Blocks' }

# Find what blocks a ticket
Import-Csv tracker\\.link-index.csv | Where-Object { 
    $_.target_ticket -eq 'DEV-STORY-001' -and $_.link_type -eq 'Blocks' 
}
```

---

## File Formats
  for each link:
    verify target ticket exists
    verify reverse link exists in target
    verify link types match (forward ↔ reverse mapping)
    if inconsistency found:
      report issue
      attempt auto-repair if safe
```

**Auto-Repair (Safe Issues)**:

- Missing reverse link → Create it with repair comment
- Duplicate links → Remove duplicates, keep first
- Orphaned reverse link (source missing) → Remove if source archived

**Manual Review Required**:

- Broken link (target doesn't exist, not archived)
- Mismatched link types (forward/reverse don't match mapping)
- Circular dependencies
- Conflicting parent relationships

### Archival and Link Cleanup

When archiving a ticket:

1. **Identify all tickets linking to this ticket** (query `.link-index.csv` where target_ticket=this ticket)
2. **Remove all links** from tracker/.config/.link-index.csv (delete rows by link_id)
3. **Update timestamps** on all referencing tickets
4. **Add comments**: "Removed link to archived ticket {ID}"
5. **Block archival** OR **cascade archive** if ticket is parent

---

## Project QA Document

**File**: `project_qa.md`

**Purpose**: Centralized knowledge base of all answered questions. Check this BEFORE creating new questions!

**Structure**: Organized by categories (Architecture, Implementation, Database, Testing, DevOps, Business, Project Owner Decisions)

**Maintenance**: When any Question resolved, copy to project_qa.md with full context and references.

---

## Configuration

See `.tracker-config.md` for:

- ID counters (next available for each type)
- Workflow statuses by ticket type
- Priority levels
- Automatic operation settings
- Agent assignments

---

## Troubleshooting

**Problem**: Don't know how to handle a ticket at current status  
**Solution**: Read `tracker/.instructions/{ticket-type}.md` for that ticket type and find the matching status section

**Problem**: Can't find ticket by assignee quickly  
**Solution**: Use `.config/.index.csv` with grep or pandas filtering:
```bash
# Windows PowerShell
Select-String -Path tracker\.config\.index.csv -Pattern ",python-dev,"
# Linux/Mac
grep ",python-dev," tracker/.config/.index.csv
```

**Problem**: Ticket stuck in Blocked status  
**Solution**: Query `tracker/.config/.link-index.csv` for all blockers where target_ticket=this ticket and link_type=Blocks. Check for:
- Questions (link_type=Question)
- Blocking tickets (link_type=Blocks)
- Dependencies (link_type=DependsOn)
Resolve or remove invalid blockers (delete from CSV by link_id), then unblock ticket

**Problem**: Question already answered elsewhere  
**Solution**: Search `project_qa.md` first! If found, reference existing answer instead of creating duplicate

**Problem**: Parent status not updating automatically  
**Solution**: Check automatic operations enabled in `.tracker-config.md`. May need manual update if rules don't cover scenario

**Problem**: Index out of date  
**Solution**: Regenerate `.config/.index.csv` by scanning all ticket files (append new rows on create/update)

**Problem**: Links inconsistent or missing  
**Solution**: Validate links in tracker/.config/.link-index.csv:
1. Query CSV for all links involving ticket
2. Verify both source_ticket and target_ticket still exist
3. Remove orphaned links (where either ticket doesn't exist)
4. Add missing required links (e.g., Contains links for parent-child relationships)

**Problem**: Unsure if work requires Feature, Task, or Developer Story  
**Solution**: 
- **Feature Request**: New business capability or significant change (multi-sprint, user-facing)
- **Developer Story**: Technical implementation work (1 sprint, part of Feature)
- **Task**: Ad-hoc work, documentation, research, admin (no implementation)

**Problem**: Don't know which sub-task type to create  
**Solution**: Consult `tracker/.instructions/index.md` for sub-task type list and purpose

---

## Best Practices

1. **Follow Process Algorithms**: ALWAYS consult `tracker/.instructions/{ticket-type}.md` before working on tickets
2. **Research Before Asking**: Check `project_qa.md`, docs/, code, and open Questions before creating new Questions
3. **Document Research**: In Questions, ALWAYS fill "Research Done" section with what you've checked
4. **Small Stories**: Keep Developer Stories completable in ONE SPRINT (no multi-sprint stories)
5. **Clear Titles**: Use specific, actionable titles:
   - ❌ "Fix bug" or "Update code"
   - ✅ "Fix connection timeout in auth module" or "Add retry logic to database connector"
6. **Business vs Technical Language**:
   - Epics/Features: Business language ("Check room availability", "Generate revenue report")
   - Developer Stories: Technical language ("Implement OAuth2 service", "Create PostgreSQL connection pool")
7. **Update Regularly**: Update timestamps and add comments for all status changes
8. **Link Management**: Add all relationship links to tracker/.config/.link-index.csv with proper link types
9. **Link Related Work**: Create relates-to links for similar functionality or cross-cutting concerns
10. **Close Promptly**: Close tickets when truly done, don't leave in Resolved indefinitely
11. **Copy Resolved Questions**: When Question resolved, immediately copy Q&A to `project_qa.md`
12. **Check Blockers**: Before starting work, query tracker/.config/.link-index.csv to verify no blockers exist (link_type=Blocks where target_ticket=this ticket)
13. **Documentation in Comments**: ALL execution plans, summaries, reports go in ticket comments (NOT separate files)
14. **Track User Activities**: Document all User/Project Owner requests as tickets (Task or appropriate type)
15. **No Stage Skipping**: Follow status progression - cannot jump stages
16. **Code Review Per DEV**: Every DEV-XXX sub-task REQUIRES a linked CODEREVIEW-XXX sub-task
17. **Time Reporting**:
    - ✅ Report time in: Sub-tasks (BA-SUB, SA-SUB, UX-SUB, DESIGN, DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, DEVOPS, WORK, QUESTION)
    - ❌ NO time reporting in: Feature Requests, Epics, Developer Stories, Tasks, Bugs
18. **UX Sub-Task Creation**: Create UX-SUB only when Feature includes UI/UX work (screens, flows, layouts, accessibility)
19. **Question Universality**: Questions can be children of ANY ticket or sub-task (not just Stories)
20. **Task Usage**: Use Task for ad-hoc work that doesn't fit Feature/Epic/Story structure (documentation, research, admin)

---

## Reference

**Process Algorithms**: `tracker/.instructions/index.md` - MANDATORY workflows for all ticket types

**Configuration**: `.tracker-config.md` - System-wide settings and references  
**ID Counters**: `.id-counters.yaml` - Structured ticket and link ID counters  
**Workflow Spec**: `.workflow.yaml` - Fields, ticket types, statuses, transitions, link types

**Full Documentation**: `docs/deliverables/requirements/issue_tracking_storage_requirements.md`

**Architecture Decisions**: `docs/deliverables/architecture/adr/`

**Resource Request Template**: `RESOURCE-REQ-TEMPLATE.md`

---

**Last Updated**: 2026-02-22  
**Maintained By**: Architect Agent  
**Questions**: Create QUESTION ticket addressed to "architect"

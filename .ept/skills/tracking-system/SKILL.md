---
name: tracking-system
description: >-
  Manages a ticket tracking system for AI agent collaboration.
  Use this skill to retrieve workflow documentation, inspect ticket type
  definitions and allowed status transitions, and perform all ticket,
  comment, and link operations. Activate when an agent needs to create,
  read, update, or search tickets; add or read comments; create, list,
  or remove inter-ticket links; or inspect the workflow configuration
  (ticket types, statuses, stage goals, responsible roles, transitions,
  or definitions of done). Keywords: tracker, ticket, issue, task, bug,
  feature, epic, dev story, question, workitem, comment, link, workflow,
  status, transition, assignee, priority, stage, DoD, create ticket,
  update ticket, list tickets, search tickets, get ticket, comment create,
  link create, workflow status, workflow transitions, workflow types.
compatibility: Requires Python with PyYAML; run from the project where `.ept/tracker/` exists.
metadata:
  author: t-jet
  version: "0.1.0"
---

## Overview

This skill operates the tracking system using CLI interface.
All operations MUST go through the CLI.

See [references/REFERENCE.md](references/REFERENCE.md) for full command
syntax, field descriptions, and exit codes.

---


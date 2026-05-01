---
id: TASK-002
type: task
title: Update all agent definitions to match canonical template
status: Closed
priority: Medium
assignee: hr
reporter: tech-lead
created: 2026-05-02
updated: 2026-05-02
---

# TASK-002: Update all agent definitions to match canonical template



## Description



Analyze all agents listed in .ept/resources/available_resources.md and update their .agent.md definition files to literally match the instructions and checklist in .ept/resources/agent_definition_template.md.



Agents to update:

- ba (.github/agents/ba.agent.md)

- Architect (.github/agents/architect.agent.md)

- HR (.github/agents/hr.agent.md)

- tech-lead (.github/agents/tech-lead.agent.md)

- python-developer (.github/agents/python-developer.agent.md)

- qa-engineer (.github/agents/qa-engineer.agent.md)

- devops-engineer (.github/agents/devops-engineer.agent.md)



## Acceptance Criteria



- [x] All agents in available_resources.md analyzed against agent_definition_template.md

- [x] Template rule #5 and Reusable Content Guidelines applied

- [x] 5 agents updated to remove project-specific details (ba, tech-lead, python-developer, qa-engineer, devops-engineer)

- [x] 2 agents verified as already compliant (architect, hr)

- [x] All agent files pass template compliance check

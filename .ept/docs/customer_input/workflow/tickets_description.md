# Types of Tasks in tracking system (e.g. Jira)

## This document lists definition for all task and sub-task types used in project activities.

---

## Terms

* **Definition of Ready (DoR)** — Criteria of the Task readiness to start working on it
* **Definition of Done (DoD)** — Criteria of Task completeness. If these criteria meet, the task is ready to pass to the next stage.

---

## Common activities

### Epic - Use Case

#### Description

Independent End-To-End scenario, implemented in a service/component/module ( = User Stories - A user story represents a small, concise statement of functionality or quality needed to deliver value to a specific stakeholder.)

#### Responsibilities

* Created by Business Analyst
* Changed to **"In Progress"** by implementation team when implementation of first related **"Developer Story"** is started (may be done automatically)
* Changed to **"Resolved"** by implementation team when all related Stories are resolved.
* Changed to **"Done"** by implementation team when all related Stories are Done.

#### DoR

There are exists a business requirement (**"Feature request" task**), which implementation requires adding of this function.

#### DoD

**Required criteria:**

* All tasks linked to this Use Case (Epic) are closed.

#### How it is presented in the tracking system (e.g. Jira)

**(Epic)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s

**Processing states**

* **OPEN** — Use Case added to backlog during designing solution for business requirement.
* **IN PROGRESS** — Use Case implementation started.
* **RESOLVED**

  * Resolution = Done — all linked tasks are done.
  * Resolution = Canceled — Implementation cancelled.
  * Resolution = Duplicated — Use case duplicates another one.
* **CLOSED** — Use case archived.

**Links to**

* **"Feature request"** — by a link of **"Epic contains"** type

**Linked by**

* **"Developer Story"** — by a link in the **"Epic Link"** field
* **"Feature request"** — by a link of **"contained in Epic"** type

**Time reporting**

* Time reporting for Epic isn't allowed

---

## Preliminary analysis/Design

### Feature request — Business initiative/requirement, User Story, Solution architecture improvement

#### Description

Business initiative (comes from Project Owner / User Department) with requirement to change or extend solution behavior.

Also serves as a main point to register required change to meet non-functional requirements, e.g. implement monitoring.

#### Responsibilities

* Created in **"New"** status:

  * by Project Owner or by Business Analyst after discussion with Project Owner for functional requirements
  * by Solution Architect for non-functional requirements.
* Transferred to **"Open"** state and prioritized in backlog by Project Owner
* Processed at **"Analysis"** stage and transferred to **"In development"** stage by Business Analyst in cooperation with Solution Architect (see sub-tasks description).
* Processed at **"In development"** stage and transferred to **"Waiting for implementation"** stage by Business Analyst in cooperation with Solution Architect (see sub-tasks description).
* Transferred to **"Resolved"** and **"Closed"** states by team, based on contained **"Developer Story"** states or automatically (requires implementation of a script )

#### DoR

**Required criteria:**

* Business Case — A clear description of the business need and the goal to be achieved is prepared (Business Case provided by Business).
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared (Acceptance and Evaluation Criteria provided by Business).

**Desirable criteria:**

* A rationale for the change has been prepared.

#### DoD

**Required criteria for functional requirement changes initiated by business:**

* Prepared a detailed description of the requirements (business requirements, functional requirements, non-functional requirements).
* The acceptance criteria by which the task will be checked have been prepared.
* An architectural solution has been prepared (target system state, critical implementation details).

#### How it is presented in tracking system (e.g. Jira)

**(New Feature)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **NEW** — The task has been identified, but the Project Owner has not yet decided that it should be put in the backlog.
* **OPEN** — The task in the backlog.
* **ANALYSIS** — Requirements collection and analysis are in progress.
* **IN DEVELOPMENT** — Requirements refinement and development of architectural solution are in progress
* **WAITING FOR IMPLEMENTATION** — The task has been transferred to an implementation and is waiting for related tasks to be completed.
* **RESOLVED**

  * Resolution = Done — solution designed, tasks for implementation are set.
  * Resolution = Canceled — the task is cancelled.
  * Resolution = Duplicated — the task is a duplicate of another one.
* **CLOSED** — the task is archived.

**Links to**

* Epic — by a link of **"Feature Contains"** type
* **"Developer Story"** — by a link of **"Contains"** type
* Bug — by a link of **"comes from"** type if **"Feature request"** created as a result of Bug investigation

**Linked by**

* Epic — by a link of **"is contained in Feature"** type
* **"Developer Story"** — by a link of **"Contained in"** type
* Bug — by a link of **"goes to"** type if **"Feature request"** created as a result of Bug investigation

**Document**

* from Use Case description document

**Time reporting**

* Time reporting for **"Feature request"** done in it's sub-tasks

---

## Sub-tasks of "Feature request" at ANALYSIS stage

### "BA Sub-Task" — BA business requirements clarification

#### Description

Work, done by Business Analyst to clarify Business Requirements with Project Owner, document requirements, align it with current solution state, including workflows, interfaces, UI/UX and business objects structure.

#### Responsibilities

* Created by Business Analyst
* Estimation, work progress and task close is done by assigned Business Analyst

#### DoR

**Required criteria:**

* Business Case defined.
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared (Acceptance and Evaluation Criteria provided by Business).

#### DoD

**Required criteria:**

* Defined finite set of business requirements, including definition of input/output data description if applicable
* Analyzed impact to all and-to-end business processes and identified finite set of required changes in all functional blocks
* Defined changes in access restrictions
* Analyzed and documented assumptions and risks related to changes
* Changes to request rate for services/modules evaluated if applicable
* Related changes in size of the persistent and transferred data are evaluated if applicable
* All functional and non-functional requirements, risks and assumptions communicated and approved by Solution Architect
* All functional and non-functional requirements, risks and assumptions communicated and approved by Project Owner

#### How it is presented in tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by Business Analyst when parent task goes to upcoming Sprint
* Time reported by assigned Business Analyst

---

### "SA Sub-Task" — SA business requirements review and clarification

#### Description

Work, done by Solution Architect to collect and discuss non-functional requirements and to define general approach to implementation of the required changes in the solution

#### Responsibilities

* Created by Business Analyst

#### DoR

**Required criteria:**

* Business requirement are in place.
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared (Acceptance and Evaluation Criteria provided by Business).

#### DoD

**Required criteria for functional requirement changes initiated by business:**

* Defined a set of affected services and interfaces
* General approach to implementation is formulated
* Stack of technologies is defined
* Defined general approach for migration to new state.

#### How it is presented in tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by Solution Architect when parent task goes to upcoming Sprint
* Time reported by assigned Solution Architect

---

### "Question Sub-Task" — Question to another team member

#### Description

Request for information from another team member. E.g. question asked by Business Analyst to Project Owner to clarify requirements.

#### Responsibilities

Created by Business Analyst, Solution Architect or a person responsible to answer one of the questions in the same parent task.

#### DoR

**Required criteria:**

* Clarification question asked in the description field, all supporting documentation referenced in the question.
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared describing what information should be provided as an answer.

#### DoD

**Required criteria for functional requirement changes initiated by business:**

* Supporting and related documentation studied to get the context.
* Question analyzed, related documentation and tracking system tickets explored to find relevant information.
* Investigation to explore different options done if required.
* Clarification questions required to answer the Question asked if required to other team members via another question tickets and answers for these tickets are collected.
* Clarification questions to Question’s author asked in the comments and answered by the author in the subsequent comment (responsible person changes to Question’s author when asking and back when author responded)
* Question is answered in the comment field with links to supporting documents.
* Related activities planned if answer implies it (e.g. architecture/requirements/coding rules update, additional functionality implementation or implementation plans update)

#### How it is presented in tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by responsible person when moving ticket to the “IN PROGRESS” state
* Time reported by assigned person

---

## Sub-tasks of "Feature request" at DESIGN stage

### "BA Sub-Task" — BA business requirements clarification

#### Description

Work done by Business Analyst to describe business requirements in details for developers

#### Responsibilities

* Created by Business Analyst
* Estimation, work progress and task close is done by assigned Business Analyst

#### DoR

**Required criteria:**

* DoD of a **" BA Sub-task"** task for ANALYSIS stage is meet.

#### DoD

**Required criteria:**

* Detailed requirements developed, including:

  * Logic flow
  * UI mocks with detailed description if applicable
  * Detailed API specification (input/output data)
  * Detailed data structure
  * Migration procedure described in detail, including data migration
* Epics for related functions created in the tracking system (e.g. Jira)
* Stories for implementation created in the tracking system (e.g. Jira)
* All requirements approved by:

  * Product Owner
  * Solution Architect(s) of all involved components
  * Lead developer(s) of all involved components

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by Business Analyst when parent task goes to upcoming Sprint
* Time reported by assigned Business Analyst

---

### "SA Sub-Task" — SA business requirements review and clarification

#### Description

Work, done by Solution Architect to define changes which will be applied to solution for **"Feature request"** implementation

#### Responsibilities

Created by Business Analyst

#### DoR

**Required criteria:**

* DoD of a **"BA Sub-Task "** task for ANALYSIS stage are meet.

#### DoD

**Required criteria:**

* Identified and defined all API endpoints of all services/modules/systems involved in implementation, including required changes.
* For each Use Case involved in implementation defined architectural approach and non-functional requirements for developers
* required changes in infrastructure to support implemented changes are identified and communicated to Delivery Manager or other responsible person
* Migration procedure described step-by-step

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by Solution Architect when parent task goes to upcoming Sprint
* Time reported by assigned Solution Architect

---

### "Question Sub-Task" — Question to another team member

#### Description

Request for information from another team member. E.g. question asked by Business Analyst to Solution Architect to clarify requirement’s feasibility or tech stack limitations.

#### Responsibilities

Created by Business Analyst, Solution Architect or a person responsible to answer one of the questions in the same parent task.

#### DoR

**Required criteria:**

* Clarification question asked in the description field, all supporting documentation referenced in the question.
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared describing what information should be provided as an answer.

#### DoD

**Required criteria for functional requirement changes initiated by business:**

* Supporting and related documentation studied to get the context.
* Question analyzed, related documentation and tracking system tickets explored to find relevant information.
* Investigation to explore different options done if required.
* Clarification questions required to answer the Question asked if required to other team members via another question tickets and answers for these tickets are collected.
* Clarification questions to Question’s author asked in the comments and answered by the author in the subsequent comment (responsible person changes to Question’s author when asking and back when author responded)
* Question is answered in the comment field with links to supporting documents.
* Related activities planned if answer implies it (e.g. architecture/requirements/coding rules update, additional functionality implementation or implementation plans update)

#### How it is presented in tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by responsible person when moving ticket to the “IN PROGRESS” state
* Time reported by assigned person

---

## Implementation/Development

### Developer Story — Implementation of Feature/Use Case to be delivered in production

#### Description

Single business case or non-functional future (like audit or monitoring implementation) which must be deployed on production environment.

Significant characteristics are:

* MUST be developed/tested/deployed in ONE SPRINT
* Defines changes to single service/module only,

#### Responsibilities

* Created in New status by Business Analyst on DESIGN stage of a **"Feature request"**, each **"Developer Story"** linked to one Use Case, separate stories may be created for migration if needed.
* Transferred to **"Analysis"** state where Business Analyst starts work on it in current sprint by assigned Business Analyst
* Transferred to **"Grooming"** state by Business Analyst when DoR for Grooming stage are meet. In that state team responsible for grooming and estimation during regular sessions.
* Transferred to **"Open"** state by team after all implementation details defined, required sub-tasks created and estimated.
* Transferred to **"Development"** stage by responsible team member when implementation of first subtask is started in current sprint (may be done automatically)
* Transferred to **"QA"** stage when all development sub-tasks is closed by responsible developer(s), On this stage QA specialist(s) performs verification of requirements implementation.
* Transferred to **"Deployment"** stage by QA specialist(s) after implementation fully verified and all found bugs is fixed and retested.
* Transferred to **"Resolved"** state by responsible team member on successful deploying to production enviroment.
* Transferred to **"Closed"** state by common team agreement on Sprint closing.

#### DoR

**Required criteria for transfer to GROOMING stage:**

* DoD criteria meet for all sub-tasks in the parent **"Feature request"** issue.
* The **"Release Notes"** field filled with a meaningful description.

**Required criteria for transfer to OPEN stage:**

* Task description reviewed by all Team Leads (Dev, QA, DevOps)
* All responsible team members understood task details and have a clear view on how they implement it, All unclear details refined in task description and/or Use Case description.
* Created ALL sub-tasks required to implement this **"Developer Story"** for Dev, QA, DevOps, ...
* ALL sub-tasks have a definition which clearly understood by responsible implementation team members
* Acceptance criteria defined for all sub-tasks
* ALL sub-task estimated

#### DoD

**Required criteria:**

* All sub-task closed.
* Backward compatibility guaranteed or new major version number increased
* All acceptance criteria meet

#### How it is presented in the tracking system (e.g. Jira)

**(Story)**

**Required fields:**

* Summary
* Description
* Priority
* Epic Link
* Component/s
* Fix version/s (planned delivery version)

**Processing states**

* **NEW** — created during **"Feature request"** refinement, requires definition by Business Analyst
* **ANALYSIS** — definition by Business Analyst in progress
* **GROOMING** — fully defined and ready for estimation by team.
* **OPEN** — estimated and ready to be implemented in next Sprint.
* **DEVELOPMENT** — implementation in progress.
* **QA** — fully implemented, testing in progress.
* **DEPLOYMENT** — ready to be deployed to production.
* **RESOLVED**

  * Resolution = Done — implemented and deployed.
  * Resolution = Canceled — task cancelled.
  * Resolution = Duplicated — task duplicates another oneзадача является дублем к уже имеющейся.
* **CLOSED** — task archived.

**Links to**

* Epic — by **"Epic Link"** field
* **"Feature request"** — by a link of **"Contained in"** type

**Linked by**

* **"Feature request"** — by a link of **"Contains"** type

**Document**

* from Use Case description document

**Time reporting**

* Time reporting for **"Developer Story"** done in it's sub-tasks

---

## Sub-tasks of a "Developer Story"

### "Design Sub-Task" — activities for grooming and estimation

#### Description

Team activities performed while grooming and estimating effort

Only one instance of sub-task of this type per **"Developer Story"** task

#### Responsibilities

* Created by Lead Developer when the **"Developer Story"** considered for grooming
* Closed by Lead Developer when **"Developer Story"** successfully groomed and estimated

#### DoR

**Required criteria:**

* DoD for parent **"Developer Story"**'s GROOMING stage satisfied

#### DoD

**Required criteria:**

* For the **"Developer Story"** created ALL sub-tasks required for implementation
* ALL sub-tasks estimated

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members participation in grooming session, followed by estimation section.
* Time reported by team members participated in grooming and estimation.

---

### "Development Sub-Task" — implementation activities done by developers

#### Description

Core of developer activity required for implementation: writing code, UI modifications, database script implementation, configuration changes, branching etc

There are as many instances of this task exists as needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead Developer during estimation session with implementation team members
* Closed by assigned developer when committed code ready for peer review

#### DoR

**Required criteria:**

* DoR for parent **"Developer Story"**' OPEN stage satisfied

#### DoD

**Required criteria:**

* All code committed to repository and ready for review (in case of git - pull request created)

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "UnitTest Sub-Task" — developer's work on writing unit tests

#### Description

Developer's activity on writing unit tests. Separated from core development activity because of increasing code coverage by unit tests may be done per se and to highlight necessity of unit tests while grooming.

There are as many instances of this task exists as needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead Developer during estimation session with implementation team members
* Closed by assigned developer when committed code with unit tests ready for peer review

#### DoR

**Required criteria:**

* DoR for parent **"Developer Story"** OPEN stage satisfied

#### DoD

**Required criteria:**

* All code committed to repository and ready for review (in case of git - pull request created)

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "CodeReview Sub-Task" — developer's work on reviewing code changes

#### Description

Developer's activity on reviewing code changes.

There are as many instances of this task exists as needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead Developer during estimation session with implementation team members
* Closed by assigned developer when committed code with unit tests ready for peer review

#### DoR

**Required criteria:**

* Related code committed to repository and ready for review (in case of git - Pull Request created)

#### DoD

**Required criteria:**

* All code committed to repository and ready for review (in case of git - pull request created)

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "TestCase Sub-Task" — QA specialist's work on Test Case development

#### Description

QA's activity on writing test cases for the **"Developer Story"**.

There are as many instances of this task exists as needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead QA specialist during estimation session with implementation team members
* Closed by assigned QA when test cases ready

#### DoR

**Required criteria:**

* DoR for parent **"Developer Story”** OPEN stage satisfied

#### DoD

**Required criteria:**

* Test Cases created in the tracking system (e.g. Jira)
* Test Set with a full set of required tests linked to parent **"Developer Story"**

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "TestExec Sub-Task" — QA specialist's work on Test Case execution

#### Description

QA's activity on a test scenarios execution, discussion about possible bugs, creating Bug sub-tasks in the tracking system (e.g. Jira) if any bug found.

There are as many instances of this task exists as needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead QA specialist during estimation session with implementation team members
* Closed by assigned QA when test cases ready

#### DoR

**Required criteria:**

* Related **"TestCases Sub-Task"** of the same **"Developer Story"**is closed (test cases developed)
* Related implementation sub-tasks of the same **"Developer Story"** in **"Resolved"** state

#### DoD

**Required criteria:**

* All related Test Cases executed
* There are no open defects (**"Bug Sub-Task"**) in parent **"Developer Story"**

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "DevOps Sub-Task" — Work, done by DevOps specialists

#### Description

Work, done by DevOps specialists if needed. E.g. configuring OpenShift environment, adding new projects to repository and including it in CI/CD pipeline and so on.

There are as many instances of this task can be created if needed (e.g. several implementation steps)

#### Responsibilities

* Created by Lead Developer / DevOps specialist during estimation session with implementation team members.
* Closed by assigned DevOps specialist when test cases ready

#### DoR

**Required criteria:**

* DoR for parent **"Developer Story"**'s OPEN stage satisfied

#### DoD

**Required criteria:**

* Work done and ready for use.
* Specific acceptance criteria must be provided.

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority

**Processing states**

* **OPEN** — Parent task added to backlog, sub-task created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated based on team members estimation during estimation session after grooming.
* Time reported by assigned team member.

---

### "Bug Sub-Task" — Work on fixing found defect

#### Description

Work, done by developer while fixing a found bug.

#### Responsibilities

* Created in **"Open"** state by QA specialist while testing (see **"TestExec Sub-Task"** above).
* Transferred to **"Resolved"** state by assigned developer after bug .
* Closed by QA after fixed version passes tests or if there is **"not-a-bug"** agreement between Dev, QA and BA in place.

#### DoR

**Required criteria for OPEN state:**

* Specific unsatisfied requirement pointed out in description
  **or**
* detailed error message given in description, with screenshot if applicable.
* Described steps to reproduce the bug.
* Exact application version (with the build number) pointed out.
* Test environment pointed out (QA, Dev, UAC, Pre-Prod, local, ...)
* Browser version specified if applicable.
* Application logs attached.

**Required criteria for RESOLVED state:**

* Defect fixed in code, fixed version passed code review and merged to proper repository branch, binary artefacts ready for testing
  **or**
* Environment re-configured (in case if DevOps work needed)
  **or**
* Agreement reached between QA specialist, Business Analyst, Developer that Bug reported by mistake (**"Cancelled"** resolution)

#### DoD

**Required criteria:**

* Test Cases created in the tracking system (e.g. Jira)
* Test Set with a full set of required tests linked to parent **"Developer Story"**

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Affected Version/s
* Fix version/s — after defect fixed and tests passed (filled by QA while closing the bug)

**Processing states**

* **OPEN** — Defect found during testing by QA (**"TestExec Sub-Task"**)
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by assigned developer.
* Time reported by assigned team member.

---

### "Question Sub-Task" — Question to another team member

#### Description

Request for information from another team member. E.g. question asked by Developer to Solution Architect to clarify project architecture or implementation details.

#### Responsibilities

Created by assignees of subtasks of the same parent task or a person responsible to answer one of the questions in the same parent task.

#### DoR

**Required criteria:**

* Clarification question asked in the description field, all supporting documentation referenced in the question.
* Acceptance and Evaluation Criteria — Acceptance Criteria have been prepared describing what information should be provided as an answer.

#### DoD

**Required criteria for functional requirement changes initiated by business:**

* Supporting and related documentation studied to get the context.
* Question analyzed, related documentation and tracking system tickets explored to find relevant information.
* Investigation to explore different options done if required.
* Clarification questions required to answer the Question asked if required to other team members via another question tickets and answers for these tickets are collected.
* Clarification questions to Question’s author asked in the comments and answered by the author in the subsequent comment (responsible person changes to Question’s author when asking and back when author responded)
* Question is answered in the comment field with links to supporting documents.
* Related activities planned if answer implies it (e.g. architecture/requirements/coding rules update, additional functionality implementation or implementation plans update)

#### How it is presented in tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s (same as in parent task)

**Processing states**

* **OPEN** — Parent task added to backlog, subtask created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Sub-task duplicates another one.
* **CLOSED** — Sub-Task archived.

**Links to**

* -

**Linked by**

* Listed in parent task Sub-Tasks list

**Time reporting**

* Work effort estimated by responsible person when moving ticket to the “IN PROGRESS” state
* Time reported by assigned person

---

## Support

### "Bug" — Defect from Production/UAT

#### Description

Work, done for handling defects found in Production and User Acceptance Testing environments

#### Responsibilities

Created in **"Open"** state:

* by L2 support specialist when incident passed to L3 support
* by QA specialist for bugs, reported by users while testing released functionality on User Acceptance Testing environment.

Transferred to **"Resolved"** state:

* by assigned developer after fixing the defect.
* by QA specialist if the Bug was reported by mistake (not-a-bug)

Closed by QA specialist after fixed version passes tests or if there is **"not-a-bug"** agreement between Dev, QA and BA in place.

#### DoR

**Required criteria for OPEN state:**

* Specific unsatisfied requirement pointed out in description
  **or**
* detailed error message given in description, with screenshot if applicable.
* Described steps to reproduce the bug.
* Exact application version (with the build number) pointed out.
* Test environment pointed out (Production, UAC, Pre-Prod)
* Browser version specified if applicable.
* Application logs attached.

**Required criteria for RESOLVED state:**

* Defect fixed in code, fixed version passed code review, merged to proper repository branch, artifacts built and ready for testing and ready for testing
  **or**
* No violated requirements identified and application works as designed, but improvement requested by user: Detailed argumentation for such decision provided in comments
  **or**
* Agreement reached between QA specialist, Business Analyst, Developer that Bug reported by mistake (**"Cancelled"** resolution): Detailed arguments for such decision provided in comments

#### DoD

**Required criteria:**

* Defect fixed and included into upcoming Release
  **or**
* **"Feature request"** created with new requirements by Business Analyst or the Bug mapped to an existing but not implemented **"Feature request"**.

#### How it is presented in the tracking system (e.g. Jira)

**(Subtask)**

**Required fields:**

* Summary
* Description
* Priority
* Component/s — only one component/module where bug is located must be specified
* Affected Version/s
* Fix version/s — after defect fixed and tests passed (filled by QA while closing the bug)

**Processing states**

* **OPEN** — Parent task added to backlog, sub-task created
* **IN PROGRESS** — Work started.
* **RESOLVED**

  * Resolution = Done — Work done.
  * Resolution = Rejected — Bug reported by mistake.
  * Resolution = Canceled — Work cancelled.
  * Resolution = Duplicated — Bug duplicates another one.
* **CLOSED** — Bug archived.

**Links to**

* **"Feature request"** — by a link of **"goes to"** type if **"Feature request"** created/mapped as an investigation’s result.
* Bug — by a link of **"duplicates"** type if this Bug duplicates another one
* Document — link to description of violated Use Case must be provided if such Use Case identified

**Linked by**

* **"Feature request"** — by a link of **"comes from"** type if **"Feature request"** created as the Bug investigation’s result.
* Bug — by a link of **"duplicated by"** type if this Bug is duplicated by another one

**Time reporting**

* Work effort estimated by assigned QA and developer.
* Time reported by assigned team member.

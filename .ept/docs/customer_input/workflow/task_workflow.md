# Design and implementation sequence

## Overview

### Phase 1 - Filling backlog

* Stage 0 - Register Feature request
* Stage 1 - Include Feature request to backlog

### Phase 2 - Requirements and scope refinement

* Stage 2 - Feature request analysis planned for the next sprint
* Stage 3 - Requirements, acceptance criteria and scope refinement
* Stage 4 - Preliminary analysis finished

### Phase 3 - Design

* Stage 5 - Detailed design planned for next sprint
* Stage 6 - Detailed design in progress
* Stage 7 - Detailed design done

### Phase 4 - Implementation

* Stage 8 - Planning for implementation
* Stage 9 - "Developer Story" estimated and ready for implementation
* Stage 10 - "Developer Story" implementation by developers, Test Cases design
* Stage 11 - Testing and bug fixing
* Stage 12 - "Developer Story" implemented and ready for deployment
* Stage 13 - "Developer Story" deployed to User Acceptance Testing environment
* Stage 14 - "Developer Story" deployed to Production environment
* Stage 15 - All "Developer Story" issues included in the Epic deployed to Production
* Stage 16 - All Epics in the Feature request deployed to Production

---

## Phase 1 - Filling backlog

### Stage 0 - Register Feature request

"Feature request" registered by Project Owner or Business Analyst with generic description and acceptance criteria.

```mermaid
flowchart LR
  Actor["Project Owner / Business Analyst"] --> FR["Feature request<br/>Status = NEW"]
```

### Stage 1 - Include Feature request to backlog

```mermaid
flowchart LR
  Actor["Project Owner / Business Analyst"] --> FR["Feature request<br/>Status = OPEN"]
```

---

## Phase 2 - Requirements and scope refinement

### Stage 2 - Feature request analysis planned for the next sprint

```mermaid
flowchart LR
  FR["Feature request<br/>Status = OPEN"]

  FR --> BA_SUB["BA Sub-Task<br/>Status = OPEN"]
  FR --> SA_SUB["SA Sub-Task<br/>Status = OPEN"]

  BA_SUB --> BA["Business Analyst"]
  SA_SUB --> SA["Solution Architect"]
```

### Stage 3 - Requirements, acceptance criteria and scope refinement

Business Analyst and Solution Architect works in cooperation with Product Owner to limit scope of changes in terms of affected use cases, refines requirements, analyses impact on end-to-end business processes, identifies affected services and modules and so on.

During this stage new Use Case documentation created in Documentation (e.g. Confluence). "Developer Story" issues for implementation created in the tracking system (e.g. Jira) and linked to Documentation (e.g. Confluence) Use Cases. New Epics created to organize Developer Stories/Use Cases into valuable scenarios.

Most of work on this stage done by Business Analyst.

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = NEW"]
  STORY["Story<br/>Status = NEW"]
  DEV["Developer Story<br/>Status = ANALYSIS"]

  STORY -->|Epic Link field| EPIC
  STORY -->|Contains / Contained in| DEV

  UC -.-> STORY
  BO -.-> STORY
  UI -.-> STORY
  SD -.-> STORY
  API -.-> STORY
  INF -.-> STORY

  DEV --> BA_SUB["BA Sub-Task<br/>Status = IN PROGRESS"] --> BA["Business Analyst"]
  DEV --> SA_SUB["SA Sub-Task<br/>Status = IN PROGRESS"] --> SA["Solution Architect"]

  BA --- PO["Project Owner"]
  SA --- PO
```

### Stage 4 - Preliminary analysis finished

Preliminary analysis finished, all artifacts developed and in place in Documentation (e.g. Confluence) and tracking system (e.g. Jira)

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = NEW"]
  DEV["Developer Story<br/>Status = NEW"]
  FR["Feature request<br/>Status = DESIGN"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  FR --> BA_SUB["BA Sub-Task<br/>Status = CLOSED"]
  FR --> SA_SUB["SA Sub-Task<br/>Status = CLOSED"]
```

---

## Phase 3 - Design

### Stage 5 - Detailed design planned for next sprint

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = OPEN"]
  DEV["Developer Story<br/>Status = ANALYSIS"]
  FR["Feature request<br/>Status = DESIGN"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  FR --> BA_CLOSED["BA Sub-Task<br/>Status = CLOSED"]
  FR --> SA_CLOSED["SA Sub-Task<br/>Status = CLOSED"]

  FR --> BA_OPEN["BA Sub-Task<br/>Status = OPEN"] --> BA["Business Analyst"]
  FR --> SA_OPEN["SA Sub-Task<br/>Status = OPEN"] --> SA["Solution Architect"]
```

### Stage 6 - Detailed design in progress

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = OPEN"]
  DEV["Developer Story<br/>Status = ANALYSIS"]
  FR["Feature request<br/>Status = DESIGN"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  FR --> BA_DONE["BA Sub-Task<br/>Status = CLOSED"]
  FR --> SA_DONE["SA Sub-Task<br/>Status = CLOSED"]

  FR --> BA_WIP["BA Sub-Task<br/>Status = IN PROGRESS"] --> BA["Business Analyst"]
  FR --> SA_WIP["SA Sub-Task<br/>Status = IN PROGRESS"] --> SA["Solution Architect"]

  BA --- PO["Project Owner"]
  SA --- PO
```

### Stage 7 - Detailed design done

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = OPEN"]
  DEV["Developer Story<br/>Status = GROOMING"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  FR --> BA_SUB["BA Sub-Task<br/>Status = CLOSED"]
  FR --> SA1["SA Sub-Task<br/>Status = CLOSED"]
  FR --> SA2["SA Sub-Task<br/>Status = CLOSED"]
  FR --> SA3["SA Sub-Task<br/>Status = CLOSED"]
```

---

## Phase 4 - Implementation

### Stage 8 - Planning for implementation

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = OPEN"]
  DEV["Developer Story<br/>Status = GROOMING"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = OPEN"]
  DEV --> DEVST["Development Sub-Task<br/>Status = OPEN"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = OPEN"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = OPEN"]
  DEV --> TC["TestCase Sub-Task<br/>Status = OPEN"]
  DEV --> TE["TestExec Sub-Task<br/>Status = OPEN"]
  DEV --> OPS["DevOps Sub-Task<br/>Status = OPEN"]

  subgraph SESS["Sessions"]
    GROOM["Grooming session"]
    PLAN["Planning session"]
  end

  BA["Business Analyst"] <--> GROOM <--> SA["Solution Architect"]
  PLAN <--> TEAM["Implementation team<br/>(Developers, QA specialists, DevOps specialists)"]
```

### Stage 9 - "Developer Story" estimated and ready for implementation

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = OPEN"]
  DEV["Developer Story<br/>Status = OPEN"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = OPEN"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = OPEN"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = OPEN"]
  DEV --> TC["TestCase Sub-Task<br/>Status = OPEN"]
  DEV --> TE["TestExec Sub-Task<br/>Status = OPEN"]
  DEV --> OPS["DevOps Sub-Task<br/>Status = OPEN"]
```

### Stage 10 - "Developer Story" implementation by developers, Test Cases design

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = IN PROGRESS"]
  DEV["Developer Story<br/>Status = DEVELOPMENT"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = IN PROGRESS"] --> DEVROLE["Developer/s"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = IN PROGRESS"] --> DEVROLE
  DEV --> CR["CodeReview Sub-Task<br/>Status = IN PROGRESS"] --> DEVROLE

  DEV --> TC["TestCase Sub-Task<br/>Status = IN PROGRESS"] --> QAROLE["QA specialist/s"]
  DEV --> TE["TestExec Sub-Task<br/>Status = OPEN"]

  DEV --> OPS["DevOps Sub-Task<br/>Status = IN PROGRESS"] --> OPSROLE["DevOps specialist/s"]
```

### Stage 11 - Testing and bug fixing

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = IN PROGRESS"]
  DEV["Developer Story<br/>Status = QA"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = RESOLVED"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = RESOLVED"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = RESOLVED"]
  DEV --> TC["TestCase Sub-Task<br/>Status = CLOSED"]

  DEV --> TE["TestExec Sub-Task<br/>Status = IN PROGRESS"] --> QAROLE["QA specialist/s"]

  DEV --> OPS["DevOps Sub-Task<br/>Status = CLOSED"]

  DEV --> BUG["Bug Sub-Task<br/>Status = OPEN"] --> DEVROLE["Developer/s"]
```

### Stage 12 - "Developer Story" implemented and ready for deployment

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = IN PROGRESS"]
  DEV["Developer Story<br/>Status = DEPLOYMENT"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = CLOSED"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = CLOSED"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = CLOSED"]
  DEV --> TC["TestCase Sub-Task<br/>Status = CLOSED"]
  DEV --> TE["TestExec Sub-Task<br/>Status = CLOSED"]
  DEV --> OPS["DevOps Sub-Task<br/>Status = CLOSED"]
  DEV --> BUG["Bug Sub-Task<br/>Status = CLOSED"]
```

### Stage 13 - "Developer Story" deployed to User Acceptance Testing environment

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = IN PROGRESS"]
  DEV["Developer Story<br/>Status = RESOLVED"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = CLOSED"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = CLOSED"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = CLOSED"]
  DEV --> TC["TestCase Sub-Task<br/>Status = CLOSED"]
  DEV --> TE["TestExec Sub-Task<br/>Status = RESOLVED"]
  DEV --> OPS["DevOps Sub-Task<br/>Status = CLOSED"]
  DEV --> BUG["Bug Sub-Task<br/>Status = CLOSED"]
```

### Stage 14 - "Developer Story" deployed to Production environment

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = IN PROGRESS"]
  DEV["Developer Story<br/>Status = CLOSED"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC

  DEV --> DSGN["Design Sub-Task<br/>Status = CLOSED"]
  DEV --> DEVST["Development Sub-Task<br/>Status = CLOSED"]
  DEV --> UT["UnitTest Sub-Task<br/>Status = CLOSED"]
  DEV --> CR["CodeReview Sub-Task<br/>Status = CLOSED"]
  DEV --> TC["TestCase Sub-Task<br/>Status = CLOSED"]
  DEV --> TE["TestExec Sub-Task<br/>Status = CLOSED"]
  DEV --> OPS["DevOps Sub-Task<br/>Status = CLOSED"]
  DEV --> BUG["Bug Sub-Task<br/>Status = CLOSED"]
```

### Stage 15 - All "Developer Story" issues included in the Epic deployed to Production

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = CLOSED"]
  DEV["Developer Story<br/>Status = CLOSED"]
  FR["Feature request<br/>Status = WAITING FOR IMPLEMENTATION"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC
```

### Stage 16 - All Epics in the Feature request deployed to Production

```mermaid
flowchart LR
  subgraph DOCS["Document artifacts (e.g. Confluence)"]
    UC["Use Case definition"]
    BO["Business Object definition"]
    UI["UI Mocks"]
    SD["Service definition"]
    API["API definition"]
    INF["Infrastructure requirements"]
  end

  EPIC["Epic<br/>Status = CLOSED"]
  DEV["Developer Story<br/>Status = CLOSED"]
  FR["Feature request<br/>Status = CLOSED"]

  UC -.-> DEV
  BO -.-> DEV
  UI -.-> DEV
  SD -.-> DEV
  API -.-> DEV
  INF -.-> DEV

  DEV -->|Epic Link field| EPIC
  DEV -->|Contains / Contained in| FR
  FR -->|Feature contains / Contained in feature| EPIC
```

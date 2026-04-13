# Open Questions — Foundry CLI Agent Skill

**Purpose:** Questions that must be answered before architecture design and implementation planning can begin.  
**Date:** 2026-04-09  
**Author:** Solution Architect

---

## Background Context

Analysis of the provided SDK source (`foundry-platform-python`) and the [Palantir Foundry API v2 documentation](https://www.palantir.com/docs/foundry/api/v2) reveals the following important facts that inform the questions below:

- The SDK already ships with a fully-generated Click-based CLI (~13 700 lines, `foundry_sdk/v2/cli.py`) registered as the `foundry_sdk_v2` entry-point. It covers all 20 v2 namespaces (`admin`, `aip_agents`, `audit`, `checkpoints`, `connectivity`, `core`, `data_health`, `datasets`, `filesystem`, `functions`, `geo`, `language_models`, `media_sets`, `models`, `ontologies`, `orchestration`, `sql_queries`, `streams`, `third_party_applications`, `widgets`).
- The SDK supports two parallel clients: `FoundryClient` (sync) and `AsyncFoundryClient`.
- Auth options are `UserTokenAuth`, `ConfidentialClientAuth` (OAuth2 client credentials), and `PublicClientAuth`.
- The SDK requires Python ≥ 3.10; NFR-01 targets Python 3.11.

---

## Section 1 — Scope & Deliverable Definition

### Q1.1 — Relationship to the existing SDK CLI

The SDK already contains a complete Click-based CLI (`foundry_sdk_v2`).  
Is the goal to:

- **A)** Build a thin wrapper / re-export of the existing CLI and focus only on agent-skill packaging?
- **B)** Build a new, purpose-designed CLI optimised for AI-agent consumption (different UX, output format, error model) that co-exists with the SDK CLI?
- **C)** Extend/augment the existing CLI with additional commands (e.g., agent-friendly output modes)?
- **D)** Something else entirely?

> Answering this prevents re-implementing ~14 000 lines of generated code unnecessarily.

### A1.1 — Relationship to the existing SDK CLI

The purpose is B) - build a new, purpose-designed CLI optimised for AI-agent consumption, but based like existing cli on the foundry_sdk package. 
The CLI utility inside SDK wouldn't be available to agents, they would be able only to install foundry_sdk package to Python and use prepared utilities.


---

### Q1.2 — FR-02 is empty

Requirement `FR-02` in `initial_task.md` has a heading but no body text.  
What is the intended content of FR-02?

### A1.2 — FR-02 is empty
Just placed here by accident.

---

### Q1.3 — "All capabilities" definition

FR-01 says tools should "cover all capabilities provided by SDK."  
The SDK v2 exposes 20 namespaces with hundreds of individual operations.

- Does "all capabilities" mean **every** operation across all namespaces, or a curated priority set?
- Should v1 API endpoints (also available in `foundry_sdk/v1/`) be included, or is v2-only sufficient?
- Are there namespaces or operations that must be **excluded** (e.g., admin operations that require elevated privileges the agent should not have)?

### A1.3 — "All capabilities" definition

- It means every operation. Several agent skills should be introduced, one skill per namespace plus one general skill which covers general knowledge about Foundry and aware about other skills and how combine them to solve questions.
- Only v2 endpoints are needed.
- All namespaces and operations should be included. CLI Wrappers should support configuration provided in .env files or environment variables which will enable/disable specific wrappers and put all or specific wrappers to read-only mode.

---

### Q1.4 — Read vs. write boundary

Should the agent skill expose:

- **Read-only** operations only (list, get, search, query)?
- **All operations** including mutating ones (create, update, delete, apply action, trigger builds)?
- **Configurable** at deployment time via allow-list/deny-list?

> Write or admin operations carried out by an AI agent create audit and governance concerns that need deliberate sign-off.

### A1.4 — Read vs. write boundary

Wrappers should expose all operations configurable by environment variables, allowing enable/disable them or put in read-only mode. Additional control should be introduced which will restrict read-only mode to reading only metadata, not datasets or files inside datasets.


---

### Q1.5 — Binary / streaming data handling

Several SDK operations return binary or paginated binary data (Parquet files, dataset files, media, Arrow tables). For agent consumption:

- Should binary responses be written to a local path and the path returned to the agent?
- Should they be Base64-encoded and returned inline?
- Should these operations be out of scope for the agent skill?

### A1.5 — Binary / streaming data handling

The safe dedicated local path inside repository should be used, excluded from the source tracking using .gitignore.
All operations should be included.

---

## Section 2 — Claude Agent Skill Format

### Q2.1 — What "Claude agent skill" means in this context

NFR-03 says the toolset must be implemented as a "Claude agent skill." This term maps to multiple distinct formats:

| Format | Description |
| --- | --- |
| **MCP Server** | A Model Context Protocol server exposing Foundry operations as tools; consumable by Claude Desktop, Cursor, VS Code Copilot, etc. |
| **`.claude/agents/*.md`** | A VS Code Copilot custom sub-agent definition file using Claude tool naming conventions (`Read`, `Bash`, `Grep`, etc.) |
| **`.github/agents/*.agent.md`** | A VS Code-native agent mode definition (different tool set) |
| **Claude.ai Project Instructions** | A system prompt and tool description uploaded to a Claude.ai Project |
| **Python function tools** | Decorated Python functions (`@tool`) used inside a Claude API tool-use workflow |

**Which format is required?** (Select all that apply.)

### A2.1 — What "Claude agent skill" means in this context

It means Claude skill, explore documentation here: https://code.claude.com/docs/en/skills#create-your-first-skill
They would be used in the VSCode: https://code.visualstudio.com/docs/copilot/customization/agent-skills
Python CLI wrappers should be included to the corresponding skill.

---

### Q2.2 — Target agent platform

Which platforms / frameworks must the tool integrate with?

- Claude Desktop (Anthropic)
- Claude API (direct, tool-use / function-calling pattern)
- VS Code Copilot agent mode (`.claude/agents`)
- Amazon Bedrock (Claude on Bedrock)
- Custom internal agent orchestration framework
- Other (specify)

### A2.2 — Target agent platform

VS Code with support of Claude agents and custom internal agent orchestration framework.


---

### Q2.3 — MCP server requirement

If the target is an MCP server:

- Should each SDK operation map to an individual MCP tool (100+ tools), or should higher-level composite tools be designed?
- Should the server be stateless per request, or maintain session/auth state between calls?
- Should it be packaged as a local stdio MCP server, an HTTP/SSE MCP server, or both?
- Which MCP SDK / framework should be used (e.g., `mcp` Python package from Anthropic)?


### A2.3 — MCP server requirement

It's not an MCP.

---

### Q2.4 — Tool granularity vs. abstraction

For agent usability, there is a trade-off:

- **Fine-grained** (1-to-1 with SDK operations): maximally flexible but exposes ~400+ tools, which can overwhelm an agent's context window.
- **Coarse-grained** (composite semantic tools, e.g., `foundry_query_objects`, `foundry_run_sql`): easier for an agent to use but requires design work and may not cover all capabilities.

Which approach is preferred, or should both be offered?

### A2.4 — Tool granularity vs. abstraction

One CLI tool per SDK namespace, one skill per CLI tool plus one general skill with Foundry knoweledge plus knowledge about other skills.


---

## Section 3 — Authentication & Security

### Q3.1 — Authentication method for agent use

The SDK supports:

- `UserTokenAuth` — personal developer token (README warns against production use)
- `ConfidentialClientAuth` — OAuth2 client credentials (recommended for production)
- `PublicClientAuth` — OAuth2 public client / PKCE flow

For the agent skill, which auth method is required?  
Is the agent expected to act on behalf of a specific service account, or on behalf of the current user?

### A3.1 — Authentication method for agent use

It should be UserTokenAuth, because agents invoked by developers.

---

### Q3.2 — Credential injection

Where and how should credentials be provided to the tool at runtime?

- Environment variables (`FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME`) — as the existing CLI uses?
- A config file (path specified via env var or CLI flag)?
- Secrets manager / vault integration (e.g., HashiCorp Vault, AWS Secrets Manager)?
- MCP server-level credential injection (passed in `env` block of server config)?

### A3.2 — Credential injection

Environment variables.

---

### Q3.3 — Scope / permission model

The SDK's `ConfidentialClientAuth` requires explicit OAuth2 scopes.

- What Foundry permission scopes will the agent be granted?
- Is there a principle-of-least-privilege requirement limiting which namespaces/operations are accessible?
- Are Foundry data markings (CBAC) relevant—i.e., will the agent encounter marking-restricted resources?

### A3.3 — Scope / permission model

Don't use this type of authentication.


---

### Q3.4 — Audit and attribution

The SDK exposes `ATTRIBUTION_VAR`, `SPAN_ID_VAR`, and `TRACE_ID_VAR` context variables.

- Should agent-initiated API calls carry a distinct attribution header identifying them as AI-agent actions?
- Are there Foundry audit log requirements that must be met for regulatory or compliance reasons?

### A3.4 — Audit and attribution

More information needed about these context variables (purpose, how they are used inside SDK, how it affects functionality) to answer correctly.


---

## Section 4 — Interaction Model & Response Format

### Q4.1 — Output format for agent consumption

The existing SDK CLI outputs Python `repr()` strings (e.g., `click.echo(repr(result))`). This is developer-readable but may not be ideal for agent parsing.

What output format should the agent skill produce?

- Structured JSON (most machine-readable, preferred for agents)?
- Human-readable plain text / Markdown?
- Configurable via a flag?


### A4.1 — Output format for agent consumption

It should be [TOON](https://github.com/toon-format/toon) where applicable or JSON if TOON doesn't match.

---

### Q4.2 — Pagination handling

Many SDK list operations return paginated results.

- Should the tool automatically iterate through all pages and return a complete result set?
- Should it expose `page_size` and `page_token` to the caller (agent manages pagination)?
- Should it return the first page only with a pagination cursor the agent can follow?

> Auto-pagination on large datasets could cause memory/timeout issues for the agent.

### A4.2 — Pagination handling

- It should expose `page_size` and `page_token` to the caller (agent manages pagination).
- It should return the first page only on the first call with `page_token` which agent can use to retrieve more pages if needed.
- It should expose batch option, allowing to retrieve specified number of pages at once and return the full result with `page_token` if not all data is read and safety limit, allowing to read no more then 40 pages in one batch. 

---

### Q4.3 — Error reporting

The SDK raises typed exceptions (`PalantirRPCException`, `BranchNotFound`, `PermissionDeniedError`, etc.).

- Should errors be returned as structured error objects (JSON) for agent interpretation?
- Should the tool retry on transient errors (e.g., 429 Rate Limit, 503), and if so, with what policy?
- Should validation errors (Pydantic) be surfaced in agent-friendly language?

### Q4.3 — Error reporting

- Errors should be returned as structured error objects (JSON) for agent interpretation.
- The tool should retry on transient errors with exponential retry policy configurable in environment variables.

---

### Q4.4 — Multi-turn / stateful sessions

AIP Agents (`aip_agents.Agent.Session`) and some streaming operations involve multi-turn context.

- Should the skill support stateful multi-turn sessions (e.g., resuming an AIP Agent conversation)?
- If so, how should session state be tracked: in memory, in a file, or in a persistent store?

### A4.4 — Multi-turn / stateful sessions

Skill should support stateful multi-run sessions, tracing sessions with files stored in dedicated folder in repository excluded from source tracking with .gitignore.


---

## Section 5 — Non-functional Requirements

### Q5.1 — Python version constraint

NFR-01 specifies Python 3.11.\*. The SDK's `pyproject.toml` requires Python ≥ 3.10.

- Is Python 3.11 a hard floor (cannot use 3.12+), or does it mean "minimum 3.11"?
- Are there known compatibility concerns with Python 3.12 or 3.13 for the SDK?

### A5.1 — Python version constraint

Target is Python 3.11.* and 3.12.*
Newer versions will require compatibility checks for removed deprecated features.


---

### Q5.2 — Deployment topology

What is the expected runtime environment for the agent skill?

- Developer laptop (local, no containerisation)?
- Docker / OCI container?
- Kubernetes pod?
- Serverless (Lambda, Cloud Run)?
- CI/CD pipeline runner?

This affects packaging, secret handling, and startup latency requirements.

### A5.2 — Deployment topology

Deployment will be done by checking out repository and copying files to the target repository.
These skills will be a part of a larger agentic development workflow(s).
Developer's laptops or cloud PCs can run Win11, MacOS or Linux.
---

### Q5.3 — Performance and throughput expectations

- What is the expected request volume (requests per minute/hour)?
- Are there latency SLAs for tool invocations from the agent?
- Should the tool support async execution (the SDK exposes `AsyncFoundryClient`)?

### A5.3 — Performance and throughput expectations

- There are no expectations for request volumes. Most bad scenario will be if the some agent will run several subagents, maybe up to 10-20 in parallel to perform independent tasks using the tools. 
- There are no SLAs because tools will connect to the server which isn't our control to perform requests. Calling overhead should be minimal.
- Not sure about it. There are no benefit from perfomance point of view, but calling async interfaces can help with setting timouts for tools which can be useful and with supporting graceful exit in case of forced termination to report correct status.

---

### Q5.4 — Observability requirements

- Is structured logging required (JSON logs to stdout)?
- Should the tool emit OpenTelemetry traces or metrics?
- Should it integrate with an existing monitoring stack (Datadog, Splunk, Grafana, etc.)?

### A5.4 — Observability requirements

- Structured logging should be supported for debug mode, which can be forced using command-line switch. 
- No  requirements for supporting OpenTelementry.
- No integrations with monitoring stacks.

---

### Q5.5 — Rate limiting and backpressure

The Foundry API enforces rate limits (SDK surfaces `RateLimitError`).

- Should the tool implement client-side rate limiting or throttling?
- Should it expose rate-limit headers/metadata back to the agent so the agent can self-throttle?

### Q5.5 — Rate limiting and backpressure

Tools should use exponential backoff retry strategy for handling rate limits, with parameters configurable via environment variables (initial delay, max delay, multiplier).

---

## Section 6 — Testing & Delivery

### Q6.1 — Test environment availability

- Is a live Palantir Foundry instance available for integration and end-to-end testing?
- If not, should tests rely exclusively on the mock server pattern used in the SDK (`tests/server.py` with FastAPI/uvicorn)?

### A6.1 — Test environment availability

There is no live Palantir Foundry instance available for testing, so tests should rely on the mock server pattern used in the SDK (`tests/server.py` with FastAPI/uvicorn).

---

### Q6.2 — Coverage expectations

- What is the minimum required test coverage (by statement, branch, or integration)?
- Are there specific operations that are considered high-risk and require mandatory integration tests?

### A6.2 — Coverage expectations

Test coverage should be at least 80% by statements, with mandatory integration tests for critical operations such as dataset manipulation, authentication flows, and any operations that have side effects (e.g., create/update/delete).
All tools should have unit tests covering expected functionality, edge cases, and error handling. Integration tests should cover end-to-end scenarios for a representative subset of tools across different namespaces, ensuring they work correctly with the mock server and handle authentication, pagination, and error conditions as expected.
All write should be considered as a high-risk operation and require mandatory integration tests, especially those that modify data or state in Foundry (e.g., dataset creation, updates, deletions, triggering builds, applying actions). Read operations that access sensitive data or have complex pagination should also be prioritized for integration testing.

---

### Q6.3 — Packaging and distribution

- Should the toolset be delivered as a standalone Python package (separate from `foundry-platform-sdk`)?
- Should it depend on `foundry-platform-sdk` from PyPI, or bundle the provided source code?
- Is there a private PyPI registry, or is public PyPI acceptable?
- Should a Docker image be published, and if so, to which registry?


### A6.3 — Packaging and distribution

- Toolset code should reside inside the skills folders in the repository, not as a standalone package.
- It should depend on `foundry-platform-sdk` from PyPI/conda. Instructions should be provided in the SKILL.md files that accompany each skill on how to install the SDK.
- Public PyPI is acceptable for the SDK dependency, but the skill code itself will be distributed via the repository.
- A Docker image is not required for this project, as the tools will be run in developer environments and integrated into agent workflows directly from the repository.

---

### Q6.4 — Licensing

- The provided SDK is Apache 2.0 licensed. Is the same licence expected for this project?
- Are there any IP or copyright constraints on reusing or wrapping the SDK CLI code?

### A6.4 — Licensing

The same Apache 2.0 license is expected for this project, and there are no additional IP or copyright constraints on reusing or wrapping the SDK CLI code, as long as proper attribution is given according to the license terms.


---

### Q6.5 — CI/CD pipeline

- Should the project include a CI pipeline (GitHub Actions, CircleCI, GitLab CI)?
- Are there code quality gates required (linting, type checking with pyright/mypy, security scanning)?

### A6.5 — CI/CD pipeline

- Not required.
- Code quality gates are required, including linting and type checking which is mandatory.
- Security scanning for OWASP Top 10 vulnerabilities should be included as part of development process.

---

## Summary Priority Matrix

| # | Question | Impact if not answered | Suggested owner |
| --- | --- | --- | --- |
| Q1.1 | Relationship to existing SDK CLI | Could duplicate 14 000 lines of code | Product Owner |
| Q1.2 | FR-02 content | Incomplete requirements | Business Analyst |
| Q2.1 | Claude agent skill format | Wrong architecture entirely | Product Owner / Architect |
| Q2.2 | Target agent platform | Affects tool interface design | Product Owner |
| Q3.1 | Auth method | Security architecture decision | Product Owner / Security |
| Q3.2 | Credential injection | Deployment blocker | DevOps / Security |
| Q1.3 | "All capabilities" scope | Scope of implementation | Product Owner |
| Q4.1 | Output format | Unusable by agents if wrong | Product Owner |
| Q2.3 | MCP server specifics | If MCP: server type determines packaging | Architect |
| Q6.1 | Test environment | Testing strategy blocked | Product Owner / DevOps |

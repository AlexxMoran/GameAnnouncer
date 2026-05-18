# Operation-Oriented Architecture

This project uses a lightweight operation-oriented architecture for complex
business behavior.

The main idea is simple: ordinary domain modules keep stable domain code, while
meaningful business operations get their own operation folder. An operation is a
business action that can be triggered by an HTTP route, background task, cron
job, event consumer, webhook, or CLI command.

Examples:

- generate an announcement bracket
- update an announcement with registration form changes
- submit a match result
- approve a registration request
- expire outdated registration requests

Simple CRUD, searches, and small one-step updates should stay in regular
modules.

## Why We Use It

Operation-oriented code makes complex workflows easier to find, read, test, and
change. Instead of spreading a scenario across a large service file, the
operation keeps the business flow in one small folder with clear
responsibilities.

This is useful when an action:

- touches multiple tables or modules
- changes lifecycle status
- has important business rules
- coordinates repositories, state machines, builders, or background work
- can be triggered from more than one entrypoint
- would otherwise grow into a large generic service

## Trade-Offs

Benefits:

- clearer location for business workflows
- works for user-triggered and system-triggered actions
- smaller files with sharper responsibilities
- easier testing of pure decisions separately from database writes
- better navigation for developers and AI agents
- smoother future extraction of business capabilities

Costs:

- more files than a single service
- extra naming discipline is required
- overuse can make simple code feel heavy
- gateway files can become new service objects if decisions are not kept clean
- documentation can drift if every small action gets its own structure

The rule is: use operations for meaningful multi-step business behavior, not for
every endpoint.

## Project Boundaries

In this project:

- `api/**` remains the HTTP interface layer and owns authorization checks
- `tasks/**` remains the system/background entrypoint layer
- `operations/**` owns complex business operations
- `modules/**` remains the domain layer with models, schemas, queries,
  repositories, validators, state machines, builders, and simple services
- `core/**` owns platform-level application support

Operations should not move permission checks out of API routes unless the
project explicitly changes its authorization model.

Entrypoints should own transaction commit boundaries unless a specific operation
needs a different transaction strategy.

## Basic Operation Structure

Use this structure first:

```text
backend/operations/{verb_object}/
  contract.py
  scenario.py
  gateway.py
  structures.py
  decisions.py
```

Use verb-object names:

- `generate_announcement_bracket`
- `update_announcement`
- `submit_match_result`
- `approve_registration_request`

Avoid generic names:

- `announcement_service`
- `bracket_manager`
- `registration_handler`
- `process_update`

## Scenario Flow

The default data flow is:

```text
Contract
  -> Scenario
  -> Gateway.load()
  -> Snapshot
  -> Decisions.make()
  -> Decision
  -> Gateway.apply()
  -> Result
```

The important separation:

- contract describes input
- scenario orders steps
- gateway translates between the world and operation data
- snapshot contains facts loaded for the operation
- decisions choose what should happen and return a plan

## File Responsibilities

### `contract.py`

Defines the input contract for running the operation. It should not know about
FastAPI, HTTP status codes, SQLAlchemy sessions, queues, or email clients.

Example:

```python
from pydantic import BaseModel


class GenerateAnnouncementBracketContract(BaseModel):
    announcement_id: int
```

### `scenario.py`

The main orchestration script. It should read like the business flow.

Example:

```python
class GenerateAnnouncementBracketScenario:
    def __init__(self, session):
        self._gateway = GenerateAnnouncementBracketGateway(session)
        self._decisions = GenerateAnnouncementBracketDecisions()

    async def run(self, contract):
        snapshot = await self._gateway.load(contract)
        decision = self._decisions.make(snapshot)
        return await self._gateway.apply(decision)
```

Keep `scenario.py` focused on order, not details.

### `gateway.py`

Loads data and applies changes through project modules, repositories, builders,
state machines, and the database session.

It is the operation's gateway to the rest of the application. It translates ORM
models, API-adjacent data, events, or external records into operation snapshots,
then applies operation decisions back to the application world.

Good responsibilities:

- load the data needed by the operation
- return a snapshot for decisions
- persist the final decision
- call repositories, lifecycle services, and builders

Avoid putting business rules here unless they are persistence-specific, such as
concurrency or database constraint handling.

### `structures.py`

Defines internal operation data structures: snapshots, decisions, and small
supporting value objects. These are not API schemas and not ORM models.

Good responsibilities:

- describe facts loaded for the operation
- describe plans returned by the decisions layer
- keep operation data shapes easy to inspect

Avoid business rules, database access, framework objects, and persistence
behavior.

### `decisions.py`

Contains business rules and calculations. Prefer pure logic where possible.

Good responsibilities:

- validate business preconditions
- choose eligible records
- calculate derived values
- produce a decision object that `gateway.py` can apply

Avoid ORM models, database calls, commits, HTTP concerns, queue calls, and email
delivery.

Think of the data structures this way:

- Snapshot = facts known before the decision
- Decision = plan to apply after the decision

Example:

```python
@dataclass(frozen=True)
class GenerateAnnouncementBracketSnapshot:
    announcement_id: int
    has_existing_matches: bool
    participants: list[BracketParticipantSnapshot]


@dataclass(frozen=True)
class GenerateAnnouncementBracketDecision:
    announcement_id: int
    participant_seeds: list[ParticipantSeedDecision]
    bracket_size: int
```

## Responsibility Rules

- Scenario does not contain business rules.
- Decisions do not access the database or depend on ORM/framework objects.
- Gateway does not invent business rules.
- Contract does not know the interface.
- API owns user authorization.
- Entrypoint owns commit unless the operation has a documented reason not to.
- Modules do not import operations.

## Extended Operation Structure

Use this only for high-risk or genuinely complex operations:

```text
backend/operations/{verb_object}/
  README.md
  contract.py
  scenario.py
  gateway.py
  structures.py
  decisions.py
  effects.py
  errors.py
  tests/
```

Optional files:

- `README.md`: human explanation, reads, writes, invariants, danger zones
- `effects.py`: events, notifications, audit logs, cache invalidation, jobs
- `errors.py`: operation-specific domain/application errors
- `tests/`: operation-level tests when module-level tests become too broad

Add optional files only when they remove confusion or support real behavior.
Do not keep empty ritual files.

## README Template

Use this template for risky operations:

```md
# Operation Name

## Purpose

## Entrypoints

## Invariants

## Reads

## Writes

## Dangerous Writes

## Test Focus
```

## When Not To Create An Operation

Do not create an operation for:

- simple CRUD
- list/search/fetch endpoints
- small field updates with no workflow
- thin calls to one repository
- actions with no meaningful business rules

In those cases, keep the code inside the existing module.

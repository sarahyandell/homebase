# CLAUDE.md

Guidance for Claude Code when working in this repo.

## Project

homebase is an event-driven household and relocation platform: tasks, long-running cases, reminders and bills, built as a core Python app with event-driven edge services. It is a public portfolio project, so code quality, tests and clear design decisions matter as much as features.

### Architecture (hybrid, see `docs/decisions/0001-service-boundaries.md`)

Rule: keep the core together; split out the parts that depend on outside systems.

| Part | Location | Responsibility | Status |
|---|---|---|---|
| Core app: Tasks module | `services/core` | Checklist templates, task instances, due dates, dependencies | Building first |
| Core app: Cases module | `services/core` | Long-running processes: stages (state machine), document checklist, deadlines, timeline | Planned |
| Core app: Household module | `services/core` | Bills, subscriptions, renewals | Planned |
| Reminders service | `services/reminders` | Consumes events, sends notifications, owns birthday data | Planned |
| Integration service | `services/integration` | Reads payment emails/bank data, publishes `payment.detected` | Idea / later |

- Inside the core app, each module owns its own tables and other modules use its code interface, never its tables directly.
- A task stores its `case_id`; Cases updates its status when related tasks close.
- The core app and edge services talk only through events on a queue (e.g. `task.completed`, `task.due_soon`, `case.stage_changed`, `bill.due_soon`). No service reads another's database.

## Stack

- Python 3.14, FastAPI, pytest
- Docker and Docker Compose for local running
- GitHub Actions for CI
- LocalStack (SQS/SNS) for events locally; Terraform and AWS (ECS Fargate) later
- Prometheus and Grafana for observability later

## Commands

Fill these in as each piece is built.

- Run tests: _TBD_ (planned: `pytest` from each service folder)
- Run locally: _TBD_ (planned: `docker compose up`)

## Rules

- **Synthetic data only.** No real names, addresses, dates of birth, reference numbers, passport or ID details, in code, tests, seed data, docs or commit messages. Use obviously fake values. Where a real reference would go, the app stores a note such as "reference in password manager".
- **No secrets.** Never write real credentials, tokens or keys to any file. Config comes from environment variables; add new ones to `.env.example` with fake values.
- **Tests for new code.** Every new behaviour gets a pytest test. Keep tests passing before moving on.
- **Small steps.** One focused change at a time, easy to review. Explain the plan before large changes.
- **Don't write my design decisions.** I write the files in `docs/decisions/` myself. You can review them or ask questions, but don't draft them.
- **Ask before implementing task dependency logic** in the Tasks service. I plan to write the core of it by hand.
- **Official sources, not hardcoded rules.** Relocation tasks link to official pages (Services Australia, ATO, VicRoads, etc.) instead of encoding government requirements in code.
- Don't commit or push unless asked.

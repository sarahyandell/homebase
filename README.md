# homebase
Event-driven household and relocation platform: tasks, long-running cases, reminders and bills, built as a core Python app with event-driven edge services, Docker, CI and Terraform.


## Why it exists
Moving to Melbourne, there are a lot of tasks that must be done here and also there. Keeping track of two phone numbers, transferring healthcare records, setting up bank accounts etc. Alongside this it will be able to keep track of long running applications such as visas and job applications. This project is aimed at helping to keep track of all these tasks, while also keeping my engineering skills fresh and developing, particularly Docker, CI/CD, Terraform and AWS alongside event-driven services.

Longer term I would like to move to using this as a general household planner, with the potential to use an old tablet as an updatable household tracker kept in the kitchen.

## Architecture
homebase is a hybrid: one core app holding the main features, plus separate services at the edges where it talks to the outside world. They communicate through events.

| Part | What it does | Status |
|---|---|---|
| **Core app** | Tasks, Cases and Household, as separate modules in one app | In progress (Tasks first) |
| **Reminders** service | Listens for events and sends notifications | Planned |
| **Integration** service | Reads payment emails or bank data and reports payments | Idea / later |

See [docs/decisions/0001-service-boundaries.md](docs/decisions/0001-service-boundaries.md) for why it is split this way.

## Planned features
- Tasks: Everyday task tracker in the form of a checklist with due dates, including dependencies as well as a next step view that shows only the tasks you can start now.
- Cases/Applications: Can be used for longer term things such as following the visa application process and job applications, linked to tasks as it will have tasks associated with the case
- Reminders: General date reminders in regards to birthdays etc but also to send notifications when something is due or overdue. Different levels of reminders- so gentle nudge vs an alarm.
  - "Still needed?" check: only a task's title is required, so tasks can be captured quickly. If a task is created without a due date or an assigned family member, a reminder is sent one week after it was created asking if it is still needed. This stops random tasks being added and then sinking to the bottom of the pile. (Uses each task's `created_at`, and needs a `task.created` event that Reminders listens for.)
- Household: keep track of general household things like bills, subscriptions and renewals.

## Ideas / later
- Automatically mark bills as paid from payment confirmation emails or bank transactions (starting with CSV import).

## Status

Early stages, repo set up including project outline.
Task services next.

## Data note
All of the data in this repo is synthetic, no real data is stored here.

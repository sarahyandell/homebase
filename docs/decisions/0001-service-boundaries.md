# 0001: Service boundaries

- **Status:** Accepted
- **Date:** 2026-10-09

## Context

The app needs to handle short tasks, long-running processes, reminders and recurring bills.

It has two goals: to be useful day to day, and to practise skills for my next role.

Constraints: one developer, ~4 hours a day, personal scale, low cost.

## Decision

homebase is a **hybrid**: one core app holding the main features, plus separate services at the edges where it talks to the outside world.

The rule: **keep the core together, and split out the parts that depend on outside systems.** The core only depends on its own data. The edge services depend on things I don't control (email providers, bank APIs), so they are allowed to fail without breaking the core.

To keep it simple and concise, the idea is to iterate on it but start with an MVP.

### The parts

**Core app** (one app, separate modules):
- **Tasks:** Individual small/simple tasks that can but don't need to be grouped by cases.
- **Cases:** Applications for things like jobs/visas, any longer term goal or piece of work that may have multiple stages to keep track on.
- **Household:** Bills, registrations, anything to do with household maintenance etc.

**Edge services** (separate apps):
- **Reminders:** Can be based off dates that relate to tasks, cases, household. Owns the birthday information and anything else important. Handles what goes *out* (notifications).
- **Integration** (later): Reads payment emails or bank data and reports payments. Handles what comes *in*.

### Why the boundaries fall where they do

**Why is a Case different from a Task?**
A case is a longer term goal, objective or application. It can be made up of many tasks, but is used to keep track of key applications etc.

**Why is Household a separate module?**
It is separate so there can be two separate sections and purposes for this project. One is Moving to Melbourne and then the other is household which can be used more long term. Alongside this the data is different: bills repeat (monthly, yearly) and have amounts and renewal dates, while tasks happen once.

**Why are Tasks, Cases and Household in one app?**
They only depend on their own data and are closely linked (cases are made up of tasks), so they are likely to change together. Separate deployments would add setup without a real benefit at this scale.

**Why is Reminders a separate service?**
You may have reminders set for different things not related to tasks, as well as tasks, cases and bills all need reminders, so keeping them in one place means none of the other parts has to handle notifications. It also has a different failure profile: it runs in the background, depends on outside email/push providers, and can retry later. If a provider is down, the core app should keep working and reminders should catch up from the queue.

**Why will Integration be a separate service?**
Like Reminders, it depends on unreliable outside systems (Gmail, bank APIs). It turns their messy data into a standard `payment.detected` event, so Household never needs to know about email formats or bank APIs (an anti-corruption layer).

**Why is Documents left out for now?**
Due to time, budget and developer constraints for the moment this is left out.

### How the parts link and talk

- **Cases and tasks:** A task will store the case ID, and when tasks are closed that relate to a case, the relevant case status will be updated.
- **Inside the core app:** each module owns its own tables. Modules don't read each other's tables directly; they go through each other's code interfaces.
- **Between the core app and edge services:** services publish events when something happens (task created, deadline passed etc.) through a message queue. Other services listen and react (when a new task is created, a relevant reminder may be set).
- Each edge service has its own data. No service reads another service's database.

## Alternatives considered

**A single app (monolith) with no internal boundaries**
This would be simpler, with one database as well, but I want to challenge myself a bit. Without clear boundaries, messy outside data and notification code would sit in the same code as the core logic.

**A modular monolith (one app, all four parts as modules)**
I decided not to put the reminders in the app and keep it separate as this functions differently to the other modules. When the other modules are tested or fail, we will know instantly as it happens instantly whereas reminders will be when I am not necessarily actively on the app or when it is running in the background. Alongside this the reminders will be connected externally, depending on the way we want the reminders to work, so this also keeps the internal data separate from any outside connection. 

**Four separate services from day one**
This was also considered as would be good learning experience but it was decided based off time constraints and unnecessary complexity that I would not follow this route. 

## Consequences

### What we gain

- Practice with real events and a message queue where it makes sense, not everywhere.
- The core app stays working if notification or bank providers fail.
- Clear data ownership, inside the core app and between services.
- Fewer moving parts than four services, so I can work towards an MVP faster.

### What it costs

- More moving parts than a single app: a queue, a second Docker image and pipeline.
- Eventual consistency: reminders react to events a moment after they happen, not instantly.
- Harder debugging across the core app and the services.
- Module boundaries inside the core app are kept by discipline, not enforced by separate deployments.
- Testing between tasks and cases still needs to be rigorous, as these relate to each other.

### How we limit the costs

Build Tasks first, add parts one at a time, stay local for the time being.

## When to revisit

- Once tested and working locally, re-look at associated cloud costs etc.
- If payment automation is added, build it as the Integration service, following the same edge rule.
- If Household's payment logic grows complex and starts changing for different reasons than Tasks and Cases, consider splitting it out.
- If Reminders and the core app keep needing to change together, consider bringing Reminders back into the core app.

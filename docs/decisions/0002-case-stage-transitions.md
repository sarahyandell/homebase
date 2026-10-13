# 0002: Case stage transitions

- **Status:** Proposed
- **Date:** 2026-10-13

## Context

How do Cases and tasks intereact with each other?
How do stages in cases change and the logic around this. 

## Decision

Tasks relate to cases, and so when a task changes or complete the system suggests moves based on the stage's tasks. 

### How a stage changes

- Stages never change on their own. 
- When all tasks in a stage are complete, you can then either accept the stage is complete and move it to the next or decline it. 
- If you say no to moving the stage when all tasks are compelte, you get a reminder in 3 days. 
- You can move the stage forward or backward at any time. 


### Ready to move on
- When all tasks are done and you accept it is ready to move on
- You only see the suggestion while the app is open
- For now as there is no frontend you just get a "ready for next stage? field in the api response
- A stage with no tasks counts as ready immidiately



### Not yet
- Click "Not Yet" to decline moving to the next stage when tasks are done
- The suggestion shows the next time you open the app after 3 days
- If after that 3 days you still don't want to move to the next stage then the wait resets. 
### Moving backwards
- If a task re-opens or a new task is created and is set to an earlier stage in the case then the system suggests moving it back and re-opening that stage


### How it links to Tasks

- Each task stores case_id and case_stage_id, an ID rather than the stage name, so renaming a stage doesn't break anything.
- A task with a case must also have a stage, and that stage must belong to the same case.
- Case tasks are created through Cases, which checks the stage and then calls Tasks' interface.
- Tasks never calls Cases. Dependencies only go one way, from Cases to Tasks.

## Alternatives considered

- Fully automatic stage changes: rejected because a case could move unexpectedly, especially backwards after something like a visa application has been submitted.
- Automatic changes with a manual override: rejected because it means deciding whether an override sticks, locks the stage, or gets undone by the next task event. Confirming every move avoids that conflict entirely.
- Tasks calling Cases directly: rejected because the two modules would depend on each other.
Cases reacting to task events (in-process or through the queue): not needed while the suggestion only appears with the app open, so it's kept for later.
- Storing the stage name instead of an ID: rejected because renaming a stage would break the link.


## When to revisit
If you want a notification when the app isn't open. That needs Cases to react to task events and publish to Reminders.
If confirming every stage change becomes tedious, consider automatic moves for some stages.


from typing import Protocol

from app.tasks.model import Task


class TaskRepository(Protocol):
    def add(self, task: Task) -> None: ...

    def get(self, task_id: str) -> Task | None: ...

    def list(self) -> list[Task]: ...


class InMemoryTaskRepository:
    """Keeps tasks in a dict. Data is lost when the app stops."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list(self) -> list[Task]:
        return list(self._tasks.values())

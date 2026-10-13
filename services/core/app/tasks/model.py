from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    OPEN = "open"
    DONE = "done"


@dataclass
class Task:
    title: str
    due_date: date | None = None
    assigned_to: str | None = None
    notes: str | None = None
    start_by: date | None = None
    case_id: str | None = None
    status: TaskStatus = TaskStatus.OPEN
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Title must not be blank")
        if self.assigned_to is not None and not self.assigned_to.strip():
            raise ValueError("Assigned family member must not be blank")
        if self.start_by and self.due_date and self.start_by > self.due_date:
            raise ValueError("Start by date must not be after the due date")

    def complete(self) -> None:
        self.status = TaskStatus.DONE

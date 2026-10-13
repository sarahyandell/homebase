from dataclasses import asdict
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.tasks.model import Task, TaskStatus
from app.tasks.repository import InMemoryTaskRepository, TaskRepository

router = APIRouter(prefix="/tasks", tags=["tasks"])

_repository = InMemoryTaskRepository()


def get_repository() -> TaskRepository:
    return _repository


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    due_date: date | None = None
    assigned_to: str | None = Field(default=None, min_length=1)
    notes: str | None = None
    start_by: date | None = None
    case_id: str | None = None


class TaskOut(BaseModel):
    id: str
    title: str
    due_date: date | None
    assigned_to: str | None
    notes: str | None
    start_by: date | None
    case_id: str | None
    status: TaskStatus
    created_at: datetime


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskOut)
def create_task(body: TaskCreate, repo: TaskRepository = Depends(get_repository)):
    try:
        task = Task(**body.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error))
    repo.add(task)
    return asdict(task)


@router.get("", response_model=list[TaskOut])
def list_tasks(repo: TaskRepository = Depends(get_repository)):
    return [asdict(task) for task in repo.list()]


@router.post("/{task_id}/complete", response_model=TaskOut)
def complete_task(task_id: str, repo: TaskRepository = Depends(get_repository)):
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task.complete()
    repo.add(task)
    return asdict(task)

from datetime import UTC, date, datetime

import pytest

from app.tasks.model import Task, TaskStatus

DUE = date(2026, 12, 1)


def make_task(**overrides) -> Task:
    fields = {"title": "Cancel phone contract", "due_date": DUE, "assigned_to": "Alex Example"}
    fields.update(overrides)
    return Task(**fields)


def test_task_needs_only_a_title():
    task = Task(title="Sort out phone numbers")

    assert task.due_date is None
    assert task.assigned_to is None


def test_new_task_records_when_it_was_created():
    before = datetime.now(UTC)
    task = make_task()
    after = datetime.now(UTC)

    assert before <= task.created_at <= after


def test_new_task_is_open():
    task = make_task()

    assert task.status == TaskStatus.OPEN


def test_new_tasks_get_unique_ids():
    first = make_task(title="First")
    second = make_task(title="Second")

    assert first.id != second.id


def test_complete_marks_task_done():
    task = make_task()

    task.complete()

    assert task.status == TaskStatus.DONE


@pytest.mark.parametrize("title", ["", "   "])
def test_blank_title_is_rejected(title):
    with pytest.raises(ValueError, match="Title"):
        make_task(title=title)


@pytest.mark.parametrize("assigned_to", ["", "   "])
def test_blank_assigned_to_is_rejected(assigned_to):
    with pytest.raises(ValueError, match="Assigned family member"):
        make_task(assigned_to=assigned_to)


def test_start_by_after_due_date_is_rejected():
    with pytest.raises(ValueError, match="Start by"):
        make_task(start_by=date(2026, 12, 2))


def test_start_by_on_due_date_is_allowed():
    task = make_task(start_by=DUE)

    assert task.start_by == DUE


def test_start_by_before_due_date_is_allowed():
    task = make_task(start_by=date(2026, 11, 15))

    assert task.start_by == date(2026, 11, 15)


def test_start_by_without_due_date_is_allowed():
    task = make_task(due_date=None, start_by=date(2026, 11, 15))

    assert task.start_by == date(2026, 11, 15)

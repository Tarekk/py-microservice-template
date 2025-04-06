import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from api.deps import CurrentUser, DBSessionDep
from api.models.shared.common import Message
from api.models.tasks import Task, TaskCreate, TaskPublic, TasksPublic, TaskUpdate

router = APIRouter()


@router.get("", response_model=TasksPublic)
def read_tasks(
    session: DBSessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve tasks.
    """
    count_statement = select(func.count()).select_from(Task)
    count = session.exec(count_statement).one()
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()

    tasks_public = [TaskPublic.model_validate(task) for task in tasks]
    return TasksPublic(data=tasks_public, count=count)


@router.get("/{id}", response_model=TaskPublic)
def read_task(
    id: uuid.UUID,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get task by ID.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskPublic.model_validate(task)


@router.post("", response_model=TaskPublic)
def create_task(
    *,
    task_in: TaskCreate,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Create new task.
    """
    task = Task.model_validate(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskPublic.model_validate(task)


@router.put("/{id}", response_model=TaskPublic)
def update_task(
    *,
    id: uuid.UUID,
    task_in: TaskUpdate,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Update a task.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_dict = task_in.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_dict)
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskPublic.model_validate(task)


@router.delete("/{id}")
def delete_task(
    id: uuid.UUID,
    session: DBSessionDep,
    current_user: CurrentUser,
) -> Message:
    """
    Delete a task.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return Message(message="Task deleted successfully")

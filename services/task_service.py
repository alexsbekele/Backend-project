from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Task, User
from schemas import TaskCreate, TaskUpdate


from typing import Literal

SORT_COLUMNS = {"created_at": Task.created_at, "title": Task.title}


def list_tasks(
    db: Session,
    user: User,
    limit: int,
    offset: int,
    completed: bool | None,
    sort_by: Literal["created_at", "title"],
    order: Literal["asc", "desc"],
) -> tuple[list[Task], int]:
    query = db.query(Task).filter(Task.user_id == user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    total = query.count()

    column = SORT_COLUMNS[sort_by]
    column = column.asc() if order == "asc" else column.desc()

    items = query.order_by(column, Task.id).offset(offset).limit(limit).all()
    return items, total


def get_owned_task(db: Session, task_id: int, user: User) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, user: User, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        completed=data.completed,
        user_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, user: User, data: TaskUpdate) -> Task:
    task = get_owned_task(db, task_id, user)
    task.title = data.title
    task.description = data.description
    task.completed = data.completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user: User) -> None:
    task = get_owned_task(db, task_id, user)
    db.delete(task)
    db.commit()
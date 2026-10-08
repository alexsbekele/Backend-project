from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Task, User
from schemas import TaskCreate, TaskUpdate


def list_tasks(db: Session, user: User) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user.id).all()


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
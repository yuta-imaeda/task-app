from sqlalchemy.orm import Session
from datetime import datetime, UTC

from task_app.models.task import Task
from task_app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Task model's database operations at repository layer."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task_in: TaskCreate) -> Task:
        """Create a new task and save to database."""
        db_task = Task(
            title=task_in.title,
            description=task_in.description,
            completed=False,
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: int) -> Task | None:
        """Get task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks with pagination support."""
        return self.db.query(Task).offset(skip).limit(limit).all()

    def update(self, task_id: int, task_in: TaskUpdate) -> Task | None:
        """Update task by ID."""
        db_task = self.get_by_id(task_id)
        if not db_task:
            return None

        update_data = task_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_task, field, value)

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        db_task = self.get_by_id(task_id)
        if not db_task:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True

    def mark_complete(self, task_id: int) -> Task | None:
        """Mark task as completed."""
        db_task = self.get_by_id(task_id)
        if not db_task:
            return None

        db_task.completed = True

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def mark_incomplete(self, task_id: int) -> Task | None:
        """Mark task as incomplete."""
        db_task = self.get_by_id(task_id)
        if not db_task:
            return None

        db_task.completed = False

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

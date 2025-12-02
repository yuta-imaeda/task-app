import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta

from task_app.database import Base
from task_app.models.task import Task
from task_app.schemas.task import TaskCreate, TaskUpdate
from task_app.repositories.task import TaskRepository


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


class TestTaskRepositoryCreate:

    def test_create_valid_task(self, db: Session):
        repo = TaskRepository(db)
        task_in = TaskCreate(title="Buy groceries", description="Milk, eggs, bread")
        
        result = repo.create(task_in)
        
        assert result.id is not None
        assert result.title == "Buy groceries"
        assert result.description == "Milk, eggs, bread"
        assert result.completed is False
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_task_without_description(self, db: Session):
        repo = TaskRepository(db)
        task_in = TaskCreate(title="Buy groceries")
        
        result = repo.create(task_in)
        
        assert result.id is not None
        assert result.title == "Buy groceries"
        assert result.description is None

    def test_create_multiple_tasks(self, db: Session):
        repo = TaskRepository(db)
        
        task1 = repo.create(TaskCreate(title="Task 1"))
        task2 = repo.create(TaskCreate(title="Task 2"))
        
        assert task1.id != task2.id
        assert task1.title == "Task 1"
        assert task2.title == "Task 2"


class TestTaskRepositoryGetById:

    def test_get_by_id_existing_task(self, db: Session):
        repo = TaskRepository(db)
        created = repo.create(TaskCreate(title="Test task"))
        
        result = repo.get_by_id(created.id)
        
        assert result is not None
        assert result.id == created.id
        assert result.title == "Test task"

    def test_get_by_id_non_existing_task(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.get_by_id(9999)
        
        assert result is None


class TestTaskRepositoryGetAll:

    def test_get_all_empty_list(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.get_all()
        
        assert result == []

    def test_get_all_returns_all_tasks(self, db: Session):
        repo = TaskRepository(db)
        task1 = repo.create(TaskCreate(title="Task 1"))
        task2 = repo.create(TaskCreate(title="Task 2"))
        task3 = repo.create(TaskCreate(title="Task 3"))
        
        result = repo.get_all()
        
        assert len(result) == 3
        assert any(t.id == task1.id for t in result)
        assert any(t.id == task2.id for t in result)
        assert any(t.id == task3.id for t in result)

    def test_get_all_with_pagination(self, db: Session):
        repo = TaskRepository(db)
        for i in range(10):
            repo.create(TaskCreate(title=f"Task {i}"))
        
        page1 = repo.get_all(skip=0, limit=5)
        page2 = repo.get_all(skip=5, limit=5)
        
        assert len(page1) == 5
        assert len(page2) == 5
        page1_ids = {t.id for t in page1}
        page2_ids = {t.id for t in page2}
        assert page1_ids.isdisjoint(page2_ids)


class TestTaskRepositoryUpdate:

    def test_update_task_title(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Original title"))
        
        result = repo.update(task.id, TaskUpdate(title="Updated title"))
        
        assert result is not None
        assert result.title == "Updated title"
        assert result.id == task.id

    def test_update_task_description(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Task", description="Original"))
        
        result = repo.update(task.id, TaskUpdate(description="Updated description"))
        
        assert result is not None
        assert result.description == "Updated description"
        assert result.title == "Task"

    def test_update_non_existing_task(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.update(9999, TaskUpdate(title="New title"))
        
        assert result is None

    def test_update_timestamp(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Task"))
        original_updated_at = task.updated_at
        
        import time
        time.sleep(0.05)
        
        result = repo.update(task.id, TaskUpdate(title="Updated"))
        
        assert result is not None
        assert result.updated_at >= original_updated_at


class TestTaskRepositoryDelete:

    def test_delete_existing_task(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Task to delete"))
        task_id = task.id
        
        result = repo.delete(task_id)
        
        assert result is True
        assert repo.get_by_id(task_id) is None

    def test_delete_non_existing_task(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.delete(9999)
        
        assert result is False


class TestTaskRepositoryMarkComplete:

    def test_mark_complete(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Task to complete"))
        
        result = repo.mark_complete(task.id)
        
        assert result is not None
        assert result.completed is True

    def test_mark_complete_non_existing_task(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.mark_complete(9999)
        
        assert result is None

    def test_mark_incomplete(self, db: Session):
        repo = TaskRepository(db)
        task = repo.create(TaskCreate(title="Task"))
        repo.mark_complete(task.id)
        
        result = repo.mark_incomplete(task.id)
        
        assert result is not None
        assert result.completed is False

    def test_mark_incomplete_non_existing_task(self, db: Session):
        repo = TaskRepository(db)
        
        result = repo.mark_incomplete(9999)
        
        assert result is None

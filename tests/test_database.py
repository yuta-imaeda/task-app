"""データベース設計・初期化のテスト（TDD）"""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from task_app.database import Base, get_db, init_db, DATABASE_URL
from task_app.models.task import Task


class TestDatabaseSetup:
    """データベース設定のテスト"""

    def test_database_url_is_configured(self):
        """DATABASE_URLが設定されていること"""
        assert DATABASE_URL is not None
        assert "sqlite" in DATABASE_URL or "postgresql" in DATABASE_URL

    def test_base_is_declarative_base(self):
        """BaseがSQLAlchemy declarative baseであること"""
        assert hasattr(Base, "metadata")
        assert hasattr(Base, "registry")


class TestTaskModel:
    """Taskモデルのテスト"""

    def test_task_table_exists(self):
        """tasksテーブルが存在すること"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "tasks" in tables

    def test_task_has_required_columns(self):
        """Taskモデルに必要なカラムがあること"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("tasks")}
        
        required_columns = {"id", "title", "description", "completed", "created_at", "updated_at"}
        assert required_columns.issubset(columns)

    def test_task_id_is_primary_key(self):
        """idがプライマリーキーであること"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        pk = inspector.get_pk_constraint("tasks")
        assert "id" in pk["constrained_columns"]

    def test_task_title_is_not_nullable(self):
        """titleがNOT NULLであること"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        columns = {col["name"]: col for col in inspector.get_columns("tasks")}
        assert columns["title"]["nullable"] is False

    def test_task_completed_default_is_false(self):
        """completedのデフォルト値がFalseであること"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        task = Task(title="Test Task")
        session.add(task)
        session.commit()
        session.refresh(task)
        
        assert task.completed is False
        session.close()


class TestDatabaseInitialization:
    """データベース初期化のテスト"""

    def test_init_db_creates_tables(self):
        """init_dbがテーブルを作成すること"""
        engine = create_engine("sqlite:///:memory:")
        init_db(engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "tasks" in tables

    def test_get_db_returns_session(self):
        """get_dbがセッションを返すこと"""
        db_generator = get_db()
        db = next(db_generator)
        assert db is not None
        # クリーンアップ
        try:
            next(db_generator)
        except StopIteration:
            pass


class TestTaskCRUD:
    """Task CRUD操作の基本テスト"""

    @pytest.fixture
    def db_session(self):
        """テスト用データベースセッション"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_task(self, db_session):
        """タスクを作成できること"""
        task = Task(title="New Task", description="Task description")
        db_session.add(task)
        db_session.commit()
        
        assert task.id is not None
        assert task.title == "New Task"
        assert task.description == "Task description"

    def test_read_task(self, db_session):
        """タスクを読み取れること"""
        task = Task(title="Read Test")
        db_session.add(task)
        db_session.commit()
        
        retrieved = db_session.query(Task).filter_by(id=task.id).first()
        assert retrieved is not None
        assert retrieved.title == "Read Test"

    def test_update_task(self, db_session):
        """タスクを更新できること"""
        task = Task(title="Original Title")
        db_session.add(task)
        db_session.commit()
        
        task.title = "Updated Title"
        task.completed = True
        db_session.commit()
        
        retrieved = db_session.query(Task).filter_by(id=task.id).first()
        assert retrieved.title == "Updated Title"
        assert retrieved.completed is True

    def test_delete_task(self, db_session):
        """タスクを削除できること"""
        task = Task(title="To Delete")
        db_session.add(task)
        db_session.commit()
        task_id = task.id
        
        db_session.delete(task)
        db_session.commit()
        
        retrieved = db_session.query(Task).filter_by(id=task_id).first()
        assert retrieved is None

    def test_task_timestamps(self, db_session):
        """created_atとupdated_atが自動設定されること"""
        task = Task(title="Timestamp Test")
        db_session.add(task)
        db_session.commit()
        
        assert task.created_at is not None
        assert task.updated_at is not None

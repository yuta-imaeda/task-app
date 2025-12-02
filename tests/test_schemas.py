"""Pydanticスキーマのテスト"""

import pytest
from datetime import datetime, UTC
from pydantic import ValidationError


class TestTaskCreate:
    """TaskCreateスキーマのテスト"""

    def test_valid_task_create(self):
        """有効なデータでTaskCreateを作成できる"""
        from task_app.schemas.task import TaskCreate

        task = TaskCreate(title="テストタスク", description="説明文")
        assert task.title == "テストタスク"
        assert task.description == "説明文"

    def test_task_create_without_description(self):
        """descriptionなしでもTaskCreateを作成できる"""
        from task_app.schemas.task import TaskCreate

        task = TaskCreate(title="タイトルのみ")
        assert task.title == "タイトルのみ"
        assert task.description is None

    def test_task_create_empty_title_fails(self):
        """空のtitleはバリデーションエラー"""
        from task_app.schemas.task import TaskCreate

        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("title",)

    def test_task_create_whitespace_only_title_fails(self):
        """空白のみのtitleはバリデーションエラー"""
        from task_app.schemas.task import TaskCreate

        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="   ")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("title",)

    def test_task_create_title_too_long_fails(self):
        """256文字以上のtitleはバリデーションエラー"""
        from task_app.schemas.task import TaskCreate

        long_title = "a" * 256
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title=long_title)
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("title",)

    def test_task_create_title_max_length(self):
        """255文字のtitleは有効"""
        from task_app.schemas.task import TaskCreate

        max_title = "a" * 255
        task = TaskCreate(title=max_title)
        assert len(task.title) == 255


class TestTaskUpdate:
    """TaskUpdateスキーマのテスト"""

    def test_task_update_partial(self):
        """一部のフィールドのみで更新できる"""
        from task_app.schemas.task import TaskUpdate

        update = TaskUpdate(title="新しいタイトル")
        assert update.title == "新しいタイトル"
        assert update.description is None
        assert update.completed is None

    def test_task_update_all_fields(self):
        """すべてのフィールドで更新できる"""
        from task_app.schemas.task import TaskUpdate

        update = TaskUpdate(
            title="新しいタイトル",
            description="新しい説明",
            completed=True
        )
        assert update.title == "新しいタイトル"
        assert update.description == "新しい説明"
        assert update.completed is True

    def test_task_update_empty_is_valid(self):
        """すべてNoneでも有効"""
        from task_app.schemas.task import TaskUpdate

        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_task_update_title_validation(self):
        """更新時もtitleのバリデーションが適用される"""
        from task_app.schemas.task import TaskUpdate

        with pytest.raises(ValidationError):
            TaskUpdate(title="")

    def test_task_update_title_too_long_fails(self):
        """更新時も256文字以上のtitleはエラー"""
        from task_app.schemas.task import TaskUpdate

        long_title = "a" * 256
        with pytest.raises(ValidationError):
            TaskUpdate(title=long_title)


class TestTaskResponse:
    """TaskResponseスキーマのテスト"""

    def test_task_response_from_dict(self):
        """辞書からTaskResponseを作成できる"""
        from task_app.schemas.task import TaskResponse

        now = datetime.now(UTC)
        data = {
            "id": 1,
            "title": "テストタスク",
            "description": "説明",
            "completed": False,
            "created_at": now,
            "updated_at": now,
        }
        response = TaskResponse.model_validate(data)
        assert response.id == 1
        assert response.title == "テストタスク"
        assert response.completed is False

    def test_task_response_from_orm(self):
        """SQLAlchemyモデルからTaskResponseを作成できる"""
        from task_app.schemas.task import TaskResponse
        from task_app.models.task import Task

        # モックオブジェクトを作成
        class MockTask:
            id = 1
            title = "ORMタスク"
            description = "ORM説明"
            completed = True
            created_at = datetime.now(UTC)
            updated_at = datetime.now(UTC)

        response = TaskResponse.model_validate(MockTask())
        assert response.id == 1
        assert response.title == "ORMタスク"
        assert response.completed is True

    def test_task_response_serialization(self):
        """TaskResponseをJSONシリアライズできる"""
        from task_app.schemas.task import TaskResponse

        now = datetime.now(UTC)
        response = TaskResponse(
            id=1,
            title="テスト",
            description=None,
            completed=False,
            created_at=now,
            updated_at=now,
        )
        json_data = response.model_dump()
        assert json_data["id"] == 1
        assert json_data["title"] == "テスト"
        assert json_data["description"] is None

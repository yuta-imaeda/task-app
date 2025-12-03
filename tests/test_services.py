"""TaskServiceのテスト"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, UTC

from task_app.services.task import TaskService
from task_app.repositories.task import TaskRepository
from task_app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from task_app.models.task import Task


class TestTaskServiceCreate:
    """TaskService.createのテスト"""

    def test_create_task_success(self):
        """正常にタスクを作成できること"""
        # Arrange
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.title = "テストタスク"
        mock_task.description = "説明"
        mock_task.completed = False
        mock_task.created_at = datetime.now(UTC)
        mock_task.updated_at = datetime.now(UTC)
        mock_repo.create.return_value = mock_task

        service = TaskService(mock_repo)
        task_in = TaskCreate(title="テストタスク", description="説明")

        # Act
        result = service.create(task_in)

        # Assert
        mock_repo.create.assert_called_once_with(task_in)
        assert result == mock_task

    def test_create_task_without_description(self):
        """説明なしでタスクを作成できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.title = "タイトルのみ"
        mock_task.description = None
        mock_task.completed = False
        mock_task.created_at = datetime.now(UTC)
        mock_task.updated_at = datetime.now(UTC)
        mock_repo.create.return_value = mock_task

        service = TaskService(mock_repo)
        task_in = TaskCreate(title="タイトルのみ")

        result = service.create(task_in)

        mock_repo.create.assert_called_once_with(task_in)
        assert result.title == "タイトルのみ"
        assert result.description is None


class TestTaskServiceGetById:
    """TaskService.get_by_idのテスト"""

    def test_get_by_id_found(self):
        """存在するIDでタスクを取得できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.title = "取得タスク"
        mock_repo.get_by_id.return_value = mock_task

        service = TaskService(mock_repo)

        result = service.get_by_id(1)

        mock_repo.get_by_id.assert_called_once_with(1)
        assert result == mock_task

    def test_get_by_id_not_found(self):
        """存在しないIDでNoneが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.get_by_id.return_value = None

        service = TaskService(mock_repo)

        result = service.get_by_id(999)

        mock_repo.get_by_id.assert_called_once_with(999)
        assert result is None


class TestTaskServiceGetAll:
    """TaskService.get_allのテスト"""

    def test_get_all_default_pagination(self):
        """デフォルトのページネーションでタスク一覧を取得できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_tasks = [Mock(spec=Task) for _ in range(3)]
        mock_repo.get_all.return_value = mock_tasks

        service = TaskService(mock_repo)

        result = service.get_all()

        mock_repo.get_all.assert_called_once_with(skip=0, limit=100)
        assert len(result) == 3

    def test_get_all_with_pagination(self):
        """ページネーションパラメータでタスク一覧を取得できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_tasks = [Mock(spec=Task) for _ in range(5)]
        mock_repo.get_all.return_value = mock_tasks

        service = TaskService(mock_repo)

        result = service.get_all(skip=10, limit=5)

        mock_repo.get_all.assert_called_once_with(skip=10, limit=5)
        assert len(result) == 5

    def test_get_all_empty_list(self):
        """タスクがない場合は空リストが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.get_all.return_value = []

        service = TaskService(mock_repo)

        result = service.get_all()

        assert result == []


class TestTaskServiceUpdate:
    """TaskService.updateのテスト"""

    def test_update_task_success(self):
        """タスクを更新できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.title = "更新後タイトル"
        mock_repo.update.return_value = mock_task

        service = TaskService(mock_repo)
        task_in = TaskUpdate(title="更新後タイトル")

        result = service.update(1, task_in)

        mock_repo.update.assert_called_once_with(1, task_in)
        assert result == mock_task

    def test_update_task_not_found(self):
        """存在しないタスクの更新でNoneが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.update.return_value = None

        service = TaskService(mock_repo)
        task_in = TaskUpdate(title="更新タイトル")

        result = service.update(999, task_in)

        mock_repo.update.assert_called_once_with(999, task_in)
        assert result is None

    def test_update_task_partial(self):
        """一部フィールドのみ更新できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.completed = True
        mock_repo.update.return_value = mock_task

        service = TaskService(mock_repo)
        task_in = TaskUpdate(completed=True)

        result = service.update(1, task_in)

        mock_repo.update.assert_called_once_with(1, task_in)
        assert result.completed is True


class TestTaskServiceDelete:
    """TaskService.deleteのテスト"""

    def test_delete_task_success(self):
        """タスクを削除できること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.delete.return_value = True

        service = TaskService(mock_repo)

        result = service.delete(1)

        mock_repo.delete.assert_called_once_with(1)
        assert result is True

    def test_delete_task_not_found(self):
        """存在しないタスクの削除でFalseが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.delete.return_value = False

        service = TaskService(mock_repo)

        result = service.delete(999)

        mock_repo.delete.assert_called_once_with(999)
        assert result is False


class TestTaskServiceMarkComplete:
    """TaskService.mark_completeのテスト"""

    def test_mark_complete_success(self):
        """タスクを完了状態にできること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.completed = True
        mock_repo.mark_complete.return_value = mock_task

        service = TaskService(mock_repo)

        result = service.mark_complete(1)

        mock_repo.mark_complete.assert_called_once_with(1)
        assert result.completed is True

    def test_mark_complete_not_found(self):
        """存在しないタスクの完了でNoneが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.mark_complete.return_value = None

        service = TaskService(mock_repo)

        result = service.mark_complete(999)

        mock_repo.mark_complete.assert_called_once_with(999)
        assert result is None


class TestTaskServiceMarkIncomplete:
    """TaskService.mark_incompleteのテスト"""

    def test_mark_incomplete_success(self):
        """タスクを未完了状態にできること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task = Mock(spec=Task)
        mock_task.id = 1
        mock_task.completed = False
        mock_repo.mark_incomplete.return_value = mock_task

        service = TaskService(mock_repo)

        result = service.mark_incomplete(1)

        mock_repo.mark_incomplete.assert_called_once_with(1)
        assert result.completed is False

    def test_mark_incomplete_not_found(self):
        """存在しないタスクの未完了でNoneが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.mark_incomplete.return_value = None

        service = TaskService(mock_repo)

        result = service.mark_incomplete(999)

        mock_repo.mark_incomplete.assert_called_once_with(999)
        assert result is None


class TestTaskServiceToggleComplete:
    """TaskService.toggle_completeのテスト"""

    def test_toggle_complete_from_incomplete(self):
        """未完了タスクを完了に切り替えできること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task_before = Mock(spec=Task)
        mock_task_before.id = 1
        mock_task_before.completed = False
        
        mock_task_after = Mock(spec=Task)
        mock_task_after.id = 1
        mock_task_after.completed = True

        mock_repo.get_by_id.return_value = mock_task_before
        mock_repo.mark_complete.return_value = mock_task_after

        service = TaskService(mock_repo)

        result = service.toggle_complete(1)

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.mark_complete.assert_called_once_with(1)
        assert result.completed is True

    def test_toggle_complete_from_complete(self):
        """完了タスクを未完了に切り替えできること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_task_before = Mock(spec=Task)
        mock_task_before.id = 1
        mock_task_before.completed = True
        
        mock_task_after = Mock(spec=Task)
        mock_task_after.id = 1
        mock_task_after.completed = False

        mock_repo.get_by_id.return_value = mock_task_before
        mock_repo.mark_incomplete.return_value = mock_task_after

        service = TaskService(mock_repo)

        result = service.toggle_complete(1)

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.mark_incomplete.assert_called_once_with(1)
        assert result.completed is False

    def test_toggle_complete_not_found(self):
        """存在しないタスクのトグルでNoneが返ること"""
        mock_repo = Mock(spec=TaskRepository)
        mock_repo.get_by_id.return_value = None

        service = TaskService(mock_repo)

        result = service.toggle_complete(999)

        mock_repo.get_by_id.assert_called_once_with(999)
        assert result is None

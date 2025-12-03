"""TaskService - タスクのビジネスロジック層"""

from typing import Optional

from task_app.models.task import Task
from task_app.repositories.task import TaskRepository
from task_app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    タスクに関するビジネスロジックを提供するサービスクラス

    TaskRepositoryをラップし、ビジネスロジックを追加する。
    依存性注入によりリポジトリを受け取ることで、テスト容易性を確保。
    """

    def __init__(self, repository: TaskRepository) -> None:
        """
        TaskServiceを初期化する

        Args:
            repository: タスクリポジトリのインスタンス
        """
        self._repository = repository

    def create(self, task_in: TaskCreate) -> Task:
        """
        新しいタスクを作成する

        Args:
            task_in: タスク作成用のスキーマ

        Returns:
            Task: 作成されたタスクモデル
        """
        return self._repository.create(task_in)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        IDでタスクを取得する

        Args:
            task_id: タスクID

        Returns:
            Task | None: 見つかったタスク、存在しない場合はNone
        """
        return self._repository.get_by_id(task_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        """
        すべてのタスクを取得する

        Args:
            skip: スキップする件数（デフォルト: 0）
            limit: 取得する最大件数（デフォルト: 100）

        Returns:
            list[Task]: タスクのリスト
        """
        return self._repository.get_all(skip=skip, limit=limit)

    def update(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        """
        タスクを更新する

        Args:
            task_id: 更新対象のタスクID
            task_in: 更新データ

        Returns:
            Task | None: 更新されたタスク、存在しない場合はNone
        """
        return self._repository.update(task_id, task_in)

    def delete(self, task_id: int) -> bool:
        """
        タスクを削除する

        Args:
            task_id: 削除対象のタスクID

        Returns:
            bool: 削除に成功した場合True、タスクが存在しない場合False
        """
        return self._repository.delete(task_id)

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        タスクを完了状態にする

        Args:
            task_id: 対象のタスクID

        Returns:
            Task | None: 更新されたタスク、存在しない場合はNone
        """
        return self._repository.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        タスクを未完了状態にする

        Args:
            task_id: 対象のタスクID

        Returns:
            Task | None: 更新されたタスク、存在しない場合はNone
        """
        return self._repository.mark_incomplete(task_id)

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """
        タスクの完了状態をトグルする

        現在の状態に応じて完了/未完了を切り替える。
        これはビジネスロジックとして、Repositoryにはないサービス固有のメソッド。

        Args:
            task_id: 対象のタスクID

        Returns:
            Task | None: 更新されたタスク、存在しない場合はNone
        """
        task = self._repository.get_by_id(task_id)
        if task is None:
            return None

        if task.completed:
            return self._repository.mark_incomplete(task_id)
        else:
            return self._repository.mark_complete(task_id)

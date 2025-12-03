"""タスク API ルーター"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from task_app.database import get_db
from task_app.repositories.task import TaskRepository
from task_app.schemas.task import TaskCreate, TaskResponse
from task_app.services.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """TaskServiceの依存性注入"""
    repository = TaskRepository(db)
    return TaskService(repository)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    新しいタスクを作成する

    Args:
        task_in: タスク作成データ
        service: TaskServiceインスタンス

    Returns:
        TaskResponse: 作成されたタスク
    """
    task = service.create(task_in)
    return task

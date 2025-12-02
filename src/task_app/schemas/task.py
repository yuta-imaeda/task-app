"""Taskスキーマ定義"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskBase(BaseModel):
    """タスクの基底スキーマ"""
    
    title: str
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """titleのバリデーション"""
        if not v or not v.strip():
            raise ValueError("タイトルは空にできません")
        if len(v) > 255:
            raise ValueError("タイトルは255文字以内にしてください")
        return v


class TaskCreate(TaskBase):
    """タスク作成用スキーマ"""
    pass


class TaskUpdate(BaseModel):
    """タスク更新用スキーマ（すべてOptional）"""
    
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """titleのバリデーション（設定された場合のみ）"""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("タイトルは空にできません")
        if len(v) > 255:
            raise ValueError("タイトルは255文字以内にしてください")
        return v


class TaskResponse(BaseModel):
    """タスクレスポンス用スキーマ"""
    
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

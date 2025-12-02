"""Taskモデル定義"""

from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

from task_app.database import Base


def utc_now():
    """UTC現在時刻を返す"""
    return datetime.now(UTC)


class Task(Base):
    """タスクモデル"""
    
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        default=utc_now, 
        onupdate=utc_now, 
        nullable=False
    )

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

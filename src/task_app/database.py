"""データベース設定と初期化"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# データベースURL（環境変数から取得、デフォルトはSQLite）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_app.db")

# SQLAlchemy エンジン
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# セッションファクトリ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()


def get_db():
    """
    データベースセッションを取得するジェネレータ。
    FastAPIの依存性注入で使用。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(engine_instance=None):
    """
    データベースを初期化（テーブル作成）。
    
    Args:
        engine_instance: 使用するエンジン。Noneの場合はデフォルトエンジンを使用。
    """
    # モデルをインポートしてテーブル定義を登録
    from task_app.models.task import Task  # noqa: F401
    
    target_engine = engine_instance or engine
    Base.metadata.create_all(bind=target_engine)

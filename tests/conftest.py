"""pytest 共通設定・フィクスチャ"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from task_app.main import app
from task_app.database import Base, get_db


@pytest.fixture
def client() -> TestClient:
    """テスト用 HTTP クライアント"""
    return TestClient(app)


@pytest.fixture
def db_session():
    """テスト用データベースセッション（インメモリSQLite）"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(db_session):
    """テスト用クライアント（DBセッションをオーバーライド）"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

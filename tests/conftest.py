"""pytest 共通設定・フィクスチャ"""

import pytest
from fastapi.testclient import TestClient

from task_app.main import app


@pytest.fixture
def client() -> TestClient:
    """テスト用 HTTP クライアント"""
    return TestClient(app)

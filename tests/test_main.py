"""メインアプリケーションのテスト"""

from fastapi.testclient import TestClient


def test_root(client: TestClient) -> None:
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TaskAPP"}


def test_health_check(client: TestClient) -> None:
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

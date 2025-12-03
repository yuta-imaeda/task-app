"""タスクAPI (POST /tasks) のテスト"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, UTC


class TestCreateTaskAPI:
    """POST /tasks - タスク作成APIのテスト"""

    def test_create_task_success(self, test_client):
        """正常にタスクを作成できること"""
        response = test_client.post(
            "/tasks",
            json={"title": "テストタスク", "description": "説明文"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "テストタスク"
        assert data["description"] == "説明文"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_description(self, test_client):
        """説明なしでタスクを作成できること"""
        response = test_client.post(
            "/tasks",
            json={"title": "タイトルのみ"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "タイトルのみ"
        assert data["description"] is None

    def test_create_task_empty_title_fails(self, test_client):
        """空のタイトルでエラーになること"""
        response = test_client.post(
            "/tasks",
            json={"title": ""}
        )
        
        assert response.status_code == 422  # Validation Error

    def test_create_task_whitespace_title_fails(self, test_client):
        """空白のみのタイトルでエラーになること"""
        response = test_client.post(
            "/tasks",
            json={"title": "   "}
        )
        
        assert response.status_code == 422

    def test_create_task_title_too_long_fails(self, test_client):
        """タイトルが長すぎるとエラーになること"""
        response = test_client.post(
            "/tasks",
            json={"title": "a" * 256}
        )
        
        assert response.status_code == 422

    def test_create_task_missing_title_fails(self, test_client):
        """タイトルなしでエラーになること"""
        response = test_client.post(
            "/tasks",
            json={"description": "説明のみ"}
        )
        
        assert response.status_code == 422

    def test_create_task_returns_correct_content_type(self, test_client):
        """正しいContent-Typeが返されること"""
        response = test_client.post(
            "/tasks",
            json={"title": "テスト"}
        )
        
        assert response.headers["content-type"] == "application/json"

    def test_create_multiple_tasks(self, test_client):
        """複数タスクを作成できること"""
        response1 = test_client.post("/tasks", json={"title": "タスク1"})
        response2 = test_client.post("/tasks", json={"title": "タスク2"})
        
        assert response1.status_code == 201
        assert response2.status_code == 201
        assert response1.json()["id"] != response2.json()["id"]


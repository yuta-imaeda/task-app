"""FastAPI アプリケーションのエントリーポイント"""

from fastapi import FastAPI

app = FastAPI(
    title="TaskAPP",
    description="タスク管理アプリケーション",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    """ルートエンドポイント"""
    return {"message": "Welcome to TaskAPP"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}

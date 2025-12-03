"""FastAPI アプリケーションのエントリーポイント"""

from fastapi import FastAPI

from task_app.api.tasks import router as tasks_router

app = FastAPI(
    title="TaskAPP",
    description="タスク管理アプリケーション",
    version="0.1.0",
)

# ルーターの登録
app.include_router(tasks_router)


@app.get("/")
async def root() -> dict[str, str]:
    """ルートエンドポイント"""
    return {"message": "Welcome to TaskAPP"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}

# TaskAPP

Python タスク管理アプリケーション

## 概要

シンプルで使いやすいタスク管理Webアプリケーションです。

## 技術スタック

- **言語**: Python 3.11+
- **Webフレームワーク**: FastAPI
- **データベース**: SQLite (SQLAlchemy ORM)
- **テスト**: pytest

## プロジェクト構造

```
task-app/
├── src/
│   └── task_app/
│       ├── __init__.py
│       ├── main.py          # FastAPI アプリケーション
│       ├── api/              # API ルーター
│       ├── models/           # データモデル
│       ├── repositories/     # データアクセス層
│       └── services/         # ビジネスロジック層
├── tests/                    # テスト
├── pyproject.toml            # プロジェクト設定
└── README.md
```

## セットアップ

### 1. 仮想環境の作成

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. 依存関係のインストール

```bash
pip install -e ".[dev]"
```

### 3. 開発サーバーの起動

```bash
uvicorn task_app.main:app --reload
```

### 4. テストの実行

```bash
pytest
```

## API ドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントを確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ライセンス

MIT License

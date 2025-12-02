#!/usr/bin/env python
"""データベース初期化スクリプト"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from task_app.database import init_db, engine


def main():
    """データベースを初期化"""
    print("Initializing database...")
    init_db(engine)
    print("Database initialized successfully!")
    print(f"Database location: {engine.url}")


if __name__ == "__main__":
    main()

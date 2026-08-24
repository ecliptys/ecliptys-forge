import sqlite3
from pathlib import Path


class Database:

    def __init__(self, path: Path) -> None:
        self.path = path
        self.connection = sqlite3.connect(path)

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                root_path TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repository_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                language TEXT NOT NULL,
                sensitivity TEXT NOT NULL,
                size INTEGER NOT NULL,
                modified_at TEXT NOT NULL,
                sha256 TEXT NOT NULL,

                UNIQUE(repository_id, path),

                FOREIGN KEY(repository_id)
                    REFERENCES repositories(id)
            );
            """
        )

        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
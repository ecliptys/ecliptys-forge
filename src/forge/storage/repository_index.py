from datetime import datetime
from pathlib import Path

from forge.repository.scanner import RepositorySnapshot
from forge.storage.database import Database


class RepositoryIndex:

    def __init__(self, database: Database) -> None:
        self.database = database

    def save(self, snapshot: RepositorySnapshot) -> None:
        repository_id = self._save_repository(snapshot.root)

        for file in snapshot.files:
            self._save_file(repository_id, file)

        self.database.connection.commit()

    def _save_repository(self, root: Path) -> int:
        now = datetime.now().isoformat()

        cursor = self.database.connection.execute(
            """
            INSERT INTO repositories (
                root_path,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(root_path)
            DO UPDATE SET updated_at = excluded.updated_at
            RETURNING id
            """,
            (str(root), now, now),
        )

        return cursor.fetchone()[0]

    def _save_file(
        self,
        repository_id: int,
        file,
    ) -> None:
        self.database.connection.execute(
            """
            INSERT INTO files (
                repository_id,
                path,
                file_type,
                language,
                sensitivity,
                size,
                modified_at,
                sha256
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(repository_id, path)
            DO UPDATE SET
                file_type = excluded.file_type,
                language = excluded.language,
                sensitivity = excluded.sensitivity,
                size = excluded.size,
                modified_at = excluded.modified_at,
                sha256 = excluded.sha256
            """,
            (
                repository_id,
                str(file.path),
                file.file_type.value,
                file.language.value,
                file.sensitivity.value,
                file.size,
                file.modified_at.isoformat(),
                file.sha256,
            ),
        )
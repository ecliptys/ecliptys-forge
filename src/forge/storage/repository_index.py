from datetime import datetime
from pathlib import Path

from forge.repository.scanner import RepositorySnapshot
from forge.storage.database import Database
from forge.repository.scanner import DiscoveredFile, RepositorySnapshot
from forge.storage.change_detection import ChangeSet


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
    
    def detect_changes(
        self,
        snapshot: RepositorySnapshot,
    ) -> ChangeSet:
        repository = self._find_repository(snapshot.root)

        if repository is None:
            return ChangeSet(
                added=[file.path for file in snapshot.files],
                modified=[],
                deleted=[],
                unchanged=[],
            )

        repository_id = repository[0]

        previous_files = self._load_files(repository_id)

        current_files = {
            file.path: file
            for file in snapshot.files
        }

        added = []
        modified = []
        unchanged = []

        for path, file in current_files.items():
            previous = previous_files.get(path)

            if previous is None:
                added.append(path)

            elif previous["sha256"] != file.sha256:
                modified.append(path)

            else:
                unchanged.append(path)

        deleted = [
            path
            for path in previous_files
            if path not in current_files
        ]

        return ChangeSet(
            added=added,
            modified=modified,
            deleted=deleted,
            unchanged=unchanged,
        )

    def _find_repository(
        self,
        root: Path,
    ):
        cursor = self.database.connection.execute(
            """
            SELECT id, root_path
            FROM repositories
            WHERE root_path = ?
            """,
            (str(root),),
        )

        return cursor.fetchone()

    def _load_files(
        self,
        repository_id: int,
    ) -> dict[Path, dict]:
        cursor = self.database.connection.execute(
            """
            SELECT path, sha256
            FROM files
            WHERE repository_id = ?
            """,
            (repository_id,),
        )

        return {
            Path(row[0]): {
                "sha256": row[1],
            }
            for row in cursor.fetchall()
        }
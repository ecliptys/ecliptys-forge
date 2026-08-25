from pathlib import Path

from forge.repository.scanner import RepositoryScanner
from forge.storage.database import Database
from forge.storage.repository_index import RepositoryIndex


def main(path: str) -> None:
    root = Path(path).resolve()

    if not root.exists():
        print(f"Error: repository path does not exist: {root}")
        return

    if not root.is_dir():
        print(f"Error: repository path is not a directory: {root}")
        return

    # Scan repository
    scanner = RepositoryScanner()
    snapshot = scanner.scan(root)

    # Initialize Forge storage
    forge_directory = root / "forge"
    forge_directory.mkdir(exist_ok=True)

    database_path = forge_directory / "index.db"

    database = Database(database_path)
    database.initialize()

    try:
        index = RepositoryIndex(database)

        # Detect changes against previous index
        changes = index.detect_changes(snapshot)

        # Persist current repository state
        index.save(snapshot)

    finally:
        database.close()

    print("Forge")
    print("─────")
    print(f"Repository: {root}")
    print(f"Files: {len(snapshot.files)}")
    print(f"Directories: {len(snapshot.directories)}")

    print()
    print("Changes")
    print("───────")
    print(f"Added: {len(changes.added)}")
    print(f"Modified: {len(changes.modified)}")
    print(f"Deleted: {len(changes.deleted)}")
    print(f"Unchanged: {len(changes.unchanged)}")

    for path in changes.added:
        print(f"  + {path}")

    for path in changes.modified:
        print(f"  ~ {path}")

    for path in changes.deleted:
        print(f"  - {path}")
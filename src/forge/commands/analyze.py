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

    forge_directory = root / "forge"
    forge_directory.mkdir(exist_ok=True)
    database_path = forge_directory / "index.db"

    database = Database(database_path)
    database.initialize()
    database.close()

    scanner = RepositoryScanner()
    snapshot = scanner.scan(root)

    forge_directory = root / "forge"
    forge_directory.mkdir(exist_ok=True)

    database = Database(forge_directory / "index.db")
    database.initialize()

    index = RepositoryIndex(database)
    index.save(snapshot)

    database.close()

    print("Forge")
    print("─────")
    print(f"Repository: {root}")
    print(f"Files: {len(snapshot.files)}")
    print(f"Directories: {len(snapshot.directories)}")
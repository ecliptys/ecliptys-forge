from pathlib import Path

from forge.repository.scanner import RepositoryScanner


def main(path: str) -> None:
    root = Path(path).resolve()

    if not root.exists():
        print(f"Error: repository path does not exist: {root}")
        return

    if not root.is_dir():
        print(f"Error: repository path is not a directory: {root}")
        return

    scanner = RepositoryScanner()
    snapshot = scanner.scan(root)

    for file in snapshot.files:
        print(
            f"{file.path} | "
            f"type={file.file_type.value} | "
            f"language={file.language.value} | "
            f"size={file.size} | "
            f"sha256={file.sha256}"
        )

    print("Forge")
    print("─────")
    print(f"Repository: {root}")
    print(f"Files: {len(snapshot.files)}")
    print(f"Directories: {len(snapshot.directories)}")
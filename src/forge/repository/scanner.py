from dataclasses import dataclass
from pathlib import Path


@dataclass
class RepositorySnapshot:
    root: Path
    directories: list[Path]
    files: list[Path]


class RepositoryScanner:

    def scan(self, root: Path) -> RepositorySnapshot:
        directories: list[Path] = []
        files: list[Path] = []

        for path in root.rglob("*"):
            relative_path = path.relative_to(root)

            if path.is_dir():
                directories.append(relative_path)
            elif path.is_file():
                files.append(relative_path)

        return RepositorySnapshot(
            root=root,
            directories=directories,
            files=files,
        )
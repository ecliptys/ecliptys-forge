from dataclasses import dataclass
from pathlib import Path

from forge.repository.scope import AnalysisScope


@dataclass
class RepositorySnapshot:
    root: Path
    directories: list[Path]
    files: list[Path]


class RepositoryScanner:

    def __init__(self, scope: AnalysisScope | None = None) -> None:
        self.scope = scope or AnalysisScope()

    def scan(self, root: Path) -> RepositorySnapshot:
        directories: list[Path] = []
        files: list[Path] = []

        self._scan_directory(
            root,
            root,
            directories,
            files,
        )

        return RepositorySnapshot(
            root=root,
            directories=directories,
            files=files,
        )

    def _scan_directory(
        self,
        directory: Path,
        root: Path,
        directories: list[Path],
        files: list[Path],
    ) -> None:
        for path in directory.iterdir():
            relative_path = path.relative_to(root)

            if path.is_dir():
                if not self.scope.includes_directory(path):
                    continue

                directories.append(relative_path)

                self._scan_directory(
                    path,
                    root,
                    directories,
                    files,
                )

            elif path.is_file():
                if not self.scope.includes_file(path):
                    continue

                files.append(relative_path)
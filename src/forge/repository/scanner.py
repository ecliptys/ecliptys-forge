from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from forge.repository.classification import FileClassifier, FileType
from forge.repository.scope import AnalysisScope
from forge.repository.language import LanguageDetector
from forge.repository.metadata import FileMetadataCollector


@dataclass
class DiscoveredFile:
    path: Path
    file_type: FileType
    language: Language
    size: int
    modified_at: datetime
    sha256: str


@dataclass
class RepositorySnapshot:
    root: Path
    directories: list[Path]
    files: list[DiscoveredFile]


class RepositoryScanner:

    def __init__(
        self,
        scope: AnalysisScope | None = None,
        classifier: FileClassifier | None = None,
        language_detector: LanguageDetector | None = None,
        metadata_collector: FileMetadataCollector | None = None,
    ) -> None:
        self.scope = scope or AnalysisScope()
        self.classifier = classifier or FileClassifier()
        self.language_detector = language_detector or LanguageDetector()
        self.metadata_collector = (
            metadata_collector or FileMetadataCollector()
        )

    def scan(self, root: Path) -> RepositorySnapshot:
        directories: list[Path] = []
        files: list[DiscoveredFile] = []

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
        files: list[DiscoveredFile],
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

                file_type = self.classifier.classify(path)
                language = self.language_detector.detect(path)
                metadata = self.metadata_collector.collect(path)

                files.append(
                    DiscoveredFile(
                        path=relative_path,
                        file_type=file_type,
                        language=language,
                        size=metadata.size,
                        modified_at=metadata.modified_at,
                        sha256=metadata.sha256,
                    )
                )
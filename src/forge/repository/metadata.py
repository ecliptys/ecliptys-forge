import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class FileMetadata:
    size: int
    modified_at: datetime
    sha256: str


class FileMetadataCollector:

    def collect(self, path: Path) -> FileMetadata:
        stat = path.stat()

        return FileMetadata(
            size=stat.st_size,
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            sha256=self._calculate_sha256(path),
        )

    def _calculate_sha256(self, path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()
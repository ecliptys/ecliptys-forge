from enum import Enum
from pathlib import Path


class FileType(Enum):
    SOURCE = "source"
    BINARY = "binary"
    UNKNOWN = "unknown"


class FileClassifier:

    BINARY_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".ico",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".7z",
        ".exe",
        ".dll",
        ".so",
        ".class",
    }

    def classify(self, path: Path) -> FileType:
        if path.suffix.lower() in self.BINARY_EXTENSIONS:
            return FileType.BINARY

        return FileType.UNKNOWN
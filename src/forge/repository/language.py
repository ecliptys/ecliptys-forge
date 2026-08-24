from enum import Enum
from pathlib import Path


class Language(Enum):
    JAVA = "java"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JSON = "json"
    MARKDOWN = "markdown"
    UNKNOWN = "unknown"


class LanguageDetector:

    EXTENSION_MAP = {
        ".java": Language.JAVA,
        ".py": Language.PYTHON,
        ".js": Language.JAVASCRIPT,
        ".jsx": Language.JAVASCRIPT,
        ".ts": Language.TYPESCRIPT,
        ".tsx": Language.TYPESCRIPT,
        ".json": Language.JSON,
        ".md": Language.MARKDOWN,
    }

    def detect(self, path: Path) -> Language:
        return self.EXTENSION_MAP.get(
            path.suffix.lower(),
            Language.UNKNOWN,
        )
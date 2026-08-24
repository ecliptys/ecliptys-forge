from pathlib import Path


class AnalysisScope:
    DEFAULT_EXCLUDED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
    }

    DEFAULT_EXCLUDED_FILES = {
        ".pyc",
        ".pyo",
    }

    def includes_directory(self, path: Path) -> bool:
        return path.name not in self.DEFAULT_EXCLUDED_DIRECTORIES

    def includes_file(self, path: Path) -> bool:
        return path.suffix not in self.DEFAULT_EXCLUDED_FILES
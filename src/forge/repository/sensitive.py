from enum import Enum
from pathlib import Path


class Sensitivity(Enum):
    NORMAL = "normal"
    SENSITIVE = "sensitive"


class SensitiveFileDetector:

    SENSITIVE_FILENAMES = {
        ".env",
        ".env.local",
        ".env.development",
        ".env.production",
        ".env.test",
        "credentials",
        "credentials.json",
        "secrets.json",
    }

    SENSITIVE_EXTENSIONS = {
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }

    def detect(self, path: Path) -> Sensitivity:
        if path.name.lower() in self.SENSITIVE_FILENAMES:
            return Sensitivity.SENSITIVE

        if path.suffix.lower() in self.SENSITIVE_EXTENSIONS:
            return Sensitivity.SENSITIVE

        return Sensitivity.NORMAL
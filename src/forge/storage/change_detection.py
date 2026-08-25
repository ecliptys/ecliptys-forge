from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChangeSet:
    added: list[Path]
    modified: list[Path]
    deleted: list[Path]
    unchanged: list[Path]
"""Duplicate Hunter: safe local duplicate-file discovery."""

from .core import DuplicateGroup, find_duplicates, sha256_file

__version__ = "1.0.0"
__all__ = ["DuplicateGroup", "find_duplicates", "sha256_file"]

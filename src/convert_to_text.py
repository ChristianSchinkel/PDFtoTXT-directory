"""Helpers for deciding whether a file can be converted to text."""

from os import PathLike

from .file_type_detection import get_file_type


def can_convert_to_text(file_path: str | PathLike[str]) -> bool:
    """Return whether ``file_path`` has a supported text conversion type."""
    return get_file_type(file_path) != "unsupported"
"""Module for file type detection."""
from os import PathLike
from pathlib import Path


def get_file_type(file_path: str | PathLike[str]) -> str:
    """Return the supported category for a file based on its extension.

    The returned values are ``"pdf"``, ``"word"``, ``"image"``, or
    ``"unsupported"``.
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return "pdf"
    if suffix in {".doc",
                  ".docx"}:
        return "word"
    if suffix in {".bmp",
                  ".gif",
                  ".jpeg",
                  ".jpg",
                  ".png",
                  ".tif",
                  ".tiff",
                  ".webp"}:
        return "image"
    return "unsupported"

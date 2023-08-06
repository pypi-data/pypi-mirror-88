"""Helpers for the installation procedure."""
import shutil
from pathlib import Path

from p5core.html import Tag

installation_directory: Path = Path(".")
source_directory: Path = Path(".")


def write_html(tag: Tag, path: Path) -> None:
    """Write an HTML tag in a file.

    Args:
        tag (Tag): HTML tag to write
        path (Path): path of the file to write

    Raises:
        TypeError: path is not a pathlib.Path
    """
    if not isinstance(path, Path):
        raise TypeError("path is not a pathlib.Path")
    with open(path, "w", encoding="utf-8") as writer:
        writer.write(str(tag))


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file in another file.

    Args:
        src (Path): source file
        dst (Path): destination file

    Raises:
        TypeError: Provided paths are not pathlib.Path
        ValueError: Provided destination path is not relative to installation directory
    """
    if not isinstance(src, Path):
        raise TypeError("src is not a pathlib.Path")

    if not isinstance(dst, Path):
        raise TypeError("dst is not a pathlib.Path")
    elif dst.is_absolute():
        raise ValueError("Destination path must be relative to installation directory")

    destination = installation_directory / dst
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy(source_directory / src, destination)

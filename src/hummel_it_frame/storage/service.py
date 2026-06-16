"""Image storage service."""

import re
from pathlib import Path

from hummel_it_frame.config import AppConfig, load_config

SUPPORTED_IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png"})
_SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


class StorageError(Exception):
    """Base class for storage service errors."""


class UnsupportedImageTypeError(StorageError, ValueError):
    """Raised when an image filename has an unsupported extension."""


class UnsafeFilenameError(StorageError, ValueError):
    """Raised when a filename cannot be safely used inside image storage."""


class ImageNotFoundError(StorageError, FileNotFoundError):
    """Raised when an image cannot be found in storage."""


class StorageService:
    """Manage image files in the configured image directory."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self._config = config or load_config()
        self.image_directory = Path(self._config.storage.image_directory)

    def list_images(self) -> list[str]:
        """List supported image files in storage."""
        if not self.image_directory.exists():
            return []

        return sorted(
            image_path.name
            for image_path in self.image_directory.iterdir()
            if image_path.is_file() and _is_supported_image(image_path.name)
        )

    def save_image(self, filename: str, content: bytes) -> Path:
        """Save an image file and return its storage path."""
        sanitized_filename = sanitize_filename(filename)
        destination = self._resolve_storage_path(sanitized_filename)

        self.image_directory.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

        return destination

    def delete_image(self, filename: str) -> None:
        """Delete an image file from storage."""
        sanitized_filename = sanitize_filename(filename)
        image_path = self._resolve_storage_path(sanitized_filename)

        if not image_path.is_file():
            msg = f"Image not found: {sanitized_filename}"
            raise ImageNotFoundError(msg)

        image_path.unlink()

    def _resolve_storage_path(self, filename: str) -> Path:
        base_path = self.image_directory.resolve(strict=False)
        candidate_path = (self.image_directory / filename).resolve(strict=False)

        if not candidate_path.is_relative_to(base_path):
            msg = "Resolved image path is outside the configured image directory"
            raise UnsafeFilenameError(msg)

        return candidate_path


def sanitize_filename(filename: str) -> str:
    """Return a safe image filename for local storage."""
    raw_filename = filename.strip()
    path = Path(raw_filename)

    if (
        not raw_filename
        or path.name != raw_filename
        or "/" in raw_filename
        or "\\" in raw_filename
    ):
        msg = "Filename must not contain path components"
        raise UnsafeFilenameError(msg)

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_EXTENSIONS:
        msg = f"Unsupported image type: {suffix or '<none>'}"
        raise UnsupportedImageTypeError(msg)

    stem = path.stem.strip()
    sanitized_stem = _SAFE_FILENAME_PATTERN.sub("_", stem).strip("._-")
    if not sanitized_stem:
        msg = "Filename must contain a safe name"
        raise UnsafeFilenameError(msg)

    return f"{sanitized_stem}{suffix}"


def _is_supported_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS

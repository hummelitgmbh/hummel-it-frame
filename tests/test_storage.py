from pathlib import Path

import pytest

from hummel_it_frame.config import AppConfig, StorageConfig
from hummel_it_frame.storage import (
    ImageNotFoundError,
    StorageService,
    UnsafeFilenameError,
    UnsupportedImageTypeError,
    sanitize_filename,
)


def test_list_images_returns_supported_images(
    storage_service: StorageService,
    image_directory: Path,
) -> None:
    (image_directory / "one.jpg").write_bytes(b"jpg")
    (image_directory / "two.jpeg").write_bytes(b"jpeg")
    (image_directory / "three.PNG").write_bytes(b"png")
    (image_directory / "ignored.gif").write_bytes(b"gif")
    (image_directory / "directory.png").mkdir()

    assert storage_service.list_images() == ["one.jpg", "three.PNG", "two.jpeg"]


def test_save_image_writes_supported_image_with_sanitized_filename(
    storage_service: StorageService,
) -> None:
    saved_path = storage_service.save_image("Family Photo.JPG", b"image-content")

    assert saved_path.name == "Family_Photo.jpg"
    assert saved_path.read_bytes() == b"image-content"


def test_save_image_rejects_unsupported_file_type(
    storage_service: StorageService,
) -> None:
    with pytest.raises(UnsupportedImageTypeError):
        storage_service.save_image("image.gif", b"not-supported")


def test_delete_image_removes_supported_image(
    storage_service: StorageService,
) -> None:
    saved_path = storage_service.save_image("image.png", b"image-content")

    storage_service.delete_image("image.png")

    assert not saved_path.exists()


def test_storage_rejects_path_traversal(storage_service: StorageService) -> None:
    with pytest.raises(UnsafeFilenameError):
        storage_service.save_image("../outside.jpg", b"image-content")

    with pytest.raises(UnsafeFilenameError):
        storage_service.delete_image("../outside.jpg")

    with pytest.raises(UnsafeFilenameError):
        storage_service.save_image(r"..\outside.jpg", b"image-content")


def test_delete_image_does_not_remove_symlink_target_outside_storage(
    tmp_path: Path,
) -> None:
    image_directory = tmp_path / "images"
    image_directory.mkdir()
    outside_image = tmp_path / "outside.jpg"
    outside_image.write_bytes(b"outside")
    (image_directory / "linked.jpg").symlink_to(outside_image)
    storage = StorageService(
        AppConfig(storage=StorageConfig(image_directory=str(image_directory)))
    )

    with pytest.raises(UnsafeFilenameError):
        storage.delete_image("linked.jpg")

    assert outside_image.read_bytes() == b"outside"


def test_list_images_returns_empty_list_for_missing_directory(tmp_path: Path) -> None:
    storage = StorageService(
        AppConfig(
            storage=StorageConfig(image_directory=str(tmp_path / "missing-images"))
        )
    )

    assert storage.list_images() == []


def test_delete_image_raises_when_file_is_missing(
    storage_service: StorageService,
) -> None:
    with pytest.raises(ImageNotFoundError):
        storage_service.delete_image("missing.jpg")


@pytest.mark.parametrize(
    "filename",
    ["", "--.jpg", "/tmp/outside.jpg"],
)
def test_sanitize_filename_rejects_unsafe_names(filename: str) -> None:
    with pytest.raises(UnsafeFilenameError):
        sanitize_filename(filename)


@pytest.mark.parametrize("filename", [".jpg", "   .png"])
def test_sanitize_filename_rejects_names_without_file_extension(
    filename: str,
) -> None:
    with pytest.raises(UnsupportedImageTypeError):
        sanitize_filename(filename)

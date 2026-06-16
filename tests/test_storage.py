from pathlib import Path

import pytest

from hummel_it_frame.config import AppConfig, StorageConfig
from hummel_it_frame.storage import (
    StorageService,
    UnsafeFilenameError,
    UnsupportedImageTypeError,
)


def create_storage_service(image_directory: Path) -> StorageService:
    return StorageService(
        AppConfig(storage=StorageConfig(image_directory=str(image_directory)))
    )


def test_list_images_returns_supported_images(tmp_path: Path) -> None:
    image_directory = tmp_path / "images"
    image_directory.mkdir()
    (image_directory / "one.jpg").write_bytes(b"jpg")
    (image_directory / "two.jpeg").write_bytes(b"jpeg")
    (image_directory / "three.PNG").write_bytes(b"png")
    (image_directory / "ignored.gif").write_bytes(b"gif")
    (image_directory / "directory.png").mkdir()

    storage = create_storage_service(image_directory)

    assert storage.list_images() == ["one.jpg", "three.PNG", "two.jpeg"]


def test_save_image_writes_supported_image_with_sanitized_filename(
    tmp_path: Path,
) -> None:
    storage = create_storage_service(tmp_path / "images")

    saved_path = storage.save_image("Family Photo.JPG", b"image-content")

    assert saved_path.name == "Family_Photo.jpg"
    assert saved_path.read_bytes() == b"image-content"


def test_save_image_rejects_unsupported_file_type(tmp_path: Path) -> None:
    storage = create_storage_service(tmp_path / "images")

    with pytest.raises(UnsupportedImageTypeError):
        storage.save_image("image.gif", b"not-supported")


def test_delete_image_removes_supported_image(tmp_path: Path) -> None:
    storage = create_storage_service(tmp_path / "images")
    saved_path = storage.save_image("image.png", b"image-content")

    storage.delete_image("image.png")

    assert not saved_path.exists()


def test_storage_rejects_path_traversal(tmp_path: Path) -> None:
    storage = create_storage_service(tmp_path / "images")

    with pytest.raises(UnsafeFilenameError):
        storage.save_image("../outside.jpg", b"image-content")

    with pytest.raises(UnsafeFilenameError):
        storage.delete_image("../outside.jpg")

    with pytest.raises(UnsafeFilenameError):
        storage.save_image(r"..\outside.jpg", b"image-content")


def test_delete_image_does_not_remove_symlink_target_outside_storage(
    tmp_path: Path,
) -> None:
    image_directory = tmp_path / "images"
    image_directory.mkdir()
    outside_image = tmp_path / "outside.jpg"
    outside_image.write_bytes(b"outside")
    (image_directory / "linked.jpg").symlink_to(outside_image)
    storage = create_storage_service(image_directory)

    with pytest.raises(UnsafeFilenameError):
        storage.delete_image("linked.jpg")

    assert outside_image.read_bytes() == b"outside"

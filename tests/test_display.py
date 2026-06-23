from pathlib import Path

import pytest

from hummel_it_frame.display import (
    ImagePlacement,
    calculate_image_placement,
    discover_images,
)


def test_calculate_fit_placement_preserves_aspect_ratio() -> None:
    placement = calculate_image_placement(
        image_size=(400, 200),
        screen_size=(300, 300),
        mode="fit",
    )

    assert placement == ImagePlacement(width=300, height=150, x=0, y=75)


def test_calculate_fill_placement_preserves_aspect_ratio_and_crops() -> None:
    placement = calculate_image_placement(
        image_size=(400, 200),
        screen_size=(300, 300),
        mode="fill",
    )

    assert placement == ImagePlacement(width=600, height=300, x=-150, y=0)


def test_calculate_stretch_placement_uses_full_screen() -> None:
    placement = calculate_image_placement(
        image_size=(400, 200),
        screen_size=(300, 300),
        mode="stretch",
    )

    assert placement == ImagePlacement(width=300, height=300, x=0, y=0)


def test_calculate_placement_rejects_zero_dimensions() -> None:
    with pytest.raises(ValueError):
        calculate_image_placement(
            image_size=(0, 200),
            screen_size=(300, 300),
            mode="fit",
        )


def test_discover_images_returns_supported_files(tmp_path: Path) -> None:
    (tmp_path / "one.jpg").write_bytes(b"jpg")
    (tmp_path / "two.JPEG").write_bytes(b"jpeg")
    (tmp_path / "three.PNG").write_bytes(b"png")
    (tmp_path / "ignored.gif").write_bytes(b"gif")
    (tmp_path / "directory.jpg").mkdir()

    images = discover_images(tmp_path)

    assert [image.name for image in images] == ["one.jpg", "three.PNG", "two.JPEG"]


def test_discover_images_returns_empty_list_for_empty_directory(
    tmp_path: Path,
) -> None:
    assert discover_images(tmp_path) == []


def test_discover_images_returns_empty_list_for_missing_directory(
    tmp_path: Path,
) -> None:
    assert discover_images(tmp_path / "missing") == []

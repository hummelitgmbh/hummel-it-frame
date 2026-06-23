from pathlib import Path
from random import Random
from typing import Any

import pytest

from hummel_it_frame.config import AppConfig, StorageConfig
from hummel_it_frame.display import (
    ImagePlacement,
    PygameSlideshow,
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


def test_calculate_fit_placement_centers_tall_image() -> None:
    placement = calculate_image_placement(
        image_size=(200, 400),
        screen_size=(300, 300),
        mode="fit",
    )

    assert placement == ImagePlacement(width=150, height=300, x=75, y=0)


def test_calculate_fill_placement_preserves_aspect_ratio_and_crops() -> None:
    placement = calculate_image_placement(
        image_size=(400, 200),
        screen_size=(300, 300),
        mode="fill",
    )

    assert placement == ImagePlacement(width=600, height=300, x=-150, y=0)


def test_calculate_fill_placement_centers_tall_image_crop() -> None:
    placement = calculate_image_placement(
        image_size=(200, 400),
        screen_size=(300, 300),
        mode="fill",
    )

    assert placement == ImagePlacement(width=300, height=600, x=0, y=-150)


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


class ReversingRandom(Random):
    def shuffle(self, x: list[Any]) -> None:
        x.reverse()


class FakeLoadedImage:
    def __init__(self, name: str) -> None:
        self.name = name

    def convert(self) -> str:
        return f"surface:{self.name}"


class FakePygameError(Exception):
    pass


class FakeImageModule:
    def load(self, image_path: str) -> FakeLoadedImage:
        path = Path(image_path)
        if path.name == "bad.jpg":
            raise FakePygameError

        return FakeLoadedImage(path.name)


class FakePygame:
    error = FakePygameError
    image = FakeImageModule()


def create_slideshow(image_directory: Path) -> PygameSlideshow:
    config = AppConfig(storage=StorageConfig(image_directory=str(image_directory)))

    return PygameSlideshow(config, random_generator=ReversingRandom())


def test_slideshow_refreshes_image_queue_when_directory_changes(
    tmp_path: Path,
) -> None:
    (tmp_path / "one.jpg").write_bytes(b"one")
    (tmp_path / "two.png").write_bytes(b"two")
    slideshow = create_slideshow(tmp_path)

    slideshow._refresh_image_queue()

    assert [image.name for image in slideshow._image_queue] == ["two.png", "one.jpg"]

    (tmp_path / "three.jpeg").write_bytes(b"three")

    slideshow._refresh_image_queue()

    assert [image.name for image in slideshow._image_queue] == [
        "two.png",
        "three.jpeg",
        "one.jpg",
    ]


def test_slideshow_load_next_surface_skips_unreadable_images(tmp_path: Path) -> None:
    (tmp_path / "bad.jpg").write_bytes(b"bad")
    (tmp_path / "good.png").write_bytes(b"good")
    slideshow = create_slideshow(tmp_path)

    surface = slideshow._load_next_surface(FakePygame)

    assert surface == "surface:good.png"

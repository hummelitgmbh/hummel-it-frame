"""Pure display helpers for image discovery and scaling."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from hummel_it_frame.storage import SUPPORTED_IMAGE_EXTENSIONS

DisplayMode = Literal["fit", "fill", "stretch"]


@dataclass(frozen=True)
class ImagePlacement:
    """Scaled image size and screen offset."""

    width: int
    height: int
    x: int
    y: int


def discover_images(image_directory: str | Path) -> list[Path]:
    """Return supported image files from an image directory."""
    directory = Path(image_directory)
    if not directory.is_dir():
        return []

    return sorted(
        image_path
        for image_path in directory.iterdir()
        if image_path.is_file()
        and image_path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )


def calculate_image_placement(
    image_size: tuple[int, int],
    screen_size: tuple[int, int],
    mode: DisplayMode,
) -> ImagePlacement:
    """Calculate scaled image size and centered offset for a display mode."""
    image_width, image_height = image_size
    screen_width, screen_height = screen_size

    if min(image_width, image_height, screen_width, screen_height) <= 0:
        msg = "Image and screen dimensions must be greater than zero"
        raise ValueError(msg)

    if mode == "stretch":
        return ImagePlacement(
            width=screen_width,
            height=screen_height,
            x=0,
            y=0,
        )

    width_scale = screen_width / image_width
    height_scale = screen_height / image_height
    scale = min(width_scale, height_scale) if mode == "fit" else max(
        width_scale, height_scale
    )
    scaled_width = round(image_width * scale)
    scaled_height = round(image_height * scale)

    return ImagePlacement(
        width=scaled_width,
        height=scaled_height,
        x=(screen_width - scaled_width) // 2,
        y=(screen_height - scaled_height) // 2,
    )

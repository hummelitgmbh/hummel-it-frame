"""Configuration models and YAML loading."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

DEFAULT_CONFIG_PATH = Path("/etc/hummel-it-frame/config.yaml")
DEFAULT_IMAGE_DIRECTORY = "/var/lib/hummel-it-frame/images"


class DisplayConfig(BaseModel):
    """Display configuration."""

    model_config = ConfigDict(extra="forbid")

    mode: Literal["fit", "fill", "stretch"] = "fill"


class SlideshowConfig(BaseModel):
    """Slideshow configuration."""

    model_config = ConfigDict(extra="forbid")

    interval_seconds: int = Field(default=20, gt=0)


class StorageConfig(BaseModel):
    """Storage configuration."""

    model_config = ConfigDict(extra="forbid")

    image_directory: str = DEFAULT_IMAGE_DIRECTORY

    @field_validator("image_directory")
    @classmethod
    def validate_image_directory(cls, image_directory: str) -> str:
        """Ensure image storage has a non-empty path."""
        image_directory = image_directory.strip()
        if not image_directory:
            msg = "storage.image_directory must not be empty"
            raise ValueError(msg)

        return image_directory


class AppConfig(BaseModel):
    """Application configuration."""

    model_config = ConfigDict(extra="forbid")

    display: DisplayConfig = Field(default_factory=DisplayConfig)
    slideshow: SlideshowConfig = Field(default_factory=SlideshowConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)


def load_config(path: str | Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    """Load application configuration from YAML or return defaults."""
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig()

    with config_path.open(encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file) or {}

    if not isinstance(config_data, dict):
        msg = "Configuration file must contain a YAML mapping"
        raise ValueError(msg)

    return AppConfig.model_validate(config_data)

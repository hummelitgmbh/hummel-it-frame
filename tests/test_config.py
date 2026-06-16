from pathlib import Path

import pytest
from pydantic import ValidationError

from hummel_it_frame.config import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_IMAGE_DIRECTORY,
    load_config,
)


def test_load_config_returns_defaults_when_file_is_missing(tmp_path: Path) -> None:
    config = load_config(tmp_path / "missing.yaml")

    assert DEFAULT_CONFIG_PATH == Path("/etc/hummel-it-frame/config.yaml")
    assert config.display.mode == "fill"
    assert config.slideshow.interval_seconds == 20
    assert config.storage.image_directory == DEFAULT_IMAGE_DIRECTORY


def test_load_config_reads_yaml_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
display:
  mode: fit

slideshow:
  interval_seconds: 30

storage:
  image_directory: /tmp/hummel-images
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.display.mode == "fit"
    assert config.slideshow.interval_seconds == 30
    assert config.storage.image_directory == "/tmp/hummel-images"


@pytest.mark.parametrize(
    "yaml_content",
    [
        """
display:
  mode: crop
""",
        """
slideshow:
  interval_seconds: 0
""",
        """
storage:
  image_directory: "   "
""",
    ],
)
def test_load_config_rejects_invalid_values(
    tmp_path: Path, yaml_content: str
) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml_content, encoding="utf-8")

    with pytest.raises(ValidationError):
        load_config(config_path)

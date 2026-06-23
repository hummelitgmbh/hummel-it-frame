from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from hummel_it_frame.config import AppConfig, StorageConfig
from hummel_it_frame.storage import StorageService
from hummel_it_frame.web.app import app
from hummel_it_frame.web.dependencies import get_app_config, get_storage_service


@pytest.fixture
def image_directory(tmp_path: Path) -> Path:
    directory = tmp_path / "images"
    directory.mkdir()

    return directory


@pytest.fixture
def client(image_directory: Path) -> Iterator[TestClient]:
    config = AppConfig(storage=StorageConfig(image_directory=str(image_directory)))

    app.dependency_overrides[get_app_config] = lambda: config
    app.dependency_overrides[get_storage_service] = lambda: StorageService(config)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_api_status_returns_ok(client: TestClient) -> None:
    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_get_api_config_returns_loaded_configuration(
    client: TestClient,
    image_directory: Path,
) -> None:
    response = client.get("/api/config")

    assert response.status_code == 200
    assert response.json() == {
        "display": {"mode": "fill"},
        "slideshow": {"interval_seconds": 20},
        "storage": {"image_directory": str(image_directory)},
    }


def test_get_api_images_returns_available_images(
    client: TestClient,
    image_directory: Path,
) -> None:
    (image_directory / "one.jpg").write_bytes(b"one")
    (image_directory / "two.png").write_bytes(b"two")
    (image_directory / "ignored.gif").write_bytes(b"ignored")

    response = client.get("/api/images")

    assert response.status_code == 200
    assert response.json() == ["one.jpg", "two.png"]

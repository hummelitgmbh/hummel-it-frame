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
def app_config(image_directory: Path) -> AppConfig:
    return AppConfig(storage=StorageConfig(image_directory=str(image_directory)))


@pytest.fixture
def storage_service(app_config: AppConfig) -> StorageService:
    return StorageService(app_config)


@pytest.fixture
def api_client(app_config: AppConfig) -> Iterator[TestClient]:
    app.dependency_overrides[get_app_config] = lambda: app_config
    app.dependency_overrides[get_storage_service] = lambda: StorageService(app_config)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

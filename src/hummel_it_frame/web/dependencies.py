"""FastAPI dependencies for the web service."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from hummel_it_frame.config import AppConfig, load_config
from hummel_it_frame.storage import StorageService


@lru_cache
def get_app_config() -> AppConfig:
    """Return the loaded application configuration."""
    return load_config()


def get_storage_service(
    config: Annotated[AppConfig, Depends(get_app_config)],
) -> StorageService:
    """Return a storage service for the configured image directory."""
    return StorageService(config)

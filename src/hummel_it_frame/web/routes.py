"""API routes for Hummel IT Frame."""

from typing import Annotated

from fastapi import APIRouter, Depends

from hummel_it_frame import __version__
from hummel_it_frame.config import AppConfig
from hummel_it_frame.storage import StorageService
from hummel_it_frame.web.dependencies import get_app_config, get_storage_service

router = APIRouter(prefix="/api")


@router.get("/status")
def get_status() -> dict[str, str]:
    """Return application status information."""
    return {"status": "ok", "version": __version__}


@router.get("/config")
def get_config(
    config: Annotated[AppConfig, Depends(get_app_config)],
) -> AppConfig:
    """Return the loaded application configuration."""
    return config


@router.get("/images")
def get_images(
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
) -> list[str]:
    """Return available image filenames."""
    return storage_service.list_images()

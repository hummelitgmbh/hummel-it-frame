"""FastAPI application for Hummel IT Frame."""

from fastapi import FastAPI

from hummel_it_frame.web.routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    fastapi_app = FastAPI(title="Hummel IT Frame")
    fastapi_app.include_router(router)

    return fastapi_app


app = create_app()

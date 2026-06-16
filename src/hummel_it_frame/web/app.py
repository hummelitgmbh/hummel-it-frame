"""FastAPI application for Hummel IT Frame."""

from fastapi import FastAPI

app = FastAPI(title="Hummel IT Frame")


@app.get("/api/status")
def get_status() -> dict[str, str]:
    """Return application health status."""
    return {"status": "ok"}

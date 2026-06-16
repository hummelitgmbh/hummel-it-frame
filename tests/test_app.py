from fastapi.routing import APIRoute

from hummel_it_frame.web.app import app


def test_get_api_status_returns_ok() -> None:
    status_route = next(
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/api/status"
    )

    assert status_route.methods == {"GET"}
    assert status_route.endpoint() == {"status": "ok"}

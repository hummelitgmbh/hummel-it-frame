from pathlib import Path

from fastapi.testclient import TestClient


def test_get_api_status_returns_ok(api_client: TestClient) -> None:
    response = api_client.get("/api/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_get_api_config_returns_loaded_configuration(
    api_client: TestClient,
    image_directory: Path,
) -> None:
    response = api_client.get("/api/config")

    assert response.status_code == 200
    assert response.json() == {
        "display": {"mode": "fill"},
        "slideshow": {"interval_seconds": 20},
        "storage": {"image_directory": str(image_directory)},
    }


def test_get_api_images_returns_available_images(
    api_client: TestClient,
    image_directory: Path,
) -> None:
    (image_directory / "one.jpg").write_bytes(b"one")
    (image_directory / "two.png").write_bytes(b"two")
    (image_directory / "ignored.gif").write_bytes(b"ignored")

    response = api_client.get("/api/images")

    assert response.status_code == 200
    assert response.json() == ["one.jpg", "two.png"]


def test_get_api_images_returns_empty_list_when_no_images(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/images")

    assert response.status_code == 200
    assert response.json() == []


def test_post_api_images_uploads_supported_image(
    api_client: TestClient,
    image_directory: Path,
) -> None:
    response = api_client.post(
        "/api/images",
        files={"file": ("Family Photo.JPG", b"image-content", "image/jpeg")},
    )

    assert response.status_code == 200
    assert response.json() == {"filename": "Family_Photo.jpg"}
    assert (image_directory / "Family_Photo.jpg").read_bytes() == b"image-content"


def test_post_api_images_rejects_invalid_file_type(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/images",
        files={"file": ("notes.txt", b"not-an-image", "text/plain")},
    )

    assert response.status_code == 400
    assert "Unsupported image type" in response.json()["detail"]


def test_post_api_images_rejects_path_traversal_filename(
    api_client: TestClient,
) -> None:
    response = api_client.post(
        "/api/images",
        files={"file": ("../outside.jpg", b"image-content", "image/jpeg")},
    )

    assert response.status_code == 400
    assert "Filename must not contain path components" in response.json()["detail"]


def test_post_api_images_requires_file_field(api_client: TestClient) -> None:
    response = api_client.post("/api/images")

    assert response.status_code == 422


def test_uploaded_image_appears_in_get_api_images(api_client: TestClient) -> None:
    upload_response = api_client.post(
        "/api/images",
        files={"file": ("upload.png", b"image-content", "image/png")},
    )

    list_response = api_client.get("/api/images")

    assert upload_response.status_code == 200
    assert list_response.status_code == 200
    assert list_response.json() == ["upload.png"]

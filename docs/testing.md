# Testing coverage

The MVP test suite is intentionally fast and deterministic. It uses pytest and
avoids hardware, system service, cloud, and display integration tests.

## Covered

Configuration service:

- default configuration when no YAML file exists
- loading full and partial YAML files
- empty YAML files
- invalid values and unknown fields
- rejection of YAML documents that are not mappings

Storage service:

- listing supported local image files
- ignoring unsupported files and directories
- missing image directory behavior
- saving images with sanitized filenames
- unsupported file type rejection
- path traversal rejection
- missing-file deletion errors
- symlink escape protection for deletion

FastAPI web API:

- `GET /api/status`
- `GET /api/config`
- `GET /api/images` for empty and populated storage
- `POST /api/images` for valid uploads
- invalid upload type rejection
- unsafe upload filename rejection
- required multipart file validation

Display service pure logic:

- image discovery and filtering
- fit, fill, and stretch scaling calculations
- invalid dimension rejection
- slideshow queue refresh when files change
- corrupt or unreadable image skip behavior using a fake pygame boundary

Packaging and installer:

- production-style systemd paths and restart policy
- separate display service unit
- installer root guard, safe config backup behavior, expected runtime paths,
  and `systemctl daemon-reload`

## Intentionally not covered

The suite does not run tests that require:

- actual display hardware or a fullscreen pygame session
- actual systemd interaction
- Raspberry Pi hardware
- Nextcloud or external network providers
- WLAN management, OTA updates, authentication, Debian packaging, or web UI

Those areas require manual appliance testing or future integration tests in an
environment designed for hardware and service orchestration.

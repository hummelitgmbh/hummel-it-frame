# Hummel IT Frame

Hummel IT Frame is a self-hosted digital picture frame platform designed for Raspberry Pi devices.

The project aims to provide a privacy-friendly alternative to commercial cloud-based digital picture frames by allowing users to manage their own images and data.

## Key Features

* Fullscreen slideshow mode
* Local image storage
* Web-based image upload
* Optional Nextcloud integration
* Automatic image updates
* Raspberry Pi optimized
* Appliance-style operation
* No vendor cloud required

## Project Status

🚧 Early development

The project is currently in active development.

The first milestone focuses on:

* Local image storage
* Web upload interface
* Fullscreen slideshow
* Automatic startup on boot

## Vision

Hummel IT Frame is intended to become a complete digital picture frame platform with:

* Nextcloud integration
* Multiple image providers
* Web-based administration
* WLAN configuration
* Appliance mode
* Self-hosted operation

## Why Hummel IT Frame?

Most commercial digital picture frames require:

* Vendor cloud services
* Mobile applications
* External user accounts

Hummel IT Frame follows a different approach:

* Your images remain under your control
* Self-hosted architecture
* Open development process
* Raspberry Pi based
* Privacy-focused design

## Target Platforms

* Raspberry Pi 4
* Raspberry Pi 5
* Raspberry Pi OS Lite

## Local Installation v0.1

The v0.1 installer prepares runtime directories, installs a default
configuration file, installs the main systemd service, and reloads systemd.
It does not install Debian packages or configure Nextcloud, WLAN, OTA updates,
authentication, or a web frontend.

Run it as root from a checked-out release or source tree:

```bash
sudo scripts/install.sh
```

The installer creates:

```text
/etc/hummel-it-frame
/var/lib/hummel-it-frame
/var/lib/hummel-it-frame/images
/var/lib/hummel-it-frame/tmp
```

It installs the default configuration to:

```text
/etc/hummel-it-frame/config.yaml
```

If a configuration file already exists, the installer creates a timestamped
backup before replacing it.

The main service file is installed to:

```text
/etc/systemd/system/hummel-it-frame.service
```

After installation, enable and start the service:

```bash
sudo systemctl enable hummel-it-frame.service
sudo systemctl start hummel-it-frame.service
```

View logs with:

```bash
journalctl -u hummel-it-frame.service -f
```

The service expects the application entrypoint to be available at
`/usr/local/bin/hummel-it-frame`.

## Testing

Run the automated MVP test suite with:

```bash
uv run pytest
```

The current coverage scope is documented in `docs/testing.md`.

## Roadmap

### v0.1

* Local image provider
* Image upload via web interface
* Fullscreen slideshow
* Configuration management

### v0.2

* Nextcloud provider
* Automatic synchronization

### v0.3

* WLAN management
* Fallback hotspot mode

### v1.0

* Appliance mode
* Read-only operation
* OTA updates
* Multiple image providers

## License

Copyright (c) 2026 Hummel IT GmbH

The source code is publicly available.

Commercial use requires a separate license agreement with Hummel IT GmbH.

See the LICENSE file for details.

## Contributing

Contribution guidelines will be published during the first public release.

## Website

Coming soon.

## Maintainer

Hummel IT GmbH

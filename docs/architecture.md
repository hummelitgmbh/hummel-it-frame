# Architecture – Hummel IT Frame

## Overview

Hummel IT Frame consists of multiple independent services.

The goal is to separate image display, image sources and administration.

## Components

### Display Service

Responsible for fullscreen image display.

Responsibilities:

- Fullscreen slideshow
- Image scaling
- Image transitions
- Automatic image reload
- Display mode handling (fit, fill, stretch)

Technology:

- Python
- pygame

### Web Service

Responsible for administration and local image uploads.

Responsibilities:

- Image upload
- Image management
- Status information
- Configuration interface

Technology:

- Python
- FastAPI

### Source Service

Responsible for image synchronization.

Supported providers:

- Local Upload Provider
- Nextcloud Provider

Future providers:

- SMB Share
- USB Storage

### Config Service

Responsible for loading and validating configuration.

Configuration file:

`/etc/hummel-it-frame/config.yaml`

## Storage

### Image Storage

All providers store images in a common local directory.

Path:

`/var/lib/hummel-it-frame/images`

### Application Data

Path:

`/var/lib/hummel-it-frame`

## Runtime Model

The Raspberry Pi remains powered on continuously.

The display may be turned off independently.

The application must automatically recover after:

- Reboot
- Power failure
- Application crash

## Service Layout

Display Service
↓
Image Directory
↑
Source Service

Web Service
↓
Config Service

## Design Principles

- Appliance-first design
- No cloud dependency required
- Local-first operation
- Automatic recovery
- Simple deployment
- Raspberry Pi optimized

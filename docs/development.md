# Development Guide – Hummel IT Frame

## Purpose

This document defines the development standards for Hummel IT Frame.

All contributors should follow these guidelines.

---

# Programming Language

Python 3.12+

---

# Package Management

uv

Reference:

https://docs.astral.sh/uv/

---

# Dependencies

Main dependencies:

* FastAPI
* pygame
* pydantic
* pyyaml

Development dependencies:

* pytest
* ruff

---

# Code Style

## Formatter

ruff format

## Linter

ruff check

---

# Testing

Framework:

pytest

Requirements:

* New functionality should include tests
* Core services must be covered by tests
* Upload functionality must be tested

---

# Project Structure

```text
src/hummel_it_frame/
├── display/
├── web/
├── config/
├── storage/
├── models/
└── main.py
```

---

# Configuration

Configuration file:

```text
/etc/hummel-it-frame/config.yaml
```

The application must start with sensible defaults.

---

# Logging

Requirements:

* Structured logging
* No excessive log output
* Support future appliance mode

Default log level:

```text
INFO
```

---

# Git Workflow

Commit messages should be concise and descriptive.

Examples:

```text
Add image upload endpoint
Implement slideshow service
Add configuration validation
```

Avoid:

```text
Fix stuff
Update files
Changes
```

---

# Branch Strategy

Main branch:

```text
main
```

Feature branches:

```text
feature/upload-service
feature/display-service
feature/systemd-support
```

---

# Continuous Integration

Future GitHub Actions should run:

* Ruff
* Pytest

Pull requests should only be merged if CI passes.

---

# Design Principles

* Appliance-first
* Local-first
* Privacy-first
* Simple deployment
* Raspberry Pi optimized
* Recover automatically after failure

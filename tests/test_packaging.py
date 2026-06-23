from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYSTEMD_DIR = PROJECT_ROOT / "packaging" / "systemd"
INSTALLER = PROJECT_ROOT / "scripts" / "install.sh"


def test_main_systemd_service_uses_production_paths() -> None:
    service = (SYSTEMD_DIR / "hummel-it-frame.service").read_text(encoding="utf-8")

    assert "ExecStart=/usr/local/bin/hummel-it-frame" in service
    assert "User=hummel-it-frame" in service
    assert "Restart=on-failure" in service
    assert "WorkingDirectory=/var/lib/hummel-it-frame" in service
    assert "/etc/hummel-it-frame/config.yaml" in service
    assert "/home/" not in service


def test_display_systemd_service_is_separate_from_web_service() -> None:
    service = (SYSTEMD_DIR / "hummel-it-frame-display.service").read_text(
        encoding="utf-8"
    )

    assert "ExecStart=/usr/local/bin/hummel-it-frame-display" in service
    assert "Wants=hummel-it-frame.service" in service
    assert "Restart=on-failure" in service
    assert "SupplementaryGroups=video input" in service


def test_installer_is_executable_and_documents_safe_operations() -> None:
    installer_text = INSTALLER.read_text(encoding="utf-8")

    assert INSTALLER.stat().st_mode & 0o111
    assert "set -Eeuo pipefail" in installer_text
    assert "This installer must be run as root" in installer_text
    assert "/etc/hummel-it-frame" in installer_text
    assert "/var/lib/hummel-it-frame/images" in installer_text
    assert 'cp -a -- "${CONFIG_FILE}" "${backup_file}"' in installer_text
    assert "systemctl daemon-reload" in installer_text

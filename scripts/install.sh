#!/usr/bin/env bash
set -Eeuo pipefail

APP_USER="hummel-it-frame"
APP_GROUP="hummel-it-frame"

CONFIG_DIR="/etc/hummel-it-frame"
CONFIG_FILE="${CONFIG_DIR}/config.yaml"

DATA_DIR="/var/lib/hummel-it-frame"
IMAGE_DIR="${DATA_DIR}/images"
TMP_DIR="${DATA_DIR}/tmp"

SERVICE_NAME="hummel-it-frame.service"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_TARGET="${SYSTEMD_DIR}/${SERVICE_NAME}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
SERVICE_SOURCE="${REPO_ROOT}/packaging/systemd/${SERVICE_NAME}"

TEMP_CONFIG=""

log() {
    printf '==> %s\n' "$*"
}

warn() {
    printf 'WARNING: %s\n' "$*" >&2
}

fail() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

cleanup() {
    if [ -n "${TEMP_CONFIG}" ] && [ -f "${TEMP_CONFIG}" ]; then
        rm -f -- "${TEMP_CONFIG}"
    fi
}

require_root() {
    if [ "${EUID}" -ne 0 ]; then
        fail "This installer must be run as root. Try: sudo ${BASH_SOURCE[0]}"
    fi
}

require_files() {
    if [ ! -f "${SERVICE_SOURCE}" ]; then
        fail "Missing systemd service file: ${SERVICE_SOURCE}"
    fi

    if ! command -v systemctl >/dev/null 2>&1; then
        fail "systemctl is required to install the systemd service"
    fi
}

ensure_user() {
    if ! getent group "${APP_GROUP}" >/dev/null; then
        log "Creating system group ${APP_GROUP}"
        groupadd --system "${APP_GROUP}"
    fi

    if ! id -u "${APP_USER}" >/dev/null 2>&1; then
        log "Creating system user ${APP_USER}"
        useradd \
            --system \
            --gid "${APP_GROUP}" \
            --home-dir "${DATA_DIR}" \
            --shell /usr/sbin/nologin \
            "${APP_USER}"
    fi
}

create_directories() {
    log "Creating runtime directories"
    install -d -o root -g "${APP_GROUP}" -m 0750 "${CONFIG_DIR}"
    install -d -o "${APP_USER}" -g "${APP_GROUP}" -m 0750 "${DATA_DIR}"
    install -d -o "${APP_USER}" -g "${APP_GROUP}" -m 0750 "${IMAGE_DIR}"
    install -d -o "${APP_USER}" -g "${APP_GROUP}" -m 0750 "${TMP_DIR}"
}

write_default_config() {
    TEMP_CONFIG="$(mktemp)"
    cat >"${TEMP_CONFIG}" <<'YAML'
display:
  mode: fill

slideshow:
  interval_seconds: 20

storage:
  image_directory: /var/lib/hummel-it-frame/images
YAML

    if [ -f "${CONFIG_FILE}" ]; then
        backup_file="${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
        if [ -e "${backup_file}" ]; then
            backup_file="${backup_file}.$$"
        fi

        log "Backing up existing config to ${backup_file}"
        cp -a -- "${CONFIG_FILE}" "${backup_file}"
    fi

    log "Installing default config to ${CONFIG_FILE}"
    install -o root -g "${APP_GROUP}" -m 0640 "${TEMP_CONFIG}" "${CONFIG_FILE}"
}

install_service() {
    log "Installing systemd service to ${SERVICE_TARGET}"
    install -o root -g root -m 0644 "${SERVICE_SOURCE}" "${SERVICE_TARGET}"
}

reload_systemd() {
    log "Reloading systemd"
    systemctl daemon-reload
}

print_next_steps() {
    if [ ! -x /usr/local/bin/hummel-it-frame ]; then
        warn "/usr/local/bin/hummel-it-frame was not found. Install the Python package before starting the service."
    fi

    cat <<EOF

Installation complete.

Next steps:
  Enable service on boot:
    sudo systemctl enable ${SERVICE_NAME}

  Start service now:
    sudo systemctl start ${SERVICE_NAME}

  View service status:
    systemctl status ${SERVICE_NAME}

  Follow logs:
    journalctl -u ${SERVICE_NAME} -f

Configuration:
  ${CONFIG_FILE}

Image directory:
  ${IMAGE_DIR}
EOF
}

main() {
    trap cleanup EXIT

    require_root
    require_files
    ensure_user
    create_directories
    write_default_config
    install_service
    reload_systemd
    print_next_steps
}

main "$@"

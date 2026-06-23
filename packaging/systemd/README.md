# systemd integration

This directory contains production-style systemd unit files for Hummel IT Frame.

## Services

`hummel-it-frame.service` runs the main web/API process using:

```text
/usr/local/bin/hummel-it-frame
```

The application loads configuration from its default path:

```text
/etc/hummel-it-frame/config.yaml
```

`hummel-it-frame-display.service` runs the fullscreen pygame slideshow using:

```text
/usr/local/bin/hummel-it-frame-display
```

The display process is intentionally separate from the web process in v0.1 so the web API and fullscreen display can restart independently. For a picture-frame appliance, enable both services. For a headless upload/API-only setup, enable only `hummel-it-frame.service`.

## Runtime paths

The services expect these production paths:

```text
/etc/hummel-it-frame/config.yaml
/var/lib/hummel-it-frame/images
```

Create a dedicated service user before enabling the services:

```bash
sudo useradd --system --home /var/lib/hummel-it-frame --shell /usr/sbin/nologin hummel-it-frame
sudo usermod -aG video,input hummel-it-frame
sudo install -d -o hummel-it-frame -g hummel-it-frame /etc/hummel-it-frame
sudo install -d -o hummel-it-frame -g hummel-it-frame /var/lib/hummel-it-frame/images
```

Install the Python package so the console entrypoints are available at `/usr/local/bin/hummel-it-frame` and `/usr/local/bin/hummel-it-frame-display`.

## Install units

Copy the desired service files to the system unit directory:

```bash
sudo cp packaging/systemd/hummel-it-frame.service /etc/systemd/system/
sudo cp packaging/systemd/hummel-it-frame-display.service /etc/systemd/system/
sudo systemctl daemon-reload
```

## Enable on boot

Enable the web/API service:

```bash
sudo systemctl enable hummel-it-frame.service
```

For fullscreen slideshow startup, also enable the display service:

```bash
sudo systemctl enable hummel-it-frame-display.service
```

## Start and stop

```bash
sudo systemctl start hummel-it-frame.service
sudo systemctl stop hummel-it-frame.service
sudo systemctl restart hummel-it-frame.service
```

For the display process:

```bash
sudo systemctl start hummel-it-frame-display.service
sudo systemctl stop hummel-it-frame-display.service
sudo systemctl restart hummel-it-frame-display.service
```

## Logs

View recent logs:

```bash
journalctl -u hummel-it-frame.service -n 100
journalctl -u hummel-it-frame-display.service -n 100
```

Follow logs:

```bash
journalctl -u hummel-it-frame.service -f
journalctl -u hummel-it-frame-display.service -f
```

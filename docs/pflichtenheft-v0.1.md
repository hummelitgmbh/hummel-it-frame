# Pflichtenheft – Hummel IT Frame v0.1

## Ziel

Implementierung eines ersten lauffähigen MVP (Minimum Viable Product).

Version 0.1 unterstützt ausschließlich den lokalen Bildmodus.

Nextcloud, WLAN-Management und OTA-Updates sind nicht Bestandteil dieser Version.

---

# Technologiestack

## Programmiersprache

* Python 3.12+

## Backend

* FastAPI

## Anzeige

* pygame

## Konfiguration

* YAML

## Tests

* pytest

## Paketmanagement

* uv

---

# Projektstruktur

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

# Verzeichnisstruktur Laufzeit

## Konfiguration

```text
/etc/hummel-it-frame/config.yaml
```

## Bildspeicher

```text
/var/lib/hummel-it-frame/images
```

## Temporäre Daten

```text
/var/lib/hummel-it-frame/tmp
```

---

# Display Service

## Aufgabe

Anzeige der Bilder im Vollbildmodus.

## Anforderungen

* Vollbilddarstellung
* Automatischer Bildwechsel
* Unterstützung von JPG
* Unterstützung von PNG
* Zufällige Reihenfolge
* Automatisches Neuladen der Bildliste

## Konfiguration

```yaml
slideshow:
  interval_seconds: 20
  display_mode: fill
```

## Unterstützte Modi

* fit
* fill
* stretch

---

# Web Service

## Aufgabe

Verwaltung der Bilder.

## Technologie

FastAPI

---

## Endpunkte

### Status

```http
GET /api/status
```

Antwort:

```json
{
  "status": "ok"
}
```

---

### Bilder auflisten

```http
GET /api/images
```

---

### Bild hochladen

```http
POST /api/images
```

Multipart Upload.

---

### Bild löschen

```http
DELETE /api/images/{filename}
```

---

# Weboberfläche

## Anforderungen

* Anzeige vorhandener Bilder
* Upload neuer Bilder
* Löschen vorhandener Bilder

Keine Benutzerverwaltung in Version 0.1.

---

# Config Service

## Aufgabe

Laden und Validieren der Konfiguration.

## Beispiel

```yaml
display:
  mode: fill

slideshow:
  interval_seconds: 20

storage:
  image_directory: /var/lib/hummel-it-frame/images
```

---

# Storage Service

## Aufgabe

Zugriff auf Bilder.

## Unterstützte Formate

* jpg
* jpeg
* png

Nicht unterstützte Dateien müssen ignoriert werden.

---

# Systemintegration

## systemd Service

Name:

```text
hummel-it-frame.service
```

Aufgabe:

Start der Anwendung beim Systemstart.

---

# Installer

## Aufgabe

Automatische Installation.

Erzeugt:

* Verzeichnisse
* Konfigurationsdatei
* systemd Service

---

# Fehlerbehandlung

## Keine Bilder vorhanden

Anzeige eines Platzhalterbildes:

```text
No images available
```

## Defekte Bilddatei

Bild überspringen.

Anwendung darf nicht abstürzen.

---

# Akzeptanzkriterien

## AC-001

Anwendung startet automatisch nach Boot.

## AC-002

Bilder können über Webinterface hochgeladen werden.

## AC-003

Neue Bilder erscheinen ohne Neustart.

## AC-004

Bilder werden im Vollbild angezeigt.

## AC-005

Anwendung läuft mindestens 24 Stunden ohne manuellen Eingriff.

## AC-006

Ein Upload von 100 Bildern funktioniert fehlerfrei.

---

# Nicht Bestandteil von Version 0.1

* Nextcloud
* WLAN-Konfiguration
* Fallback-Hotspot
* Mehrere Alben
* Benutzerverwaltung
* OTA-Updates
* Read-Only-Modus
* Mehrere Provider

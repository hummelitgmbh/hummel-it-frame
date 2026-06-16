# Lastenheft – Hummel IT Frame

## 1. Zielsetzung

Hummel IT Frame ist eine selbst gehostete Plattform für digitale Bilderrahmen auf Basis von Raspberry Pi.

Ziel ist die Bereitstellung eines einfach zu bedienenden digitalen Bilderrahmens ohne Hersteller-Cloud und ohne Abhängigkeit von externen Diensten.

Die Plattform soll sowohl für Privatanwender als auch für Organisationen geeignet sein.

---

## 2. Produktvision

Der Hummel IT Frame soll als Appliance betrieben werden können.

Der Anwender soll lediglich:

* Strom anschließen
* Bilder bereitstellen
* den Bilderrahmen nutzen

Linux-Kenntnisse dürfen nicht erforderlich sein.

---

## 3. Zielplattform

Primäre Zielplattform:

* Raspberry Pi 4
* Raspberry Pi 5

Betriebssystem:

* Raspberry Pi OS Lite

---

## 4. Betriebsarten

### Modus 1 – Lokaler Upload

Bilder werden lokal auf dem Gerät gespeichert.

Der Upload erfolgt über eine Weboberfläche.

### Modus 2 – Nextcloud

Bilder werden automatisch aus einer Nextcloud synchronisiert.

Die Anzeige muss auch bei fehlender Netzwerkverbindung weiter funktionieren.

---

## 5. Funktionale Anforderungen

### Anzeige

* Vollbilddarstellung
* Automatischer Bildwechsel
* Unterstützung von Hoch- und Querformat
* Unterstützung verschiedener Darstellungsmodi

  * Fit
  * Fill
  * Stretch

### Bildquellen

* Lokaler Upload
* Nextcloud

### Verwaltung

* Weboberfläche
* Bildverwaltung
* Upload neuer Bilder
* Löschen vorhandener Bilder
* Konfigurationsverwaltung

### Systembetrieb

* Automatischer Start nach Boot
* Automatische Wiederherstellung nach Fehlern
* Dauerbetrieb des Raspberry Pi

---

## 6. Nichtfunktionale Anforderungen

### Stabilität

* 24/7-Betrieb
* Automatische Fehlerbehandlung
* Neustart abgestürzter Dienste

### Performance

* Flüssiger Bildwechsel
* Unterstützung von mindestens 5.000 Bildern

### Offlinefähigkeit

* Anzeige muss ohne Internetverbindung funktionieren

### Wartbarkeit

* Modulare Architektur
* Erweiterbare Provider-Struktur

---

## 7. Branding

Der Produktname lautet:

Hummel IT Frame

Der Hersteller ist:

Hummel IT GmbH

Folgende Komponenten müssen Branding unterstützen:

* Bootscreen
* Splashscreen
* Weboberfläche
* Fehlerseiten

---

## 8. Energie- und Betriebskonzept

Der Raspberry Pi bleibt dauerhaft eingeschaltet.

Das Display kann unabhängig vom Raspberry Pi ein- oder ausgeschaltet werden.

Nach dem Einschalten des Displays muss die Anzeige ohne vollständigen Systemstart verfügbar sein.

---

## 9. Architekturprinzipien

* Appliance-First
* Local-First
* Privacy-First
* Keine Hersteller-Cloud erforderlich
* Raspberry-Pi-optimiert
* Erweiterbar durch Provider

---

## 10. Langfristige Ziele

* WLAN-Konfiguration über Weboberfläche
* Fallback-Hotspot
* Read-Only-Betrieb
* OTA-Updates
* Mehrere Bildquellen
* Mehrere Alben
* Zentrale Verwaltung mehrerer Geräte

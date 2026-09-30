# IMPOLA – Website impola.de (Stand 30.09.2026)

Statische Website (HTML/CSS/JS) + `kontakt.php` für GoDaddy Linux-Hosting.
Kein Tracking, keine Cookies, keine externen Dienste, Schrift lokal.

## Hochladen
Inhalt von `public_html/` per cPanel-Dateimanager oder FTP in das Web-Root der Domain laden
(inkl. der versteckten Datei `.htaccess`). `build.py` und diese README **nicht** hochladen.

## Bilder
Eingebaut (WebP in `public_html/img/`): hero-bad-desktop, hero-bad-mobile, karte-badumbau,
badumbau-kopf, vorher-1-wanne / nachher-1-dusche (Vergleich auf /badumbau), karte-objektservice,
karte-verwaltung, b2b-pflegedienste, og-image.jpg.

Noch Platzhalter (`.svg`) – finales Bild als `.webp` gleichen Namens ablegen und `python3 build.py`
ausführen; `build.py` nimmt automatisch die WebP-Datei, sobald sie existiert:

| Datei | Format | Prompt |
|---|---|---|
| karte-sanierung | 800 × 600 | 4.4 |
| karte-umbau | 800 × 600 | 4.5 |
| portrait-tim-pomian / portrait-dennis-lasch | 1000 × 1250 | echtes Foto |

Vorher/Nachher: Beide Bilder eines Paares exakt gleich zuschneiden. KI-Bilder bleiben als
„Beispielvisualisierung“ gekennzeichnet; echte Kundenfotos nur mit schriftlicher Freigabe.

## Vor dem Livegang
- `datenschutz.html`: vollständigen, geprüften Text einsetzen (Pflichtinhalte im HTML-Kommentar)
- `impressum.html`: Registergericht, HRB, ggf. USt-IdNr. ergänzen (gelb markiert)
- `kontakt.php`: Empfänger/Absender prüfen, Testanfrage senden, Spam-Ordner kontrollieren
- Rollen Tim/Dennis auf `ueber-uns.html`, Leistungsliste Objektservice, Erreichbarkeit „Mo–Fr 8–18 Uhr“ bestätigen
- Test: https://impola.de/badumbau (saubere URL für den Postkarten-QR-Code)

## GitHub
- Repository **privat** anlegen (z. B. `impola-website`).
- Deployment: `.github/workflows/deploy.yml` lädt `public_html/` per FTPS auf GoDaddy.
  Secrets unter *Settings → Secrets and variables → Actions* anlegen: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.
  Start vorerst manuell über den Tab *Actions*.
- Seiten ändern: Inhalte in `build.py` anpassen → `python3 build.py` → committen.

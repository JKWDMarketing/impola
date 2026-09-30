# IMPOLA – Website impola.de (Stand 30.09.2026)

Statische Website (HTML/CSS/JS) + `kontakt.php` für GoDaddy Linux-Hosting.
Kein Tracking, keine Cookies, keine externen Dienste, Schrift lokal.

## Hochladen
Inhalt von `public_html/` per cPanel-Dateimanager oder FTP in das Web-Root der Domain laden
(inkl. der versteckten Datei `.htaccess`). `build.py` und diese README **nicht** hochladen.

## Bilder austauschen
Alle Platzhalter liegen in `public_html/img/` als `.svg` im Zielformat.
Finales Bild als `.webp` gleichen Namens speichern und in den HTML-Dateien `.svg` → `.webp` ersetzen
(bzw. in `build.py` in der Funktion `ph()` und im Hero-Block, dann `python3 build.py` ausführen).

| Datei | Format | Prompt |
|---|---|---|
| hero-bad-desktop | 1600 × 1200 | 4.1 |
| hero-bad-mobile | 900 × 1125 | 4.2 |
| karte-badumbau | 800 × 600 | 4.3 |
| karte-sanierung | 800 × 600 | 4.4 |
| karte-umbau | 800 × 600 | 4.5 |
| karte-objektservice | 800 × 600 | 4.6 |
| karte-verwaltung | 800 × 600 | 4.7 |
| b2b-pflegedienste | 1200 × 800 | 4.8 |
| og-image.png | 1200 × 630 (PNG/JPG, nicht WebP) | 4.9 |
| portrait-tim-pomian / portrait-dennis-lasch | 1000 × 1250 | echtes Foto |
| vorher-1-wanne-fliesen / nachher-1-bodengleich | 1600 × 1200 | V1 / N1 |
| vorher-2-wanne-standard / nachher-2-paneele | 1600 × 1200 | V2 / N2 |
| vorher-3-kleines-bad / nachher-3-klappsitz | 1600 × 1200 | V3 / N3 |

Vorher/Nachher (Badumbau-Seite): Pfade stehen zusätzlich in den `data-vorher`/`data-nachher`-Attributen
der Auswahl-Buttons – dort ebenfalls `.svg` → `.webp` ändern. Vorher- und Nachher-Bild eines Paares
exakt gleich zuschneiden, sonst „springt“ der Raum beim Ziehen.

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

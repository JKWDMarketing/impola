# IMPOLA – Website www.impola.de

Statische Website auf **Vercel**, verbunden mit diesem GitHub-Repository. Jeder Commit auf `main` wird automatisch veröffentlicht.

## Aufbau
- `public_html/` – die Website (HTML, CSS, JS, Schriften, Bilder)
- `api/kontakt.js` – Kontaktformular (Vercel-Funktion): Mail an info@impola.de + Eingangsbestätigung an den Absender
- `vercel.json` – Ausgabeordner `public_html`, saubere URLs (`/badumbau`), Sicherheits-Header
- `build.py` – erzeugt alle HTML-Seiten, `sitemap.xml` und `robots.txt` neu. Texte dort ändern, dann `python3 build.py`

## Kontaktformular (Vercel → Settings → Environment Variables, danach neu deployen)
| Variable | Wert |
|---|---|
| `SMTP_HOST` | Mailserver des E-Mail-Anbieters (info@impola.de liegt bei Zoom Mail – SMTP-Adresse dort nachsehen). Standard ohne Angabe: smtp.gmail.com |
| `SMTP_PORT` | 465 (Standard) oder 587 |
| `SMTP_USER` | info@impola.de |
| `SMTP_PASS` | Passwort bzw. App-Passwort |
| `MAIL_TO` | optional, Standard info@impola.de |
| `AUTO_REPLY` | optional, `aus` schaltet die Eingangsbestätigung ab |

Nach dem Einrichten je eine Testanfrage mit und ohne E-Mail-Adresse senden, Spam-Ordner prüfen.

## Nach der Eintragung ins Handelsregister
In `build.py` bei `FIRMA` den Zusatz ` i. G.` entfernen und im Impressum Registergericht + HRB eintragen, dann `python3 build.py`.

## Kundenstimmen
In `build.py` die Liste `STIMMEN` durch echte, schriftlich freigegebene Rückmeldungen ersetzen (Originalwortlaut, Vorname + Stadtteil).

## Zur Prüfung markiert (HTML-Kommentare in `build.py`)
- Datenschutz: Speicherdauer der Vercel-Logs, SMTP-Anbieter des Formulars, Anbieter/Anschrift von „das programm“
- Impressum: Handwerkskammer, falls eingetragen
- Widerrufsbelehrung: anwaltlich prüfen lassen (Werkverträge mit Material)

## Aufräumen
Die alten Ordner `impola`, `impola 2` und `impola-vercel` im Repo werden nicht ausgeliefert und können gelöscht werden.

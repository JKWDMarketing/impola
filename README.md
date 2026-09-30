# IMPOLA – Website impola.de

Statische Website auf **Vercel**, verbunden mit diesem GitHub-Repository.
Jeder Commit auf `main` wird automatisch veröffentlicht.

## Aufbau
- `public_html/` – die Website (HTML, CSS, JS, Schriften, Bilder)
- `api/kontakt.js` – Versand des Kontaktformulars (Vercel-Funktion)
- `vercel.json` – Einstellungen: Ausgabeordner `public_html`, saubere URLs (`/badumbau`), Sicherheits-Header
- `build.py` – erzeugt die HTML-Seiten neu (Texte hier ändern, dann `python3 build.py`)

## Kontaktformular aktivieren
In Vercel unter *Settings → Environment Variables* anlegen, danach neu deployen:
`SMTP_USER` (z. B. info@impola.de), `SMTP_PASS` (App-Passwort des Google-Kontos), optional `MAIL_TO`.

## Bilder
Noch Platzhalter (`.svg`): karte-sanierung (4.4), karte-umbau (4.5), Porträts Tim/Dennis (echte Fotos).
Finales Bild als `.webp` gleichen Namens in `public_html/img/` ablegen und `python3 build.py` ausführen.
Vorher/Nachher bleibt als „Beispielvisualisierung“ gekennzeichnet, bis echte, freigegebene Kundenfotos vorliegen.

## Vor dem Livegang mit impola.de
- Datenschutzerklärung vollständig einsetzen (Pflichtinhalte im HTML-Kommentar, Hosting: Vercel)
- Impressum: Registergericht, HRB, ggf. USt-IdNr. ergänzen
- Domain impola.de in Vercel hinzufügen und DNS bei GoDaddy auf Vercel umstellen
- Vercel-Tarif prüfen: Hobby ist nur für nicht-kommerzielle Nutzung – für die Firmenwebsite Pro nutzen

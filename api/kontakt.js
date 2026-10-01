// IMPOLA – Kontaktformular als Vercel-Funktion (POST /api/kontakt).
// Speichert nichts. Sendet die Anfrage an info@impola.de und – falls eine E-Mail angegeben ist –
// eine kurze Eingangsbestätigung an den Absender.
//
// Umgebungsvariablen in Vercel (Settings → Environment Variables), danach neu deployen:
//   SMTP_HOST      Mailserver des E-Mail-Anbieters (Standard: smtp.gmail.com)
//   SMTP_PORT      465 (SSL, Standard) oder 587 (STARTTLS)
//   SMTP_USER      Absenderkonto, z. B. info@impola.de
//   SMTP_PASS      Passwort bzw. App-Passwort dieses Kontos
//   MAIL_TO        Empfänger (optional, Standard: info@impola.de)
//   AUTO_REPLY     "aus" schaltet die Eingangsbestätigung ab (optional)
const nodemailer = require("nodemailer");

const ANLIEGEN = {
  badumbau: "Barrierefreier Badumbau",
  sanierung: "Sanierung oder Umbau",
  objektservice: "Objektservice",
  b2b: "Zusammenarbeit (Pflegedienst, Hausverwaltung)",
  partner: "Partner werden (Handwerksbetrieb)",
  sonstiges: "Etwas anderes",
};
const zeile = (v, max) => String(v || "").replace(/[\r\n]+/g, " ").trim().slice(0, max);
const weiter = (res, ziel) => { res.statusCode = 303; res.setHeader("Location", ziel); res.end(); };

const BESTAETIGUNG = (name) =>
  `Guten Tag ${name},\n\n` +
  "vielen Dank für Ihre Nachricht. Ihre Anfrage ist bei uns eingegangen. Wir melden uns innerhalb von zwei Werktagen telefonisch bei Ihnen, um einen kostenlosen Termin vor Ort zu vereinbaren.\n\n" +
  "Wenn es eilt, erreichen Sie uns Montag bis Freitag von 8 bis 18 Uhr unter 0178 9176594.\n\n" +
  "Freundliche Grüße\nIhr IMPOLA-Team\n\n" +
  "IMPOLA · Schillstr. 6 · 44339 Dortmund · info@impola.de · www.impola.de\n" +
  "Diese E-Mail wurde automatisch versendet, weil Ihre E-Mail-Adresse im Kontaktformular auf impola.de angegeben wurde.\n";

module.exports = async (req, res) => {
  if (req.method !== "POST") return weiter(res, "/kontakt");
  const b = req.body || {};

  // Spam-Schutz: Honeypot + Mindestzeit 3 Sekunden
  if (b.website) return weiter(res, "/danke");
  const ts = parseInt(b.ts, 10) || 0;
  if (ts > 0 && Date.now() / 1000 - ts < 3) return weiter(res, "/danke");

  const name = zeile(b.name, 120);
  const telefon = zeile(b.telefon, 40);
  let email = zeile(b.email, 160);
  const plz = zeile(b.plz, 5).replace(/\D/g, "");
  let anliegen = zeile(b.anliegen, 30);
  const nachricht = String(b.nachricht || "").trim().slice(0, 4000);

  if (!ANLIEGEN[anliegen]) anliegen = "sonstiges";
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) email = "";
  const fehler = "/kontakt?fehler=1&anliegen=" + encodeURIComponent(anliegen);
  if (!name || !/^[0-9 +\/()\-]{6,40}$/.test(telefon)) return weiter(res, fehler);
  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
    console.error("SMTP_USER/SMTP_PASS fehlen in den Vercel-Umgebungsvariablen.");
    return weiter(res, fehler);
  }

  const port = parseInt(process.env.SMTP_PORT, 10) || 465;
  const transport = nodemailer.createTransport({
    host: process.env.SMTP_HOST || "smtp.gmail.com",
    port,
    secure: port === 465,
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  });

  const text =
    "Neue Anfrage über impola.de\n\n" +
    `Anliegen:  ${ANLIEGEN[anliegen]}\nName:      ${name}\nTelefon:   ${telefon}\n` +
    `E-Mail:    ${email || "–"}\nPLZ:       ${plz || "–"}\n\nNachricht:\n${nachricht || "–"}\n`;

  try {
    await transport.sendMail({
      from: `IMPOLA Website <${process.env.SMTP_USER}>`,
      to: process.env.MAIL_TO || "info@impola.de",
      replyTo: email || undefined,
      subject: `[Website] ${ANLIEGEN[anliegen]}${plz ? " – " + plz : ""}: ${name}`,
      text,
    });
  } catch (e) {
    console.error("Mailversand fehlgeschlagen:", e.message);
    return weiter(res, fehler);
  }

  // Eingangsbestätigung – ein Fehler hier blockiert die Anfrage nicht.
  if (email && process.env.AUTO_REPLY !== "aus") {
    try {
      await transport.sendMail({
        from: `IMPOLA <${process.env.SMTP_USER}>`,
        to: email,
        replyTo: process.env.MAIL_TO || "info@impola.de",
        subject: "Ihre Anfrage bei IMPOLA ist angekommen",
        text: BESTAETIGUNG(name),
      });
    } catch (e) {
      console.error("Eingangsbestätigung fehlgeschlagen:", e.message);
    }
  }
  return weiter(res, "/danke");
};

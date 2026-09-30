// IMPOLA – Kontaktformular als Vercel-Funktion (POST /api/kontakt).
// Speichert nichts, versendet nur eine E-Mail über Google Workspace (SMTP).
// Umgebungsvariablen in Vercel (Settings → Environment Variables):
//   SMTP_USER  = Google-Workspace-Adresse, die sendet (z. B. info@impola.de)
//   SMTP_PASS  = App-Passwort dieses Kontos (nicht das normale Passwort)
//   MAIL_TO    = Empfänger (optional, Standard: info@impola.de)
const nodemailer = require("nodemailer");

const ERLAUBT = ["badumbau", "sanierung", "objektservice", "b2b", "partner", "sonstiges"];
const zeile = (v, max) => String(v || "").replace(/[\r\n]+/g, " ").trim().slice(0, max);
const weiter = (res, ziel) => { res.statusCode = 303; res.setHeader("Location", ziel); res.end(); };

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
  const plz = zeile(b.plz, 5);
  let anliegen = zeile(b.anliegen, 30);
  const nachricht = String(b.nachricht || "").trim().slice(0, 4000);

  if (!ERLAUBT.includes(anliegen)) anliegen = "sonstiges";
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) email = "";
  const fehler = "/kontakt?fehler=1&anliegen=" + encodeURIComponent(anliegen);
  if (!name || !/^[0-9 +\/()\-]{6,40}$/.test(telefon)) return weiter(res, fehler);
  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) return weiter(res, fehler);

  const text =
    "Neue Anfrage über impola.de\n\n" +
    `Anliegen:  ${anliegen}\nName:      ${name}\nTelefon:   ${telefon}\n` +
    `E-Mail:    ${email || "–"}\nPLZ:       ${plz || "–"}\n\nNachricht:\n${nachricht || "–"}\n`;

  try {
    const transport = nodemailer.createTransport({
      host: "smtp.gmail.com", port: 465, secure: true,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
    await transport.sendMail({
      from: `IMPOLA Website <${process.env.SMTP_USER}>`,
      to: process.env.MAIL_TO || "info@impola.de",
      replyTo: email || undefined,
      subject: `Anfrage ${anliegen}: ${name}`,
      text,
    });
    return weiter(res, "/danke");
  } catch (e) {
    console.error("Mailversand fehlgeschlagen:", e.message);
    return weiter(res, fehler);
  }
};

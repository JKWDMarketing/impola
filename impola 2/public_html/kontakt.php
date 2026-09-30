<?php
/**
 * IMPOLA – Kontaktformular-Versand (ohne Datenbank, ohne Speicherung).
 * Voraussetzung: GoDaddy Linux-Hosting mit PHP. Vor Livegang testen!
 * Empfehlung: Bei Zustellproblemen auf SMTP (z. B. PHPMailer + Google Workspace) umstellen.
 */
declare(strict_types=1);

$EMPFAENGER = 'info@impola.de';          // Empfänger der Anfragen
$ABSENDER   = 'website@impola.de';         // Muss zur Domain gehören (SPF/DKIM!)

function zurueck(string $ziel): void { header('Location: ' . $ziel, true, 303); exit; }
function sauber(string $s, int $max): string {
    $s = trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $s));   // Header-Injection verhindern
    return mb_substr($s, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { zurueck('kontakt.html'); }

// Spam-Schutz: Honeypot + Mindestzeit (3 s) statt reCAPTCHA
if (!empty($_POST['website'])) { zurueck('danke.html'); }
$ts = (int)($_POST['ts'] ?? 0);
if ($ts > 0 && (time() - $ts) < 3) { zurueck('danke.html'); }

$name     = sauber((string)($_POST['name'] ?? ''), 120);
$telefon  = sauber((string)($_POST['telefon'] ?? ''), 40);
$email    = sauber((string)($_POST['email'] ?? ''), 160);
$plz      = sauber((string)($_POST['plz'] ?? ''), 5);
$anliegen = sauber((string)($_POST['anliegen'] ?? ''), 30);
$nachricht = mb_substr(trim((string)($_POST['nachricht'] ?? '')), 0, 4000);

$erlaubt = ['badumbau','sanierung','objektservice','b2b','partner','sonstiges'];
if (!in_array($anliegen, $erlaubt, true)) { $anliegen = 'sonstiges'; }
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) { $email = ''; }

if ($name === '' || !preg_match('/^[0-9 +\/()\-]{6,40}$/', $telefon)) {
    zurueck('kontakt.html?fehler=1&anliegen=' . urlencode($anliegen));
}

$text  = "Neue Anfrage über impola.de\n\n";
$text .= "Anliegen:  $anliegen\nName:      $name\nTelefon:   $telefon\n";
$text .= "E-Mail:    " . ($email ?: '–') . "\nPLZ:       " . ($plz ?: '–') . "\n\n";
$text .= "Nachricht:\n" . ($nachricht ?: '–') . "\n";

$header  = "From: IMPOLA Website <$ABSENDER>\r\n";
if ($email !== '') { $header .= "Reply-To: $email\r\n"; }
$header .= "Content-Type: text/plain; charset=UTF-8\r\n";

$betreff = '=?UTF-8?B?' . base64_encode("Anfrage $anliegen: $name") . '?=';
$ok = mail($EMPFAENGER, $betreff, $text, $header, '-f' . $ABSENDER);

zurueck($ok ? 'danke.html' : 'kontakt.html?fehler=1&anliegen=' . urlencode($anliegen));

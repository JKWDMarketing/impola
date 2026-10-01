#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten für impola.de (gemeinsamer Header/Footer)."""
import json, os, re, datetime

OUT = "public_html"
DOMAIN = "https://www.impola.de"   # Primär-Domain in Vercel (impola.de leitet auf www weiter)
# Bis zur Eintragung ins Handelsregister mit Zusatz „i. G.“ auftreten (§ 11 GmbHG). Nach Eintragung: " i. G." löschen, build.py ausführen.
FIRMA = "IMPOLA UG (haftungsbeschränkt) i. G."
STAND = "Oktober 2026"
TEL_ANZEIGE = "0178 9176594"
TEL_LINK = "+491789176594"
MAIL = "info@impola.de"

ICON_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_OK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

NAV = [
    ("badumbau.html", "Badumbau"),
    ("sanierung.html", "Sanierung & Umbau"),
    ("objektservice.html", "Objektservice"),
    ("ueber-uns.html", "Über uns"),
    ("kontakt.html", "Kontakt"),
]


def ph(name, alt, w, h, cls="", lazy=True):
    """Bild-Platzhalter. Später: .svg durch .webp ersetzen, alt-Text beibehalten."""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    ext = "webp" if os.path.exists(os.path.join(OUT, "img", name + ".webp")) else "svg"
    return f'<img src="img/{name}.{ext}" alt="{alt}" width="{w}" height="{h}"{c}{l}>'


def head(title, desc, slug, extra="", og="og-image"):
    canon = DOMAIN + ("/" if slug == "index" else f"/{slug}")
    canon_tag = "" if slug in ("404", "danke") else f'<link rel="canonical" href="{canon}">\n'
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{canon_tag}<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="IMPOLA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/img/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="theme-color" content="#1E252C">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/montserrat-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
{extra}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
'''


def header(aktiv):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == aktiv else ""}>{t}</a></li>' for h, t in NAV
    )
    return f'''<header class="header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="IMPOLA – zur Startseite"><img src="assets/img/impola-logo.png" alt="IMPOLA" width="640" height="201"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="hauptnavigation"><span aria-hidden="true">☰</span><span class="label">Menü</span></button>
    <nav class="nav" id="hauptnavigation" aria-label="Hauptnavigation"><ul>{items}</ul></nav>
    <a class="header-tel" href="tel:{TEL_LINK}" aria-label="Anrufen: {TEL_ANZEIGE}">{ICON_TEL}<span>{TEL_ANZEIGE}</span></a>
    <a class="btn btn-primaer" href="kontakt.html">Beratung anfragen</a>
  </div>
</header>
<main id="inhalt">
'''


FOOTER = f'''</main>
<footer class="footer">
  <div class="wrap">
    <div class="spalten">
      <div>
        <a class="logo" href="index.html"><img src="assets/img/impola-logo.png" alt="IMPOLA" width="640" height="201" loading="lazy"></a>
        <p>Alles rund um die Immobilie – aus einer Hand.</p>
      </div>
      <div>
        <h2>Leistungen</h2>
        <ul>
          <li><a href="badumbau.html">Barrierefreier Badumbau</a></li>
          <li><a href="sanierung.html">Sanierung & Umbau</a></li>
          <li><a href="objektservice.html">Objektservice</a></li>
          <li><a href="verwaltung.html">Immobilienverwaltung</a> <span class="leise">(in Vorbereitung)</span></li>
        </ul>
      </div>
      <div>
        <h2>Unternehmen</h2>
        <ul>
          <li><a href="ueber-uns.html">Über uns</a></li>
          <li><a href="partner-werden.html">Partner werden</a></li>
          <li><a href="kontakt.html">Kontakt</a></li>
        </ul>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li><a href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a></li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li>Schillstr. 6<br>44339 Dortmund</li>
        </ul>
      </div>
    </div>
    <div class="footer-unten">
      <span>© <span id="jahr">2026</span> {FIRMA}</span>
      <span><a href="impressum.html">Impressum</a> &nbsp; <a href="datenschutz.html">Datenschutz</a> &nbsp; <a href="widerruf.html">Widerrufsbelehrung</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def cta(titel="Sprechen wir über Ihr Vorhaben.", text="Rufen Sie an oder schreiben Sie uns. Wir melden uns innerhalb von zwei Werktagen und vereinbaren einen Termin vor Ort.", anliegen=""):
    q = f"?anliegen={anliegen}" if anliegen else ""
    return f'''<section class="abschnitt" aria-labelledby="cta-titel">
  <div class="wrap">
    <div class="cta-block">
      <div>
        <img class="logo-neg" src="assets/img/impola-logo-negativ.png" alt="" width="640" height="201" loading="lazy">
        <h2 id="cta-titel">{titel}</h2>
        <p>{text}</p>
      </div>
      <div class="cta-aktionen">
        <a class="tel-gross" href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a>
        <p class="kleingedruckt">Montag bis Freitag, 8 bis 18 Uhr</p>
        <a class="btn btn-hell" href="kontakt.html{q}">Beratung anfragen</a>
      </div>
    </div>
  </div>
</section>
'''


def seitenkopf(krumen, h1, einleitung, bild=None, aktionen=True, anliegen=""):
    q = f"?anliegen={anliegen}" if anliegen else ""
    akt = f'''<div class="hero-aktionen">
        <a class="btn btn-primaer" href="kontakt.html{q}">Beratung anfragen</a>
        <p class="hero-anruf">Oder anrufen: <a href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a></p>
      </div>''' if aktionen else ""
    cls = "seitenkopf" if bild else "seitenkopf ohne-bild"
    b = f'<div class="seitenkopf-bild">{bild}</div>' if bild else ""
    return f'''<section class="{cls}">
  <div class="wrap">
    <div>
      <nav class="brotkrumen" aria-label="Brotkrumen"><a href="index.html">Start</a> / {krumen}</nav>
      <h1>{h1}</h1>
      <p class="einleitung">{einleitung}</p>
      {akt}
    </div>
    {b}
  </div>
</section>
'''


def saubere_links(html):
    """index.html -> /, badumbau.html?x#y -> /badumbau?x#y, img/ und assets/ -> absolut (wichtig für 404 und Unterpfade)."""
    html = re.sub(r'href="index\.html"', 'href="/"', html)
    html = re.sub(r'href="([a-z0-9-]+)\.html([?#][^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', html)
    html = re.sub(r'(href|src)="(assets|img)/', r'\1="/\2/', html)
    return html


def page(slug, title, desc, aktiv, body, extra="", og="og-image"):
    html = saubere_links(head(title, desc, slug, extra, og) + header(aktiv) + body + FOOTER)
    with open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ------------------------------------------------------------------ Bausteine
FOERDERCHECK = f'''<section class="abschnitt" id="foerdercheck-bereich" aria-labelledby="check-titel">
  <div class="wrap">
    <div class="check">
      <div>
        <h2 id="check-titel">Kommt ein Zuschuss für Ihr Bad in Frage?</h2>
        <p>Drei kurze Fragen, eine erste Einschätzung. Ihre Antworten bleiben in Ihrem Browser – sie werden weder gespeichert noch an uns übertragen.</p>
      </div>
      <form id="foerdercheck" onsubmit="return false" aria-describedby="check-hinweis">
        <fieldset>
          <legend><span class="schritt">1.</span>Ist ein Pflegegrad festgestellt?</legend>
          <div class="optionen">
            <label><input type="radio" name="pflegegrad" value="ja"><span>Ja</span></label>
            <label><input type="radio" name="pflegegrad" value="offen"><span>Beantragt oder unklar</span></label>
            <label><input type="radio" name="pflegegrad" value="nein"><span>Nein</span></label>
          </div>
        </fieldset>
        <fieldset>
          <legend><span class="schritt">2.</span>Wie wohnen Sie?</legend>
          <div class="optionen">
            <label><input type="radio" name="wohnen" value="eigentum"><span>Im Eigentum</span></label>
            <label><input type="radio" name="wohnen" value="miete"><span>Zur Miete</span></label>
          </div>
        </fieldset>
        <fieldset>
          <legend><span class="schritt">3.</span>Was stört im Bad am meisten?</legend>
          <div class="optionen">
            <label><input type="radio" name="problem" value="wanne"><span>Hoher Wanneneinstieg</span></label>
            <label><input type="radio" name="problem" value="rutsch"><span>Rutschgefahr</span></label>
            <label><input type="radio" name="problem" value="platz"><span>Zu wenig Platz</span></label>
            <label><input type="radio" name="problem" value="anderes"><span>Etwas anderes</span></label>
          </div>
        </fieldset>
        <div class="check-ergebnis" id="check-ergebnis" hidden tabindex="-1" aria-live="polite">
          <h3>Ihre erste Einschätzung</h3>
          <ul id="check-punkte"></ul>
          <a class="btn btn-primaer" href="kontakt.html?anliegen=badumbau">Kostenlose Beratung anfragen</a>
        </div>
        <p class="kleingedruckt" id="check-hinweis">Unverbindliche Ersteinschätzung, keine Förderzusage. Über den Zuschuss entscheidet Ihre Pflegekasse.</p>
      </form>
    </div>
  </div>
</section>
'''

FAQ_BAD = [
    ("Wie hoch ist der Zuschuss der Pflegekasse?",
     "<p>Für Maßnahmen, die das Wohnumfeld verbessern, zahlt die Pflegekasse bis zu 4.180 € je Maßnahme (§ 40 Abs. 4 SGB XI). Voraussetzung ist ein festgestellter Pflegegrad – schon ab Pflegegrad 1. Wohnen mehrere Pflegebedürftige zusammen, kann sich der Betrag erhöhen. Über die Höhe entscheidet die Pflegekasse im Einzelfall.</p>"),
    ("Muss ich den Zuschuss vor dem Umbau beantragen?",
     "<p>Ja. Stellen Sie den Antrag bei Ihrer Pflegekasse, bevor die Arbeiten beginnen. Wir erstellen das Angebot, das Sie dafür brauchen, und helfen beim Ausfüllen.</p>"),
    ("Wie lange dauert ein Badumbau?",
     "<p>Ein typischer Umbau von der Wanne zur bodengleichen Dusche dauert meist ein bis zwei Wochen. Die genaue Dauer nennen wir Ihnen nach dem Termin vor Ort – verbindlich im Angebot.</p>"),
    ("Wie viel Schmutz und Lärm entsteht?",
     "<p>Abbrucharbeiten sind laut, das lässt sich nicht vermeiden. Wir kündigen laute Tage vorher an, decken Wege und Böden ab und hinterlassen die Wohnung jeden Tag besenrein.</p>"),
    ("Ich wohne zur Miete. Geht das trotzdem?",
     "<p>Ja, mit Erlaubnis Ihres Vermieters. Für Umbauten, die Barrieren reduzieren, haben Mieter darauf in der Regel einen Anspruch (§ 554 BGB). Wir helfen Ihnen, die Anfrage an den Vermieter vorzubereiten.</p>"),
    ("Was kostet ein barrierefreies Bad?",
     "<p>Das hängt von Größe, Zustand und Ausstattung ab. Nach dem kostenlosen Termin vor Ort erhalten Sie ein schriftliches Festpreisangebot – so sehen Sie, welcher Eigenanteil nach einem möglichen Zuschuss bleibt.</p>"),
]


def faq(items):
    rows = "".join(f"<details><summary>{q}</summary><div>{a}</div></details>" for q, a in items)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("<p>", "").replace("</p>", "")}}
        for q, a in items]}
    return rows, f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'


ABLAUF = '''<ol class="ablauf">
  <li><h3>Anfrage</h3><p>Sie rufen an oder schreiben uns. Wir besprechen kurz, worum es geht.</p></li>
  <li><h3>Termin vor Ort</h3><p>Wir sehen uns Bad oder Wohnung an, messen auf und hören zu, was Ihnen wichtig ist.</p></li>
  <li><h3>Angebot & Förderantrag</h3><p>Sie erhalten ein schriftliches Angebot. Wenn ein Zuschuss möglich ist, helfen wir beim Antrag.</p></li>
  <li><h3>Umbau aus einer Hand</h3><p>Wir koordinieren alle Gewerke bis zur Übergabe. Sie haben einen festen Ansprechpartner.</p></li>
</ol>'''

ABLAUF_SAN = '''<ol class="ablauf">
  <li><h3>Besichtigung</h3><p>Wir gehen Wohnung oder Haus gemeinsam durch, nehmen den Zustand auf und klären Ihre Wünsche.</p></li>
  <li><h3>Leistungsplan</h3><p>Sie erhalten eine klare Aufstellung aller Arbeiten – mit Reihenfolge und realistischem Zeitplan.</p></li>
  <li><h3>Festpreisangebot</h3><p>Ein schriftliches Angebot für das ganze Vorhaben. Sie wissen vorher, was es kostet.</p></li>
  <li><h3>Koordination bis zur Übergabe</h3><p>Wir steuern alle Gewerke, halten Sie auf dem Laufenden und übergeben besenrein.</p></li>
</ol>'''

# Kundenstimmen: Layout steht. Die Texte unten sind Platzhalter und werden 1:1 durch echte,
# schriftlich freigegebene Rückmeldungen ersetzt (Originalwortlaut, Vorname + Stadtteil).
# Sobald echte Stimmen drin sind, STIMMEN_HINWEIS auf den Prüfhinweis umstellen (§ 5b Abs. 3 UWG).
STIMMEN = [
    ("Badumbau", "Hier steht bald die Rückmeldung unserer ersten Kundin oder unseres ersten Kunden – im Originalwortlaut und mit Einverständnis.", "Vorname, Stadtteil"),
    ("Sanierung", "Wie lief die Planung, wie die Baustelle, wie die Übergabe? Was unsere Kunden dazu sagen, lesen Sie nach Abschluss der ersten Projekte hier.", "Vorname, Stadtteil"),
    ("Objektservice", "Auch Hausverwaltungen und Eigentümer kommen hier zu Wort – sobald die ersten gemeinsamen Aufträge abgeschlossen sind.", "Hausverwaltung, Dortmund"),
]
STIMMEN_HINWEIS = "Wir veröffentlichen ausschließlich echte Rückmeldungen von Kunden, deren Projekt wir abgeschlossen haben – mit deren Einverständnis."
ICON_ZITAT = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M20 12C11 14 6 20 6 29v7h14V22h-7c0-4 3-6.5 8-7.5zM42 12c-9 2-14 8-14 17v7h14V22h-7c0-4 3-6.5 8-7.5z"/></svg>'


def stimmen_html():
    karten = "".join(
        f'''<figure class="stimme">
        <span class="stimme-art">{art}</span>
        {ICON_ZITAT}
        <blockquote><p>{text}</p></blockquote>
        <figcaption>{wer}</figcaption>
      </figure>''' for art, text, wer in STIMMEN)
    return f'''<section class="abschnitt" aria-labelledby="ref-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="ref-titel">Stimmen unserer Kunden</h2></div>
    <div class="stimmen">{karten}</div>
    <p class="kleingedruckt stimmen-hinweis">{STIMMEN_HINWEIS}</p>
  </div>
</section>'''

# ------------------------------------------------------------------ Startseite
faq_rows, faq_schema = faq(FAQ_BAD[:5])
localbusiness = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "name": "IMPOLA", "legalName": FIRMA, "url": DOMAIN + "/",
    "logo": DOMAIN + "/assets/img/impola-logo.png", "image": DOMAIN + "/img/og-image.jpg",
    "telephone": "+49 178 9176594", "email": MAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Schillstr. 6", "postalCode": "44339",
                "addressLocality": "Dortmund", "addressCountry": "DE"},
    "areaServed": ["Dortmund", "Ruhrgebiet"],
}
ls_schema = f'<script type="application/ld+json">{json.dumps(localbusiness, ensure_ascii=False)}</script>\n'

PINSELHAUS = f'''<div class="pinselhaus">
      <div class="pinselhaus-bild">
        <picture>
          <source media="(max-width: 820px)" srcset="img/hero-bad-mobile.webp">
          <img src="img/hero-bad-desktop.webp" alt="Helles, barrierefreies Bad mit bodengleicher Dusche, Haltegriff und Duschklappsitz" width="1600" height="1200" fetchpriority="high">
        </picture>
      </div>
      <svg class="pinselhaus-strich" viewBox="0 0 600 560" preserveAspectRatio="none" aria-hidden="true">
        <path d="M6 206 L300 22 L594 206" fill="none" stroke="#1E252C" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M30 212 L302 40 L570 208" fill="none" stroke="#1E252C" stroke-width="3" stroke-linecap="round" opacity=".55"/>
        <path class="boden" d="M-4 548 C 160 540, 420 552, 610 544" fill="none" stroke="#518419" stroke-width="11" stroke-linecap="round"/>
      </svg>
    </div>'''

index_body = f'''<section class="hero">
  <div class="wrap">
    <div>
      <h1><span>Ihr Bad.</span><span>Barrierefrei.</span><span>Aus einer Hand.</span></h1>
      <p class="einleitung">Wir bauen Ihr Bad so um, dass Sie sich sicher darin bewegen – mit bodengleicher Dusche, Haltegriffen und genug Platz. Und wir helfen beim Zuschuss der Pflegekasse.</p>
      <div class="hero-aktionen">
        <a class="btn btn-primaer" href="kontakt.html?anliegen=badumbau">Kostenlos beraten lassen</a>
        <p class="hero-anruf">Oder anrufen: <a href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a></p>
      </div>
      <ul class="vertrauen">
        <li>{ICON_OK}Ein Ansprechpartner</li>
        <li>{ICON_OK}Fachgewerke durch Meisterpartner</li>
        <li>{ICON_OK}Zuschuss ab Pflegegrad 1 möglich</li>
      </ul>
    </div>
    {PINSELHAUS}
  </div>
</section>

{FOERDERCHECK}

<section class="abschnitt" aria-labelledby="leistungen-titel">
  <div class="wrap">
    <div class="kopf">
      <h2 id="leistungen-titel">Was wir für Sie übernehmen</h2>
      <p class="einleitung">Vom einzelnen Bad bis zur ganzen Wohnung: Wir planen, koordinieren und sorgen dafür, dass jedes Gewerk zur richtigen Zeit kommt.</p>
    </div>
    <div class="leistungen">
      <a class="leistung gross" href="badumbau.html">
        {ph("karte-badumbau", "Hand greift an einen Haltegriff neben einer bodengleichen Dusche", 800, 600)}
        <div class="leistung-text">
          <h3>Barrierefreier Badumbau</h3>
          <p>Bodengleiche Dusche statt Wanne, Haltegriffe, Duschsitz, unterfahrbarer Waschtisch. Altersgerecht und behindertengerecht – für Bäder und ganze Wohnungen.</p>
          <p class="mehr">Mehr zum Badumbau</p>
        </div>
      </a>
      <a class="leistung" href="sanierung.html">
        {ph("karte-sanierung", "Frisch sanierte, helle Altbauwohnung", 1200, 900)}
        <div class="leistung-text"><h3>Sanierung komplett</h3><p>Wohnungen und Häuser von Grund auf erneuern – koordiniert aus einer Hand.</p></div>
      </a>
      <a class="leistung" href="sanierung.html#umbau">
        {ph("karte-umbau", "Handwerker montiert eine Trockenbauwand", 1200, 900)}
        <div class="leistung-text"><h3>Umbau</h3><p>Grundrisse ändern, Wände setzen, Räume neu aufteilen.</p></div>
      </a>
      <a class="leistung" href="objektservice.html">
        {ph("karte-objektservice", "Gepflegtes Mehrfamilienhaus aus Klinker", 800, 600)}
        <div class="leistung-text"><h3>Objektservice</h3><p>Kleinreparaturen, Instandhaltung und Pflege rund ums Objekt.</p></div>
      </a>
    </div>
    <p class="hinweis-zeile">Immobilienverwaltung bereiten wir als weiteres Angebot vor. <a href="verwaltung.html">Stand der Vorbereitung</a></p>
  </div>
</section>

<section class="abschnitt" aria-labelledby="ablauf-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="ablauf-titel">So läuft es ab</h2></div>
    {ABLAUF}
  </div>
</section>

<section class="abschnitt" aria-labelledby="warum-titel">
  <div class="wrap zweispaltig">
    <div>
      <h2 id="warum-titel">Alles rund um die Immobilie – aus einer Hand.</h2>
      <p class="einleitung">Sie müssen nicht fünf Handwerker anrufen und Termine abstimmen. Das übernehmen wir.</p>
    </div>
    <ul class="argumente">
      <li><strong>Ein fester Ansprechpartner</strong>Von der ersten Frage bis zur Übergabe spricht immer dieselbe Person mit Ihnen.</li>
      <li><strong>Fachgewerke durch unseren Meisterpartner</strong>Fliesen, Abdichtung und Sanitär übernimmt ein eingetragener Meisterbetrieb.</li>
      <li><strong>Klare Zusagen</strong>Schriftliches Angebot, fester Zeitplan, besenreine Übergabe.</li>
    </ul>
  </div>
</section>

<section class="abschnitt" aria-labelledby="b2b-titel">
  <div class="wrap zweispaltig">
    <div class="bild-rund">{ph("b2b-pflegedienste", "Zwei Personen im Gespräch in einem Wohnungsflur", 1200, 800)}</div>
    <div>
      <h2 id="b2b-titel">Für Pflegedienste und Hausverwaltungen</h2>
      <p>Ihre Kundinnen, Kunden oder Mieter brauchen ein sicheres Bad? Wir sind der verlässliche Ansprechpartner für den Umbau – mit kurzen Wegen, klarer Kommunikation und sauberer Dokumentation für Eigentümer und Kassen.</p>
      <a class="btn btn-sekundaer" href="kontakt.html?anliegen=b2b">Zusammenarbeit anfragen</a>
    </div>
  </div>
</section>

{stimmen_html()}

<section class="abschnitt" aria-labelledby="faq-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="faq-titel">Häufige Fragen</h2></div>
    <div class="faq">{faq_rows}</div>
  </div>
</section>

{cta()}
'''
page("index", "Barrierefreier Badumbau & Sanierung in Dortmund | IMPOLA",
     "Barrierefreier Badumbau, Sanierung und Objektservice aus einer Hand in Dortmund und im Ruhrgebiet. Wir helfen beim Zuschuss der Pflegekasse.",
     "index.html", index_body, ls_schema + faq_schema)

# ------------------------------------------------------------------ Badumbau
faq_rows_bad, faq_schema_bad = faq(FAQ_BAD)
bad_body = seitenkopf("Barrierefreier Badumbau", "Barrierefreier Badumbau in Dortmund",
    "Ein Bad, in dem Sie sich sicher bewegen – heute und in zehn Jahren. Wir planen den Umbau, koordinieren alle Gewerke und unterstützen Sie beim Zuschuss der Pflegekasse.",
    ph("badumbau-kopf", "Bodengleiche Dusche mit Glaswand, Haltegriff und Wandnische", 800, 600, lazy=False), anliegen="badumbau") + f'''
<section class="abschnitt" aria-labelledby="umfang-titel">
  <div class="wrap zweispaltig oben">
    <div>
      <h2 id="umfang-titel">Was wir umbauen</h2>
      <ul class="haken">
        <li>Bodengleiche Dusche statt Badewanne</li>
        <li>Rutschhemmende Fliesen</li>
        <li>Haltegriffe und Stützklappgriffe am WC</li>
        <li>Duschsitz oder Klappsitz</li>
        <li>Unterfahrbarer Waschtisch</li>
        <li>Breitere Türen, wo baulich möglich</li>
        <li>Erhöhtes WC</li>
      </ul>
      <p>Altersgerecht oder behindertengerecht – wir richten uns nach Ihrem Bedarf, nicht nach einem Standardpaket. Auf Wunsch betrachten wir die ganze Wohnung.</p>
    </div>
    <div class="foerderbox">
      <p class="betrag">bis zu 4.180 €</p>
      <p><strong>Zuschuss der Pflegekasse je Maßnahme</strong> nach § 40 Abs. 4 SGB XI – möglich ab Pflegegrad 1.</p>
      <p class="kleingedruckt">Den Antrag stellen Sie vor Beginn des Umbaus bei Ihrer Pflegekasse. Wir erstellen das nötige Angebot und helfen beim Antrag. Eine Bewilligung können wir nicht zusagen – darüber entscheidet die Pflegekasse.</p>
    </div>
  </div>
</section>
{FOERDERCHECK}
<section class="abschnitt" aria-labelledby="ablauf-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="ablauf-titel">So läuft Ihr Badumbau ab</h2></div>
    {ABLAUF}
  </div>
</section>
<section class="abschnitt" aria-labelledby="vorher-titel">
  <div class="wrap">
    <div class="kopf">
      <h2 id="vorher-titel">Von der Wanne zur Dusche</h2>
      <p class="einleitung">So kann Ihr Bad nach dem Umbau aussehen. Ziehen Sie den Regler, um vorher und nachher zu vergleichen.</p>
    </div>
    <!-- Beispielvisualisierung. Sobald echte Projektfotos vorliegen: Bilder tauschen und Kennzeichnung durch „Kundenprojekt“ ersetzen – nur mit schriftlicher Freigabe des Kunden. Weitere Paare später als Auswahl-Buttons ergänzen. -->
    <figure class="vn">
      <div class="vn-buehne" style="--pos: 50%">
        <img class="vn-vorher" src="img/vorher-1-wanne.webp" alt="Vorher: Badewanne mit Duschvorhang, beige Fliesen mit Blumenbordüre" width="1600" height="1200" loading="lazy">
        <img class="vn-nachher" src="img/nachher-1-dusche.webp" alt="Nachher: flache Duschtasse mit Glastür, heller Wandverkleidung, Haltegriff und Thermostat-Brausestange" width="1600" height="1200" loading="lazy">
        <span class="vn-label vn-links" aria-hidden="true">Vorher</span>
        <span class="vn-label vn-rechts" aria-hidden="true">Nachher</span>
        <span class="vn-kennzeichnung">Beispiel</span>
        <span class="vn-linie" aria-hidden="true"><span class="vn-griff"></span></span>
        <input class="vn-regler" type="range" min="0" max="100" value="50" step="1" aria-label="Vergleich: nach links für nachher, nach rechts für vorher">
      </div>
      <figcaption>
        <p class="vn-text">Die Wanne mit hohem Rand kommt raus, eine flache Duschtasse mit Glastür, fugenarmer Wandverkleidung und Haltegriff kommt rein. Der Rest des Bades bleibt, wie er ist – das spart Zeit und Kosten.</p>
      </figcaption>
    </figure>
  </div>
</section>
<section class="abschnitt" aria-labelledby="faq-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="faq-titel">Fragen zum Badumbau</h2></div>
    <div class="faq">{faq_rows_bad}</div>
  </div>
</section>
{cta("Ihr Bad, sicher und bequem.", "Vereinbaren Sie einen kostenlosen Termin vor Ort. Wir melden uns innerhalb von zwei Werktagen.", "badumbau")}
'''
page("badumbau", "Barrierefreier Badumbau in Dortmund mit Zuschuss | IMPOLA",
     "Bodengleiche Dusche, Haltegriffe, unterfahrbarer Waschtisch: barrierefreier Badumbau in Dortmund. Bis zu 4.180 € Zuschuss möglich – wir helfen beim Antrag.",
     "badumbau.html", bad_body, faq_schema_bad, og="og-badumbau")

# ------------------------------------------------------------------ Sanierung & Umbau
san_body = seitenkopf("Sanierung & Umbau", "Sanierung und Umbau aus einer Hand",
    "Ob eine Wohnung nach dem Auszug, ein älteres Haus oder ein neuer Grundriss: Wir koordinieren alle Arbeiten, damit Sie nicht jedes Gewerk einzeln beauftragen müssen.",
    ph("karte-sanierung", "Frisch sanierte, helle Altbauwohnung mit Parkett und Stuckdecke", 1200, 900, lazy=False), anliegen="sanierung") + f'''
<section class="abschnitt" aria-labelledby="san-titel">
  <div class="wrap zweispaltig oben">
    <div>
      <h2 id="san-titel">Komplettsanierung</h2>
      <p>Wir erneuern Wohnungen und Häuser von Grund auf – Böden, Wände, Decken, Bad und Küche. Sie erhalten einen Zeitplan und ein Angebot für das ganze Vorhaben.</p>
      <ul class="haken">
        <li>Rückbau und Entsorgung</li>
        <li>Trockenbau, Putz- und Malerarbeiten</li>
        <li>Bodenbeläge</li>
        <li>Bad- und Küchenerneuerung</li>
        <li>Koordination von Elektro, Sanitär und Heizung über Fachbetriebe</li>
      </ul>
    </div>
    <div id="umbau">
      <h2>Umbau</h2>
      <p>Räume neu aufteilen, Wände setzen oder entfernen, Wohnungen an neue Lebenssituationen anpassen – auch altersgerecht und barrierefrei.</p>
      <div class="bild-rund">{ph("karte-umbau", "Handwerker montiert eine Trockenbauwand", 1200, 900)}</div>
    </div>
  </div>
</section>
<section class="abschnitt" aria-labelledby="fach-titel">
  <div class="wrap">
    <div class="infobox">
      <h2 id="fach-titel" style="font-size:1.4rem">Wer macht was?</h2>
      <p>Wir planen, koordinieren und übernehmen Vorbereitung, Rückbau und Trockenbau. Arbeiten, für die das Handwerksrecht einen Meisterbetrieb vorschreibt – etwa Fliesen, Abdichtung, Sanitär oder Elektro – führen eingetragene Fachbetriebe aus unserem Partnernetzwerk aus. Für Sie bleibt es trotzdem ein Ansprechpartner.</p>
    </div>
  </div>
</section>
<section class="abschnitt" aria-labelledby="ablauf-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="ablauf-titel">So läuft Ihre Sanierung ab</h2></div>
    {ABLAUF_SAN}
  </div>
</section>
{cta(anliegen="sanierung")}
'''
page("sanierung", "Sanierung & Umbau in Dortmund – koordiniert aus einer Hand | IMPOLA",
     "Komplettsanierung und Umbau von Wohnungen und Häusern in Dortmund und im Ruhrgebiet. Alle Gewerke koordiniert, ein fester Ansprechpartner.",
     "sanierung.html", san_body, og="og-sanierung")

# ------------------------------------------------------------------ Objektservice
obj_body = seitenkopf("Objektservice", "Objektservice für Wohnhäuser",
    "Für Eigentümer und Hausverwaltungen: Wir kümmern uns um Kleinreparaturen, Instandhaltung und die Pflege rund ums Objekt – zuverlässig und dokumentiert.",
    ph("karte-objektservice", "Gepflegtes Mehrfamilienhaus aus Klinker", 800, 600, lazy=False), anliegen="objektservice") + f'''
<section class="abschnitt" aria-labelledby="obj-titel">
  <div class="wrap zweispaltig oben">
    <div>
      <h2 id="obj-titel">Was wir übernehmen</h2>
      <ul class="haken">
        <li>Kleinreparaturen in Wohnungen und Gemeinschaftsflächen</li>
        <li>Instandhaltung und Wohnungsrenovierung bei Mieterwechsel</li>
        <li>Regelmäßige Objektbegehungen</li>
        <li>Koordination von Fachbetrieben bei größeren Schäden</li>
      </ul>
      <!-- Leistungsliste mit Tim/Dennis abstimmen: nur aufführen, was tatsächlich angeboten wird (z. B. Grünpflege, Winterdienst, Treppenhausreinigung). -->
    </div>
    <div>
      <h2>Für Hausverwaltungen</h2>
      <p>Ein Ansprechpartner für viele Aufgaben, kurze Reaktionszeiten und nachvollziehbare Abrechnung. Sprechen Sie uns auf eine feste Zusammenarbeit an.</p>
      <a class="btn btn-sekundaer" href="kontakt.html?anliegen=b2b">Zusammenarbeit anfragen</a>
    </div>
  </div>
</section>
{cta(anliegen="objektservice")}
'''
page("objektservice", "Objektservice in Dortmund für Eigentümer & Hausverwaltungen | IMPOLA",
     "Kleinreparaturen, Instandhaltung und Pflege rund ums Objekt in Dortmund und im Ruhrgebiet – für Eigentümer und Hausverwaltungen.",
     "objektservice.html", obj_body, og="og-objektservice")

# ------------------------------------------------------------------ Verwaltung (in Vorbereitung)
verw_body = seitenkopf("Immobilienverwaltung", "Immobilien&shy;verwaltung – in Vorbereitung",
    "Verwaltung und Handwerk aus einer Hand: Wir bauen eine Immobilienverwaltung auf, bei der kaputte Haustüren nicht wochenlang auf einen Handwerker warten.",
    ph("karte-verwaltung", "Schlüsselbund und Aktenordner auf einem Schreibtisch", 800, 600, lazy=False), aktionen=False) + f'''
<section class="abschnitt">
  <div class="wrap">
    <!-- WICHTIG: Keine Mandate, keine Preise, kein Anfrageformular, bis die Erlaubnis nach § 34c GewO erteilt ist. -->
    <div class="infobox status">
      <p><strong>Stand:</strong> Wir nehmen derzeit noch keine Verwaltungsmandate an. Wir starten, sobald die gewerberechtliche Erlaubnis nach § 34c GewO und die nötigen Versicherungen vorliegen.</p>
    </div>
  </div>
</section>
<section class="abschnitt" aria-labelledby="geplant-titel">
  <div class="wrap">
    <div class="kopf">
      <h2 id="geplant-titel">Was wir vorbereiten</h2>
      <p class="einleitung">Für Eigentümer in Dortmund und im Ruhrgebiet, die eine Verwaltung suchen, die selbst anpacken kann.</p>
    </div>
    <div class="karten3">
      <div class="karte"><h3>Mietverwaltung</h3><p>Mieterwechsel, Nebenkostenabrechnung, Mietzahlungen, Kommunikation mit Mietern – für einzelne Wohnungen und ganze Häuser.</p></div>
      <div class="karte"><h3>WEG-Verwaltung</h3><p>Eigentümerversammlungen, Wirtschaftsplan, Jahresabrechnung und Beschlussumsetzung nach dem Wohnungseigentumsgesetz.</p></div>
      <div class="karte"><h3>Sonder&shy;eigentums&shy;verwaltung</h3><p>Für Kapitalanleger mit einzelnen Eigentumswohnungen: Wir kümmern uns um Mieter, Abrechnung und Instandhaltung Ihrer Einheit.</p></div>
    </div>
  </div>
</section>
<section class="abschnitt" aria-labelledby="anders-titel">
  <div class="wrap zweispaltig oben">
    <div>
      <h2 id="anders-titel">Was uns unterscheiden soll</h2>
      <p>Viele Verwaltungen verwalten nur – für jede Reparatur wird ein Fremdbetrieb gesucht. Bei uns sitzen Verwaltung, Objektservice und Sanierung unter einem Dach.</p>
    </div>
    <ul class="argumente">
      <li><strong>Kurze Wege bei Schäden</strong>Kleinreparaturen erledigt unser Objektservice direkt, größere Arbeiten koordinieren wir mit unseren Meisterpartnern.</li>
      <li><strong>Instandhaltung mit Plan</strong>Regelmäßige Begehungen, dokumentierter Zustand und eine vorausschauende Planung für Rücklagen.</li>
      <li><strong>Nachvollziehbar</strong>Klare Abrechnung, feste Ansprechpartner und erreichbare Zeiten.</li>
    </ul>
  </div>
</section>
<section class="abschnitt">
  <div class="wrap">
    <div class="infobox">
      <h2 style="font-size:1.4rem">Interesse?</h2>
      <p>Schreiben Sie uns eine kurze E-Mail, wenn wir Sie zum Start informieren sollen: <a href="mailto:{MAIL}?subject=Immobilienverwaltung%20%E2%80%93%20bitte%20zum%20Start%20informieren">{MAIL}</a>. Unsere Leistungen rund um <a href="sanierung.html">Sanierung</a>, <a href="badumbau.html">Badumbau</a> und <a href="objektservice.html">Objektservice</a> stehen Eigentümern und Hausverwaltungen schon heute zur Verfügung.</p>
    </div>
  </div>
</section>
'''
page("verwaltung", "Immobilienverwaltung – in Vorbereitung | IMPOLA",
     "IMPOLA bereitet Mietverwaltung, WEG-Verwaltung und Sondereigentumsverwaltung in Dortmund vor – Verwaltung und Handwerk aus einer Hand.", "", verw_body,
     '<meta name="robots" content="noindex, follow">\n', og="og-verwaltung")

# ------------------------------------------------------------------ Über uns
ueber_body = seitenkopf("Über uns", "Wer hinter IMPOLA steht",
    "Wir sind ein Dortmunder Unternehmen für Sanierung, Umbau und Objektservice. Unser Anspruch: Sie haben einen Ansprechpartner, der sich um alles kümmert.",
    ph("ueber-uns", "Grundriss, Zollstock und Materialmuster auf einem Planungstisch", 1200, 900, lazy=False), aktionen=False) + f'''
<section class="abschnitt" aria-labelledby="team-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="team-titel">Ihre Ansprechpartner</h2></div>
    <div class="ansprech">
      <div class="ansprech-karte">
        <h3>Tim Pomian</h3>
        <p class="rolle">Projektleitung vor Ort</p>
        <p>Ihr Ansprechpartner auf der Baustelle – vom ersten Termin bis zur Übergabe.</p>
      </div>
      <div class="ansprech-karte">
        <h3>Dennis Lasch</h3>
        <p class="rolle">Geschäftsführung</p>
        <p>Verantwortet Angebote, Verträge und Organisation im Hintergrund.</p>
      </div>
      <div class="ansprech-kontakt">
        <h3>So erreichen Sie uns</h3>
        <ul>
          <li><span class="leise">Telefon</span><a href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a><br><span class="leise">Mo–Fr, 8–18 Uhr</span></li>
          <li><span class="leise">E-Mail</span><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li><span class="leise">Anschrift</span>Schillstr. 6, 44339 Dortmund</li>
        </ul>
        <a class="btn btn-primaer" href="kontakt.html">Beratung anfragen</a>
      </div>
    </div>
  </div>
</section>
<section class="abschnitt" aria-labelledby="arbeit-titel">
  <div class="wrap zweispaltig oben">
    <div>
      <h2 id="arbeit-titel">Wie wir arbeiten</h2>
      <p>Wir verstehen uns als Generalunternehmer: Wir planen, koordinieren und stehen gegenüber unseren Kunden für das Ergebnis ein. Die einzelnen Gewerke führen wir selbst oder über geprüfte Partnerbetriebe aus – meisterpflichtige Arbeiten ausschließlich durch eingetragene Meisterbetriebe.</p>
    </div>
    <div>
      <h2>Unser Partnernetzwerk</h2>
      <p>Wir arbeiten mit Handwerksbetrieben aus Dortmund und dem Ruhrgebiet zusammen, die wir persönlich kennen. Sie sind Handwerker und möchten dazugehören?</p>
      <a class="btn btn-sekundaer" href="partner-werden.html">Partner werden</a>
    </div>
  </div>
</section>
{cta()}
'''
page("ueber-uns", "Über uns – IMPOLA aus Dortmund",
     "IMPOLA aus Dortmund: Sanierung, Umbau und Objektservice aus einer Hand. Lernen Sie Ihre Ansprechpartner kennen.",
     "ueber-uns.html", ueber_body, og="og-ueber-uns")

# ------------------------------------------------------------------ Partner werden
partner_body = seitenkopf("Partner werden", "Für Handwerksbetriebe: Partner werden",
    "Wir suchen zuverlässige Betriebe aus Dortmund und dem Ruhrgebiet für Badumbau, Sanierung und Umbau. Sie konzentrieren sich aufs Handwerk – wir kümmern uns um Kunden und Organisation.",
    ph("partner-werden", "Zwei Handwerker geben sich auf einer Baustelle die Hand", 1200, 900, lazy=False), anliegen="partner") + '''
<section class="abschnitt">
  <div class="wrap zweispaltig oben">
    <div>
      <h2>Was Sie von uns erwarten können</h2>
      <ul class="haken">
        <li>Planbare Aufträge mit klarer Leistungsbeschreibung</li>
        <li>Ein fester Ansprechpartner auf unserer Seite</li>
        <li>Schriftlicher Rahmenvertrag und Projektvertrag</li>
        <li>Pünktliche Zahlung nach Abnahme</li>
      </ul>
    </div>
    <div>
      <h2>Was wir von Ihnen brauchen</h2>
      <ul class="haken">
        <li>Gewerbeanmeldung, bei meisterpflichtigen Gewerken Eintrag in die Handwerksrolle</li>
        <li>Betriebshaftpflichtversicherung</li>
        <li>Freistellungsbescheinigung nach § 48b EStG</li>
        <li>Unbedenklichkeitsbescheinigungen, z. B. SOKA-BAU und Berufsgenossenschaft, soweit zutreffend</li>
        <li>Termintreue und saubere Arbeit beim Kunden</li>
      </ul>
    </div>
  </div>
</section>
'''+ cta("Lernen wir uns kennen.", "Erzählen Sie uns kurz, welches Gewerk Sie abdecken und in welchem Gebiet Sie arbeiten.", "partner")
page("partner-werden", "Partner werden – Handwerksbetriebe im Ruhrgebiet | IMPOLA",
     "Handwerksbetriebe aus Dortmund und dem Ruhrgebiet: Werden Sie Partner von IMPOLA für Badumbau, Sanierung und Umbau.",
     "", partner_body, og="og-partner")

# ------------------------------------------------------------------ Kontakt
kontakt_body = seitenkopf("Kontakt", "Beratung anfragen",
    "Schreiben Sie uns kurz, worum es geht. Wir rufen Sie innerhalb von zwei Werktagen zurück und vereinbaren einen kostenlosen Termin vor Ort.",
    None, aktionen=False) + f'''
<section class="abschnitt">
  <div class="wrap zweispaltig oben">
    <form class="formular" action="/api/kontakt" method="post" novalidate>
      <p class="meldung fehler" id="formular-fehler" hidden role="alert">Die Nachricht wurde nicht gesendet. Bitte füllen Sie Name und Telefonnummer aus und versuchen Sie es erneut – oder rufen Sie uns an.</p>
      <div class="feldgruppe">
        <div class="feld"><label for="name">Ihr Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
        <div class="feld"><label for="telefon">Telefonnummer</label><input id="telefon" name="telefon" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="feldgruppe">
        <div class="feld"><label for="email">E-Mail <span class="optional">(optional)</span></label><input id="email" name="email" type="email" autocomplete="email"></div>
        <div class="feld"><label for="plz">Postleitzahl <span class="optional">(optional)</span></label><input id="plz" name="plz" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="5"></div>
      </div>
      <div class="feld">
        <label for="anliegen">Worum geht es?</label>
        <select id="anliegen" name="anliegen">
          <option value="badumbau">Barrierefreier Badumbau</option>
          <option value="sanierung">Sanierung oder Umbau</option>
          <option value="objektservice">Objektservice</option>
          <option value="b2b">Zusammenarbeit (Pflegedienst, Hausverwaltung)</option>
          <option value="partner">Partner werden (Handwerksbetrieb)</option>
          <option value="sonstiges">Etwas anderes</option>
        </select>
      </div>
      <div class="feld">
        <label for="nachricht">Ihre Nachricht <span class="optional">(optional)</span></label>
        <textarea id="nachricht" name="nachricht" aria-describedby="nachricht-hilfe"></textarea>
        <p class="hilfe" id="nachricht-hilfe">Bitte keine Angaben zu Gesundheit oder Pflegegrad – das besprechen wir persönlich.</p>
      </div>
      <div class="hp" aria-hidden="true"><label for="website">Bitte leer lassen</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
      <input type="hidden" name="ts" id="ts" value="">
      <p class="kleingedruckt">Wir verwenden Ihre Angaben nur, um Ihre Anfrage zu bearbeiten. Mehr dazu in unserer <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
      <div><button class="btn btn-primaer" type="submit">Anfrage senden</button></div>
    </form>
    <aside class="kontaktdaten" aria-label="Kontaktdaten">
      <dl>
        <dt>Telefon</dt><dd><a href="tel:{TEL_LINK}">{TEL_ANZEIGE}</a><br><span class="leise">Montag bis Freitag, 8 bis 18 Uhr</span></dd>
        <dt>E-Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd>
        <dt>Anschrift</dt><dd>{FIRMA}<br>Schillstr. 6<br>44339 Dortmund</dd>
        <dt>Einsatzgebiet</dt><dd>Dortmund und Ruhrgebiet</dd>
      </dl>
      <div class="kontakt-bild">{ph("kontakt-termin", "Aufmaß im Bad beim kostenlosen Termin vor Ort", 1200, 900)}</div>
    </aside>
  </div>
</section>
'''
page("kontakt", "Kontakt – Beratung anfragen | IMPOLA Dortmund",
     "Kostenlose Beratung zu Badumbau, Sanierung und Objektservice in Dortmund. Rufen Sie an oder schreiben Sie uns.",
     "kontakt.html", kontakt_body, og="og-kontakt")

# ------------------------------------------------------------------ Danke
danke_body = seitenkopf("Anfrage gesendet", "Danke, Ihre Anfrage ist bei uns angekommen.",
    "Wir melden uns innerhalb von zwei Werktagen telefonisch bei Ihnen. Eilt es? Dann rufen Sie uns direkt an.", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap"><a class="btn btn-sekundaer" href="tel:{TEL_LINK}">{TEL_ANZEIGE} anrufen</a> &nbsp; <a href="index.html">Zur Startseite</a></div></section>
'''
page("danke", "Anfrage gesendet | IMPOLA", "Ihre Anfrage ist bei IMPOLA angekommen.", "", danke_body,
     '<meta name="robots" content="noindex">\n')

# ------------------------------------------------------------------ 404
nf_body = seitenkopf("Seite nicht gefunden", "Diese Seite gibt es nicht.",
    "Vielleicht hat sich die Adresse geändert. Von der Startseite aus finden Sie alle Leistungen.", None, aktionen=False) + '''
<section class="abschnitt"><div class="wrap"><a class="btn btn-primaer" href="/">Zur Startseite</a></div></section>
'''
page("404", "Seite nicht gefunden | IMPOLA", "Seite nicht gefunden.", "", nf_body, '<meta name="robots" content="noindex">\n')

# ------------------------------------------------------------------ Impressum
impressum_body = seitenkopf("Impressum", "Impressum", "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap rechtstext">
  <p><strong>{FIRMA}</strong><br>Schillstr. 6<br>44339 Dortmund</p>
  <h2>Vertreten durch</h2>
  <p>Geschäftsführer: Dennis Lasch</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{TEL_LINK}">+49 178 9176594</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <h2>Registereintrag</h2>
  <p>Die Eintragung in das Handelsregister folgt. Registergericht und Registernummer ergänzen wir nach der Eintragung.</p>
  <!-- Nach Eintragung ersetzen durch: Registergericht: Amtsgericht Dortmund · Registernummer: HRB ….. und in build.py bei FIRMA " i. G." entfernen. -->
  <h2>Umsatzsteuer-Identifikationsnummer</h2>
  <p>Die Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG ergänzen wir nach Erteilung.</p>
  <!-- Falls IMPOLA in die Handwerksrolle / das Verzeichnis zulassungsfreier Gewerbe eingetragen wird: Zuständige Kammer (Handwerkskammer Dortmund, Ardeystraße 93, 44139 Dortmund) und Berufsbezeichnung hier ergänzen. -->
  <h2>Verbraucherstreitbeilegung</h2>
  <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
  <h2>Haftung für Inhalte und Links</h2>
  <p>Wir erstellen die Inhalte dieser Website mit Sorgfalt. Angaben zu Förderungen, etwa zum Zuschuss der Pflegekasse, sind allgemeine Informationen und ersetzen keine Einzelfallprüfung durch die zuständige Stelle. Für Inhalte verlinkter fremder Websites sind ausschließlich deren Betreiber verantwortlich.</p>
</div></section>
'''
page("impressum", "Impressum | IMPOLA", "Impressum der IMPOLA UG (haftungsbeschränkt), Dortmund.", "", impressum_body,
     '<meta name="robots" content="noindex, follow">\n')

# ------------------------------------------------------------------ Datenschutz
# Entwurf, zuletzt angepasst: Hosting Vercel, Formular per E-Mail, Postfach Zoom Mail, Videoberatung Zoom,
# Handwerkersoftware „das programm“. Vor Freigabe prüfen (Anwalt/Datenschutzgenerator) – siehe Kommentare.
ds_body = seitenkopf("Datenschutz", "Datenschutz&shy;erklärung", "Wie wir mit Ihren Daten umgehen – verständlich erklärt.", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap rechtstext">
  <h2>1. Verantwortlicher</h2>
  <p>{FIRMA}<br>Schillstr. 6, 44339 Dortmund<br>Vertreten durch den Geschäftsführer Dennis Lasch<br>Telefon: +49 178 9176594<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <p>Ein Datenschutzbeauftragter ist bei uns gesetzlich nicht vorgeschrieben. Bei Fragen zum Datenschutz wenden Sie sich direkt an die oben genannte Adresse.</p>

  <h2>2. Das Wichtigste in Kürze</h2>
  <ul>
    <li>Wir setzen auf dieser Website <strong>keine Cookies</strong>, kein Tracking, keine Analyse-Tools und keine Werbe- oder Social-Media-Dienste ein.</li>
    <li>Schriftarten liegen auf unserem eigenen Server. Beim Aufruf werden keine Daten an Schriftanbieter übertragen.</li>
    <li>Der Zuschuss-Check läuft nur in Ihrem Browser. Ihre Antworten werden weder gespeichert noch an uns übertragen.</li>
    <li>Daten, die Sie uns über das Kontaktformular, per E-Mail oder Telefon geben, nutzen wir nur, um Ihre Anfrage und Ihren Auftrag zu bearbeiten.</li>
  </ul>

  <h2>3. Hosting und Server-Logfiles</h2>
  <p>Diese Website wird bei Vercel Inc., 440 N Barranca Avenue #4133, Covina, CA 91723, USA, gehostet. Beim Aufruf einer Seite verarbeitet der Server technisch notwendige Daten: IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Referrer-URL, Browser und Betriebssystem sowie übertragene Datenmenge. Das ist nötig, um die Website auszuliefern und gegen Angriffe abzusichern.</p>
  <p>Rechtsgrundlage ist unser berechtigtes Interesse an einem sicheren und stabilen Betrieb (Art. 6 Abs. 1 lit. f DSGVO). Mit Vercel besteht ein Vertrag zur Auftragsverarbeitung (Art. 28 DSGVO). Für die Übermittlung in die USA gelten die EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO), die Bestandteil dieses Vertrags sind. Logdaten werden nur kurzfristig gespeichert und anschließend gelöscht.</p>
  <!-- PRÜFEN: Speicherdauer der Logs laut aktuellem Vercel-DPA; ob Vercel zusätzlich unter dem EU-US Data Privacy Framework zertifiziert ist. -->

  <h2>4. Verschlüsselung</h2>
  <p>Die Website nutzt aus Sicherheitsgründen eine TLS-Verschlüsselung. Sie erkennen sie am Schloss-Symbol und an „https://“ in der Adresszeile.</p>

  <h2>5. Kontaktformular</h2>
  <p>Wenn Sie uns über das Formular schreiben, verarbeiten wir Ihren Namen, Ihre Telefonnummer, Ihr Anliegen und – falls angegeben – E-Mail-Adresse, Postleitzahl und Nachricht. Zusätzlich wird ein Zeitstempel übertragen, mit dem wir automatisierte Spam-Einsendungen erkennen.</p>
  <p>Die Angaben werden über eine Serverfunktion unseres Hosters verarbeitet und als E-Mail an {MAIL} gesendet. Auf dem Webserver selbst werden sie nicht gespeichert. Haben Sie eine E-Mail-Adresse angegeben, schicken wir Ihnen eine automatische Eingangsbestätigung.</p>
  <p>Rechtsgrundlage ist die Durchführung vorvertraglicher Maßnahmen auf Ihre Anfrage (Art. 6 Abs. 1 lit. b DSGVO), bei sonstigen Anfragen unser berechtigtes Interesse an deren Beantwortung (Art. 6 Abs. 1 lit. f DSGVO). Name und Telefonnummer brauchen wir, um Sie zurückrufen zu können; ohne diese Angaben können wir die Anfrage über das Formular nicht bearbeiten.</p>
  <p>Bitte machen Sie im Formular keine Angaben zu Ihrer Gesundheit oder einem Pflegegrad. Das besprechen wir persönlich.</p>

  <h2>6. E-Mail und Telefon</h2>
  <p>Wenn Sie uns anrufen oder eine E-Mail schreiben, verarbeiten wir die mitgeteilten Daten zur Bearbeitung Ihres Anliegens (Art. 6 Abs. 1 lit. b bzw. f DSGVO). Unser E-Mail-Postfach wird bei Zoom Communications, Inc., 55 Almaden Boulevard, 6th Floor, San Jose, CA 95113, USA, betrieben (Zoom Mail). Mit Zoom besteht ein Vertrag zur Auftragsverarbeitung. Die Übermittlung in die USA erfolgt auf Grundlage des Angemessenheitsbeschlusses der EU-Kommission zum EU-US Data Privacy Framework, ergänzend auf Grundlage der EU-Standardvertragsklauseln.</p>
  <!-- PRÜFEN: Über welchen SMTP-Server versendet das Formular (Umgebungsvariable SMTP_HOST in Vercel)? Ist es nicht Zoom, sondern z. B. Google Workspace, hier zusätzlich nennen: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. -->

  <h2>7. Videoberatung mit Zoom</h2>
  <p>Auf Wunsch beraten wir Sie per Video. Dafür nutzen wir Zoom, ebenfalls ein Dienst der Zoom Communications, Inc. Verarbeitet werden dabei Name und E-Mail-Adresse, Bild- und Tondaten während des Gesprächs, Meeting-Metadaten (Datum, Uhrzeit, Dauer) sowie technische Verbindungsdaten wie die IP-Adresse. Gespräche zeichnen wir nicht auf.</p>
  <p>Rechtsgrundlage ist die Durchführung vorvertraglicher Maßnahmen bzw. des Vertrags (Art. 6 Abs. 1 lit. b DSGVO). Für die Übermittlung in die USA gelten die unter Ziffer 6 genannten Grundlagen. Sie können eine Videoberatung jederzeit ablehnen – wir beraten Sie dann telefonisch oder vor Ort.</p>

  <h2>8. Angebote, Aufträge und Rechnungen</h2>
  <p>Für Kundenverwaltung, Angebote, Auftragsplanung und Rechnungen nutzen wir die cloudbasierte Handwerkersoftware „das programm“. Dort verarbeiten wir die für Ihren Auftrag nötigen Daten: Name, Anschrift, Kontaktdaten, Objektadresse, Aufmaße, Fotos vom Objekt, Angebote, Rechnungen und Zahlungsinformationen. Mit dem Anbieter besteht ein Vertrag zur Auftragsverarbeitung (Art. 28 DSGVO).</p>
  <!-- PRÜFEN: Anbieter, Anschrift und Serverstandort von „das programm“ laut AVV hier eintragen. -->
  <p>Rechtsgrundlage ist die Erfüllung des Vertrags (Art. 6 Abs. 1 lit. b DSGVO) sowie die Erfüllung gesetzlicher Aufbewahrungspflichten (Art. 6 Abs. 1 lit. c DSGVO).</p>

  <h2>9. Angaben zu Pflegegrad und Gesundheit</h2>
  <p>Für einen Zuschuss der Pflegekasse kann es nötig sein, dass wir Angaben zu einem Pflegegrad kennen, etwa um ein passendes Angebot für den Förderantrag zu erstellen. Diese Angaben sind Gesundheitsdaten. Wir verarbeiten sie nur mit Ihrer ausdrücklichen Einwilligung (Art. 9 Abs. 2 lit. a DSGVO) und nur für diesen Zweck. Sie können die Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen.</p>

  <h2>10. Kundenstimmen</h2>
  <p>Rückmeldungen von Kunden veröffentlichen wir nur mit deren ausdrücklicher Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) – mit Vornamen, Stadtteil und Art des Projekts. Die Einwilligung kann jederzeit widerrufen werden; wir entfernen die Stimme dann von der Website.</p>

  <h2>11. Empfänger</h2>
  <p>Ihre Daten erhalten nur, wer sie für die genannten Zwecke braucht: unsere Dienstleister für Hosting, E-Mail, Videoberatung und Auftragssoftware (jeweils als Auftragsverarbeiter), die Fachbetriebe aus unserem Partnernetzwerk, soweit sie Arbeiten bei Ihnen ausführen (Art. 6 Abs. 1 lit. b DSGVO), unser Steuerberater sowie Behörden, wenn wir gesetzlich dazu verpflichtet sind. An Ihre Pflegekasse geben wir nur Unterlagen weiter, wenn Sie das wünschen.</p>

  <h2>12. Speicherdauer</h2>
  <p>Anfragen, aus denen kein Auftrag entsteht, löschen wir spätestens sechs Monate nach dem letzten Kontakt. Auftragsunterlagen bewahren wir so lange auf, wie es das Handels- und Steuerrecht verlangt: Rechnungen und Buchungsbelege acht Jahre, Handels- und Geschäftsbriefe sechs Jahre, Jahresabschlüsse zehn Jahre (§ 257 HGB, § 147 AO). Danach werden die Daten gelöscht.</p>

  <h2>13. Ihre Rechte</h2>
  <p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18) und Datenübertragbarkeit (Art. 20). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen (Art. 7 Abs. 3 DSGVO). Eine formlose Nachricht an {MAIL} genügt.</p>
  <div class="infobox"><p><strong>Widerspruchsrecht (Art. 21 DSGVO):</strong> Soweit wir Daten auf Grundlage berechtigter Interessen verarbeiten (Art. 6 Abs. 1 lit. f DSGVO), können Sie dieser Verarbeitung aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit widersprechen.</p></div>
  <p>Sie können sich außerdem bei einer Datenschutz-Aufsichtsbehörde beschweren. Für uns zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen, Kavalleriestraße 2–4, 40213 Düsseldorf, <a href="https://www.ldi.nrw.de" rel="noopener">www.ldi.nrw.de</a>.</p>

  <h2>14. Keine automatisierten Entscheidungen</h2>
  <p>Wir treffen keine Entscheidungen, die ausschließlich auf einer automatisierten Verarbeitung beruhen (Art. 22 DSGVO). Auch der Zuschuss-Check ist nur eine unverbindliche Orientierung.</p>

  <p class="leise">Stand: {STAND}</p>
</div></section>
'''
page("datenschutz", "Datenschutzerklärung | IMPOLA", "Datenschutzerklärung der IMPOLA UG (haftungsbeschränkt): Hosting, Kontaktformular, E-Mail, Videoberatung und Ihre Rechte.", "", ds_body)

# ------------------------------------------------------------------ Widerrufsbelehrung
# Muster nach Anlage 1 zu Art. 246a § 1 Abs. 2 EGBGB (Dienstleistungen/Werkleistungen) und Anlage 2 (Formular).
# Vor Verwendung in Angeboten anwaltlich prüfen lassen – insbesondere bei Werkverträgen mit Materiallieferung.
widerruf_body = seitenkopf("Widerrufsbelehrung", "Widerrufs&shy;belehrung",
    "Für Verbraucher, die einen Vertrag mit uns außerhalb unserer Geschäftsräume – etwa beim Termin bei Ihnen zu Hause – oder ausschließlich per Telefon oder E-Mail schließen.", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap rechtstext">
  <h2>Widerrufsrecht</h2>
  <p>Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen.</p>
  <p>Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsabschlusses.</p>
  <p>Um Ihr Widerrufsrecht auszuüben, müssen Sie uns ({FIRMA}, Schillstr. 6, 44339 Dortmund, Telefon: +49 178 9176594, E-Mail: {MAIL}) mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief oder eine E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren. Sie können dafür das unten stehende Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.</p>
  <p>Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.</p>
  <h2>Folgen des Widerrufs</h2>
  <p>Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der zusätzlichen Kosten, die sich daraus ergeben, dass Sie eine andere Art der Lieferung als die von uns angebotene, günstigste Standardlieferung gewählt haben), unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung Entgelte berechnet.</p>
  <p>Haben Sie verlangt, dass die Dienstleistungen während der Widerrufsfrist beginnen sollen, so haben Sie uns einen angemessenen Betrag zu zahlen, der dem Anteil der bis zu dem Zeitpunkt, zu dem Sie uns von der Ausübung des Widerrufsrechts hinsichtlich dieses Vertrags unterrichten, bereits erbrachten Dienstleistungen im Vergleich zum Gesamtumfang der im Vertrag vorgesehenen Dienstleistungen entspricht.</p>

  <div class="infobox">
    <h3 style="margin-top:0">Gut zu wissen: früher anfangen</h3>
    <p>Soll der Umbau schon innerhalb der vierzehn Tage beginnen, bestätigen Sie uns das bitte ausdrücklich und schriftlich. Ihr Widerrufsrecht bleibt bestehen, bis die Arbeiten vollständig erbracht sind. Bei einem Widerruf zahlen Sie dann den Anteil, der bis dahin geleistet wurde.</p>
  </div>

  <h2 id="formular">Muster-Widerrufsformular</h2>
  <p>Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses Formular aus und senden Sie es zurück.</p>
  <div class="formularmuster">
    <p>An {FIRMA}, Schillstr. 6, 44339 Dortmund, E-Mail: {MAIL}</p>
    <p>Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag über den Kauf der folgenden Waren (*)/die Erbringung der folgenden Dienstleistung (*)</p>
    <p class="linie">&nbsp;</p>
    <p>Bestellt am (*)/erhalten am (*)</p>
    <p class="linie">&nbsp;</p>
    <p>Name des/der Verbraucher(s)</p>
    <p class="linie">&nbsp;</p>
    <p>Anschrift des/der Verbraucher(s)</p>
    <p class="linie">&nbsp;</p>
    <p>Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier)</p>
    <p class="linie">&nbsp;</p>
    <p>Datum</p>
    <p class="linie">&nbsp;</p>
    <p class="kleingedruckt">(*) Unzutreffendes streichen.</p>
  </div>
  <p class="leise">Stand: {STAND}</p>
</div></section>
'''
page("widerruf", "Widerrufsbelehrung | IMPOLA", "Widerrufsbelehrung und Muster-Widerrufsformular der IMPOLA für Verbraucher.", "", widerruf_body,
     '<meta name="robots" content="noindex, follow">\n')

# ------------------------------------------------------------------ Sitemap & robots
HEUTE = datetime.date.today().isoformat()
SITEMAP = ["", "badumbau", "sanierung", "objektservice", "ueber-uns", "partner-werden", "kontakt", "datenschutz"]
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in SITEMAP:
        f.write(f"  <url><loc>{DOMAIN}/{u}</loc><lastmod>{HEUTE}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {DOMAIN}/sitemap.xml\n")

print("Seiten erzeugt.")

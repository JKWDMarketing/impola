#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten für impola.de (gemeinsamer Header/Footer)."""
import json, os

OUT = "public_html"
DOMAIN = "https://impola.de"
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


def head(title, desc, slug, extra=""):
    canon = DOMAIN + ("/" if slug == "index" else f"/{slug}")
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="IMPOLA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/img/og-image.jpg">
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
          <li><a href="verwaltung.html">Immobilienverwaltung</a></li>
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
      <span>© <span id="jahr">2026</span> IMPOLA UG (haftungsbeschränkt)</span>
      <span><a href="impressum.html">Impressum</a> &nbsp; <a href="datenschutz.html">Datenschutz</a></span>
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


def page(slug, title, desc, aktiv, body, extra=""):
    html = head(title, desc, slug, extra) + header(aktiv) + body + FOOTER
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

# ------------------------------------------------------------------ Startseite
faq_rows, faq_schema = faq(FAQ_BAD[:5])
localbusiness = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "name": "IMPOLA UG (haftungsbeschränkt)", "url": DOMAIN + "/",
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
        {ph("karte-sanierung", "Frisch sanierte, helle Altbauwohnung", 800, 600)}
        <div class="leistung-text"><h3>Sanierung komplett</h3><p>Wohnungen und Häuser von Grund auf erneuern – koordiniert aus einer Hand.</p></div>
      </a>
      <a class="leistung" href="sanierung.html#umbau">
        {ph("karte-umbau", "Handwerker montiert eine Trockenbauwand", 800, 600)}
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

<section class="abschnitt" aria-labelledby="ref-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="ref-titel">Stimmen unserer Kunden</h2></div>
    <!-- PLATZHALTER: Nur echte, schriftlich freigegebene Kundenstimmen einsetzen (UWG). Bis dahin bleibt dieser Hinweis stehen. -->
    <div class="leer"><p>Hier zeigen wir bald Rückmeldungen aus unseren ersten Projekten – echte Stimmen, mit Einverständnis unserer Kunden.</p></div>
  </div>
</section>

<section class="abschnitt" aria-labelledby="faq-titel">
  <div class="wrap">
    <div class="kopf"><h2 id="faq-titel">Häufige Fragen</h2></div>
    <div class="faq">{faq_rows}</div>
  </div>
</section>

{cta()}
'''
page("index", "IMPOLA – Barrierefreier Badumbau, Sanierung & Objektservice in Dortmund",
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
        <span class="vn-kennzeichnung">Beispielvisualisierung</span>
        <span class="vn-linie" aria-hidden="true"><span class="vn-griff"></span></span>
        <input class="vn-regler" type="range" min="0" max="100" value="50" step="1" aria-label="Vergleich: nach links für nachher, nach rechts für vorher">
      </div>
      <figcaption>
        <p class="vn-text">Die Wanne mit hohem Rand kommt raus, eine flache Duschtasse mit Glastür, fugenarmer Wandverkleidung und Haltegriff kommt rein. Der Rest des Bades bleibt, wie er ist – das spart Zeit und Kosten.</p>
        <p class="kleingedruckt">Die Bilder sind computergenerierte Beispiele zur Veranschaulichung, kein Kundenprojekt. Echte Vorher-nachher-Fotos aus unseren Projekten folgen.</p>
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
page("badumbau", "Barrierefreier Badumbau in Dortmund – Zuschuss der Pflegekasse | IMPOLA",
     "Bodengleiche Dusche, Haltegriffe, unterfahrbarer Waschtisch: barrierefreier Badumbau in Dortmund. Bis zu 4.180 € Zuschuss der Pflegekasse möglich – wir helfen beim Antrag.",
     "badumbau.html", bad_body, faq_schema_bad)

# ------------------------------------------------------------------ Sanierung & Umbau
san_body = seitenkopf("Sanierung & Umbau", "Sanierung und Umbau aus einer Hand",
    "Ob eine Wohnung nach dem Auszug, ein älteres Haus oder ein neuer Grundriss: Wir koordinieren alle Arbeiten, damit Sie nicht jedes Gewerk einzeln beauftragen müssen.",
    ph("karte-sanierung", "Frisch sanierte, helle Altbauwohnung", 800, 600, lazy=False), anliegen="sanierung") + f'''
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
      <div class="bild-rund">{ph("karte-umbau", "Handwerker montiert eine Trockenbauwand", 800, 600)}</div>
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
    <div class="kopf"><h2 id="ablauf-titel">So läuft es ab</h2></div>
    {ABLAUF}
  </div>
</section>
{cta(anliegen="sanierung")}
'''
page("sanierung", "Sanierung & Umbau in Dortmund – koordiniert aus einer Hand | IMPOLA",
     "Komplettsanierung und Umbau von Wohnungen und Häusern in Dortmund und im Ruhrgebiet. Alle Gewerke koordiniert, ein fester Ansprechpartner.",
     "sanierung.html", san_body)

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
     "objektservice.html", obj_body)

# ------------------------------------------------------------------ Verwaltung (nur Info!)
verw_body = seitenkopf("Immobilienverwaltung", "Immobilienverwaltung – in Vorbereitung",
    "Wir bereiten die Immobilienverwaltung als weiteres Angebot vor. Sobald alle Voraussetzungen erfüllt sind, informieren wir an dieser Stelle.",
    ph("karte-verwaltung", "Schlüsselbund und Aktenordner auf einem Schreibtisch", 800, 600, lazy=False), aktionen=False) + '''
<section class="abschnitt">
  <div class="wrap">
    <!-- WICHTIG: Kein Anfrageformular, keine Preise, keine Leistungszusagen, bis die Erlaubnis nach § 34c GewO erteilt ist. -->
    <div class="infobox">
      <p>Aktuell nehmen wir noch keine Verwaltungsmandate an. Unsere Leistungen rund um <a href="sanierung.html">Sanierung</a>, <a href="badumbau.html">Badumbau</a> und <a href="objektservice.html">Objektservice</a> stehen Eigentümern und Hausverwaltungen schon heute zur Verfügung.</p>
    </div>
  </div>
</section>
'''
page("verwaltung", "Immobilienverwaltung – in Vorbereitung | IMPOLA",
     "IMPOLA bereitet die Immobilienverwaltung als weiteres Angebot vor.", "", verw_body,
     '<meta name="robots" content="noindex, follow">\n')

# ------------------------------------------------------------------ Über uns
ueber_body = seitenkopf("Über uns", "Wer hinter IMPOLA steht",
    "Wir sind ein Dortmunder Unternehmen für Sanierung, Umbau und Objektservice. Unser Anspruch: Sie haben einen Ansprechpartner, der sich um alles kümmert.",
    None, aktionen=False) + f'''
<section class="abschnitt" aria-labelledby="team-titel">
  <div class="wrap">
    <h2 id="team-titel" class="kopf">Ihre Ansprechpartner</h2>
    <!-- PLATZHALTER Porträts: echte Fotos, 1000 × 1250 px (4:5), heller Hintergrund, Kleidung Anthrazit. Keine KI-Porträts. Rollenbezeichnungen vor Livegang abstimmen. -->
    <div class="team">
      <div class="person">
        {ph("portrait-tim-pomian", "Porträt Tim Pomian", 1000, 1250)}
        <h3>Tim Pomian</h3>
        <p class="rolle">Projektleitung vor Ort</p>
        <p>Tim ist Ihr Ansprechpartner auf der Baustelle – vom ersten Termin bis zur Übergabe.</p>
      </div>
      <div class="person">
        {ph("portrait-dennis-lasch", "Porträt Dennis Lasch", 1000, 1250)}
        <h3>Dennis Lasch</h3>
        <p class="rolle">Geschäftsführung</p>
        <p>Dennis verantwortet Angebote, Verträge und Organisation im Hintergrund.</p>
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
     "ueber-uns.html", ueber_body)

# ------------------------------------------------------------------ Partner werden
partner_body = seitenkopf("Partner werden", "Für Handwerksbetriebe: Partner werden",
    "Wir suchen zuverlässige Betriebe aus Dortmund und dem Ruhrgebiet für Badumbau, Sanierung und Umbau. Sie konzentrieren sich aufs Handwerk – wir kümmern uns um Kunden und Organisation.",
    None, anliegen="partner") + '''
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
        <li>Freistellungsbescheinigung nach § 48b EStG</li>
        <li>Unbedenklichkeitsbescheinigungen, z. B. SOKA-BAU und Berufsgenossenschaft, soweit zutreffend</li>
        <li>Termintreue und saubere Arbeit beim Kunden</li>
      </ul>
    </div>
  </div>
</section>
'''+ cta("Lernen wir uns kennen.", "Erzählen Sie uns kurz, welches Gewerk Sie abdecken und in welchem Gebiet Sie arbeiten.", "partner")
page("partner-werden", "Partner werden – Handwerksbetriebe im Ruhrgebiet | IMPOLA",
     "Handwerksbetriebe aus Dortmund und dem Ruhrgebiet: Werden Sie Partner von IMPOLA für Badumbau, Sanierung und Umbau.",
     "", partner_body)

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
        <dt>Anschrift</dt><dd>IMPOLA UG (haftungsbeschränkt)<br>Schillstr. 6<br>44339 Dortmund</dd>
        <dt>Einsatzgebiet</dt><dd>Dortmund und Ruhrgebiet</dd>
      </dl>
    </aside>
  </div>
</section>
'''
page("kontakt", "Kontakt – Beratung anfragen | IMPOLA Dortmund",
     "Kostenlose Beratung zu Badumbau, Sanierung und Objektservice in Dortmund. Rufen Sie an oder schreiben Sie uns.",
     "kontakt.html", kontakt_body)

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
impressum_body = seitenkopf("Impressum", "Impressum", "Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap rechtstext">
  <p><strong>IMPOLA UG (haftungsbeschränkt)</strong><br>Schillstr. 6<br>44339 Dortmund</p>
  <h2>Vertreten durch</h2>
  <p>Geschäftsführer: Dennis Lasch <!-- bei Wechsel der Geschäftsführung sofort aktualisieren --></p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{TEL_LINK}">+49 178 9176594</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <h2>Registereintrag</h2>
  <p>Registergericht: <span class="offen">[Amtsgericht – nach Eintragung ergänzen]</span><br>Registernummer: <span class="offen">[HRB – nach Eintragung ergänzen]</span></p>
  <h2>Umsatzsteuer-Identifikationsnummer</h2>
  <p>gemäß § 27a UStG: <span class="offen">[USt-IdNr. ergänzen oder Abschnitt entfernen, falls keine vergeben]</span></p>
  <h2>Verbraucherstreitbeilegung</h2>
  <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
</div></section>
'''
page("impressum", "Impressum | IMPOLA", "Impressum der IMPOLA UG (haftungsbeschränkt), Dortmund.", "", impressum_body,
     '<meta name="robots" content="noindex, follow">\n')

# ------------------------------------------------------------------ Datenschutz (Rahmen)
ds_body = seitenkopf("Datenschutz", "Datenschutzerklärung", "Informationen zur Verarbeitung Ihrer Daten auf dieser Website.", None, aktionen=False) + f'''
<section class="abschnitt"><div class="wrap rechtstext">
  <!--
    HIER DEN GEPRÜFTEN TEXT DER BESTEHENDEN DATENSCHUTZERKLÄRUNG EINFÜGEN.
    Für diese Website müssen mindestens enthalten sein:
      1. Verantwortlicher (Block unten)
      2. Hosting: Vercel Inc. (Server-Logfiles, Art. 6 Abs. 1 lit. f DSGVO, DPA/AVV mit Vercel, Drittlandtransfer USA – Grundlage angeben); E-Mail-Versand des Formulars über Google Workspace (SMTP)
      3. Kontaktformular und E-Mail/Telefon (Art. 6 Abs. 1 lit. b bzw. f DSGVO, Speicherdauer)
      4. Lokal eingebundene Schriftarten (keine Übertragung an Dritte)
      5. Förder-Check: läuft nur im Browser, keine Speicherung, keine Übertragung
      6. Keine Cookies, kein Tracking (solange zutreffend – sonst Usercentrics + Dienste ergänzen)
      7. Betroffenenrechte, Beschwerderecht (LDI NRW), Stand-Datum
    Superchat und Autocalls.ai NICHT aufnehmen, solange sie auf der Website nicht eingesetzt werden.
  -->
  <h2>Verantwortlicher</h2>
  <p>IMPOLA UG (haftungsbeschränkt)<br>Schillstr. 6, 44339 Dortmund<br>Telefon: +49 178 9176594<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
  <div class="infobox"><p class="offen">[Platzhalter: Vollständigen Text der geprüften Datenschutzerklärung hier einsetzen. Die Seite erst veröffentlichen, wenn der Text vollständig ist.]</p></div>
</div></section>
'''
page("datenschutz", "Datenschutzerklärung | IMPOLA", "Datenschutzerklärung der IMPOLA UG (haftungsbeschränkt).", "", ds_body)

print("Seiten erzeugt.")

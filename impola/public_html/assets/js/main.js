/* IMPOLA – main.js (ohne Tracking, ohne externe Abhängigkeiten) */
(function () {
  "use strict";

  // ---- Mobile Navigation ----
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hauptnavigation");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var offen = nav.classList.toggle("offen");
      toggle.setAttribute("aria-expanded", offen ? "true" : "false");
      toggle.querySelector(".label").textContent = offen ? "Schließen" : "Menü";
    });
  }

  // ---- Jahr im Footer ----
  var jahr = document.getElementById("jahr");
  if (jahr) jahr.textContent = new Date().getFullYear();

  // ---- Förder-Check ----
  // Läuft ausschließlich im Browser. Es wird nichts gespeichert oder übertragen –
  // wichtig, weil die Frage nach dem Pflegegrad ein Gesundheitsdatum (Art. 9 DSGVO) betrifft.
  var check = document.getElementById("foerdercheck");
  if (check) {
    var ergebnis = document.getElementById("check-ergebnis");
    var punkte = document.getElementById("check-punkte");

    var texte = {
      pflegegrad: {
        ja: "Mit Pflegegrad ist ein Zuschuss der Pflegekasse von bis zu 4.180 € je Maßnahme möglich (§ 40 Abs. 4 SGB XI). Wichtig: Den Antrag stellen Sie, bevor der Umbau beginnt – wir helfen dabei.",
        offen: "Ein festgestellter Pflegegrad ist Voraussetzung für den Zuschuss der Pflegekasse. Ist er beantragt, planen wir so, dass der Förderantrag direkt nach der Einstufung gestellt werden kann.",
        nein: "Ohne Pflegegrad gibt es den Zuschuss der Pflegekasse nicht. Ein barrierefreies Bad kann trotzdem sinnvoll sein – wir zeigen Ihnen Kosten und Möglichkeiten und prüfen weitere Förderwege im Einzelfall."
      },
      wohnen: {
        eigentum: "Im Eigentum können Sie direkt starten. Bei Eigentumswohnungen klären wir gemeinsam, ob die Eigentümergemeinschaft einbezogen werden muss.",
        miete: "In einer Mietwohnung braucht es die Erlaubnis Ihres Vermieters. Für barrierereduzierende Umbauten haben Mieter darauf in der Regel einen Anspruch (§ 554 BGB). Wir unterstützen Sie bei der Anfrage."
      },
      problem: {
        wanne: "Häufigste Lösung bei einem hohen Wanneneinstieg: Die Wanne kommt raus, eine bodengleiche Dusche kommt rein.",
        rutsch: "Gegen Rutschgefahr helfen rutschhemmende Fliesen, Haltegriffe und ein Duschsitz – oft schon mit überschaubarem Aufwand.",
        platz: "Bei wenig Bewegungsfreiheit prüfen wir Türbreite, Waschtisch und Raumaufteilung – auch für Rollator oder Rollstuhl.",
        anderes: "Schildern Sie uns Ihre Situation – wir schauen sie uns vor Ort an."
      }
    };

    check.addEventListener("change", function () {
      var pg = check.querySelector('input[name="pflegegrad"]:checked');
      var wo = check.querySelector('input[name="wohnen"]:checked');
      var pr = check.querySelector('input[name="problem"]:checked');
      if (!(pg && wo && pr)) return;

      punkte.innerHTML = "";
      [texte.pflegegrad[pg.value], texte.wohnen[wo.value], texte.problem[pr.value]].forEach(function (t) {
        var li = document.createElement("li");
        li.textContent = t;
        punkte.appendChild(li);
      });
      var warVersteckt = ergebnis.hidden;
      ergebnis.hidden = false;
      if (warVersteckt) ergebnis.focus({ preventScroll: false });
    });
  }

  // ---- Kontaktformular: Anliegen per URL vorbelegen (?anliegen=badumbau) ----
  var anliegen = document.getElementById("anliegen");
  if (anliegen && window.URLSearchParams) {
    var p = new URLSearchParams(window.location.search);
    var wert = p.get("anliegen");
    if (wert && anliegen.querySelector('option[value="' + wert.replace(/[^a-z-]/g, "") + '"]')) {
      anliegen.value = wert;
    }
    if (p.get("fehler")) {
      var m = document.getElementById("formular-fehler");
      if (m) { m.hidden = false; }
    }
  }

  // Zeitstempel für einfachen Spam-Schutz (Formular zu schnell abgeschickt = Bot)
  var ts = document.getElementById("ts");
  if (ts) ts.value = Math.floor(Date.now() / 1000);
  // ---- Vorher/Nachher-Vergleich ----
  var buehne = document.querySelector(".vn-buehne");
  if (buehne) {
    var regler = buehne.querySelector(".vn-regler");
    var vorher = buehne.querySelector(".vn-vorher");
    var nachher = buehne.querySelector(".vn-nachher");
    var vnText = document.querySelector(".vn-text");
    var setzen = function () { buehne.style.setProperty("--pos", regler.value + "%"); };
    regler.addEventListener("input", setzen);
    document.querySelectorAll(".vn-auswahl button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".vn-auswahl button").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        vorher.src = btn.dataset.vorher; vorher.alt = btn.dataset.altVorher;
        nachher.src = btn.dataset.nachher; nachher.alt = btn.dataset.altNachher;
        vnText.textContent = btn.dataset.text;
        regler.value = 50; setzen();
      });
    });
  }
})();

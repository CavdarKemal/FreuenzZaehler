# Anhang – Simulator-Dateien

Zu den Kapiteln gehören Simulationen im Ordner `sim/`. Du kannst jede Baugruppe am
Rechner ausprobieren, **bevor** du etwas kaufst oder lötest.

## Welcher Simulator wofür?

| Simulator | Dateiendung | Stärke | Bezug |
|-----------|-------------|--------|-------|
| **Falstad / CircuitJS** | `.txt` (Import aus Text) | Analog + Logik, im Browser | <https://www.falstad.com/circuit/> |
| **LTspice** | `.cir` / `.asc` | genaue Analog-/SPICE-Simulation | kostenlos (Analog Devices) |
| **KiCad / KiCanvas** | `.kicad_sch` | kompletter Schaltplan, im Browser ansehbar | <https://kicanvas.org> |

## KiCad-Gesamtschaltplan ansehen

Der komplette Schaltplan liegt als `sim/kicad/freuenzzaehler.kicad_sch` vor und lässt sich
**ohne Installation** ansehen: Öffne **<https://kicanvas.org>** und ziehe die Datei ins
Browserfenster. Alle Symbole sind eingebettet – keine externen Bibliotheken nötig.
Verdrahtung über **globale Netz-Labels** (gleicher Name = verbunden); Netznamen-Liste in
`sim/kicad/README.md`.

## Status der Dateien (ehrlich)

| Datei | Teil | Status |
|-------|------|--------|
| `ltspice/teil5-eingangsstufe.cir` | 5 | ✅ fertig & lauffähig |
| `falstad/teil7-netzteil.txt` | 7 | ✅ fertig (RC-Glättung) |
| `falstad/teil6-reset.txt` | 6 | ✅ fertig (Reset-Differenzierer C3/R3) |
| Logik-Sims (Tor, Teiler, Zähler, 7-Seg, Schmitt) | 1–6 | 📋 als **Aufbaurezept** unten |

!!! info "Warum Rezepte statt fertiger Logik-Dateien?"
    Falstads **analoge** Schaltungen lassen sich als Textdatei zuverlässig bereitstellen.
    Bei **Logik**-Schaltungen (Gatter, Flipflops, Zähler) nutzt man am besten Falstads
    eingebaute Bausteine über das **Menü** – das ist in 1–2 Minuten erledigt und
    **garantiert korrekt verbunden**, während handgeschriebener Logik-Code leicht
    unverbundene Pins hat. Deshalb unten präzise Klick-Rezepte.

## So lädst du eine Falstad-Datei

1. Öffne <https://www.falstad.com/circuit/>.
2. Menü **Datei → Import aus Text** (*File → Import From Text*).
3. Inhalt der `.txt`-Datei hineinkopieren → **OK**.
4. Bauteilwerte per Rechtsklick ändern, Verlauf im Scope beobachten.

---

## Falstad-Aufbaurezepte für die Logik-Sims

Alle Menüpunkte unter **Draw** (Zeichnen). Jeder Baustein wird einfach aufs Raster
gesetzt und mit **Wire** (Draw → Add Wire) verbunden.

### Teil 1 – Zeitbasis (Teilerkette ÷2 je Stufe)

1. **Draw → Inputs and Sources → Add Clock** – der Takt (Rechtsklick → Frequenz z. B. 8 Hz, damit man es sieht).
2. 3–4× **Draw → Digital Chips → Add D Flip-Flop**.
3. Jedes FF als ÷2 verschalten: Ausgang **Q̄** zurück auf **D** desselben FF; **Q** als Takt ins nächste FF.
4. An jeden Q-Ausgang **Draw → Outputs and Labels → Add Logic Output** (oder eine LED).
5. Beobachtung: Stufe 1 blinkt mit halbem, Stufe 2 mit viertel … Takt. Das ist \( f/2^n \).

### Teil 2 – Das Tor (UND-Gatter)

1. **Draw → Inputs and Sources → Add Clock** (schnelles Signal, „Eingang").
2. **Draw → Inputs and Sources → Add Logic Input** (das „Torsignal", von Hand schaltbar).
3. **Draw → Logic Gates → Add AND Gate**; beide Eingänge anschließen.
4. **Draw → Outputs and Labels → Add Logic Output** an den Gatterausgang.
5. Beobachtung: Impulse erscheinen nur, solange das Torsignal **High** ist.

### Teil 3 – Vorteiler ÷10 / Zählerkette

1. **Draw → Digital Chips → Add Counter** – Rechtsklick → *Modulus = 10* ⇒ Dekadenzähler (÷10).
2. Als Zählerkette mehrere Dekadenzähler kaskadieren: **Carry/Übertrag** einer Stufe auf den **Takt** der nächsten.
3. Takt über **Add Clock** zuführen; Zählerstände mit **Add 7-Segment Decoder/Display** sichtbar machen.

### Teil 4 – 7-Segment-Anzeige

1. **Draw → Digital Chips → Add Counter** (Modulus 10) als Ziffernquelle.
2. **Draw → Outputs and Labels → Add 7-Segment LED** und **Add 7-Segment Decoder** dazwischen.
3. Takt per **Add Clock**; die Anzeige zählt 0–9 sichtbar hoch.

### Teil 5 – Schmitt-Trigger

1. **Draw → Inputs and Sources → Add A/C Voltage Source** (Sinus, kleine Amplitude; optional Rauschen).
2. **Draw → Logic Gates → Add Schmitt Trigger** (bzw. *Inverting Schmitt Trigger*).
3. **Add Logic Output / Scope** an den Ausgang.
4. Beobachtung: Erst wenn das Signal die **obere** Schwelle übersteigt, kippt der Ausgang auf High – Hysterese macht das Rechteck rausch­fest.

### Teil 6 – Timing: Zähler mit vs. ohne Latch

1. **Add Clock** → **Add Counter** (Zähler).
2. Variante A (ohne Latch): Zählerausgang direkt auf **7-Segment** → zappelt.
3. Variante B (mit Latch): **Draw → Digital Chips → Add Latch** zwischen Zähler und Anzeige, mit einem Übernahme-Takt → Anzeige steht ruhig.
4. Der fertige **Reset-Impuls** (C3/R3) als Analogteil: siehe Datei `falstad/teil6-reset.txt`.

---

## Enthaltene fertige Dateien im Detail

- **`falstad/teil7-netzteil.txt`** – pulsierende Eingangsspannung (0…10 V), Serienwiderstand,
  Glättungskondensator und Last. Zeigt, wie der Kondensator die Spannung stützt (Abblockung/Siebung aus Teil 7).
- **`falstad/teil6-reset.txt`** – Rechteck über 220 pF auf 10 kΩ gegen Masse: das
  **Differenzierglied** erzeugt an jeder Flanke einen schmalen Nadelimpuls (τ ≈ 2,2 µs) –
  genau der Reset-Impuls aus Teil 6.
- **`ltspice/teil5-eingangsstufe.cir`** – einstufiger Verstärker, zeigt Arbeitspunkt
  (Kollektor ≈ 1,9 V) und die Verstärkung eines kleinen Signals.

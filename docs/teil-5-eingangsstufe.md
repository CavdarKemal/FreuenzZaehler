# Teil 5 – Die Eingangsstufe: schwache, krumme Signale zählbar machen

!!! abstract "Ziel dieses Teils"
    Du verstehst, warum man ein echtes Messsignal nicht direkt zählen kann, wie ein
    **Verstärker** kleine Signale anhebt, was ein **Schmitt-Trigger** macht und warum der
    **Arbeitspunkt** auf \( U_b/2 \) gelegt wird.

## 1. Das Problem mit echten Signalen

Die Digitalteile ab Teil 2 erwarten ein sauberes Rechteck zwischen 0 V und 5 V. Ein
reales Messsignal sieht aber oft ganz anders aus:

- Es ist **klein** – manchmal nur wenige Millivolt (der BX-020 spricht ab 20 mV<sub>SS</sub> an).
- Es ist **sinusförmig oder verschliffen** – keine steilen Flanken.
- Es liegt evtl. auf einer **Gleichspannung** (Offset) oder ist um 0 V symmetrisch.

Würde man so etwas direkt an ein Logikgatter legen, bekäme man unzählige Fehlzählungen
(das Gatter „zittert" an der Schaltschwelle). Die Eingangsstufe macht aus dem rohen
Signal ein **sauberes, pegelrichtiges Rechteck**. Sie besteht aus zwei Funktionen:
**Verstärken** und **Formen**.

```mermaid
flowchart LR
    IN([kleines, krummes\nMesssignal]) --> AMP[Verstärker\nT1]
    AMP --> SHAPE[Formen\nSchmitt-Trigger /\nschnelles Logiktor]
    SHAPE --> OUT([sauberes 0/5 V-\nRechteck zum Tor])
```

## 2. Der Verstärker (T1)

Im BX-020 übernimmt der **HF-Transistor T1 (SF245)** die Verstärkung. Er hebt Signale ab
\( U_\text{eSS}=20\,\text{mV} \) auf Pegel an, die der nachfolgende Vorteiler sauber
verarbeiten kann. Wichtige Punkte:

- **Arbeitspunkt auf \( U_b/2 \):** Der Eingang des Vorteilers ist auf die halbe
  Betriebsspannung (2,5 V) vorgespannt (Widerstände R6, R7). So kann das verstärkte
  Signal **symmetrisch** nach oben **und** unten aussteuern, bevor es die Schaltschwelle
  überschreitet – man nutzt den vollen Aussteuerbereich.
- **Kollektorstrom ~3–4 mA:** Nur im richtigen Arbeitspunkt ist der Transistor schnell
  und empfindlich genug. Die BX-020-Doku nennt als Kontrolle: Gleichspannung am
  Kollektor von T1 ≈ 1,8 ± 0,3 V.

!!! info "Empfindlichkeit ist frequenzabhängig"
    Laut Vorbild spricht der Zähler bei 1–10 MHz schon ab ~2 mV an, bei 45 MHz erst ab
    ~15 mV. Je höher die Frequenz, desto mehr Eingangsspannung ist nötig – typisch für
    reale Verstärker (die Verstärkung sinkt zu hohen Frequenzen hin).

## 3. Das Formen: der Schmitt-Trigger

Verstärken allein genügt nicht – ein verstärktes Sinussignal hat immer noch keine steilen
Flanken. Hier kommt der **Schmitt-Trigger** ins Spiel. Er ist ein Schaltelement mit
**zwei verschiedenen Schaltschwellen** (Hysterese):

- Übersteigt das Signal die **obere** Schwelle → Ausgang kippt auf High.
- Erst wenn es unter die **untere** Schwelle fällt → Ausgang kippt zurück auf Low.

```
Eingang (Sinus mit Rauschen)      Ausgang (sauberes Rechteck)
   ╱╲    ╱╲    ╱╲                    ┌──┐  ┌──┐  ┌──┐
  ╱  ╲  ╱  ╲  ╱  ╲      ─────►       │  │  │  │  │  │
─╯    ╲╱    ╲╱    ╲─               ──┘  └──┘  └──┘  └──
  ↑obere Schwelle
  ↓untere Schwelle (Abstand = Hysterese)
```

Durch die Hysterese erzeugt **leichtes Rauschen keine Mehrfach-Schaltungen** mehr – das
Signal muss erst den ganzen Hysterese-Abstand durchlaufen, bevor der Ausgang wieder
kippt. Heraus kommt ein sauberes, prellfreies Rechteck, perfekt zum Zählen.

!!! note "Im Elektor-NF-Zähler ausdrücklich vorhanden"
    Der Elektor-Niederfrequenzzähler nennt explizit einen **Schmitt-Trigger mit einem
    Einstellpoti (P1)**, der das Eingangssignal in ein Rechteck wandelt. Im BX-020 ist
    die Formung eng mit dem schnellen Vorteilereingang (auf \( U_b/2 \) vorgespannt)
    verwoben; das Prinzip ist dasselbe.

## 4. Simulieren (hier lohnt sich LTspice)

Die Eingangsstufe ist der **analogste** Teil des Geräts – ideal für eine genaue
SPICE-Simulation.

=== "LTspice (Verstärker-Arbeitspunkt)"

    Lade `sim/ltspice/teil5-eingangsstufe.asc`. Du kannst den Arbeitspunkt (DC operating
    point) berechnen lassen und die Kollektorspannung prüfen, eine Sinusquelle mit
    wenigen mV anlegen und die Verstärkung im Transientenlauf beobachten.

=== "Falstad (Schmitt-Trigger-Wirkung)"

    Folge dem **Aufbaurezept Teil 5** im [Anhang](anhang-simulation.md): eine
    **A/C-Spannungsquelle** (kleiner Sinus) auf einen **Schmitt Trigger** aus dem
    Falstad-Menü. Am Ausgang entsteht ein sauberes Rechteck. Verändere die Amplitude und
    beobachte, ab wann (Hysterese) der Ausgang überhaupt kippt.

## 5. Messen

- **Gleichspannung am Kollektor von T1** gegen GND messen → soll ~1,8 V sein. Das ist der
  schnellste Funktionstest der Eingangsstufe mit einem einfachen Multimeter.
- Mit Signalgenerator ein kleines Sinussignal anlegen und prüfen, ab welcher Amplitude
  der Zähler anspricht (Empfindlichkeitskurve).

## 6. Typische Fehler

!!! danger
    - **Falscher Arbeitspunkt** (Kollektorspannung weit weg von 1,8 V) → Stufe
      unempfindlich oder übersteuert. Vorspannungswiderstände prüfen.
    - **Kein Schmitt-Trigger / keine Hysterese** → bei langsamen oder verrauschten
      Signalen zählt das Gerät viel zu viel.
    - **Eingang nicht auf \( U_b/2 \) vorgespannt** → asymmetrische Aussteuerung, halbe
      Empfindlichkeit.

## Zusammenfassung

- Reale Signale sind klein/krumm → sie müssen **verstärkt** und **geformt** werden.
- **T1** verstärkt ab ~20 mV; Arbeitspunkt auf \( U_b/2 \) für symmetrische Aussteuerung.
- Der **Schmitt-Trigger** erzeugt per **Hysterese** ein sauberes, rausch­festes Rechteck.
- Dies ist der analogste Block → **LTspice** ist hier das passende Werkzeug.

## Übungsfragen

??? question "1. Warum spannt man den Eingang auf die halbe Betriebsspannung vor?"
    Damit das Signal symmetrisch nach oben und unten aussteuern kann und der volle
    Bereich genutzt wird – maximale Empfindlichkeit ohne einseitiges Clipping.

??? question "2. Was verhindert die Hysterese des Schmitt-Triggers?"
    Mehrfachschaltungen durch Rauschen an der Schaltschwelle (unerwünschte Fehlzählungen).

??? question "3. Warum braucht man bei 45 MHz mehr Eingangsspannung als bei 1 MHz?"
    Die Verstärkung des Transistors sinkt zu hohen Frequenzen hin, also ist für denselben
    Ausgangspegel mehr Eingangssignal nötig.

---

Weiter mit [Teil 6 – Steuerung & Timing](teil-6-steuerung.md): Wie wird der Zähler
rechtzeitig zurückgesetzt – und warum flimmert die Anzeige eigentlich?

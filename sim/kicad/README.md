# KiCad – Gesamtschaltplan

`freuenzzaehler.kicad_sch` ist der komplette Schaltplan des BX-020-Frequenzzählers
(Zeitbasis, Eingangsstufe, Vorteiler, 5× Zähler/Anzeige, Reset, Netzteil).

## In KiCad-Desktop öffnen (empfohlen)

Es liegt ein **vollständiges Projekt** vor (`freuenzzaehler.kicad_pro` +
`freuenzzaehler.kicad_sch`):

1. KiCad starten → **Datei → Projekt öffnen…** (*Open Existing Project*).
2. **`freuenzzaehler.kicad_pro`** auswählen.
3. Im Projektfenster auf die Schaltplan-Datei doppelklicken → der Schaltplan-Editor öffnet
   sich.

!!! wichtig
    Direkt eine `.kicad_sch` über den **Projekt-Manager** zu öffnen schlägt fehl
    („Endung stimmt nicht") – der Projekt-Manager erwartet die `.kicad_pro`. Entweder das
    **Projekt** öffnen (oben) oder den **Schaltplan-Editor** separat starten und dort
    *Datei → Öffnen* → `.kicad_sch`.

Alle Symbole sind **in der Datei eingebettet** – es werden keine externen Bibliotheken
benötigt, der Plan öffnet überall identisch. Bauteile lassen sich in KiCad frei
verschieben; die elektrischen Verbindungen (Drähte, Labels, Power-Symbole) bleiben erhalten.

## Online ansehen (ohne Installation)

1. Öffne **<https://kicanvas.org>**.
2. Ziehe `freuenzzaehler.kicad_sch` ins Browserfenster.
3. Der Schaltplan wird direkt gerendert (eingebettete Symbole).

## Layout-Vorschau

`preview.png` zeigt das aktuelle Layout als Bild (vom Generator erzeugt) – praktisch für
einen schnellen Blick ohne KiCad.

## Aufbauprinzip des Plans

- Verdrahtung über **globale Netz-Labels**: Pins mit gleichem Label-Namen sind
  elektrisch verbunden (z. B. alle `+5V`, alle `GND`, `TOR`, `RESET`, `FE_DIV10`, …).
  Das hält den Plan übersichtlich ohne quer verlaufende Leitungen.
- Die Symbole sind **kompakte Lehr-Symbole** (Kästchen mit beschrifteten Pins), kein
  pin-genaues Package-Layout. Für Verständnis und Übersicht optimiert.

## Wichtige Netznamen

| Netz | Bedeutung |
|------|-----------|
| `+5V`, `GND` | Versorgung |
| `UB` | Eingangsspannung +Ub (DC-Buchse, vor 7805) |
| `OSC1/2/3` | Quarzoszillator-Knoten um IC3 |
| `F200`, `F100`, `TOR`, `TORN` | Zeitbasis: 200 Hz → 100 Hz → 50 Hz (Tor + invertiert) |
| `RESET` | Reset-Impuls (aus C3/R3) an alle 4026 |
| `FE_IN` | Signaleingang |
| `DIV_IN` | Eingang des Vorteilers (auf Ub/2 vorgespannt) |
| `FE_DIV10` | Signal nach 10:1-Vorteiler |
| `CAR1..CAR5` | Überträge (Carry) zwischen den Zählstufen |
| `S1a..S5g` | Segmentleitungen der 5 Anzeigestellen |

## Neu generieren

Der Plan wird reproduzierbar erzeugt:

```bash
python gen_schematic.py
```

!!! Hinweis
    Das Layout ist automatisch gesetzt; in KiCad lassen sich Symbole bei Bedarf
    verschieben, um es noch aufgeräumter zu machen. Die elektrische Verbindung bleibt
    über die Labels erhalten, unabhängig von der Position.

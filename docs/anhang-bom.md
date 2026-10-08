# Anhang – Bauteilliste (BOM)

Diese Stückliste entspricht dem **5-stelligen BX-020-Frequenzzähler** (FUNKAMATEUR /
Box 73). Sie ist die Referenz für den realen Aufbau in Teil 8.

## Halbleiter / ICs

| Kurzz. | Typ / Wert | Funktion | Tutorial-Teil |
|--------|------------|----------|---------------|
| IC1 | 74HC4017 | 10:1-Vorteiler (schnell) | Teil 3 |
| IC2 | 74HC74 | 2× D-Flipflop, Teiler ÷4 | Teil 1 |
| IC3 | 74HC4060 | Quarzoszillator + 14-Stufen-Teiler | Teil 1 |
| IC4–IC8 | 4026BE (5×) | Dekadenzähler + 7-Segment-Dekoder | Teil 3/4 |
| T1 | SF245 | HF-Eingangstransistor (Verstärker) | Teil 5 |
| D1 | 1N4148 | Si-Diode | Teil 6 |
| U1 | 7805 | 5-V-Spannungsregler | Teil 7 |

## Quarz

| Kurzz. | Typ / Wert | Anmerkung |
|--------|------------|-----------|
| Q1 | 3,2768 MHz | HC-18-Standardquarz; **1 mm über Platine** montieren! |

## Widerstände

| Kurzz. | Wert | Farbcode | Funktion |
|--------|------|----------|----------|
| R1 | 2,2 kΩ | rot-rot-rot | Oszillator/Vorspannung |
| R2 | 1 MΩ | braun-schwarz-grün | Oszillator-Rückkopplung |
| R3 | 10 kΩ | braun-schwarz-orange | Reset-Differenzierglied (mit C3) |
| R4, R8 | 1,2 kΩ | braun-rot-rot | R8 = Dezimalpunkt-Vorwiderstand (1,0–1,5 kΩ) |
| R5 | 12 kΩ | braun-rot-orange | Eingangsstufe |
| R6, R7 | 150 kΩ | braun-grün-gelb | Vorspannung Eingang auf U_b/2 |

## Kondensatoren

| Kurzz. | Wert | Typ | Funktion |
|--------|------|-----|----------|
| C1, C2 | 100 pF „101" | NP0-Keramik, 5-mm-Raster | Quarz-Lastkapazität |
| C3 | 220 pF „221" | NP0-Keramik | Reset-Differenzierglied (mit R3) |
| C4, C5, C6, C8, C10, C12 | 100 nF | Vielschicht | Abblockung |
| C7, C9, C11 | 47 µF | Elko 16/25 V | Siebung/Pufferung |

## Anzeige & Mechanik

| Kurzz. | Typ / Wert | Anmerkung |
|--------|------------|-----------|
| LED1–LED5 | SC52-11, superrot | 7-Segment, **gemeinsame Katode**, 5 Stück (KINGBRIGHT) |
| BU1 | DC-Buchse | Spannungseinspeisung |
| P1…P6 | Lötstifte ∅1,0 mm | 6 Stück |

## Hinweise zur Versorgung

- **Mit Regler:** 7–20 V DC an BU1; U1 (7805) bestückt.
- **Direkt 5 V:** U1 **nicht** bestücken, 5 V an Lötstift P3 anlegen **oder** Ein-/
  Ausgangslötaugen von U1 überbrücken und 5 V an BU1 anlegen.
- Stromaufnahme max. **65 mA**. **Kein Verpolungsschutz** auf der Platine → Polarität
  prüfen!

!!! tip "Für reinen Simulations-/Lernbetrieb"
    Du brauchst **nichts** von dieser Liste, um die Simulationen durchzuarbeiten – sie ist
    nur für den optionalen realen Aufbau (Teil 8) relevant.

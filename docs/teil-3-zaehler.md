# Teil 3 – Der Zähler: Impulse in Ziffern verwandeln

!!! abstract "Ziel dieses Teils"
    Du verstehst, wie ein **Dekadenzähler** zählt, wie man mehrere Stellen zu einem
    mehrstelligen Zähler **kaskadiert**, welche Rolle der **10:1-Vorteiler** spielt und
    warum der Baustein **4026** für unser Vorbild so praktisch ist.

## 1. Vom Binärzähler zum Dekadenzähler

In Teil 1 haben wir gesehen: Ein Flipflop zählt (teilt) durch 2. Reiht man vier
Flipflops, zählt die Kette binär 0,1,2,…,15 (also bis \( 2^4-1 \)). Für eine **dezimale**
Anzeige wollen wir aber Ziffern 0–9. Ein **Dekadenzähler** ist deshalb so gebaut, dass er
nach **9 wieder auf 0** springt und dabei einen **Übertrag (Carry)** ausgibt.

```
Impulse:   1 2 3 4 5 6 7 8 9 10 11 ...
Ziffer:    1 2 3 4 5 6 7 8 9  0  1 ...
Carry:     ________________↑_______   (Übertrag beim Übergang 9→0)
```

## 2. Kaskadieren: mehrstellig zählen

Der Carry-Ausgang einer Stelle treibt den Takteingang der **nächsthöheren** Stelle. So
entsteht aus Dekaden eine mehrstellige Dezimalzahl – genau wie beim Kilometerzähler im
Auto:

```mermaid
flowchart LR
    IN([gezählte Impulse]) --> D1
    D1[Dekade 1\nEiner] -->|Carry 9→0| D2
    D2[Dekade 2\nZehner] -->|Carry| D3
    D3[Dekade 3\nHunderter] -->|Carry| D4
    D4[Dekade 4\nTausender] -->|Carry| D5[Dekade 5\nZehntausender]
```

Im BX-020 sind das **fünf** Dekaden (IC4–IC8) für eine fünfstellige Anzeige.

## 3. Der 10:1-Vorteiler – Zugang zu hohen Frequenzen

Ein 4026 schafft bei 5 V nur ~2,5 MHz (typisch 5 MHz). Für 45 MHz reicht das nie. Deshalb
sitzt **vor** der Zählerkette ein **Vorteiler**, der die Frequenz durch 10 teilt – im
BX-020 realisiert durch einen **74HC4017** (ein Johnson-Zähler, der als ÷10 betrieben
wird). Dieser IC ist mit bis zu 77 MHz (Philips-Datenblatt) deutlich schneller als der
4026 und übernimmt die „erste Front" der hohen Frequenz.

Weil der Vorteiler durch 10 teilt, sieht die Zählerkette nur noch \( f/10 \). Den Faktor
10 holen wir über die Torzeit wieder herein (siehe Teil 2). Nettorechnung:

\[
f = N \cdot \underbrace{\frac{1}{T_\text{Tor}}}_{=100\,\text{(bei 10 ms)}} \cdot \underbrace{10}_{\text{Vorteiler}} = N \cdot 1000
\]

!!! info "Warum gerade der 74HC4017 als Vorteiler?"
    Der erste zählende Baustein muss die **höchste** Frequenz verkraften. Der 74HC4017
    ist dafür schnell genug und teilt sauber durch 10. Die obere Grenzfrequenz des
    ganzen Zählers wird laut BX-020-Doku gemeinsam vom Vorteiler **und** der ersten
    4026-Dekade bestimmt.

## 4. Der 4026: Zähler **und** Anzeige-Dekoder in einem

Der **CD4026 / HCF4026** ist für dieses Projekt ideal, weil er zwei Aufgaben vereint:

1. Er ist ein **Dekadenzähler** (zählt 0–9, gibt Carry aus).
2. Er hat einen eingebauten **7-Segment-Dekoder** – die Ausgänge a…g treiben direkt eine
   Siebensegmentanzeige (dazu Teil 4).

Dadurch braucht man **pro Ziffer nur einen IC** plus Anzeige – extrem bauteilsparend.
Wichtige Pins im Vorbild:

| Pin (4026) | Funktion | Im BX-020 |
|------------|----------|-----------|
| Clock (1) | Zähltakt | von Vorteiler bzw. vorheriger Dekade |
| Clock-Inhibit (2) | Zählen sperren | 50-Hz-Torsteuerung (Teil 2) |
| Display-Enable (3) | Anzeige freigeben | 50-Hz-Torsteuerung |
| Reset (15) | auf 0 setzen | Reset-Impuls (Teil 6) |
| Carry-out (5) | Übertrag 9→0 | Takt der nächsten Dekade |
| a…g | Segmentausgänge | zur 7-Segment-Anzeige |

!!! warning "Die entscheidende Eigenschaft: KEIN Latch"
    Der 4026 hat **keinen Zwischenspeicher**. Was er gerade zählt, zeigt er sofort an.
    Das macht ihn billig und einfach – erzwingt aber die kurze Torzeit und das damit
    verbundene Flimmern/Auflösungsproblem (Teil 2 und 6). Merke dir diese Eigenschaft;
    sie ist der rote Faden zu Teil 9.

## 5. Simulieren

Folge dem **Aufbaurezept Teil 3** im [Anhang → Simulator-Dateien](anhang-simulation.md):
In Falstad setzt du über *Draw → Digital Chips* einen **Counter** mit *Modulus 10* (= ÷10,
die Funktion des 74HC4017) und kaskadierst mehrere davon über den **Übertrag**. Mit
7-Segment-Anzeigen siehst du den Übertrag von Einer zu Zehner zu Hunderter – das
Kaskadierprinzip zum Anfassen.

## 6. Typische Fehler

!!! danger
    - **Carry an den falschen Eingang** der nächsten Dekade → Stellen zählen nicht
      korrekt weiter.
    - **Vorteiler vergessen/zu langsamer erster IC** → hohe Frequenzen werden gar nicht
      oder falsch gezählt (Zählverluste).
    - **Reset nicht angeschlossen** → der Zähler startet jede Messung auf einem zufälligen
      Wert statt bei 0.

## Zusammenfassung

- Ein **Dekadenzähler** zählt 0–9 und gibt bei 9→0 einen **Carry** aus.
- **Kaskadieren** über den Carry ergibt mehrstellige Zählung.
- Ein **10:1-Vorteiler (74HC4017)** macht hohe Frequenzen für die langsameren 4026
  messbar; der Faktor 10 wird über die Torzeit kompensiert.
- Der **4026** vereint Zähler + 7-Segment-Dekoder, hat aber **keinen Latch**.

## Übungsfragen

??? question "1. Wie viele Dekaden braucht man, um bis 99 999 zu zählen?"
    Fünf (jede Dekade eine Ziffer 0–9).

??? question "2. Der Zähler misst mit 10 ms Tor und 10:1-Vorteiler. N = 45. Welche Frequenz?"
    \( f = 45 \cdot 1000\,\text{Hz} = 45\,\text{kHz} \).

??? question "3. Warum kann man die hohe Eingangsfrequenz nicht direkt an die erste 4026-Dekade legen?"
    Der 4026 ist zu langsam (~2,5 MHz). Oberhalb seiner Grenzfrequenz verliert er
    Impulse. Der schnellere Vorteiler nimmt ihm die hohe Frequenz ab.

---

Weiter mit [Teil 4 – Die Anzeige](teil-4-anzeige.md): Wie werden aus den Zählerständen
leuchtende Ziffern?

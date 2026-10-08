# Anhang – Glossar

Kurze Erklärungen der wichtigsten Begriffe, alphabetisch.

**Abblockkondensator** – kleiner Kondensator (meist 100 nF) direkt am IC, der kurze
Strom­spitzen beim Schalten lokal liefert und so die Versorgungsspannung stabil hält.

**Arbeitspunkt** – die Gleichspannungs-/Stromeinstellung eines Transistors im Ruhezustand.
Richtig gewählt (hier Kollektor ~1,8 V), damit das Signal symmetrisch verstärkt wird.

**BCD** – *binary coded decimal*; eine Dezimalziffer (0–9) in 4 Bit kodiert.

**Carry (Übertrag)** – Signal, das ein Dekadenzähler beim Übergang 9→0 ausgibt, um die
nächsthöhere Stelle weiterzuschalten.

**Dekadenzähler** – Zähler, der von 0 bis 9 zählt und dann mit einem Carry auf 0 springt.

**Differenzierglied** – RC-Schaltung, die nur Signal**änderungen** durchlässt; erzeugt aus
einer Flanke einen kurzen Impuls (hier: Reset).

**Flipflop (D-FF)** – 1-Bit-Speicher. Mit Rückkopplung ein Frequenzteiler ÷2.

**Frequenz (f)** – Schwingungen pro Sekunde, Einheit Hertz (Hz). \( f = 1/T \).

**Gemeinsame Katode** – Anzeigetyp, bei dem alle LED-Minuspole zusammen an GND liegen;
Segment leuchtet bei High am Anodenpin.

**Hysterese** – zwei unterschiedliche Schaltschwellen (beim Schmitt-Trigger), die
Mehrfachschaltungen durch Rauschen verhindern.

**Latch (Zwischenspeicher)** – hält ein Messergebnis fest, während der Zähler schon weiter
zählt; macht die Anzeige flimmerfrei. Fehlt beim 4026 (BX-020), vorhanden im 74C925.

**Multiplexing** – Ziffern werden sehr schnell nacheinander angezeigt; das Auge sieht sie
dank Trägheit gleichzeitig. Spart Bauteile.

**NP0 / C0G** – besonders temperaturstabiler Keramik-Kondensatortyp; wichtig für
Quarz-Lastkapazität und Timing.

**Periodendauer (T)** – Zeit für eine vollständige Schwingung. \( T = 1/f \).

**Ppm** – *parts per million*, 0,0001 %. Maß für die Genauigkeit eines Quarzes.

**Quantisierungsfehler (±1 Digit)** – unvermeidbare Unsicherheit, weil nur ganze
Schwingungen gezählt werden.

**Quarz (Schwingquarz)** – piezoelektrischer Kristall mit sehr stabiler Eigenfrequenz;
das genauigkeitsbestimmende Zeitnormal des Zählers.

**Reziprok-Messung** – Frequenzbestimmung über die Messung der Periodendauer (\( f=1/T \));
genau bei niedrigen Frequenzen.

**Schmitt-Trigger** – Schaltelement mit Hysterese, das krumme/verrauschte Signale in
saubere Rechtecke wandelt.

**Spannungsregler (7805)** – erzeugt aus einer höheren, schwankenden Spannung konstante
5 V.

**Torzeit (gate time, \(T_\text{Tor}\))** – die exakt bekannte Zeitspanne, während der
gezählt wird. Bestimmt die Auflösung (\( 1/T_\text{Tor} \)).

**Vorteiler (prescaler)** – teilt eine zu hohe Eingangsfrequenz (z. B. ÷10) herunter,
damit langsamere Zähler sie verarbeiten können.

**Zeitbasis** – die Baugruppe (Quarz + Teiler), die das präzise Zeitsignal/die Torzeit
erzeugt.

**7-Segment-Anzeige** – Ziffernanzeige aus sieben einzeln schaltbaren LED-Segmenten.

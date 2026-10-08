# Simulator-Projektdateien

Dieser Ordner enthält die Simulationen zu den einzelnen Tutorial-Teilen. Eine
ausführliche Zuordnung findest du in der Doku unter **Anhang → Simulator-Dateien**.

## Ordner

| Ordner | Simulator | Öffnen mit |
|--------|-----------|-----------|
| `falstad/` | Falstad / CircuitJS | <https://www.falstad.com/circuit/> → *Datei → Import aus Text* |
| `ltspice/` | LTspice | SPICE-Netzliste über *File → Open* laden und `Run` |
| `logic/`   | Logisim Evolution | `.circ` direkt öffnen |
| `kicad/`   | KiCad 7+ | `.kicad_pro` öffnen |

## Status

| Datei | Status |
|-------|--------|
| `ltspice/teil5-eingangsstufe.cir` | ✅ fertig & lauffähig (SPICE-Netzliste) |
| `falstad/teil7-netzteil.txt` | ✅ fertig (RC-Glättung) |
| `falstad/teil6-reset.txt` | ✅ fertig (Reset-Differenzierer C3/R3) |
| Logik-Sims (Tor, Teiler, Zähler, 7-Seg, Schmitt) | 📋 Aufbaurezepte in der Doku (Anhang → Simulator-Dateien) |
| `kicad/freuenzzaehler.kicad_sch` | ✅ Gesamtschaltplan (auf kicanvas.org ansehen, siehe `kicad/README.md`) |

**Analoge** Falstad-Schaltungen liegen als fertige `.txt`-Importe vor. **Logik**-Sims
baut man in Falstad am schnellsten über die eingebauten Menü-Bausteine – dafür gibt es in
der Doku präzise **Klick-Rezepte** (garantiert korrekt verbunden). So liegen keine
Dateien mit unverbundenen Pins im Repo.

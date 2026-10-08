#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator fuer den KiCad-Gesamtschaltplan des BX-020-Frequenzzaehlers.

Erzeugt eine valide .kicad_sch (KiCad-7-Format) mit EINGEBETTETEN Symbol-
Definitionen, damit sie auf https://kicanvas.org (bzw. in KiCad) ohne externe
Bibliotheken dargestellt werden kann.

Konzept:
- Jede Baugruppe wird mit kompakten, selbst definierten Symbolen gezeichnet.
- Die Verdrahtung erfolgt ueber GLOBALE NETZ-LABELS (gleicher Name = gleicher
  Knoten). Das haelt den Plan robust und vermeidet quer verlaufende Draehte.
- +5V und GND sind ebenfalls globale Labels.

Aufruf:  python gen_schematic.py   ->  schreibt freuenzzaehler.kicad_sch
"""

import uuid as _uuid
import os

def U():
    return str(_uuid.uuid4())

PS   = 2.54      # Pin-Raster
HW   = 12.7      # halbe Breite IC-Koerper
PLEN = 2.54      # Pinlaenge
STUB = 2.54      # Draht-Stummel bis zum Label

# ---------------------------------------------------------------------------
# Symbol-Bibliothek (eingebettet)
# Pins:  (nummer, name, seite 'L'/'R', etype)
# ---------------------------------------------------------------------------
SYMS = {}

def def_ic(libname, pins):
    SYMS[libname] = {"kind": "ic", "pins": pins}

def def_small(libname, pins, kind):
    SYMS[libname] = {"kind": kind, "pins": pins}

def_ic("IC_4060", [(16,"VDD","R","power_in"),(8,"VSS","R","power_in"),
                   (3,"Q14","R","output"),
                   (11,"RTC","L","input"),(10,"CTC","L","passive"),
                   (9,"CIN","L","passive"),(12,"MR","L","input")])

def_ic("IC_7474", [(1,"CLR1","L","input"),(2,"D1","L","input"),(3,"CLK1","L","input"),
                   (4,"PRE1","L","input"),(7,"GND","L","power_in"),
                   (10,"CLK2","L","input"),(11,"D2","L","input"),
                   (12,"PRE2","L","input"),(13,"CLR2","L","input"),
                   (5,"Q1","R","output"),(6,"Q1N","R","output"),(14,"VCC","R","power_in"),
                   (8,"Q2N","R","output"),(9,"Q2","R","output")])

def_ic("IC_4017", [(16,"VDD","R","power_in"),(12,"CO","R","output"),
                   (8,"VSS","L","power_in"),(14,"CLK","L","input"),
                   (13,"CKEN","L","input"),(15,"MR","L","input")])

def_ic("IC_4026", [(16,"VDD","R","power_in"),(5,"CO","R","output"),
                   (10,"a","R","output"),(12,"b","R","output"),(13,"c","R","output"),
                   (9,"d","R","output"),(11,"e","R","output"),(6,"f","R","output"),
                   (7,"g","R","output"),
                   (8,"VSS","L","power_in"),(1,"CLK","L","input"),(2,"INH","L","input"),
                   (3,"DE","L","input"),(15,"RST","L","input")])

def_ic("DISP_7SEG", [(1,"a","L","passive"),(2,"b","L","passive"),(3,"c","L","passive"),
                     (4,"d","L","passive"),(5,"e","L","passive"),(6,"f","L","passive"),
                     (7,"g","L","passive"),(8,"CC","R","passive")])

def_ic("REG_7805", [(1,"IN","L","power_in"),(2,"GND","L","power_in"),(3,"OUT","R","power_out")])

def_ic("Q_NPN", [(1,"B","L","input"),(2,"C","R","passive"),(3,"E","R","passive")])

def_small("R_sym",  [(1,"1","L","passive"),(2,"2","R","passive")], "r")
def_small("C_sym",  [(1,"1","L","passive"),(2,"2","R","passive")], "c")
def_small("XTAL",   [(1,"1","L","passive"),(2,"2","R","passive")], "x")
def_small("DIODE",  [(1,"A","L","passive"),(2,"K","R","passive")], "d")


def sym_geometry(libname):
    """liefert lokale Pin-Koordinaten (y-up Lib-Konvention) und Koerpergrafik."""
    s = SYMS[libname]
    pins = s["pins"]
    left  = [p for p in pins if p[2] == "L"]
    right = [p for p in pins if p[2] == "R"]
    n = max(len(left), len(right), 1)
    top = (n - 1) * PS / 2.0
    coords = {}
    for i, p in enumerate(left):
        y = top - i * PS
        coords[p[0]] = (-(HW + PLEN), y, 0, p)      # rot 0 (zeigt nach rechts/Koerper)
    for j, p in enumerate(right):
        y = top - j * PS
        coords[p[0]] = (+(HW + PLEN), y, 180, p)    # rot 180
    half_h = top + PS
    return coords, half_h


def emit_lib_symbol(libname):
    coords, half_h = sym_geometry(libname)
    kind = SYMS[libname]["kind"]
    out = []
    out.append(f'    (symbol "fz:{libname}" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)')
    out.append(f'      (property "Reference" "U" (at 0 {half_h+2.54:.2f} 0) (effects (font (size 1.27 1.27))))')
    out.append(f'      (property "Value" "{libname}" (at 0 {-(half_h+2.54):.2f} 0) (effects (font (size 1.27 1.27))))')
    out.append(f'      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    out.append(f'      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    # Koerpergrafik
    out.append(f'      (symbol "fz:{libname}_0_1"')
    if kind == "ic":
        out.append(f'        (rectangle (start {-HW:.2f} {half_h:.2f}) (end {HW:.2f} {-half_h:.2f}) '
                   f'(stroke (width 0.254) (type default)) (fill (type background)))')
    elif kind == "r":
        out.append(f'        (rectangle (start {-HW:.2f} 1.02) (end {HW:.2f} -1.02) '
                   f'(stroke (width 0.254) (type default)) (fill (type none)))')
    elif kind == "c":
        out.append(f'        (polyline (pts (xy -1.27 2.03) (xy -1.27 -2.03)) (stroke (width 0.3) (type default)) (fill (type none)))')
        out.append(f'        (polyline (pts (xy 1.27 2.03) (xy 1.27 -2.03)) (stroke (width 0.3) (type default)) (fill (type none)))')
    elif kind == "x":
        out.append(f'        (rectangle (start -1.27 1.52) (end 1.27 -1.52) (stroke (width 0.254) (type default)) (fill (type none)))')
    elif kind == "d":
        out.append(f'        (polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27) (xy 1.27 0) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))')
        out.append(f'        (polyline (pts (xy 1.27 1.27) (xy 1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))')
    out.append('      )')
    # Pins
    out.append(f'      (symbol "fz:{libname}_1_1"')
    for num, (x, y, rot, p) in coords.items():
        name = p[1]
        etype = p[3]
        out.append(f'        (pin {etype} line (at {x:.2f} {y:.2f} {rot}) (length {PLEN:.2f}) '
                   f'(name "{name}" (effects (font (size 1.0 1.0)))) '
                   f'(number "{num}" (effects (font (size 1.0 1.0)))))')
    out.append('      )')
    out.append('    )')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Instanzen
# ---------------------------------------------------------------------------
INSTANCES = []   # (ref, libname, value, x, y, {pinnum: net})
TEXTS = []       # (text, x, y, size)

def place(ref, lib, value, x, y, nets):
    INSTANCES.append((ref, lib, value, x, y, nets))

def note(text, x, y, size=2.0):
    TEXTS.append((text, x, y, size))

P5, GND = "+5V", "GND"

# ---- Zeitbasis -------------------------------------------------------------
note("ZEITBASIS (Teil 1)", 40, 20)
place("Q1","XTAL","3.2768MHz", 40, 40, {1:"OSC1",2:"OSC2"})
place("R2","R_sym","1M",       40, 55, {1:"OSC1",2:"OSC2"})
place("C2","C_sym","100p",     40, 68, {1:"OSC1",2:GND})
place("R1","R_sym","2k2",      40, 81, {1:"OSC2",2:"OSC3"})
place("C1","C_sym","100p",     40, 94, {1:"OSC3",2:GND})
place("IC3","IC_4060","74HC4060", 95, 55,
      {16:P5,8:GND,3:"F200",11:"OSC1",10:"OSC2",9:"OSC3",12:GND})
place("IC2","IC_7474","74HC74", 160, 60,
      {3:"F200",2:"Q1N",6:"Q1N",5:"F100",1:P5,4:P5,7:GND,14:P5,
       10:"F100",11:"TORN",8:"TORN",9:"TOR",12:P5,13:P5})

# ---- Reset-Erzeugung -------------------------------------------------------
note("RESET (Teil 6)", 220, 20)
place("C3","C_sym","220p",  225, 45, {1:"TORN",2:"RESET"})
place("R3","R_sym","10k",   225, 58, {1:"RESET",2:GND})
place("D1","DIODE","1N4148",225, 71, {1:GND,2:"RESET"})

# ---- Eingangsstufe + Vorteiler --------------------------------------------
note("EINGANGSSTUFE + VORTEILER (Teil 5/3)", 40, 118)
place("C4","C_sym","100n", 40, 135, {1:"FE_IN",2:"T1B"})
place("R5","R_sym","12k",  40, 148, {1:P5,2:"T1B"})
place("T1","Q_NPN","SF245",95, 140, {1:"T1B",2:"T1C",3:GND})
place("R4","R_sym","1k2",  40, 161, {1:P5,2:"T1C"})
place("C5","C_sym","100n", 40, 174, {1:"T1C",2:"DIV_IN"})
place("R6","R_sym","150k", 40, 187, {1:P5,2:"DIV_IN"})
place("R7","R_sym","150k", 40, 200, {1:"DIV_IN",2:GND})
place("IC1","IC_4017","74HC4017", 150, 160,
      {16:P5,8:GND,14:"DIV_IN",13:GND,15:GND,12:"FE_DIV10"})
note("FE_IN = Signaleingang", 40, 128, 1.5)

# ---- Zaehlerkette + Anzeige (5 Stellen) -----------------------------------
note("ZAEHLERKETTE + ANZEIGE (Teil 3/4)", 40, 225)
clk_in = ["FE_DIV10","CAR1","CAR2","CAR3","CAR4"]
co_out = ["CAR1","CAR2","CAR3","CAR4","CAR5"]
xcols  = [45, 130, 215, 300, 385]
for i in range(5):
    icref = f"IC{4+i}"
    dispref = f"DISP{i+1}"
    stage = i+1
    seg = {s: f"S{stage}{s}" for s in ["a","b","c","d","e","f","g"]}
    x = xcols[i]
    place(icref, "IC_4026", "4026", x, 255,
          {16:P5,8:GND,1:clk_in[i],2:"TOR",3:"TOR",15:"RESET",5:co_out[i],
           10:seg["a"],12:seg["b"],13:seg["c"],9:seg["d"],11:seg["e"],6:seg["f"],7:seg["g"]})
    place(dispref, "DISP_7SEG", f"7SEG St.{stage}", x, 300,
          {1:seg["a"],2:seg["b"],3:seg["c"],4:seg["d"],5:seg["e"],6:seg["f"],7:seg["g"],8:GND})

# ---- Stromversorgung -------------------------------------------------------
note("STROMVERSORGUNG (Teil 7)", 40, 325)
place("U1","REG_7805","7805", 70, 345, {1:"UB",2:GND,3:P5})
place("C7","C_sym","47u",  40, 360, {1:"UB",2:GND})
place("C9","C_sym","47u",  40, 373, {1:P5,2:GND})
place("C11","C_sym","47u", 40, 386, {1:P5,2:GND})
place("C6","C_sym","100n", 130, 360, {1:P5,2:GND})
place("C8","C_sym","100n", 130, 373, {1:P5,2:GND})
place("C10","C_sym","100n",130, 386, {1:P5,2:GND})
place("C12","C_sym","100n",130, 399, {1:P5,2:GND})
note("UB = +Ub (DC-Buchse BU1, 7...20V)", 40, 335, 1.5)


# ---------------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------------
ROOT = U()
PROJECT = "freuenzzaehler"

def abs_pin(px, py, lx, ly):
    # Lib y-up -> Schematic y-down
    return (px + lx, py - ly)

def emit():
    L = []
    L.append('(kicad_sch (version 20230121) (generator eeschema)')
    L.append(f'  (uuid "{ROOT}")')
    L.append('  (paper "A2")')
    L.append('  (title_block')
    L.append('    (title "Frequenzzaehler (BX-020-Nachbau) - Gesamtschaltplan")')
    L.append('    (company "Tutorial-Projekt FreuenzZaehler")')
    L.append('    (comment 1 "Verdrahtung ueber globale Netz-Labels")')
    L.append('  )')
    # lib_symbols
    L.append('  (lib_symbols')
    for libname in SYMS:
        L.append(emit_lib_symbol(libname))
    L.append('  )')
    # Texte / Blockbeschriftungen
    for text, x, y, size in TEXTS:
        L.append(f'  (text "{text}" (at {x:.2f} {y:.2f} 0) '
                 f'(effects (font (size {size:.2f} {size:.2f})) (justify left bottom)) (uuid "{U()}"))')
    # Instanzen + Stubs + Labels
    for ref, lib, value, x, y, nets in INSTANCES:
        coords, half_h = sym_geometry(lib)
        L.append(f'  (symbol (lib_id "fz:{lib}") (at {x:.2f} {y:.2f} 0) (unit 1) '
                 f'(in_bom yes) (on_board yes) (uuid "{U()}")')
        L.append(f'    (property "Reference" "{ref}" (at {x+ (HW+4):.2f} {y-half_h-1:.2f} 0) '
                 f'(effects (font (size 1.27 1.27)) (justify left)))')
        L.append(f'    (property "Value" "{value}" (at {x+(HW+4):.2f} {y-half_h+1.5:.2f} 0) '
                 f'(effects (font (size 1.0 1.0)) (justify left)))')
        L.append(f'    (instances (project "{PROJECT}" (path "/{ROOT}" (reference "{ref}") (unit 1))))')
        L.append('  )')
        # Stubs + globale Labels
        for num, (lx, ly, rot, p) in coords.items():
            net = nets.get(num)
            if net is None:
                continue
            ax, ay = abs_pin(x, y, lx, ly)
            if lx < 0:   # linker Pin -> Stummel nach links
                ex, ey = ax - STUB, ay
                just = "right"
                lrot = 180
            else:        # rechter Pin -> Stummel nach rechts
                ex, ey = ax + STUB, ay
                just = "left"
                lrot = 0
            L.append(f'  (wire (pts (xy {ax:.2f} {ay:.2f}) (xy {ex:.2f} {ey:.2f})) '
                     f'(stroke (width 0) (type default)) (uuid "{U()}"))')
            L.append(f'  (global_label "{net}" (shape bidirectional) (at {ex:.2f} {ey:.2f} {lrot}) '
                     f'(effects (font (size 1.0 1.0)) (justify {just})) (uuid "{U()}"))')
    L.append('  (sheet_instances (path "/" (page "1")))')
    L.append(')')
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(here, "freuenzzaehler.kicad_sch")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(emit())
    print("geschrieben:", outpath)
    print("Instanzen:", len(INSTANCES), " Symbole:", len(SYMS))

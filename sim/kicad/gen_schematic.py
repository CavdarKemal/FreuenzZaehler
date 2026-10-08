#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator fuer den KiCad-Gesamtschaltplan des BX-020-Frequenzzaehlers.

Erzeugt eine valide .kicad_sch (KiCad-7-Format) mit EINGEBETTETEN Symbolen,
darstellbar auf https://kicanvas.org bzw. in KiCad.

Darstellung als erkennbarer Schaltplan:
- ECHTE Drahtverbindungen fuer die Zaehler->Anzeige-Segmentleitungen und die
  Carry-Kette zwischen den Zaehlstufen.
- POWER-SYMBOLE (+5V / GND) statt Text an jedem Versorgungspin.
- Gut lesbare lokale Netz-LABELS fuer verteilte Steuersignale (TOR, RESET, ...).

Zusatz:  render_preview() erzeugt preview.png (Layout-Kontrolle ohne KiCad).

Aufruf:  python gen_schematic.py
"""

import uuid as _uuid
import os

def U():
    return str(_uuid.uuid4())

PS   = 2.54
HW   = 12.7
PLEN = 2.54
STUB = 2.54
LBL  = 1.8     # Label-Schriftgroesse

# ---------------------------------------------------------------------------
# Symbol-Bibliothek (eingebettet). Pins: (nummer, name, 'L'/'R', etype)
# ---------------------------------------------------------------------------
SYMS = {}
def def_sym(name, pins, kind):
    SYMS[name] = {"kind": kind, "pins": pins}

def_sym("IC_4060", [(16,"VDD","R","power_in"),(8,"VSS","R","power_in"),(3,"Q14","R","output"),
                    (11,"RTC","L","input"),(10,"CTC","L","passive"),(9,"CIN","L","passive"),
                    (12,"MR","L","input")], "ic")
def_sym("IC_7474", [(1,"CLR1","L","input"),(2,"D1","L","input"),(3,"CLK1","L","input"),
                    (4,"PRE1","L","input"),(7,"GND","L","power_in"),(10,"CLK2","L","input"),
                    (11,"D2","L","input"),(12,"PRE2","L","input"),(13,"CLR2","L","input"),
                    (5,"Q1","R","output"),(6,"Q1N","R","output"),(14,"VCC","R","power_in"),
                    (8,"Q2N","R","output"),(9,"Q2","R","output")], "ic")
def_sym("IC_4017", [(16,"VDD","R","power_in"),(12,"CO","R","output"),(8,"VSS","L","power_in"),
                    (14,"CLK","L","input"),(13,"CKEN","L","input"),(15,"MR","L","input")], "ic")
# 4026: Steuer/Takt links, Versorgung+Segmente rechts (Anzeige steht rechts daneben)
def_sym("IC_4026", [(1,"CLK","L","input"),(2,"INH","L","input"),(3,"DE","L","input"),
                    (15,"RST","L","input"),(8,"VSS","L","power_in"),(5,"CO","L","output"),
                    (16,"VDD","R","power_in"),(10,"a","R","output"),(12,"b","R","output"),
                    (13,"c","R","output"),(9,"d","R","output"),(11,"e","R","output"),
                    (6,"f","R","output"),(7,"g","R","output")], "ic")
def_sym("DISP_7SEG", [(1,"a","L","passive"),(2,"b","L","passive"),(3,"c","L","passive"),
                      (4,"d","L","passive"),(5,"e","L","passive"),(6,"f","L","passive"),
                      (7,"g","L","passive"),(8,"CC","R","passive")], "ic")
def_sym("REG_7805", [(1,"IN","L","power_in"),(2,"GND","L","power_in"),(3,"OUT","R","power_out")], "ic")
def_sym("Q_NPN", [(1,"B","L","input"),(2,"C","R","passive"),(3,"E","R","passive")], "ic")
def_sym("R_sym", [(1,"1","L","passive"),(2,"2","R","passive")], "r")
def_sym("C_sym", [(1,"1","L","passive"),(2,"2","R","passive")], "c")
def_sym("XTAL",  [(1,"1","L","passive"),(2,"2","R","passive")], "x")
def_sym("DIODE", [(1,"A","L","passive"),(2,"K","R","passive")], "d")


def geom(libname):
    """lokale Pin-Koordinaten (Lib y-up) + halbe Hoehe."""
    pins = SYMS[libname]["pins"]
    left  = [p for p in pins if p[2] == "L"]
    right = [p for p in pins if p[2] == "R"]
    n = max(len(left), len(right), 1)
    top = (n - 1) * PS / 2.0
    coords = {}
    for i, p in enumerate(left):
        coords[p[0]] = (-(HW + PLEN), top - i * PS, 0, p)
    for j, p in enumerate(right):
        coords[p[0]] = (+(HW + PLEN), top - j * PS, 180, p)
    return coords, top + PS


def emit_lib_symbol(libname):
    coords, half_h = geom(libname)
    kind = SYMS[libname]["kind"]
    o = []
    o.append(f'    (symbol "fz:{libname}" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)')
    o.append(f'      (property "Reference" "U" (at 0 {half_h+2.5:.2f} 0) (effects (font (size 1.27 1.27))))')
    o.append(f'      (property "Value" "{libname}" (at 0 {-(half_h+2.5):.2f} 0) (effects (font (size 1.27 1.27))))')
    o.append(f'      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    o.append(f'      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    o.append(f'      (symbol "fz:{libname}_0_1"')
    if kind == "ic":
        o.append(f'        (rectangle (start {-HW:.2f} {half_h:.2f}) (end {HW:.2f} {-half_h:.2f}) '
                 f'(stroke (width 0.254) (type default)) (fill (type background)))')
    elif kind == "r":
        o.append(f'        (rectangle (start {-HW:.2f} 1.02) (end {HW:.2f} -1.02) (stroke (width 0.254) (type default)) (fill (type none)))')
    elif kind == "c":
        o.append('        (polyline (pts (xy -1.0 2.0) (xy -1.0 -2.0)) (stroke (width 0.4) (type default)) (fill (type none)))')
        o.append('        (polyline (pts (xy 1.0 2.0) (xy 1.0 -2.0)) (stroke (width 0.4) (type default)) (fill (type none)))')
    elif kind == "x":
        o.append('        (rectangle (start -1.2 1.5) (end 1.2 -1.5) (stroke (width 0.254) (type default)) (fill (type none)))')
    elif kind == "d":
        o.append('        (polyline (pts (xy -1.2 1.2) (xy -1.2 -1.2) (xy 1.2 0) (xy -1.2 1.2)) (stroke (width 0.254) (type default)) (fill (type none)))')
        o.append('        (polyline (pts (xy 1.2 1.2) (xy 1.2 -1.2)) (stroke (width 0.254) (type default)) (fill (type none)))')
    o.append('      )')
    o.append(f'      (symbol "fz:{libname}_1_1"')
    for num, (x, y, rot, p) in coords.items():
        o.append(f'        (pin {p[3]} line (at {x:.2f} {y:.2f} {rot}) (length {PLEN:.2f}) '
                 f'(name "{p[1]}" (effects (font (size 0.9 0.9)))) '
                 f'(number "{num}" (effects (font (size 0.9 0.9)))))')
    o.append('      )')
    o.append('    )')
    return "\n".join(o)


POWER_LIB = '''    (symbol "fz:PWR_5V" (power) (pin_names (offset 0)) (in_bom no) (on_board yes)
      (property "Reference" "#PWR" (at 0 -2.5 0) (effects (font (size 1.0 1.0)) hide))
      (property "Value" "+5V" (at 0 3.2 0) (effects (font (size 1.4 1.4))))
      (symbol "fz:PWR_5V_0_1"
        (polyline (pts (xy -0.76 1.27) (xy 0 2.54) (xy 0.76 1.27)) (stroke (width 0.3) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0.3) (type default)) (fill (type none)))
      )
      (symbol "fz:PWR_5V_1_1"
        (pin power_in line (at 0 0 90) (length 0) (name "+5V" (effects (font (size 1.0 1.0)))) (number "1" (effects (font (size 1.0 1.0)))))
      )
    )
    (symbol "fz:PWR_GND" (power) (pin_names (offset 0)) (in_bom no) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.5 0) (effects (font (size 1.0 1.0)) hide))
      (property "Value" "GND" (at 0 -3.8 0) (effects (font (size 1.4 1.4))))
      (symbol "fz:PWR_GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27)) (stroke (width 0.3) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27)) (stroke (width 0.3) (type default)) (fill (type none)))
        (polyline (pts (xy -0.76 -1.9) (xy 0.76 -1.9)) (stroke (width 0.3) (type default)) (fill (type none)))
        (polyline (pts (xy -0.25 -2.5) (xy 0.25 -2.5)) (stroke (width 0.3) (type default)) (fill (type none)))
      )
      (symbol "fz:PWR_GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) (name "GND" (effects (font (size 1.0 1.0)))) (number "1" (effects (font (size 1.0 1.0)))))
      )
    )'''

# ---------------------------------------------------------------------------
# Platzierung
# ---------------------------------------------------------------------------
INST = {}      # ref -> (lib, value, x, y, nets)
ORDER = []     # Reihenfolge
WIRES = []     # Liste von Punktlisten [(x,y),...]
LABELS = []    # (net, x, y, side)
PWRS = []      # (type '5V'/'GND', x, y)
TEXTS = []     # (text, x, y, size)
SKIP = set()   # (ref, pinnum) -> nicht automatisch labeln/powern

def place(ref, lib, value, x, y, nets):
    INST[ref] = (lib, value, x, y, nets); ORDER.append(ref)

def note(t, x, y, s=2.2):
    TEXTS.append((t, x, y, s))

def pin_abs(ref, pinnum):
    lib, value, x, y, nets = INST[ref]
    coords, _ = geom(lib)
    lx, ly, rot, p = coords[pinnum]
    return (x + lx, y - ly, 'L' if lx < 0 else 'R')

def wire(*pts):
    WIRES.append(list(pts))

P5, GND = "+5V", "GND"

# ================= ZEITBASIS (Teil 1) =================
note("ZEITBASIS (Teil 1)", 25, 18)
place("Q1","XTAL","3.2768MHz", 30, 35, {1:"OSC1",2:"OSC2"})
place("R2","R_sym","1M",       30, 48, {1:"OSC1",2:"OSC2"})
place("C2","C_sym","100p",     30, 61, {1:"OSC1",2:GND})
place("R1","R_sym","2k2",      30, 74, {1:"OSC2",2:"OSC3"})
place("C1","C_sym","100p",     30, 87, {1:"OSC3",2:GND})
place("IC3","IC_4060","74HC4060", 90, 55, {16:P5,8:GND,3:"F200",11:"OSC1",10:"OSC2",9:"OSC3",12:GND})
place("IC2","IC_7474","74HC74", 160, 60,
      {3:"F200",2:"Q1N",6:"Q1N",5:"F100",1:P5,4:P5,7:GND,14:P5,10:"F100",11:"TORN",8:"TORN",9:"TOR",12:P5,13:P5})

# ================= RESET (Teil 6) =================
note("RESET-ERZEUGUNG (Teil 6)", 220, 18)
place("C3","C_sym","220p",  225, 40, {1:"TORN",2:"RESET"})
place("R3","R_sym","10k",   225, 53, {1:"RESET",2:GND})
place("D1","DIODE","1N4148",225, 66, {1:GND,2:"RESET"})

# ================= EINGANGSSTUFE + VORTEILER (Teil 5/3) =================
note("EINGANGSSTUFE + VORTEILER (Teil 5/3)", 25, 108)
note("FE_IN = Signaleingang", 25, 118, 1.6)
place("C4","C_sym","100n", 30, 130, {1:"FE_IN",2:"T1B"})
place("R5","R_sym","12k",  30, 143, {1:P5,2:"T1B"})
place("T1","Q_NPN","SF245",90, 135, {1:"T1B",2:"T1C",3:GND})
place("R4","R_sym","1k2",  30, 156, {1:P5,2:"T1C"})
place("C5","C_sym","100n", 30, 169, {1:"T1C",2:"DIV_IN"})
place("R6","R_sym","150k", 30, 182, {1:P5,2:"DIV_IN"})
place("R7","R_sym","150k", 30, 195, {1:"DIV_IN",2:GND})
place("IC1","IC_4017","74HC4017", 150, 165, {16:P5,8:GND,14:"DIV_IN",13:GND,15:GND,12:"FE_DIV10"})

# ================= ZAEHLERKETTE + ANZEIGE (Teil 3/4) =================
note("ZAEHLERKETTE + ANZEIGE (Teil 3/4)  -  5 Stellen, Carry-Kette + Segmentleitungen", 205, 104)
clk_in = ["FE_DIV10","CAR1","CAR2","CAR3","CAR4"]
co_out = ["CAR1","CAR2","CAR3","CAR4","CAR5"]
segs = ["a","b","c","d","e","f","g"]
x_cnt, x_disp = 235, 300
row_y = [120, 160, 200, 240, 280]
for i in range(5):
    ic, disp, st = f"IC{4+i}", f"DISP{i+1}", i+1
    yc = row_y[i]
    yd = yc + 1.27   # Segmentpins ausrichten
    segmap = {s: f"S{st}{s}" for s in segs}
    place(ic, "IC_4026", "4026", x_cnt, yc,
          {16:P5,8:GND,1:clk_in[i],2:"TOR",3:"TOR",15:"RESET",5:co_out[i],
           10:segmap["a"],12:segmap["b"],13:segmap["c"],9:segmap["d"],
           11:segmap["e"],6:segmap["f"],7:segmap["g"]})
    place(disp, "DISP_7SEG", f"7SEG-{st}", x_disp, yd,
          {1:segmap["a"],2:segmap["b"],3:segmap["c"],4:segmap["d"],
           5:segmap["e"],6:segmap["f"],7:segmap["g"],8:GND})

# ---- Segmentleitungen als echte Draehte (Zaehler rechts -> Anzeige links) ----
segpin_ic   = {"a":10,"b":12,"c":13,"d":9,"e":11,"f":6,"g":7}
segpin_disp = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7}
for i in range(5):
    ic, disp = f"IC{4+i}", f"DISP{i+1}"
    for s in segs:
        ax, ay, _ = pin_abs(ic, segpin_ic[s])
        bx, by, _ = pin_abs(disp, segpin_disp[s])
        wire((ax, ay), (bx, by))
        SKIP.add((ic, segpin_ic[s])); SKIP.add((disp, segpin_disp[s]))

# ---- Carry-Kette als echte Draehte (CO links -> naechste CLK links) ----
for i in range(4):
    ic, nic = f"IC{4+i}", f"IC{5+i}"
    cox, coy, _ = pin_abs(ic, 5)    # CO (links)
    clx, cly, _ = pin_abs(nic, 1)   # CLK (links)
    lane = min(cox, clx) - 8
    wire((cox, coy), (lane, coy), (lane, cly), (clx, cly))
    SKIP.add((ic, 5)); SKIP.add((nic, 1))

# ================= STROMVERSORGUNG (Teil 7) =================
note("STROMVERSORGUNG (Teil 7)", 25, 230)
note("UB = +Ub (DC-Buchse BU1, 7..20V)", 25, 240, 1.6)
place("U1","REG_7805","7805", 70, 258, {1:"UB",2:GND,3:P5})
place("C7","C_sym","47u",  30, 275, {1:"UB",2:GND})
place("C9","C_sym","47u",  30, 288, {1:P5,2:GND})
place("C11","C_sym","47u", 30, 301, {1:P5,2:GND})
place("C6","C_sym","100n", 120, 275, {1:P5,2:GND})
place("C8","C_sym","100n", 120, 288, {1:P5,2:GND})
place("C10","C_sym","100n",120, 301, {1:P5,2:GND})
place("C12","C_sym","100n",120, 314, {1:P5,2:GND})

# ---------------------------------------------------------------------------
# Automatik: Power-Symbole fuer +5V/GND, Labels fuer restliche Signale
# ---------------------------------------------------------------------------
def build_connections():
    for ref in ORDER:
        lib, value, x, y, nets = INST[ref]
        coords, _ = geom(lib)
        for num, (lx, ly, rot, p) in coords.items():
            if (ref, num) in SKIP:
                continue
            net = nets.get(num)
            if net is None:
                continue
            ax, ay = x + lx, y - ly
            if net == P5:
                wire((ax, ay), (ax, ay - 5)); PWRS.append(("5V", ax, ay - 5))
            elif net == GND:
                wire((ax, ay), (ax, ay + 5)); PWRS.append(("GND", ax, ay + 5))
            else:
                if lx < 0:
                    ex = ax - STUB; side = 'L'
                else:
                    ex = ax + STUB; side = 'R'
                wire((ax, ay), (ex, ay))
                LABELS.append((net, ex, ay, side))

# ---------------------------------------------------------------------------
# KiCad-Ausgabe
# ---------------------------------------------------------------------------
ROOT = U()
PROJECT = "freuenzzaehler"
_pwrn = [0]

def emit_instance(ref):
    lib, value, x, y, nets = INST[ref]
    coords, half_h = geom(lib)
    o = []
    o.append(f'  (symbol (lib_id "fz:{lib}") (at {x:.2f} {y:.2f} 0) (unit 1) (in_bom yes) (on_board yes) (uuid "{U()}")')
    o.append(f'    (property "Reference" "{ref}" (at {x-HW:.2f} {y-half_h-1.2:.2f} 0) (effects (font (size 1.4 1.4)) (justify left)))')
    o.append(f'    (property "Value" "{value}" (at {x-HW:.2f} {y+half_h+2.6:.2f} 0) (effects (font (size 1.2 1.2)) (justify left)))')
    o.append(f'    (instances (project "{PROJECT}" (path "/{ROOT}" (reference "{ref}") (unit 1))))')
    o.append('  )')
    return "\n".join(o)

def emit_power(ptype, x, y):
    _pwrn[0] += 1
    lib = "fz:PWR_5V" if ptype == "5V" else "fz:PWR_GND"
    val = "+5V" if ptype == "5V" else "GND"
    vy = y - 3.2 if ptype == "5V" else y + 3.6
    o = []
    o.append(f'  (symbol (lib_id "{lib}") (at {x:.2f} {y:.2f} 0) (unit 1) (in_bom no) (on_board yes) (uuid "{U()}")')
    o.append(f'    (property "Reference" "#PWR0{_pwrn[0]}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.0 1.0)) hide))')
    o.append(f'    (property "Value" "{val}" (at {x:.2f} {vy:.2f} 0) (effects (font (size 1.3 1.3))))')
    o.append(f'    (instances (project "{PROJECT}" (path "/{ROOT}" (reference "#PWR0{_pwrn[0]}") (unit 1))))')
    o.append('  )')
    return "\n".join(o)

def emit():
    L = []
    L.append('(kicad_sch (version 20230121) (generator eeschema)')
    L.append(f'  (uuid "{ROOT}")')
    L.append('  (paper "A2")')
    L.append('  (title_block (title "Frequenzzaehler (BX-020-Nachbau) - Gesamtschaltplan") '
             '(company "Tutorial FreuenzZaehler") (comment 1 "Power-Symbole + Netz-Labels; Segmente/Carry verdrahtet"))')
    L.append('  (lib_symbols')
    for name in SYMS:
        L.append(emit_lib_symbol(name))
    L.append(POWER_LIB)
    L.append('  )')
    for t, x, y, s in TEXTS:
        L.append(f'  (text "{t}" (at {x:.2f} {y:.2f} 0) (effects (font (size {s:.2f} {s:.2f})) (justify left bottom)) (uuid "{U()}"))')
    for pts in WIRES:
        for a, b in zip(pts, pts[1:]):
            L.append(f'  (wire (pts (xy {a[0]:.2f} {a[1]:.2f}) (xy {b[0]:.2f} {b[1]:.2f})) '
                     f'(stroke (width 0.1524) (type default)) (uuid "{U()}"))')
    for net, x, y, side in LABELS:
        just = "right" if side == 'L' else "left"
        rot = 180 if side == 'L' else 0
        L.append(f'  (label "{net}" (at {x:.2f} {y:.2f} {rot}) '
                 f'(effects (font (size {LBL:.2f} {LBL:.2f})) (justify {just} bottom)) (uuid "{U()}"))')
    for ref in ORDER:
        L.append(emit_instance(ref))
    for ptype, x, y in PWRS:
        L.append(emit_power(ptype, x, y))
    L.append('  (sheet_instances (path "/" (page "1")))')
    L.append(')')
    return "\n".join(L) + "\n"

# ---------------------------------------------------------------------------
# PNG-Vorschau (Layout-Kontrolle)
# ---------------------------------------------------------------------------
def render_preview(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(22, 18))
    for ref in ORDER:
        lib, value, x, y, nets = INST[ref]
        coords, half_h = geom(lib)
        ax.add_patch(Rectangle((x-HW, y-half_h), 2*HW, 2*half_h,
                     fill=True, facecolor="#fff7cc", edgecolor="#884400", lw=1.2, zorder=2))
        ax.text(x, y-half_h-1.6, ref, fontsize=8, color="#aa0000", ha="center", va="bottom", zorder=4)
        ax.text(x, y, value, fontsize=6, color="#333333", ha="center", va="center", zorder=4)
        for num, (lx, ly, rot, p) in coords.items():
            ax.text(x+lx*0.78, y-ly, p[1], fontsize=4.5, color="#005577",
                    ha="right" if lx < 0 else "left", va="center", zorder=4)
    for pts in WIRES:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        ax.plot(xs, ys, color="#0066aa", lw=0.8, zorder=1)
    for net, x, y, side in LABELS:
        ax.text(x + (-0.6 if side == 'L' else 0.6), y, net, fontsize=5.5, color="#007700",
                ha="right" if side == 'L' else "left", va="center", zorder=5)
        ax.plot([x], [y], marker='o', ms=1.5, color="#007700", zorder=5)
    for ptype, x, y in PWRS:
        c = "#cc0000" if ptype == "5V" else "#000000"
        m = "^" if ptype == "5V" else "v"
        ax.plot([x], [y], marker=m, ms=5, color=c, zorder=5)
        ax.text(x, y + (-1.4 if ptype == "5V" else 1.6), ptype, fontsize=4.5, color=c,
                ha="center", va="bottom" if ptype == "5V" else "top", zorder=5)
    for t, x, y, s in TEXTS:
        ax.text(x, y, t, fontsize=7, color="#222222", ha="left", va="bottom",
                fontweight="bold", zorder=6)
    ax.set_aspect("equal"); ax.invert_yaxis(); ax.autoscale()
    ax.margins(0.03); ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    build_connections()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "freuenzzaehler.kicad_sch")
    with open(out, "w", encoding="utf-8") as f:
        f.write(emit())
    print("geschrieben:", out)
    print("Instanzen:", len(ORDER), "Symbole:", len(SYMS)+2,
          "Draehte:", sum(len(p)-1 for p in WIRES), "Labels:", len(LABELS), "Power:", len(PWRS))
    try:
        prev = os.path.join(here, "preview.png")
        render_preview(prev)
        print("Vorschau:", prev)
    except Exception as e:
        print("Vorschau fehlgeschlagen:", e)

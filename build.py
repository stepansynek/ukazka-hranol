#!/usr/bin/env python3
"""Sestaví web HRANOL ze složky src/.

  python3 build.py              statické stránky do kořene projektu (index.html, vyroba.html, …)
  python3 build.py --spa OUT    všechny stránky v jednom HTML souboru (náhled, přepínání přes #)

Obsah stránek je v src/pages/<id>.html. První řádek je komentář s JSON metadaty.
Odkazy mezi stránkami se píšou jako href="@stroje" nebo href="@vyroba#frezovani",
build je přepíše podle výstupu. Zástupné značky {{capacity}}, {{machines}} a {{status}} vyplní data níže.
Týdny kapacity se počítají od data sestavení; main.js je v prohlížeči posune na aktuální týden.
"""
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

PAGES = ["domu", "vyroba", "stroje", "reference", "o-firme", "poptavka"]
FILES = {"domu": "index.html", "vyroba": "vyroba.html", "stroje": "stroje.html",
         "reference": "reference.html", "o-firme": "o-firme.html", "poptavka": "poptavka.html"}
NAV = [("vyroba", "Výroba"), ("stroje", "Strojový park"), ("reference", "Reference"), ("o-firme", "O firmě")]

# Písmo Archivo a three.js jsou v assets/, web nenačítá nic z cizích serverů.
FONTS = ["assets/fonts/archivo-latin.woff2", "assets/fonts/archivo-latin-ext.woff2"]
THREE = "assets/vendor/three.min.js"
# Kde web poběží (README, sekce Přidání do portfolia). Potřebují ho og:image a JSON-LD, které chtějí plné adresy.
BASE_URL = "https://stepansynek.com/ukazka-hranol/"

# ---------------------------------------------------------------- data

# Vytížení v % podle technologie a týdne (týden 0 = aktuální). Hodiny = kapacita za týden (stroje × 2 směny × 40 h).
CAPACITY = [
    ("5osé frézování", 240, [96, 94, 88, 62, 55, 48, 40, 35]),
    ("3osé frézování", 240, [92, 86, 71, 66, 60, 52, 45, 38]),
    ("Soustružení", 320, [98, 97, 92, 85, 80, 72, 64, 50]),
    ("Broušení", 80, [88, 82, 78, 64, 58, 52, 46, 40]),
    ("Svařování", 320, [92, 90, 86, 80, 74, 66, 58, 50]),
    ("Montáž", 160, [70, 78, 84, 80, 72, 64, 56, 48]),
]
FREE_BELOW = 75
MONTHS = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]


def week_start(offset=0):
    today = dt.date.today()
    return today - dt.timedelta(days=today.weekday()) + dt.timedelta(weeks=offset)


def first_free(values):
    return next((i for i, v in enumerate(values) if v < FREE_BELOW), None)


def short_date(d):
    return f"{d.day}.&nbsp;{d.month}."

# id, název, technologie (filtr), popis technologie, druh obálky, obálka, vybavení, ks, rok
MACHINES = [
    ("dmu65", "DMG MORI DMU 65 monoBLOCK", "frezovani", "5osé frézování", "box", (735, 650, 560),
     "Heidenhain TNC 640, sonda Renishaw", 2, "2019, 2022"),
    ("hermle", "Hermle C 42 U", "frezovani", "5osé frézování", "box", (800, 800, 550),
     "paletový zásobník na 12 palet, provoz bez obsluhy", 1, "2023"),
    ("mcv1270", "Kovosvit MAS MCV 1270", "frezovani", "3osé frézování", "box", (1270, 610, 720),
     "4. osa, otočný stůl", 3, "2011–2017"),
    ("qt250", "Mazak QUICK TURN 250MY", "soustruzeni", "soustružení", "round", (380, 1000),
     "osa Y, poháněné nástroje, podavač tyčí do Ø 65 mm", 2, "2018, 2021"),
    ("sp430", "Kovosvit MAS SP 430 SY", "soustruzeni", "soustružení", "round", (430, 1100),
     "protivřeteno, osa Y", 2, "2016"),
    ("s33", "Studer S33", "brouseni", "broušení na kulato", "round", (350, 1000),
     "vnější i vnitřní broušení", 1, "2020"),
    ("tps400", "Fronius TPS 400i", "svarovani", "svařování MIG/MAG", "weld", (2500,),
     "pulzní svařování, polohovadla do 2,5 t", 4, "2015–2021"),
    ("magicwave", "Fronius MagicWave 230i", "svarovani", "svařování TIG", "weld", (800,),
     "nerez a hliník", 2, "2021"),
    ("contura", "Zeiss CONTURA 10/12/6", "mereni", "3D měření", "box", (1000, 1200, 600),
     "MPE_E 1,8 + L/300 µm, měrovna 20 ± 1 °C", 1, "2023"),
]
FILTERS = [("all", "Vše"), ("frezovani", "Frézování"), ("soustruzeni", "Soustružení"),
           ("brouseni", "Broušení"), ("svarovani", "Svařování"), ("mereni", "Měření")]

# Půdorys haly 80 × 40 m (3 200 m²), souřadnice v metrech, x podél haly od skladu k expedici.
# id, název, x, y, šířka, hloubka, m², lidí, popis, kotva popisku na šířku (x, y), kotva na výšku (x, y) po transpozici
ZONES = [
    ("sklad", "Sklad a dělení", 0, 0, 12, 40, 480, 3,
     "Tyče, desky a jekly s atestem 3.1. Pásová pila nařeže přířezy na míru, zbytky evidujeme podle tavby.",
     (1.6, 29.5), (22, 6.4)),
    ("obrobna", "Obrobna", 12, 0, 36, 26, 936, 14,
     "Jedenáct CNC strojů ve dvou řadách: pětiosá centra, tříosé frézky, soustruhy a bruska na kulato.",
     (13.6, 11.6), (8, 21)),
    ("svarovna", "Svařovna", 48, 0, 18, 24, 432, 8,
     "Šest svařovacích pracovišť s odsáváním a žíhací pec. Svařenec po žíhání jede rovnou do obrobny.",
     (58.4, 18.6), (13, 60.6)),
    ("montaz", "Montáž", 66, 0, 14, 24, 336, 6,
     "Montážní stoly a zkušební stanoviště pro podsestavy do 800 kg.",
     (67.6, 13.8), (11.2, 72)),
    ("kancelare", "Kanceláře", 12, 26, 24, 14, 336, 10,
     "Nacenění, programování CNC, nákup a kvalita. Technik má výrobu hned za dveřmi.",
     (13.6, 31.4), (27.6, 17)),
    ("merovna", "Měrovna", 36, 26, 12, 14, 168, 2,
     "Klimatizovaná místnost s teplotou 20 ± 1 °C, 3D měřicí stroj a drsnoměr.",
     (37.4, 29.4), (27.6, 39.6)),
    ("expedice", "Expedice", 48, 24, 32, 16, 512, 3,
     "Balení, měřicí protokoly a nakládka. Dvě rampy, pro kamion i pro dodávku.",
     (49.6, 29.4), (26, 55)),
]
# stroj (id v tabulce strojů nebo None), popisek, x, y, šířka, hloubka
HALL_ITEMS = [
    ("dmu65", "DMU 65", 14, 2, 3.2, 3.6), ("dmu65", "DMU 65", 18.6, 2, 3.2, 3.6),
    ("hermle", "Hermle C 42", 23.4, 2, 5.4, 4.2),
    ("mcv1270", "MCV 1270", 30.6, 2, 4.4, 3.2), ("mcv1270", "MCV 1270", 36.4, 2, 4.4, 3.2), ("mcv1270", "MCV 1270", 42.2, 2, 4.4, 3.2),
    ("qt250", "QT 250", 14, 20.5, 3.2, 2.2), ("qt250", "QT 250", 18.6, 20.5, 3.2, 2.2),
    ("sp430", "SP 430", 23.4, 20.3, 4.2, 2.4), ("sp430", "SP 430", 29, 20.3, 4.2, 2.4),
    ("s33", "Studer S33", 35, 20.3, 3.8, 2.4),
    ("tps400", "TPS 400i", 49.5, 2, 4, 4), ("tps400", "TPS 400i", 55, 2, 4, 4), ("tps400", "TPS 400i", 60.5, 2, 4, 4),
    ("tps400", "TPS 400i", 49.5, 8.5, 4, 4), ("magicwave", "MagicWave", 55, 8.5, 4, 4), ("magicwave", "MagicWave", 60.5, 8.5, 4, 4),
    (None, "žíhací pec", 49.5, 17, 8, 4.5),
    ("contura", "CONTURA", 44.4, 34, 2.6, 3.6),
    (None, "pila", 5, 18.5, 3.6, 1.8),
    (None, "", 1, 2, 1.6, 13), (None, "", 1, 24, 1.6, 13), (None, "", 9.5, 2, 1.6, 10),
    (None, "", 68, 3, 4, 2), (None, "", 74, 3, 4, 2), (None, "", 68, 9, 4, 2), (None, "", 74, 9, 4, 2),
    (None, "", 68, 20, 10, 3),
]
HALL_DOORS = [(0, 16.5, 4), (80, 27, 3), (80, 33.5, 3)]  # vrata na čelních stěnách: x stěny, y, šířka (vjezd materiálu, dvě rampy)

# Vyhledávání (⌘K): skupina, název, stránka, kotva, doplňující slova
SEARCH = [
    ("Stránky", "Úvod", "domu", "", "domů hlavní stránka"),
    ("Stránky", "Výroba", "vyroba", "", "technologie služby"),
    ("Stránky", "Strojový park", "stroje", "", "stroje vybavení"),
    ("Stránky", "Reference", "reference", "", "zakázky případové studie"),
    ("Stránky", "O firmě", "o-firme", "", "historie lidé"),
    ("Stránky", "Poptávka", "poptavka", "", "nacenění cena výkres kontakt"),
    ("Technologie", "Frézování", "vyroba", "frezovani", "cnc 5osé 3osé fréza obrábění hliník skříně"),
    ("Technologie", "Soustružení", "vyroba", "soustruzeni", "cnc soustruh hřídel"),
    ("Technologie", "Broušení na kulato", "vyroba", "brouseni", "bruska drsnost ra"),
    ("Technologie", "Svařování", "vyroba", "svarovani", "mig mag tig svářeč rám"),
    ("Technologie", "Montáž podsestav", "vyroba", "montaz", "sestava kompletace"),
    ("Technologie", "Povrchové úpravy", "vyroba", "upravy", "elox zinek kalení lakování nikl hliník nitridace"),
    ("Technologie", "Materiály", "vyroba", "materialy", "ocel nerez hliník mosaz bronz plast pom peek 7075 6082 1.4301 42crmo4"),
    ("Technologie", "Kvalita a dokumentace", "vyroba", "kvalita", "protokol atest iso 3.1"),
    ("Nástroje", "Vejde se váš díl?", "stroje", "overeni", "rozměry obálka pracovní prostor"),
    ("Nástroje", "Volná kapacita", "domu", "kapacita", "vytížení termín volno týden"),
    ("Firma", "Hala", "o-firme", "hala", "půdorys provoz obrobna svařovna měrovna sklad expedice"),
    ("Firma", "Lidé a kontakty", "o-firme", "lide", "kalous svobodová hrubý kontakt technik kvalita telefon"),
    ("Firma", "Kariéra", "o-firme", "kariera", "práce volná místa operátor svářeč"),
    ("Firma", "Certifikace", "o-firme", "certifikace", "iso 9001 3834"),
    ("Firma", "Časté otázky", "poptavka", "faq", "nda formáty minimální množství export"),
    ("Reference", "Formátové díly z hliníku", "reference", "ref-baleni", "balicí linky hvězdice 7075"),
    ("Reference", "Svařované rámy", "reference", "ref-ramy", "zemědělská technika rám s355"),
    ("Reference", "Prototypy chapadel", "reference", "ref-chapadla", "robotika chapadlo elox pom"),
    ("Reference", "Pístnice a víka válců", "reference", "ref-hydraulika", "hydraulika chrom broušení 42crmo4"),
] + [("Stroje", name, "stroje", f"stroj-{mid}", f"{tech} {kw}")
     for mid, name, _, tech, _, _, kw, _, _ in MACHINES]


def build_capacity():
    """Tabulka vytížení. Data týdnů a texty bublin dopočítá main.js podle dnešního data."""
    head = "".join(
        f'<th scope="col" role="columnheader" data-week="{i}"><span class="cap__wk">T{week_start(i).isocalendar()[1]}</span>'
        f'<span class="cap__date">{short_date(week_start(i))}</span></th>'
        for i in range(8))
    rows = []
    for name, hours, values in CAPACITY:
        ff = first_free(values)
        when = (f'<span class="cap__when" data-week="{ff}">volno od {short_date(week_start(ff))}</span>'
                if ff is not None else '<span class="cap__when">bez volna</span>')
        cells = []
        for i, v in enumerate(values):
            free = v < FREE_BELOW
            free_h = round(hours * (100 - v) / 100)
            cells.append(
                f'<td role="cell" class="cap__cell{" is-free" if free else ""}" tabindex="0" data-week="{i}" '
                f'data-v="{v}" data-free-h="{free_h}">'
                f'<span class="cap__bar" style="--v:{v}"></span>'
                f'<span class="sr-only">{v} %{", volno" if free else ""}</span></td>')
        rows.append(f'<tr role="row"><th scope="row" role="rowheader"><span class="cap__name">{name}</span>{when}</th>{"".join(cells)}</tr>')
    # Role zůstávají i na mobilu, kde se tabulka přeskládá do mřížky (jinak by prohlížeč zahodil sémantiku tabulky).
    return (f'<table class="cap__table" role="table"><caption class="sr-only">Vytížení výroby podle technologie '
            f'a týdne v procentech</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader" class="cap__corner">Technologie</th>'
            f'{head}</tr></thead><tbody role="rowgroup">{"".join(rows)}</tbody></table>')


def build_status():
    """Řádek v úvodu: nejbližší volno na pětiosém frézování a jeho vytížení na osm týdnů."""
    name, _, values = CAPACITY[0]
    ff = first_free(values)
    d = week_start(ff)
    bars = "".join(f'<i{" class=is-free" if v < FREE_BELOW else ""} style="--v:{v}"></i>' for v in values)
    return (f'<a class="status" href="@domu#kapacita" data-status data-week="{ff}">'
            f'<span class="status__bars" aria-hidden="true">{bars}</span>'
            f'<span>Volno na pětiosém frézování od <span data-status-date>{d.day}.&nbsp;{MONTHS[d.month - 1]}</span></span></a>')


def fmt_env(kind, env):
    if kind == "round":
        return f"Ø {env[0]} × {env[1]:,} mm".replace(",", " ")
    if kind == "weld":
        return f"do {env[0]:,} kg".replace(",", " ")
    return " × ".join(f"{v:,}".replace(",", " ") for v in env) + " mm"


def build_machines():
    filters = "".join(
        f'<button type="button" class="chip" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">'
        f'{label} <span class="chip__count">'
        f'{len(MACHINES) if key == "all" else sum(1 for m in MACHINES if m[2] == key)}</span></button>'
        for key, label in FILTERS)
    rows = "".join(
        f'<tr id="stroj-{mid}" data-tech="{group}" data-kind="{kind}" data-env="{",".join(map(str, env))}" data-count="{count}">'
        f'<td><span class="mt__name">{name}</span><span class="mt__tech">{tech}</span>'
        f'<span class="mt__fit" aria-hidden="true">vejde se</span></td>'
        f'<td class="data">{fmt_env(kind, env)}</td><td class="mt__note">{note}</td>'
        f'<td class="data num">{count}</td><td class="data">{year}</td></tr>'
        for mid, name, group, tech, kind, env, note, count, year in MACHINES)
    return (f'<div class="filters" role="toolbar" aria-label="Filtrovat stroje podle technologie">{filters}</div>'
            f'<div class="table-scroll"><table class="mtable"><caption class="sr-only">Stroje a jejich pracovní rozsahy</caption>'
            f'<thead><tr><th scope="col">Stroj</th><th scope="col">Pracovní rozsah</th><th scope="col">Vybavení</th>'
            f'<th scope="col" class="num">Ks</th><th scope="col">Rok</th></tr></thead><tbody>{rows}</tbody></table></div>')


def people_word(n):
    return "člověk" if n == 1 else "lidé" if n < 5 else "lidí"


def zone_of(x, y):
    return next(z[0] for z in ZONES if z[2] <= x < z[2] + z[4] and z[3] <= y < z[3] + z[5])


def hall_svg(portrait):
    """Půdorys jako SVG. Na výšku se hala transponuje (sklad nahoře, expedice dole), popisky zůstávají vodorovně.
    Každá zóna je skupina se svými stroji, takže najetí na stroj zónu nezhasne."""
    k = 10  # jednotek na metr
    tr = (lambda x, y, w, h: (y, x, h, w)) if portrait else (lambda x, y, w, h: (x, y, w, h))
    W, H = (40, 80) if portrait else (80, 40)
    # Velikosti v metrech půdorysu: na šířku se plán kreslí zhruba 0,8–1 px na jednotku, popisky strojů tak mají aspoň 11 px.
    fs_name, fs_meta, fs_item = (1.6, 1.3, 0) if portrait else (1.3, 1.15, 1.3)
    out = [f'<svg class="hall__svg hall__svg--{"tall" if portrait else "wide"}" viewBox="-6 -6 {W * k + 12} {H * k + 12}" aria-hidden="true">']
    for zid, name, x, y, w, h, area, ppl, _, land, tall in ZONES:
        rx, ry, rw, rh = tr(x, y, w, h)
        lx, ly = tall if portrait else land
        out.append(f'<g class="hall__zone" data-zone="{zid}"><rect class="hall__area" x="{rx * k + 4}" y="{ry * k + 4}" '
                   f'width="{rw * k - 8}" height="{rh * k - 8}"/>')
        for mid, label, ix, iy, iw, ih in HALL_ITEMS:
            if zone_of(ix, iy) != zid:
                continue
            bx, by, bw, bh = tr(ix, iy, iw, ih)
            cls = "hall__machine" if mid else ("hall__fixture" if label else "hall__rack")
            rect = f'<rect class="{cls}" x="{bx * k}" y="{by * k}" width="{bw * k}" height="{bh * k}"/>'
            if mid:
                text = (f'<text class="hall__label" x="{(bx + bw / 2) * k}" y="{(by + bh) * k + fs_item * k * 1.15}" text-anchor="middle" '
                        f'font-size="{fs_item * k}">{label}</text>') if fs_item else ""
                out.append(f'<a href="@stroje#stroj-{mid}" tabindex="-1" class="hall__link"><title>{label}</title>{rect}{text}</a>')
            else:
                text = (f'<text class="hall__fixture-label" x="{(bx + bw / 2) * k}" y="{(by + bh / 2) * k}" text-anchor="middle" '
                        f'dominant-baseline="central" font-size="{1.1 * k}">{label}</text>') if label and fs_item else ""
                out.append(rect + text)
        out.append(f'<text x="{lx * k}" y="{ly * k}" class="hall__name" font-size="{fs_name * k}">{name}</text>'
                   f'<text x="{lx * k}" y="{(ly + fs_meta * 1.7) * k}" class="hall__meta" font-size="{fs_meta * k}">{area} m², {ppl} {people_word(ppl)}</text></g>')
    out.append(f'<rect class="hall__wall" x="0" y="0" width="{W * k}" height="{H * k}"/>')
    for x, y, w in HALL_DOORS:
        if portrait:
            out.append(f'<rect class="hall__door" x="{y * k}" y="{x * k - 4}" width="{w * k}" height="8"/>')
        else:
            out.append(f'<rect class="hall__door" x="{x * k - 4}" y="{y * k}" width="8" height="{w * k}"/>')
    out.append("</svg>")
    return "".join(out)


def build_hall():
    zones = []
    for zid, name, _, _, _, _, area, ppl, desc, _, _ in ZONES:
        machines = []
        seen = set()
        for mid, label, *_ in HALL_ITEMS:
            if not mid or mid in seen:
                continue
            m = next(m for m in MACHINES if m[0] == mid)
            hx, hy = next((it[2], it[3]) for it in HALL_ITEMS if it[0] == mid)
            if zone_of(hx, hy) == zid:
                seen.add(mid)
                machines.append(f'<a href="@stroje#stroj-{mid}">{m[1]}</a>{f" ({m[7]}×)" if m[7] > 1 else ""}')
        links = f'<p class="zones__machines">{", ".join(machines)}</p>' if machines else ""
        zones.append(f'<li data-zone="{zid}"><h3>{name}</h3><p class="zones__meta">{area} m², {ppl} {people_word(ppl)}</p>'
                     f'<p>{desc}</p>{links}</li>')
    return (f'<div class="hall" data-hall><div class="hall__plan">{hall_svg(False)}{hall_svg(True)}</div>'
            f'<ul class="zones">{"".join(zones)}</ul></div>')


# ---------------------------------------------------------------- šablona

LOGO = json.loads((SRC / "logo.json").read_text(encoding="utf-8"))


def logo_svg(label="HRANOL"):
    a11y = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="logo" viewBox="{LOGO["viewBox"]}" {a11y}>'
            f'<g fill="currentColor">{LOGO["ink"]}</g><path class="logo__cut" d="{LOGO["strip"]}"/></svg>')


def header():
    """Čelní panel stánku: logo, navigace, hledání a výzva k poptávce."""
    items = "".join(f'<li><a href="@{pid}" data-nav="{pid}">{label}</a></li>' for pid, label in NAV)
    return f'''<header class="fascia">
  <div class="stand fascia__bar">
    <a class="fascia__brand" href="@domu" aria-label="HRANOL, úvodní stránka">{logo_svg("")}</a>
    <nav class="nav" id="nav" aria-label="Hlavní navigace"><ul>{items}<li class="nav__cta"><a href="@poptavka" data-nav="poptavka">Poptávka</a></li></ul></nav>
    <button class="search-btn" type="button" data-palette-open aria-haspopup="dialog" aria-keyshortcuts="Meta+K Control+K" aria-label="Hledat na webu">
      <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5"/><path d="m12.5 12.5 5 5"/></svg>
      <span class="search-btn__label">Hledat</span><kbd data-kbd>Ctrl K</kbd>
    </button>
    <a class="btn btn--ink btn--sm fascia__cta" href="@poptavka" data-nav="poptavka">Poptávka</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>'''


def footer(page=None):
    """Závěrečná stěna s výzvou k nahrání výkresu a pod ní patička. Na stránce poptávky stěna chybí, formulář je hned nad ní."""
    pages = "".join(f'<li><a href="@{pid}">{label}</a></li>' for pid, label in [("domu", "Úvod")] + NAV + [("poptavka", "Poptávka")])
    cta = "" if page == "poptavka" else '''<section class="close" aria-labelledby="close-title" data-ftr-cta>
  <div class="stand">
    <div class="wall close__wall">
      <div class="panel panel--2 close__claim"><h2 class="letter close__title" id="close-title">Máte výkres? Cenu a termín znáte do 48 hodin.</h2></div>
      <div class="panel close__act">
        <a class="btn btn--ink" href="@poptavka">Nahrát výkres</a>
        <p>Nebo zavolejte technikovi na <a href="tel:+420517000100">+420 517 000 100</a>.</p>
      </div>
    </div>
  </div>
</section>
'''
    return f'''{cta}<footer class="ftr">
  <div class="stand stand--inset">
    <div class="ftr__grid">
      <div class="ftr__brand">
        <a class="fascia__brand" href="@domu" aria-label="HRANOL, úvodní stránka">{logo_svg("")}</a>
        <p>Přesné obrábění a svařence pro výrobce strojů. Rousínov u Brna, od roku 1994.</p>
      </div>
      <nav aria-label="Stránky"><h2 class="ftr__h">Stránky</h2><ul>{pages}</ul></nav>
      <div><h2 class="ftr__h">Kontakt</h2><p><a href="tel:+420517000100">+420 517 000 100</a><br><a href="mailto:poptavky@hranol-obrabeni.cz">poptavky@hranol-obrabeni.cz</a><br>Průmyslová 1187, 683 01 Rousínov</p></div>
      <div><h2 class="ftr__h">Provoz</h2><p>Výroba Po–Pá 6:00–22:00<br>Kancelář Po–Pá 7:00–15:30</p></div>
    </div>
    <div class="ftr__legal">
      <p>© 2026 HRANOL s.r.o.</p>
      <p>Ukázkový web fiktivní firmy. Návrh, texty a kód <a href="https://stepansynek.com" rel="author">Štěpán Synek</a>. Fotografie provozu Unsplash, rendery dílů vlastní.</p>
    </div>
  </div>
</footer>'''


PALETTE = '''<dialog class="palette" id="palette" aria-label="Hledat na webu">
  <div class="palette__box">
    <div class="palette__field">
      <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5"/><path d="m13 13 4 4"/></svg>
      <input id="palette-q" type="text" placeholder="Hledat stroj, materiál, technologii…" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="true" aria-controls="palette-list" aria-autocomplete="list" aria-label="Hledat">
    </div>
    <ul class="palette__list" id="palette-list" role="listbox" aria-label="Výsledky"></ul>
    <p class="palette__empty" id="palette-empty" hidden>Nic jsme nenašli. Zkuste třeba „hliník“, „soustružení“ nebo „DMU“.</p>
    <p class="palette__foot"><span><kbd>↑</kbd> <kbd>↓</kbd> výběr</span><span><kbd>Enter</kbd> otevřít</span><span><kbd>Esc</kbd> zavřít</span></p>
  </div>
</dialog>'''

JSONLD = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"HRANOL s.r.o.","description":"Zakázková výroba přesných dílů a svařenců pro výrobce strojů: CNC frézování, soustružení, broušení, svařování a montáž podsestav.","foundingDate":"1994","email":"poptavky@hranol-obrabeni.cz","telephone":"+420517000100","url":"''' + BASE_URL + '''","logo":"''' + BASE_URL + '''assets/brand/hranol-logo.svg","address":{"@type":"PostalAddress","streetAddress":"Průmyslová 1187","postalCode":"683 01","addressLocality":"Rousínov","addressCountry":"CZ"},"areaServed":["CZ","DE","AT"]}</script>'''


# ---------------------------------------------------------------- pomocné

def read_page(pid):
    raw = (SRC / "pages" / f"{pid}.html").read_text(encoding="utf-8")
    first, body = raw.split("\n", 1)
    meta = json.loads(re.match(r"<!--\s*(\{.*\})\s*-->", first).group(1))
    body = (body.replace("{{capacity}}", build_capacity()).replace("{{machines}}", build_machines())
            .replace("{{status}}", build_status()).replace("{{hall}}", build_hall()))
    return meta, body


def links(text, spa):
    def repl(m):
        page, anchor = m.group(1), m.group(2)
        if spa:
            return f'href="#{anchor[1:] if anchor else page}"'
        return f'href="{FILES[page]}{anchor or ""}"'
    return re.sub(r'href="@([a-z-]+)(#[\w-]+)?"', repl, text)


def search_json():
    items = [{"group": g, "title": t, "page": p, "anchor": a, "keys": k} for g, t, p, a, k in SEARCH]
    return '<script type="application/json" id="search-index">' + json.dumps(items, ensure_ascii=False) + "</script>"


NB = "&nbsp;"


def czech_nbsp(document):
    """Nezlomitelné mezery za jednopísmennými předložkami a mezi čísly a jednotkami (jen v textu)."""
    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->|<[^>]+>)", document)

    def fix(t):
        if not t.strip():
            return t
        t = re.sub(r"(?:^|(?<=[\s(„]))([kKsSvVzZoOuUaAiI])[ \t]+(?=\S)", r"\1" + NB, t)
        t = re.sub(r"(\d)[ \t]+(?=\d{2,3}\b)", r"\1" + NB, t)
        t = re.sub(r"[ \t]+([×±])[ \t]+", NB + r"\1" + NB, t)
        t = re.sub(r"(\d)[ \t]+(?=[^\s\d<&–])", r"\1" + NB, t)
        t = re.sub(r"\b(ISO|EN|Ra|Ing\.|Ø|T\d\d)[ \t]+(?=\S)", r"\1" + NB, t)
        return t

    return "".join(fix(p) if i % 2 == 0 else p for i, p in enumerate(parts))


def chrome(mains, page=None):
    return (f'<a class="skip" href="#obsah">Přeskočit na obsah</a>\n'
            f'<div class="demo"><p class="stand stand--inset">Ukázkový web fiktivní firmy HRANOL. Návrh, texty a kód: '
            f'<a href="https://stepansynek.com" rel="author">Štěpán Synek</a></p></div>\n'
            f'{header()}\n<div id="obsah" tabindex="-1">\n{mains}\n</div>\n{footer(page)}\n{PALETTE}\n{search_json()}')


def mark_current(text, pid):
    return text.replace(f'data-nav="{pid}"', f'data-nav="{pid}" aria-current="page"')


# ---------------------------------------------------------------- výstupy

def build_static():
    for pid in PAGES:
        meta, body = read_page(pid)
        main = f'<main data-page="{pid}">\n{body}\n</main>'
        page = mark_current(chrome(main, pid), pid)
        head_extra = JSONLD if pid == "domu" else ""
        scripts = f'<script defer src="{THREE}"></script>\n<script defer src="assets/part.js"></script>' if pid == "domu" else ""
        preload = "\n".join(f'<link rel="preload" href="{f}" as="font" type="font/woff2" crossorigin>' for f in FONTS)
        document = f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(meta["title"])}</title>
<meta name="description" content="{html.escape(meta["description"])}">
<!-- Ukázkový web fiktivní firmy: vyhledávače ho nemají indexovat. Na ostrém webu tento řádek smazat. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:locale" content="cs_CZ">
<meta property="og:site_name" content="HRANOL s.r.o.">
<meta property="og:title" content="{html.escape(meta["title"])}">
<meta property="og:description" content="{html.escape(meta["description"])}">
<meta property="og:url" content="{BASE_URL}{"" if pid == "domu" else FILES[pid]}">
<meta property="og:image" content="{BASE_URL}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{preload}
<link rel="stylesheet" href="assets/styles.css">
{head_extra}
<script defer src="assets/main.js"></script>
{scripts}
</head>
<body>
{links(page, False)}
</body>
</html>
'''
        (ROOT / FILES[pid]).write_text(czech_nbsp(document), encoding="utf-8")
        print("ok", FILES[pid])


def build_spa(out):
    mains = []
    for pid in PAGES:
        meta, body = read_page(pid)
        hidden = "" if pid == "domu" else " hidden"
        mains.append(f'<main data-page="{pid}" data-title="{html.escape(meta["title"])}"{hidden}>\n{body}\n</main>')
    css = (ROOT / "assets/styles.css").read_text(encoding="utf-8").replace('url("fonts/', 'url("assets/fonts/')
    js = (ROOT / "assets/main.js").read_text(encoding="utf-8")
    part = (ROOT / "assets/part.js").read_text(encoding="utf-8")
    page = mark_current(chrome("\n".join(mains)), "domu")
    document = f'''<meta charset="utf-8">
<title>HRANOL přesné obrábění</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Ukázkový web fiktivní strojírenské firmy HRANOL s.r.o. Návrh, texty a kód: Štěpán Synek.">
<style>
{css}
</style>
{links(page, True)}
<script>document.documentElement.lang = "cs"; window.HRANOL_SPA = true;</script>
<script src="{THREE}"></script>
<script>
{js}
</script>
<script>
{part}
</script>
'''
    Path(out).write_text(czech_nbsp(document), encoding="utf-8")
    print("ok", out)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--spa":
        build_spa(sys.argv[2])
    else:
        build_static()

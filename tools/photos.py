#!/usr/bin/env python3
"""Fotky provozu: stáhne zdroje z Pexels, sjednotí je do jednoho vzhledu a uloží WebP do assets/img/foto/.

  python3 tools/photos.py [složka-cache]

Vzhled „náběhové barvy“: studené odstíny ztratí většinu barvy a stáhnou se k modré oceli, teplé (jiskry, žár,
mosaz, kůže) zůstanou. Stíny sednou na modrou tmavou barvu písma, světla se oteplí ke slámové. Fotky od různých
autorů tak vypadají jako jedno focení. Ke každému souboru se zapíše původ do <soubor>.json.
"""
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/foto"

INK = np.array([0x15, 0x1B, 0x33]) / 255.0      # temper blue, barva písma
STRAW = np.array([1.0, 0.955, 0.86])            # teplé světlo

# slug: (Pexels ID, autor, popis, výřez (vlevo, nahoře, vpravo, dole) v podílech nebo None)
# Nastavení před sjednocením, jako když kolorista nejdřív srovná expozici snímků:
#   gamma > 1 ztmaví přesvícené snímky, aby stíny došly až k modré písma,
#   warm < 1 utlumí snímky, kde je teplé skoro všechno (mosaz), glow obarví nejsvětlejší místa do zlata.
SET = {
    "svarenec": (28929545, "Connor Lucock", "svářeč u vyvrtaného otvoru velkého odlitku", None, {"glow": 0.55}),
    "frezovani": (8865189, "Daniel Smyth", "čelní fréza nad ocelovým obrobkem", None),
    "soustruzeni": (32845679, "Sergey Sergeev", "dva seřizovači u CNC soustruhu", None),
    "svarovani": (11624249, "Rik Schots", "svařování TIG na nerezovém prstenci", None),
    "hala": (15947586, "Hoang NC", "dílna, kde se svařují a brousí ocelové konstrukce", None),
    "pec": (38406567, "Roselino Rocha", "díl v rozžhavené peci", None),
    "mereni": (37660313, "Sandin Redzo", "kontrola dílu číselníkovým úchylkoměrem", None),
    "montaz": (9242911, "Mikhail Nilov", "montáž mechanismu podsestavy", None),
    "sklad": (15508177, "Zakhar Vozhdaienko", "konzolový regál s tyčemi a trubkami", None, {"gamma": 1.45}),
    "dily": (28752153, "Connor Lucock", "obrobené díly z mosazi", None, {"warm": 0.2, "gamma": 1.15}),
    "obsluha": (35072831, "Bulat843", "obsluha u ovládacího panelu stroje", (0, 0.08, 1, 0.82)),
}


LARGE = {"svarenec", "frezovani", "soustruzeni", "svarovani", "hala", "mereni", "montaz", "sklad", "dily", "obsluha"}


def grade(im, gamma=1.0, warm=1.0, glow=0.0):
    a = (np.asarray(im.convert("RGB")).astype(np.float32) / 255.0) ** gamma
    lum = lambda x: (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    L = lum(a)
    mx, mn = a.max(-1, keepdims=True), a.min(-1, keepdims=True)
    warm_mask = np.clip((a[..., :1] - a[..., 2:3]) / (mx - mn + 1e-4), 0, 1) * np.clip((mx - mn) * 4, 0, 1)
    a = L + (a - L) * (0.22 + 0.58 * warm_mask * warm)
    a = np.clip(0.5 + (a - 0.5) * 1.12, 0, 1)
    a = a * a * (3 - 2 * a) * 0.4 + a * 0.6
    L = lum(a)
    sh = (1 - L) ** 2.0 * 0.82
    hi = L ** 2.2 * 0.75
    a = a * (1 - sh) + (INK + (a - L) * 0.6 + L * 0.35) * sh
    a = a * (1 - hi) + a * STRAW * hi
    if glow:
        g = np.clip((L - 0.72) / 0.28, 0, 1) ** 1.5 * glow
        a = a * (1 - g) + a * np.array([1.0, 0.8, 0.46]) * g
    a = INK * 0.9 + a * (1 - INK * 0.9)
    # společné zrno: rozbije pruhy v plynulých přechodech a sjednotí snímky z různých fotoaparátů
    a += np.random.default_rng(1).normal(0, 0.012, a.shape[:2])[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def save(im, path, width, origin):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=76, method=6)
    path.with_name(path.name + ".json").write_text(json.dumps(
        {"prompt": origin, "createdAt": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return im.size


def main():
    cache = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".cache/hranol-foto")
    cache.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (pid, who, desc, crop, *opts) in SET.items():
        src = cache / f"{pid}.jpg"
        if not src.exists():
            url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2600"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            src.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        im = Image.open(src).convert("RGB")
        if crop:
            w, h = im.size
            im = im.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h)))
        im = grade(im, **(opts[0] if opts else {}))
        origin = (f"Origin: sourced stock photo, Pexels, photographer {who}, https://www.pexels.com/photo/{pid}/, "
                  f"Pexels License (free to use, no attribution required; credited on the site anyway). Colour-graded by "
                  f"tools/photos.py (cool hues drained to blue steel, warm hues kept, shadows on #151B33, straw highlights) "
                  f"and resized to WebP for the HRANOL demo; stand-in for the client's own shop photos. Subject: {desc}.")
        portrait = im.height > im.width
        # Velká verze jen u fotek, které web ukazuje přes celou šířku nebo velké; ostatní stačí v 900 px.
        big = save(im, OUT / f"{slug}.webp", 1500 if portrait else 2400, origin) if slug in LARGE else None
        small = save(im, OUT / f"{slug}-900.webp", 700 if portrait else 900, origin)
        print(slug, big, small)


if __name__ == "__main__":
    main()

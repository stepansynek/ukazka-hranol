#!/usr/bin/env python3
"""Vlastní render: svar TIG na broušeném nerezovém plechu s náběhovými barvami kolem housenky.

  python3 tools/heat-tint.py            -> assets/img/foto/nabehove-barvy.webp a -900.webp s původem v .json

Výšková mapa (plech s brusnými stopami, housenka s šupinkami), z ní normály a odlesk kovu. Barva oxidu se počítá
z tloušťky vrstvy, která klesá se vzdáleností od svaru: u housenky modrá a fialová, dál bronzová, zlatá a slámová,
nakonec čistý kov. Pohled je šikmý (perspektiva) s malou hloubkou ostrosti, jako makro fotka.
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/foto"
rng = np.random.default_rng(7)

W, H = 3000, 2000                      # plech v rovině, x napříč svarem, y podél
x = np.linspace(-1.5, 1.5, W)[None, :].repeat(H, 0)
y = np.linspace(0, 2.0, H)[:, None].repeat(W, 1)


def smooth_noise(shape, scale, seed):
    r = np.random.default_rng(seed)
    small = r.standard_normal((max(2, shape[0] // scale), max(2, shape[1] // scale)))
    im = Image.fromarray(((small - small.min()) / (np.ptp(small)) * 255).astype(np.uint8))
    return np.asarray(im.resize((shape[1], shape[0]), Image.BICUBIC)).astype(np.float32) / 255 - 0.5


# housenka: mírně se vlní, šupinky jako půlměsíce po krocích elektrody
wander = 0.025 * np.sin(y * 3.1) + 0.012 * smooth_noise((H, W), 400, 1)
xc = x - wander
bw = 0.095                                       # poloviční šířka housenky
bead = np.clip(1 - (xc / bw) ** 2, 0, None) ** 0.55
# šupinky svaru TIG: překrývající se půlměsíce, každý s ostrou přední hranou a pozvolným náběhem (pila, ne sinus)
phase = (y + 0.9 * xc ** 2 / bw + 0.004 * smooth_noise((H, W), 90, 5)) / 0.068
f = phase - np.floor(phase)
ripple = f ** 0.55
height = bead * (0.022 + 0.0035 * ripple) + 0.0008 * smooth_noise((H, W), 60, 2) * bead
# broušení plechu: jemné rýhy napříč
grain = rng.standard_normal((1, W)).astype(np.float32)
grain = np.asarray(Image.fromarray(grain).resize((W, H), Image.BILINEAR))
grain = np.asarray(Image.fromarray(((grain - grain.min()) / np.ptp(grain) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255 - 0.5
streak = rng.standard_normal((H, 1)).astype(np.float32)
height += (0.00025 * grain + 0.00012 * streak) * (1 - np.clip(bead * 3, 0, 1))  # housenka brusné rýhy nemá

# normály a světlo: slámové hlavní světlo zleva shora, modré protisvětlo zprava
gy, gx = np.gradient(height, 2.0 / H, 3.0 / W)
n = np.dstack([-gx, -gy, np.ones_like(gx)])
n /= np.linalg.norm(n, axis=2, keepdims=True)
view = np.array([0, -0.55, 0.83]); view /= np.linalg.norm(view)


def spec(light, power):
    light = np.array(light, dtype=np.float32); light /= np.linalg.norm(light)
    h = light + view; h /= np.linalg.norm(h)
    return np.clip((n * h).sum(2), 0, 1) ** power


# tloušťka oxidu podle vzdálenosti od kraje housenky, s nepravidelností podél svaru
d = np.clip(np.abs(xc) - bw * 0.9, 0, None)
reach = 0.42 * (1 + 0.18 * smooth_noise((H, W), 300, 3) + 0.08 * np.sin(y * 5.3))
t = np.exp(-d / (reach * 0.42))                  # 1 u housenky, 0 daleko
t = np.where(np.abs(xc) < bw * 0.9, 0.88 + 0.1 * ripple, t)
# náběhová řada (tloušťka vrstvy -> barva), stejné pořadí jako na webu
stops = np.array([0.0, 0.10, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92, 1.0])
cols = np.array([
    [0.62, 0.63, 0.65],   # čistý kov
    [0.68, 0.63, 0.50],   # světlá sláma
    [0.72, 0.56, 0.30],   # sláma
    [0.64, 0.42, 0.20],   # zlatá až bronzová
    [0.44, 0.25, 0.17],   # bronz
    [0.32, 0.18, 0.33],   # fialová
    [0.14, 0.20, 0.42],   # modrá
    [0.22, 0.30, 0.44],   # světle modrá
    [0.24, 0.25, 0.27],   # šedý oxid na housence
])
oxide = np.dstack([np.interp(t, stops, cols[:, c]) for c in range(3)])

key = spec([-0.5, 0.7, 0.9], 70)
rim = spec([0.8, 0.3, 0.6], 90)
diffuse = np.clip((n * np.array([-0.3, 0.5, 0.8])).sum(2), 0, 1)
# broušený nerez: pruh odlesku podél rýh, který slábne do stran (anizotropní lesk)
sheen = np.exp(-((x + 0.55) / 0.55) ** 2) * (0.8 + 0.55 * np.clip(grain * 2.2, -0.5, 1))
img = oxide * (0.30 + 0.38 * diffuse[..., None] + 0.42 * sheen[..., None] * (1 - bead[..., None]))
img += key[..., None] * np.array([1.0, 0.86, 0.6]) * 0.75 * (0.4 + bead[..., None])
img += rim[..., None] * np.array([0.45, 0.58, 1.0]) * 0.5
img *= (0.86 + 0.14 * np.clip(1 - np.abs(x) / 1.5, 0, 1))[..., None]
img = np.clip(img, 0, 1)
im = Image.fromarray((img ** (1 / 1.05) * 255).astype(np.uint8))

# šikmý pohled: perspektiva, horní okraj dál
out_w, out_h = 2400, 1600


def perspective(src, top_scale, margin=0.16):
    w, h = src.size
    mx, my = w * margin, h * margin
    iw = w - 2 * mx
    inset = iw * (1 - top_scale) / 2
    # cílové rohy -> zdrojové rohy uvnitř plechu, aby po otočení nebyly vidět jeho okraje
    pa = [(0, 0), (out_w, 0), (out_w, out_h), (0, out_h)]
    pb = [(mx + inset, my), (w - mx - inset, my), (w - mx, h - my), (mx, h - my)]
    A, B = [], []
    for (u, v), (X, Y) in zip(pa, pb):
        A.append([u, v, 1, 0, 0, 0, -X * u, -X * v]); B.append(X)
        A.append([0, 0, 0, u, v, 1, -Y * u, -Y * v]); B.append(Y)
    coeffs = np.linalg.solve(np.array(A, float), np.array(B, float))
    return src.transform((out_w, out_h), Image.PERSPECTIVE, tuple(coeffs), Image.BICUBIC)


im = im.rotate(-14, resample=Image.BICUBIC, expand=False)
im = perspective(im, 0.7)
# hloubka ostrosti: ostrý pruh uprostřed, nahoře a dole rozmazané
sharp = np.asarray(im).astype(np.float32)
soft = np.asarray(im.filter(ImageFilter.GaussianBlur(3.5))).astype(np.float32)
yy = np.linspace(-1, 1, out_h)[:, None, None]
m = np.clip((np.abs(yy + 0.05) - 0.5) / 0.5, 0, 1) ** 1.8
arr = sharp * (1 - m) + soft * m
# vinětace a zrno
xx = np.linspace(-1, 1, out_w)[None, :, None]
arr *= 1 - 0.28 * np.clip(xx ** 2 + yy ** 2 - 0.3, 0, 1)
arr += rng.normal(0, 3.2, arr.shape[:2])[..., None]
im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

origin = ("Origin: own procedural render, not generated by an image model and not a photograph. tools/heat-tint.py builds a "
          "height field of a ground stainless plate with a TIG weld bead, lights it with a straw key and a temper-blue rim, "
          "colours the oxide by thickness (blue and purple at the bead, bronze, gold and straw further out) and adds "
          "perspective, shallow depth of field and grain. Shows the temper colours the site's palette is named after.")
now = dt.datetime.now(dt.timezone.utc).isoformat()
for name, w in (("nabehove-barvy.webp", 2400), ("nabehove-barvy-900.webp", 900)):
    out = im if w == out_w else im.resize((w, round(out_h * w / out_w)), Image.LANCZOS)
    out.save(OUT / name, "WEBP", quality=80, method=6)
    (OUT / (name + ".json")).write_text(json.dumps({"prompt": origin, "createdAt": now}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ok", name, out.size)

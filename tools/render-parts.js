/* Rendery dílů pro reference. Spuštění: python3 -m http.server 8765 v kořeni webu, pak
   node tools/render-parts.js (potřebuje playwright-core a Google Chrome). Výstup: assets/img/ref-<díl>-1600.webp a -900.webp
   s průhledným pozadím a s původem v <soubor>.json. Převod do WebP dělá tools/webp.py (Pillow). */
const { chromium } = require("playwright-core");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const ROOT = path.resolve(__dirname, "..");
const BASE = process.env.BASE || "http://localhost:8765/";
const parts = process.argv.slice(2).length ? process.argv.slice(2) : ["hvezdice", "ram", "celisti", "pistnice"];
(async () => {
  const b = await chromium.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", args: ["--use-angle=metal", "--enable-webgl", "--ignore-gpu-blocklist"] });
  for (const part of parts) {
    const p = await b.newPage({ viewport: { width: 800, height: 600 } });
    p.on("pageerror", (e) => console.log("pageerror", e.message));
    await p.goto(`${BASE}tools/render-parts.html?part=${part}&w=3200&h=2400`);
    await p.waitForFunction(() => window.DONE === true, null, { timeout: 120000 });
    const data = await p.evaluate(() => document.getElementById("c").toDataURL("image/png"));
    const png = path.join(require("os").tmpdir(), `hranol-${part}.png`);
    fs.writeFileSync(png, Buffer.from(data.split(",")[1], "base64"));
    execFileSync("python3", [path.join(__dirname, "webp.py"), png, path.join(ROOT, `assets/img/ref-${part}`)], { stdio: "inherit" });
    await p.close();
  }
  await b.close();
})();

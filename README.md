# HRANOL s.r.o. (ukázkový web do portfolia)

Web fiktivní strojírenské firmy z Rousínova: zakázkové CNC obrábění, svařence a montáž podsestav.
Šest stránek, vlastní logo a na každé stránce jeden pracovní prvek místo dekorace.

Vzhled „Náběhové barvy“ (od 23. 10. 2026): barvy, které dostane ocel při ohřevu. Slámová plocha rámuje každou
stránku, písmo je modré jako popuštěná ocel a obsah leží na bílém archu. Fotky provozu od různých autorů jsou
sjednocené mezi tyto dvě barvy, rendery dílů nasvícené slámovým a modrým světlem. Celá řada náběhových barev od slámové
po modrou je jen v tabulce volné kapacity, kde ukazuje vytížení. Nadpisy jsou v široké Anybody, text a data v Archivu.
Pravidla vzhledu jsou v `DESIGN.md`.

**HRANOL je fiktivní firma.** Zakázky, citace, čísla, lidé, telefony, adresa i půdorys haly jsou smyšlené. Název není
v obchodním rejstříku (ARES, říjen 2026) a doména `hranol-obrabeni.cz` neexistuje. Web má `noindex`.

## Stránky

| Soubor | Obsah | Pracovní prvek |
| --- | --- | --- |
| `index.html` | Úvod, technologie, svařenec v jedné hale, kapacita, reference, postup | Pult na výkresy, tabulka volné kapacity na 8 týdnů v náběhových barvách, odkaz na nejbližší volno na 5osém frézování |
| `vyroba.html` | Technologie s parametry, povrchové úpravy, materiály, kvalita | Přichycené podmenu technologií, tabulka materiál × technologie |
| `stroje.html` | Strojový park, měrovna | „Vejde se váš díl?“: zadáte rozměry, výsledek se seskupí podle technologie a tabulka označí stroje; filtr podle technologie |
| `reference.html` | Čtyři zakázky (výchozí stav, řešení, výsledek), citace, obory | Rendery dílů, které zakázka dodávala |
| `o-firme.html` | Hala, historie, lidé, kariéra, certifikace | Půdorys haly 80 × 40 m: zóny s plochou a počtem lidí, stroje vedou do strojového parku. Na mobilu se hala otočí na výšku |
| `poptavka.html` | Poptávka ve třech krocích, časté otázky | Nahrání výkresů, živé shrnutí, validace po krocích |

Na všech stránkách funguje vyhledávání přes ⌘K / Ctrl K (nebo „/“): stránky, technologie, stroje, materiály, reference, lidé.
Přechod mezi stránkami je krok do strany podle pořadí v menu (View Transitions, kde je prohlížeč podporuje).

### Pult na výkresy

V úvodu stojí pult „Máte výkres?“ před fotkou svářeče. Soubor jde přetáhnout kamkoli do okna, pult se zvedne a výkres na něm zůstane.
„Pokračovat k poptávce“ otevře formulář, kde už výkresy čekají v prvním kroku. Soubory se mezi stránkami drží v IndexedDB
prohlížeče (v náhledu v jednom souboru jen v paměti) a smažou se po odeslání nebo nové poptávce.

### Kapacita nestárne

Data kapacity v `build.py` jsou relativní: týden 0 je aktuální týden. Build zapíše data ke dni sestavení a `main.js`
je v prohlížeči přepočítá od pondělí aktuálního týdne (čísla týdnů, data, „volno od“, bubliny, řádek pod tlačítky v úvodu).
Ukázka tak ani za půl roku neukazuje prošlé termíny. Barva buňky je vytížení v náběhových barvách: světlá sláma pod 45 %,
modrá od 93 %. Pod 75 % je v týdnu volno. Najetí na buňku zvýrazní její technologii a týden.

## Logo

`assets/brand/`: čelo čtyřhranné tyče se sraženou hranou 45°, sražení je světlá plocha čerstvě obrobeného kovu.
Stejné sražení 45° má na webu jediný prvek: pravý horní roh velké fotky v úvodu.
Wordmark HRANOL je převedený do křivek z Archivo ExtraBold na šířce 125 %, logo tedy nezávisí na písmu
(křivky jsou v `src/logo.json`).

- `hranol-logo.svg`: barevné logo
- `hranol-logo-white.svg`: na tmavé pozadí
- `hranol-mark.svg`: samotná značka
- `../favicon.svg`: favicon na slámovém čtverci; `../apple-touch-icon.png` pro iOS

Barvy: sláma `#edb93c`, modř popuštěné oceli `#151b33`, bílá, světlá ocel `#eef0f3`, bronz `#5e3b10` pro vedlejší
text na slámové. Náběhová řada pro kapacitu: `#f7e3a1`, `#edb93c`, `#d4932b`, `#9c5a2e`, `#63396f`, `#24397a`.

Písmo: Anybody (OFL) pro nadpisy, váha 800 na šířce 112 až 122 %, a Archivo (OFL) pro text, tabulky a čísla
s tabulkovými číslicemi; nula v Archivu není přeškrtnutá, takže se neplete se znakem průměru (Ø40). Obě jsou
v `assets/fonts/`, Anybody je zúžené na latinku, váhy 600 až 900 a šířky 100 až 140 %. Web nenačítá nic z cizích serverů.

## Úpravy a sestavení

Obsah stránek je v `src/pages/*.html`. Společná hlavička a patička, data kapacity, strojů, půdorysu haly a vyhledávání
jsou v `build.py`. Odkazy mezi stránkami se v obsahu píšou jako `href="@stroje"` nebo `href="@vyroba#frezovani"`,
zástupné značky `{{capacity}}`, `{{status}}`, `{{machines}}` a `{{hall}}` vyplní build.

```bash
python3 build.py                     # vygeneruje index.html, vyroba.html, … do kořene
python3 build.py --spa nahled.html   # všech šest stránek v jednom souboru (náhled, přepínání přes #)
python3 -m http.server 8000          # náhled na http://localhost:8000
```

Vygenerované HTML se nemá upravovat ručně, přepíše se při dalším sestavení. Build doplní české nezlomitelné mezery.

Sdílecí náhled (`assets/og.jpg`, 1200 × 630) a `og:url` míří na adresu `BASE_URL` v `build.py`. Při jiném umístění webu
ji změňte a sestavte znovu.

Obrázky se vyrábějí skripty v `tools/` (potřebují Pillow a numpy, rendery a náhled navíc playwright-core a Google Chrome
a spuštěný `python3 -m http.server 8765` v kořeni webu):

```bash
python3 tools/photos.py            # stáhne fotky z Pexels, sjednotí barvy, uloží WebP a původ do assets/img/foto/
node tools/render-parts.js         # rendery dílů z tools/render-parts.html do assets/img/ref-*.webp
node tools/og.js                   # sdílecí náhled assets/og.jpg a apple-touch-icon.png
```

## Přidání do portfolia

Web běží z tohoto repozitáře přes GitHub Pages (větev `main`, `.nojekyll`) na `stepansynek.com/ukazka-hranol/`.

## Obrázky

Fotky ukazují provoz, rendery na slámové ploše díly, které firma dodala. Každý rastr má vedle sebe soubor `.json`
s původem (fotka z Pexels a její autor, vlastní render nebo snímek z kódu).

Rendery (`ref-hvezdice`, `ref-ram`, `ref-celisti`, `ref-pistnice`) jsou vlastní: modely dílů v three.js
(`tools/render-parts.html`) ve studiu se slámovým hlavním světlem a modrým protisvětlem, takže kov odráží barvy webu.
Živý 3D model příruby v úvodu z předchozí verze zmizel, nahradila ho fotka.

Fotografie jsou z Pexels (Pexels License: komerční použití zdarma, uvedení autora není povinné; na webu je autor
u každého snímku). `tools/photos.py` je převede do jednoho vzhledu: studené barvy skoro vymizí do modré oceli,
teplé (jiskry, žár, rukavice, mosaz) zůstanou, stíny sednou na modrou písma a světla se oteplí ke slámové.

| Soubor | Autor | Zdroj |
| --- | --- | --- |
| `svarenec` | Connor Lucock | https://www.pexels.com/photo/28929545/ |
| `frezovani` | Daniel Smyth | https://www.pexels.com/photo/8865189/ |
| `soustruzeni` | Sergey Sergeev | https://www.pexels.com/photo/32845679/ |
| `svarovani` | Rik Schots | https://www.pexels.com/photo/11624249/ |
| `hala` | Hoang NC | https://www.pexels.com/photo/15947586/ |
| `pec` | Roselino Rocha | https://www.pexels.com/photo/38406567/ |
| `mereni` | Sandin Redzo | https://www.pexels.com/photo/37660313/ |
| `montaz` | Mikhail Nilov | https://www.pexels.com/photo/9242911/ |
| `sklad` | Zakhar Vozhdaienko | https://www.pexels.com/photo/15508177/ |
| `dily` | Connor Lucock | https://www.pexels.com/photo/28752153/ |
| `obsluha` | Bulat843 | https://www.pexels.com/photo/35072831/ |

U skutečného klienta by tu byly fotky přímo z jeho provozu a rendery z jeho výkresů.

# HRANOL s.r.o. (ukázkový web do portfolia)

Web fiktivní strojírenské firmy z Rousínova: zakázkové CNC obrábění, svařence a montáž podsestav.
Šest stránek, vlastní logo a na každé stránce jeden pracovní prvek místo dekorace.

**HRANOL je fiktivní firma.** Zakázky, citace, čísla, lidé, telefony, adresa i půdorys haly jsou smyšlené. Název není
v obchodním rejstříku (ARES, říjen 2026) a doména `hranol-obrabeni.cz` neexistuje. Web má `noindex`.

## Stránky

| Soubor | Obsah | Pracovní prvek |
| --- | --- | --- |
| `index.html` | Úvod, technologie, kapacita, reference, postup | 3D model obrobené příruby (three.js), tabulka volné kapacity na 8 týdnů, pod tlačítky nejbližší volno na 5osém frézování |
| `vyroba.html` | Šest technologií s parametry, materiály, kvalita | Přichycené podmenu technologií, tabulka materiál × technologie |
| `stroje.html` | Strojový park, měrovna | „Vejde se váš díl?“: zadáte rozměry, výsledek se seskupí podle technologie a tabulka označí stroje; filtr podle technologie |
| `reference.html` | Čtyři zakázky (výchozí stav, řešení, výsledek), citace, obory | Rendery dílů, které zakázka dodávala |
| `o-firme.html` | Hala, historie, lidé, kariéra, certifikace | Půdorys haly 80 × 40 m: zóny s plochou a počtem lidí, stroje vedou do strojového parku. Na mobilu se hala otočí na výšku |
| `poptavka.html` | Poptávka ve třech krocích, časté otázky | Nahrání výkresů, živé shrnutí, validace po krocích |

Na všech stránkách funguje vyhledávání přes ⌘K / Ctrl K (nebo „/“): stránky, technologie, stroje, materiály, reference, lidé.
Přechody mezi stránkami používají View Transitions, kde je prohlížeč podporuje.

### Kapacita nestárne

Data kapacity v `build.py` jsou relativní: týden 0 je aktuální týden. Build zapíše data ke dni sestavení a `main.js`
je v prohlížeči přepočítá od pondělí aktuálního týdne (čísla týdnů, data, „volno od“, bubliny, řádek pod tlačítky v úvodu).
Ukázka tak ani za půl roku neukazuje prošlé termíny. Šedá část sloupce je obsazená kapacita, oranžová volná rezerva
v týdnech s vytížením pod 75 %.

## Logo

`assets/brand/`: blok se dvěma sraženými hranami 45° (obrys hranolu i obrobku), jedna hrana oranžová jako čerstvě
obrobená plocha. Wordmark „hranol“ je převedený do křivek z Mona Sans SemiExpanded SemiBold, logo tedy nezávisí na písmu.

- `hranol-logo.svg`: barevné logo
- `hranol-logo-white.svg`: na tmavé pozadí
- `hranol-mark.svg`: samotná značka
- `../favicon.svg`: favicon, v tmavé liště prohlížeče se přebarví; `../apple-touch-icon.png` pro iOS

Barvy: grafit `#15212b`, oranžová hrana `#ff5a1f`, mlha `#f3f4f5`. Oranžová znamená jen dvě věci: volnou kapacitu
a aktivní stav (aktuální stránka, krok formuláře, zvýrazněná zóna haly).

Písmo: jen Mona Sans, nadpisy rozšířené na 112,5 %. Číslice zůstávají proporcionální: tabulkové mají v Mona Sans
přeškrtnutou nulu, která by se u strojírny pletla se znakem průměru (Ø40).

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

## Přidání do portfolia

Zkopírujte složku bez `src/` a `build.py` do `stepansynek.github.io/public/ukazky/hranol/`. Next.js ji při exportu
přenese beze změny a web poběží na `stepansynek.com/ukazky/hranol/`.

## Obrázky

Fotky ukazují provoz, rendery na mlze díly, které firma dodala.

Rendery (`ref-hvezdice`, `ref-ram`, `ref-celisti`, `ref-pistnice`, `priruba`) jsou vlastní: modely dílů v three.js
nasvícené stejným studiem jako 3D příruba v úvodu. `priruba-1200.webp` se ukáže v úvodu místo 3D modelu, když prohlížeč
nemá WebGL. `og.jpg` je složený z loga, nadpisu a stejné příruby.

Fotografie jsou z Unsplash (Unsplash License: komerční použití zdarma, bez nutnosti uvádět autora), mírně sjednocené
a převedené do WebP:

| Soubor | Zdroj |
| --- | --- |
| `frezovani` | https://images.unsplash.com/photo-1602664876866-d3b33b77756b |
| `soustruzeni` | https://images.unsplash.com/photo-1666634157070-6fd830fb5672 |
| `svarovani` | https://images.unsplash.com/photo-1683470156390-703e9313dab6 |
| `montaz` | https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0 |
| `mereni` | https://images.unsplash.com/photo-1758873263563-5ba4aa330799 |
| `kotouce` | https://images.unsplash.com/photo-1715433675788-9e0fb059d928 |

U skutečného klienta by tu byly fotky přímo z jeho provozu a rendery z jeho výkresů.

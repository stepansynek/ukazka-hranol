# HRANOL s.r.o. (ukázkový web do portfolia)

Web fiktivní strojírenské firmy z Rousínova: zakázkové CNC obrábění, svařence a montáž podsestav.
Šest stránek, vlastní logo a na každé stránce jeden pracovní prvek místo dekorace.

Vzhled „Veletržní stánek“: firma se představuje jako vlastní stánek na strojírenském veletrhu. Žlutá systémová stěna
s nápisem, hliníkové sloupky mezi stejnými panely, exponáty na bílých podstavcích a bílé pulty s grafitovou deskou pro
pracovní nástroje. Žlutá stěna přesvědčuje, bílý pult pracuje; na bílé žlutá znamená volno a akci. Pravidla vzhledu
jsou v `DESIGN.md`.

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
Přechod mezi stránkami je krok podél stánku do strany podle pořadí v menu (View Transitions, kde je prohlížeč podporuje).

### Pult na výkresy

V úvodu stojí pult „Máte výkres?“. Soubor jde přetáhnout kamkoli do okna, pult se rozsvítí a výkres na něm zůstane.
„Pokračovat k poptávce“ otevře formulář, kde už výkresy čekají v prvním kroku. Soubory se mezi stránkami drží v IndexedDB
prohlížeče (v náhledu v jednom souboru jen v paměti) a smažou se po odeslání nebo nové poptávce.

### Kapacita nestárne

Data kapacity v `build.py` jsou relativní: týden 0 je aktuální týden. Build zapíše data ke dni sestavení a `main.js`
je v prohlížeči přepočítá od pondělí aktuálního týdne (čísla týdnů, data, „volno od“, bubliny, řádek pod tlačítky v úvodu).
Ukázka tak ani za půl roku neukazuje prošlé termíny. Grafitový sloupec je obsazená kapacita, žlutá plocha nad ním
volná rezerva v týdnech s vytížením pod 75 %.

## Logo

`assets/brand/`: čelo čtyřhranné tyče se sraženou hranou 45°, sražení je žlutá plocha čerstvě obrobeného kovu.
Wordmark HRANOL je převedený do křivek z Archivo ExtraBold na šířce 125 %, logo tedy nezávisí na písmu
(křivky jsou v `src/logo.json`).

- `hranol-logo.svg`: barevné logo
- `hranol-logo-white.svg`: na tmavé pozadí
- `hranol-mark.svg`: samotná značka
- `../favicon.svg`: favicon na žlutém čtverci; `../apple-touch-icon.png` pro iOS

Barvy: signální žlutá `#f5c400`, grafit `#1c1e21`, hliník `#c9ced3`, bílá a podlaha haly `#e4e4df`.

Písmo: jen Archivo (OFL), uložené v `assets/fonts/` (latinka a latinka rozšířená, variabilní váha i šířka). Nápisy
mají šířku 125 % a váhu 800, data a tabulky šířku 87 % s tabulkovými číslicemi; nula v Archivu není přeškrtnutá,
takže se neplete se znakem průměru (Ø40). Web nenačítá nic z cizích serverů, three.js r128 je v `assets/vendor/`.

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

Web běží z tohoto repozitáře přes GitHub Pages (větev `main`, `.nojekyll`) na `stepansynek.com/ukazka-hranol/`.

## Obrázky

Fotky ukazují provoz, rendery na žlutých panelech díly, které firma dodala. Každý rastr má v metadatech zapsaný
původ (fotka z Unsplash, vlastní render nebo snímek z kódu).

Rendery (`ref-hvezdice`, `ref-ram`, `ref-celisti`, `ref-pistnice`, `priruba`) jsou vlastní: modely dílů v three.js
nasvícené stejným studiem jako 3D příruba v úvodu. `priruba-1200.webp` se ukáže v úvodu místo 3D modelu, když prohlížeč
nemá WebGL; je to snímek ze stejné scény s průhledným pozadím. `og.jpg` je složený z loga, nadpisu a stejné příruby.

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

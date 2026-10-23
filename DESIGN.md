---
name: HRANOL s.r.o.
description: Precision parts and weldments for machine makers, shown in the temper colours of heated steel.
colors:
  straw: "#EDB93C"
  straw-pale: "#FBEFC9"
  ink: "#151B33"
  ink-hover: "#2B3766"
  bronze: "#5E3B10"
  white: "#FFFFFF"
  steel: "#EEF0F3"
  line: "#D5D9E0"
  field: "#838CA0"
  muted: "#545D72"
  error: "#B42318"
  temper-1-pale-straw: "#F7E3A1"
  temper-2-straw: "#EDB93C"
  temper-3-gold: "#D4932B"
  temper-4-bronze: "#9C5A2E"
  temper-5-purple: "#63396F"
  temper-6-blue: "#24397A"
typography:
  display:
    fontFamily: "Anybody, Archivo, system-ui, sans-serif"
    fontSize: "clamp(2.75rem, 1.2rem + 5.4vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 122"
  headline:
    fontFamily: "Anybody, Archivo, system-ui, sans-serif"
    fontSize: "clamp(2rem, 1.3rem + 2.2vw, 3.375rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 122"
  headline-feature:
    fontFamily: "Anybody, Archivo, system-ui, sans-serif"
    fontSize: "clamp(2.25rem, 1.2rem + 3.3vw, 4.5rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 112"
  title:
    fontFamily: "Anybody, Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.375rem, 1.1rem + 0.9vw, 1.875rem)"
    fontWeight: 750
    lineHeight: 1.08
    letterSpacing: "-0.01em"
    fontVariation: "'wdth' 112"
  numeral:
    fontFamily: "Anybody, Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.375rem, 1.1rem + 0.9vw, 1.875rem)"
    fontWeight: 750
    lineHeight: 1.15
    fontVariation: "'wdth' 100"
  lead:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.1875rem, 1.05rem + 0.45vw, 1.375rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
    fontFeature: "'tnum'"
rounded:
  none: "0px"
spacing:
  gut: "clamp(10px, 2.2vw, 32px)"
  pad: "clamp(18px, 4.4vw, 72px)"
  sec: "clamp(64px, 7.5vw, 128px)"
  max: "1600px"
  cut: "clamp(44px, 6vw, 112px)"
components:
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0 26px"
    height: "52px"
  button-ink-hover:
    backgroundColor: "{colors.ink-hover}"
    textColor: "{colors.white}"
  button-straw:
    backgroundColor: "{colors.straw}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 26px"
    height: "52px"
  button-straw-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.straw}"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 26px"
    height: "52px"
  button-line-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "12px 14px"
    height: "52px"
  chip:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "40px"
  chip-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
  drawing-counter:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "clamp(22px, 2.2vw, 32px)"
    width: "420px"
  drop-zone:
    backgroundColor: "{colors.steel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "18px 18px 16px"
  drop-zone-armed:
    backgroundColor: "{colors.straw}"
    textColor: "{colors.ink}"
  capacity-cell:
    backgroundColor: "{colors.temper-1-pale-straw}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    height: "58px"
  summary-panel:
    backgroundColor: "{colors.steel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "24px"
---

# Design System: HRANOL s.r.o.

## Overview

**Creative North Star: "Náběhové barvy"**

HRANOL is shown in the colours steel takes when it is heated, the temper colours every machinist reads off a part: pale straw, straw, gold, bronze, purple, blue. The page itself is straw, the ink is temper blue, and every photograph is graded between those two poles so that pictures from many photographers read as one shoot. The look is warm, flat and workmanlike: square corners, hairline rules, wide heavy lettering, plain Czech with numbers.

Every page is framed by a straw ground (top strip, header, page head, interludes, footer with the closing call). Content sits on white sheets inset in that straw by a narrow gutter, so a thin straw edge always shows on both sides of the sheet. One left axis runs through headlines, leads and sheet content; section heads put the headline in columns 1 to 7 and the aside in columns 8 to 12. Sections vary in form rather than repeating a card grid: a technology list with a photograph that changes per row, a plate photograph beside a vertical step axis, the capacity heat board, a case interlude on straw, a before and after comparison table.

The full temper ramp is a physical scale, not a decoration. It appears as UI colour in exactly one place, the capacity board, where load runs from pale straw (free) to blue (booked) in real heating order, and once as material, in the own heat-tint render of a TIG weld. Motion is limited to state changes on one exponential ease-out plus a sideways cross-document view transition; there are no scroll reveals.

**Key Characteristics:**
- Straw ground frames every page; white sheets inset by the gutter carry content.
- Temper-blue ink for all type and primary buttons; bronze for secondary text on straw, slate for secondary text on white.
- Anybody, wide and heavy, for lettering; Archivo for text, tables and tabular figures.
- Square corners everywhere; the only angled edge is the 45° chamfer on the home hero photograph, echoing the logo.
- Photography graded to one look by `tools/photos.py`, always captioned with subject and credit.
- The temper ramp appears once as UI (capacity board) and once as material (heat-tint weld render).

## Colors

A fixed palette of two poles, straw and temper blue, with neutral steel greys on white and a six-step temper ramp reserved for one job.

### Primary
- **Straw** (straw): the ground of the whole site. Header, page heads, interludes, footer and the gutter around every sheet. Also the fill of the straw button, the armed drop zone, the current rail tab, the selected search result and the active hall zone.
- **Temper Blue Ink** (ink): all text, primary buttons, rules of 2px weight, focus outlines, the capacity tooltip, text selection (with straw text), and the shadow pole of photo grading.

### Secondary
- **Dark Bronze** (bronze): secondary text on straw only (top strip, breadcrumbs, captions and credits on straw, footer copy and legal line, fact labels in the interlude).
- **Pale Straw** (straw-pale): a highlight on white. Hovered technology rows, fitting machine rows, active hall zone list item, the carried-files notice in the RFQ, segmented-control hover.
- **Lighter Temper Blue** (ink-hover): hover state of ink buttons and hall-plan machines only.

### Tertiary
- **The Temper Ramp** (temper-1-pale-straw through temper-6-blue): load levels on the capacity board (below 45 %, 45 to 59 %, 60 to 74 %, 75 to 84 %, 85 to 92 %, 93 % and over), with white numerals from bronze upward, and the legend strip beneath it. Its second step is identical to the straw ground.

### Neutral
- **White** (white): the content sheets, the drawing counter, search button, inputs, chips, the search palette and mobile menu.
- **Light Steel** (steel): fields on white: drop zone at rest, RFQ summary panel, hall floor areas, rail tab hover, key caps.
- **Hairline** (line): 1px rules between rows and list items on white.
- **Field Edge** (field): 1.5px borders of inputs, chips and step numbers, dashed drop-zone border; 3:1 against white.
- **Slate Muted** (muted): secondary text on white (section asides, specs labels, table heads, credits on white).
- **Error Red** (error): field errors and the error summary only.

### Named Rules
**The Two Poles Rule.** Straw frames, white carries, ink speaks. No colour outside the palette is introduced, and no gradients are used. One sanctioned exception: the wide piston-rod render in the reference interlude fades out at its bottom through an alpha mask, so its contact shadow dissolves into the straw instead of ending at the crop edge. It is a transparency mask on an image, never a colour gradient.

**The Heating Order Rule.** The temper ramp keeps the physical order pale straw, straw, gold, bronze, purple, blue. It is never shuffled, never used as decoration, and appears as UI colour only on the capacity board.

**The Right Secondary Rule.** Secondary text on straw is bronze; secondary text on white is slate muted. Never put muted on straw or bronze on white.

## Typography

**Display Font:** Anybody (self-hosted variable, weight 600 to 900, width 100 to 140 %), falling back to Archivo
**Body Font:** Archivo (self-hosted variable), falling back to system-ui

**Character:** Anybody set wide and heavy gives the lettering the stance of stamped stock; Archivo keeps text, specs and tables plain and legible. A 4:3 scale from 17px body text, with the upper steps fluid.

### Hierarchy
- **Display** (800, 44 to 96px, width 122 %, line-height 0.92): the home H1 and inner page titles on straw. The home claim sets in three lines at 1440 and is capped at 11svh so the hero photo stays in the first viewport; width drops to 114 % under 720px.
- **Headline** (800, 32 to 54px, width 122 %, line-height 1): section titles on sheets, RFQ step legends, the completion title.
- **Headline Feature** (800, 36 to 72px, width 112 %): case titles, the interlude title, the footer closing call, pull quotes.
- **Title** (750, 22 to 30px, width 112 %, line-height 1.08): H3s, job titles, sector names, mobile menu links. Small lettering (row names in capacity and machine tables, footer heads, zone names, contact names) uses the same 750 / 110 to 112 % at body size.
- **Numeral** (750 to 800, width 100 to 104 %): fact values in the case interlude, step marks in sequences and the timeline. Numerals narrow to near-normal width so figures stay readable.
- **Lead** (400, 19 to 22px, line-height 1.5, max 52 to 54ch): the opening paragraph beside a page head.
- **Body** (400, 17px, line-height 1.55; 16px under 720px): running text, 44 to 66ch.
- **Label** (600, 14px): table heads, capacity week and date, credits, small metadata. Sentence case. Tabular figures in every table, `dd`, size and week readout.

### Named Rules
**The Wide Letter Rule.** Anybody is lettering only: 800 weight at width 112 to 122 % for headings, 100 to 104 % for numerals. Paragraphs, tables, forms and buttons are always Archivo.

**The Plain Label Rule.** Labels are sentence case Archivo. No uppercase tracking, no monospace, no eyebrow line above a heading.

## Layout

Each page block (top strip, header bar, hero, page head, photo band, sheet, interlude, machine tool panel, footer parts) is the same width, `min(100% - 2 × gut, 1600px)`, centred, so a straw gutter of 10 to 32px shows on both sides. Inner padding `pad` (18 to 72px) gives one left axis shared by straw and white areas. Sections on a sheet are separated by `sec` (64 to 128px); consecutive sections drop their top padding. Section heads are a 12-column grid with the headline at 1 to 7 and the aside at 8 to 12, bottom aligned; the home hero lead uses the same 8 to 12 column. Body compositions are mostly 7:5 or 5:7 splits, with a sticky media column where a photo follows the list.

Sections take different forms on purpose: list plus changing photo, plate photo beside a vertical step axis, the capacity heat board, a straw interlude with image and facts, a four-step horizontal sequence with tick marks, comparison and machine tables, a hall plan with linked zone list. Photographs run at plate scale, never as card thumbnails.

Breakpoints: 1279px (hero lead widens, counter drops below the photo top edge), 1079px (header collapses to menu, all splits stack to one column, header 64px), 719px (sequences turn vertical on a left axis, the comparison table and capacity board reflow to stacked rows, drawing counter overlaps the photo bottom by 56px). A short-viewport rule (min-width 1080px and max-height 860px) compacts the counter.

## Elevation & Depth

Flat by default. Depth comes from the straw-to-white step and hairline rules. A single lifted shadow (ink-tinted, `0 1px 2px` plus a long soft drop) is reserved for surfaces that physically stand over others: the drawing counter over the hero photo, the machine-fit panel over the following sheet, the mobile menu and the search palette. The sticky header gains a faint shadow only once the page is scrolled.

### Shadow Vocabulary
- **Lift** (`box-shadow: 0 1px 2px rgb(21 27 51 / 0.12), 0 28px 48px -24px rgb(21 27 51 / 0.45)`): drawing counter, fit-checker panel, mobile menu.
- **Armed Lift** (`box-shadow: 0 2px 4px rgb(21 27 51 / 0.14), 0 40px 60px -24px rgb(21 27 51 / 0.6)`): the counter when a file is dragged over the window, paired with a 6px rise; the search palette box.
- **Scrolled Header** (`box-shadow: 0 1px 0 rgb(21 27 51 / 0.18), 0 14px 28px -22px rgb(21 27 51 / 0.6)`): the sticky header after scroll.

### Named Rules
**The Standing Surface Rule.** Only a surface that stands over another layer casts a shadow. Sheets, cards, tables and photos are flat.

## Shapes

Every corner is square (0px): buttons, inputs, chips, sheets, cells, photos, the counter. Structure is drawn with rules: 2px ink rules open lists, specs, tables, step sequences and people groups; 1px hairlines separate rows. Sequences and the weldment steps use a straight axis with short perpendicular ticks, and the timeline ends in a small ink square. Square markers stand in for bullets and yes/no states.

The one angled edge on the site is the 45° chamfer cut from the top-right corner of the home hero photograph (`cut`, 44 to 112px), echoing the logo: a chamfered square bar end with a light 45° facet in white.

### Named Rules
**The One Chamfer Rule.** The 45° chamfer belongs to the logo and the home hero photo only. No other element is clipped, rounded or angled.

## Components

### Buttons
Solid, square and heavy-lettered in Archivo 700.
- **Shape:** square (0px), 52px tall, 2px border; small variant 44px.
- **Ink:** ink fill, white text. The header Poptávka button and form actions. Hover lightens to ink-hover.
- **Straw:** straw fill, ink text, used on white (counter upload, capacity booking, mobile menu call). Hover inverts to ink fill with straw text.
- **Line:** transparent with a 2px ink border; hover fills ink with white text.
- **Focus:** 3px ink outline, 2px offset, on every interactive element. Transitions 0.25s on the shared ease-out.

### Links
Ink text with a 1.5px underline at 0.22em offset that thickens to 3px on hover; emphasised links run 2px to 4px. Plain text, no trailing arrows.

### Chips
- **Style:** white, 1.5px field border, 40px tall, 600 weight, count in tabular figures.
- **State:** hover borders ink; pressed fills ink with white text.

### Inputs / Fields
- **Style:** white, 1.5px field border, square, 52px minimum; dimension inputs 58px with Archivo 650 at title size and a unit inside.
- **Focus:** border shifts to ink, plus the global ink outline.
- **Error:** 2px error border and a 600-weight error line beneath; an error summary box at step top.
- **Segmented control:** 2px ink frame, pale straw on hover, straw when checked.

### Navigation
Header on straw: logo, Archivo 600 links with a 2px ink underline that grows from the left on hover (3px for the current page), a white search button with a key cap, and the ink Poptávka button. Below 1080px the links collapse into a white drop panel with lifted shadow, links set in title lettering, and a straw call to action. Inner pages add a sticky white rail of section tabs (steel hover, straw current).

### Drawing Counter (signature)
A white panel standing over the dark left of the home hero photograph and rising into the straw under the H1: Anybody title, the 48-hour line in 600, a steel drop zone with a 2px dashed field border, and a straw upload button. Dragging a file anywhere over the window arms it: it lifts 6px with the armed shadow, the drop zone turns solid ink-bordered straw and its hint turns bronze. Dropped files ride into step 1 of the RFQ, where a pale straw notice confirms them.

### Capacity Board (signature)
Six technologies by eight rolling weeks, 4px gaps, 58px cells filled by the temper ramp by load, percentages in tabular 600. Hovering a cell isolates its technology row and week column (others fade to 22 %), outlines the cell in 3px ink and shows an ink tooltip. A six-swatch legend with ranges sits below. On phones each technology becomes a row of eight compact cells.

### Photographs and Renders
Photographs are graded by `tools/photos.py`: cool hues drained toward blue steel, warm hues (sparks, glow, brass, skin) kept, shadows sat on ink, highlights warmed toward straw, a shared fine grain. Each carries a caption with subject and photographer credit ("Foto …, Pexels"). Own three.js part renders stand on straw tiles, lit by a straw key and a blue rim, captioned "Vlastní render". Photo backgrounds fall back to ink while loading.

## Do's and Don'ts

### Do:
- **Do** frame every page in straw and set content on white sheets inset by the gutter, square-cornered.
- **Do** use temper-blue ink for all type and primary actions; bronze for secondary text on straw, slate muted on white.
- **Do** set lettering in Anybody 800 at width 112 to 122 % and numerals at 100 to 104 %; set text, tables and forms in Archivo with tabular figures.
- **Do** keep the temper ramp in heating order and use it as UI colour only on the capacity board.
- **Do** grade every photograph with `tools/photos.py` and caption it with subject and credit; stand renders on straw tiles with a straw key and blue rim.
- **Do** vary section form (list with changing photo, plate with step axis, heat board, interlude, comparison table) and keep one left axis.
- **Do** limit motion to state changes on the single exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) and the sideways view transition; honour reduced motion.

### Don't:
- **Don't** add eyebrows or kickers above headings, all-caps labels, or monospace type.
- **Don't** put arrows in links or em dashes in copy.
- **Don't** round, clip or angle anything other than the hero photo's single 45° chamfer and the logo.
- **Don't** introduce colours outside the palette or colour gradients; the temper ramp is a stepped scale, not a gradient. The only fade is the alpha mask on the reference interlude render.
- **Don't** use the temper ramp decoratively or reorder it.
- **Don't** run photographs as thumbnails in cards, or ship an ungraded or uncredited photo.
- **Don't** cast shadows from flat content; only standing surfaces (counter, fit panel, menu, palette) lift.
- **Don't** add scroll reveals.

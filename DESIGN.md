---
name: HRANOL s.r.o.
description: A machine shop's website built as its own stand at the Brno engineering fair; yellow walls persuade, white counters work.
colors:
  wall: "#f5c400"
  wall-ink-2: "#4d4100"
  wall-pale: "#fff4c2"
  ink: "#1c1e21"
  ink-2: "#4a4f55"
  floor: "#e4e4df"
  floor-deep: "#d3d3cc"
  white: "#ffffff"
  alu: "#c9ced3"
  alu-lo: "#a3aab1"
  groove: "#8f969d"
  line: "#dcdfe2"
  line-strong: "#8c939a"
  error: "#b42318"
typography:
  display:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, min(5.9vw, 9.6svh), 5.75rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 125"
  headline-page:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(2.75rem, 6.6vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 125"
  headline-wall:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(2rem, 3.7vw, 3.5rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 125"
  headline-section:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.875rem, 3.3vw, 3.125rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 125"
  title-counter:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.75rem, 2.5vw, 2.375rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontVariation: "'wdth' 125"
  title-panel:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.375rem, 1.9vw, 1.75rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.005em"
    fontVariation: "'wdth' 118"
  title-item:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 700
    lineHeight: 1.2
    fontVariation: "'wdth' 112"
  lead:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.125rem, 1.35vw, 1.3125rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
    fontVariation: "'wdth' 100"
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 700
    lineHeight: 1.1
    fontVariation: "'wdth' 112"
  data:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.35
    fontFeature: "'tnum' 1"
    fontVariation: "'wdth' 87"
rounded:
  none: "0px"
  key: "2px"
spacing:
  post: "10px"
  post-mobile: "6px"
  gut: "clamp(16px, 3.4vw, 48px)"
  pad: "clamp(20px, 2.8vw, 44px)"
  sec: "clamp(72px, 8.5vw, 136px)"
  sink: "clamp(96px, 15svh, 148px)"
  lift: "clamp(72px, 9vw, 128px)"
  plinth-top: "26px"
components:
  button-sign:
    backgroundColor: "{colors.wall}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "52px"
  button-sign-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.wall}"
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "52px"
  button-ink-small:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0 18px"
    height: "44px"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "52px"
  button-line-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
  chip:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "40px"
  chip-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
  input-field:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "12px 14px"
    height: "52px"
  panel-wall:
    backgroundColor: "{colors.wall}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "{spacing.pad}"
  panel-white:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "{spacing.pad}"
  counter:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "{spacing.pad}"
  plinth:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "18px 22px 22px"
  rail-link-current:
    backgroundColor: "{colors.wall}"
    textColor: "{colors.ink}"
    padding: "12px 16px"
---

# Design System: HRANOL s.r.o.

## Overview

**Creative North Star: "The Fair Stand"**

The site is a machine shop's own stand at the Brno engineering fair, seen in frontal elevation. Signal-yellow system walls are framed by aluminium posts and rails; claims are lettered onto the panels in wide, heavy Archivo; delivered parts stand as exhibits on white plinths; work happens at white counters with graphite tops (capacity, fit check, machine table, request form). The page ground is the warm grey of the hall floor. Everything is square, built from equal panels, and lit by real, soft shadows only where an object physically stands in front of the wall.

The governing split is home and away: yellow walls persuade, white counters work. On white, yellow is no longer a surface but a signal, marking what is free (capacity weeks), what is selected (palette item, rail position, segmented choice) and what is actionable (the drawing upload). Density is moderate and factual: big lettering on walls, tight tabular data on counters, nothing decorative that is not a piece of stand hardware.

It must read as a believable Moravian job shop, never as an art piece, a dark "tech" site, or a blueprint pastiche, and it shares no grammar with the sibling SETINA demo.

**Key Characteristics:**
- Yellow wall panels in an aluminium post-and-rail grid, every panel outlined by a groove line.
- White counters (10px graphite top) and white plinths stand in front of the wall with soft, warm shadows.
- One family, Archivo variable, carried by width: 125 for lettering, 112 for labels and names, 87 with tabular figures for data.
- Square corners everywhere; borders and solid fills instead of rounding.
- One authored motion: a sideways step along the stand between pages, exponential ease-out.

## Colors

A three-material palette (signal yellow, graphite, aluminium) on a warm hall-floor ground, with white for everything that works.

### Primary
- **Signal Yellow** (`wall`): the system wall panels, the hero and closing walls, page heads; on white it marks free capacity cells, the current rail item, selected palette rows, the pressed segment, the active hall zone, the armed drop zone, the sign button and the text selection.
- **Yellow-Wall Ink** (`wall-ink-2`): secondary text on yellow (breadcrumbs, quote attribution, close-wall note, hint text inside an armed drop zone). Never used on white.
- **Pale Yellow** (`wall-pale`): the soft "marked" state on white: matching machine rows, the targeted table row, the active zone in the zone list, the carried-drawings note in the form, segment hover.

### Neutral
- **Graphite** (`ink`): all lettering and body text, counter tops, the ink button, pressed chips, done steps, focus outlines, list rules (2px), tooltip and hall machine fills.
- **Soft Graphite** (`ink-2`): secondary text on white and on the floor, capacity bars, meta lines.
- **Hall Floor** (`floor`): the page background, empty capacity cells, keycaps, initials tiles.
- **Deep Floor** (`floor-deep`): the fictional-firm strip at the top and the footer's legal divider.
- **Counter White** (`white`): counters, plinths, fascia, white wall panels, inputs, chips.
- **Aluminium** (`alu`): posts, rails and the fascia rails; the sticky technology rail.
- **Low Aluminium** (`alu-lo`): the outer edge of walls and panels, plinth lip, scrollbar thumb, hall fixtures.
- **Groove** (`groove`): the 2px groove line drawn through each post around every panel.
- **Hairline** (`line`): 1px row dividers and separators on white.
- **Field Edge** (`line-strong`): borders of inputs, chips, the search button, the dashed drop zone and empty step numbers; held at 3:1 against white.
- **Fault Red** (`error`): field errors and the error summary only.

### Named Rules
**The Home and Away Rule.** Yellow walls persuade, white counters work. On a white surface, yellow means free, selected or actionable; it is never decoration there.

**The Ink-on-Yellow Rule.** Text on yellow is graphite or Yellow-Wall Ink, nothing else; white text never sits on yellow.

## Typography

**Display Font:** Archivo variable, self-hosted (with system-ui, sans-serif)
**Body Font:** Archivo variable (same file)
**Data:** Archivo at width 87 with tabular figures

**Character:** One grotesque stretched across its width axis does all the work: the 125-width 800 weight reads as lettering cut for a fair stand; the narrow 87 width with tabular numbers reads as a spec sheet. No second family, no monospace.

### Hierarchy
- **Display** (800, width 125, hero clamp up to 5.75rem, line-height 0.94): the home claim on the hero wall only.
- **Page headline** (800, width 125, up to 6rem, 0.94): inner-page H1 on the page-head wall.
- **Wall headline** (800, width 125, up to 3.5rem): the closing wall claim; feature, tech and case titles use the same lettering at 1.625 to 2.625rem.
- **Section headline** (800, width 125, up to 3.125rem, 0.98): section heads standing on the floor.
- **Counter title** (800, width 125, up to 2.375rem, 1.0): titles on white counters.
- **Panel title** (800, width 118, up to 1.75rem, 1.05): titles inside panels, certificates, sectors, mobile nav.
- **Item title** (700, width 112, 1.1875rem, 1.2): plinth names, sequence steps, machine names, FAQ and job titles (1.0625 to 1.25rem).
- **Lead** (400, up to 1.3125rem, 1.5, max 34em): the one paragraph under a headline.
- **Body** (400, 1.0625rem desktop / 1rem mobile, 1.55): running text, measures held at 34 to 64ch.
- **Label** (700, width 112, 1.0625rem): buttons; nav links are 600 at normal width.
- **Data** (500 to 700, width 87, tabular figures, 0.875 to 1.375rem): dimensions, dates, weeks, counts, specs, file sizes.

### Named Rules
**The Lettering Rule.** Headlines are lettered, not typeset: weight 800, width 125, slightly negative tracking, balanced wrapping. Display tops out at 6rem.

**The Spec-Sheet Rule.** Every number a buyer compares (dimensions, tolerances, dates, capacity, sizes) is set at width 87 with tabular figures. No monospace, no all-caps labels.

## Layout

The stand is centred and capped at 1680px; floor content is inset by the gutter (16 to 48px). A wall is a CSS grid on an aluminium background whose gaps are the posts (10px, 6px on mobile) and whose padding is the rail; panels are equal-width "metre" modules in 2, 3, 4 or 6 columns, spanning 2 or the full row for wide panels. Panels pad by `pad` (20 to 44px). Sections step down the floor at `sec` (72 to 136px).

Depth is staged by overlap: counters and plinths on the hero sink below the wall bottom by `sink` and the first floor block lifts into the wall above by `lift`, so objects visibly stand in front of the wall. The header fascia (72px band between aluminium rails) stays sticky; inner pages with sections add a sticky aluminium rail beneath it.

Breakpoints: 1279px (6-column walls and sequences go to 3), 1079px (mobile menu, walls and counters stack, page-head panels merge without grooves), 719px (single column everywhere, tighter posts and padding, wide tables pin their first column and fade their right edge, capacity becomes an 8-week grid per technology). Low desktop screens (max-height 820px) keep the hero counter in the first viewport.

## Elevation & Depth

Hybrid: the wall itself is flat, built by aluminium gaps and groove lines; depth belongs only to objects standing in front of it. Shadows are long, soft and tinted by what they fall on (warm brown on yellow, graphite on the floor); none is a hard offset.

### Shadow Vocabulary
- **On the wall** (`box-shadow: 0 1px 2px rgb(64 50 0 / 0.14), 0 20px 36px -16px rgb(64 50 0 / 0.42)`): plinths, the hero counter, the fit checker, the request form and summary.
- **On the floor** (`box-shadow: 0 1px 2px rgb(28 30 33 / 0.08), 0 24px 44px -24px rgb(28 30 33 / 0.38)`): counters standing on the hall floor.
- **Armed counter** (`box-shadow: 0 2px 4px rgb(64 50 0 / 0.14), 0 34px 50px -18px rgb(64 50 0 / 0.5)`, with an 8px lift): the hero counter while a file is dragged over the window.
- **Lifted fascia** (`box-shadow: 0 14px 28px -20px rgb(28 30 33 / 0.5)`): the header once the page scrolls.
- **Palette** (`box-shadow: 0 2px 6px rgb(0 0 0 / 0.12), 0 40px 70px -24px rgb(0 0 0 / 0.55)`): the search dialog over a 50% graphite backdrop.

### Named Rules
**The Standing Object Rule.** Only something that physically stands in front of the wall or floor (plinth, counter, open menu, dialog) casts a shadow; wall panels never do.

## Shapes

Square-cornered throughout: walls, panels, counters, plinths, buttons, chips, inputs, steps and dialogs all have 0 radius. The single exception is the keycap in the search button (2px). Form comes from stand hardware: the post-and-rail grid, a 2px groove line drawn through the middle of each post around every panel, the 10px graphite top on counters, and the plinth's top board seen slightly from above (a trapezoid clipped 4% in at the back edge). Lists and tables open with a 2px graphite rule and divide with 1px hairlines. Small markers are filled squares (yes, timeline today, job bullets in yellow with a graphite edge), never circles or glyphs.

## Components

### Buttons
Solid, square and heavy-labelled; they look like signs on the stand.
- **Shape:** square (0), 2px border, 52px tall (44px small), 24px side padding (18px small).
- **Sign (yellow):** yellow fill, graphite label; hover inverts to graphite fill with yellow label. Used for the drawing upload and capacity booking.
- **Ink (graphite):** graphite fill, white label; hover lightens to #3a3e44. The header "Poptávka" is the small ink button.
- **Line:** transparent with a 2px graphite border; hover fills graphite (label turns yellow on a yellow wall, white elsewhere).
- **Motion:** colour transitions 0.25s on the house ease; disabled at 45% opacity.
- **Text link "more":** 700 weight, 2px underline offset 0.3em, thickening to 4px on hover.

### Chips
- **Style:** white, 1.5px Field Edge border, 40px tall, 600 weight, with a tabular count.
- **State:** hover darkens the border to graphite; pressed fills graphite with white text.

### Segmented control
A 2px graphite frame with 44px segments separated by 2px graphite dividers; hover is Pale Yellow, the checked segment is Signal Yellow.

### Cards / Containers
- **Wall panel:** yellow (or white on a white wall), square, padded by `pad`, groove-outlined; media panels are graphite under a full-bleed photo or render.
- **Counter:** white, 10px graphite top border, padded by `pad`, floor or wall shadow depending on what it stands in front of.
- **Plinth:** white label board (18px 22px 22px) under a trapezoid top board; carries the exhibit's name and a two-column spec list in data type.

### Inputs / Fields
- **Style:** white, 1.5px Field Edge border, square, 52px min height (120px textarea), 600-weight label above; dimension inputs use 1.375rem data type with an inline unit.
- **Focus:** border goes graphite plus a 3px graphite outline offset 2px; hover also turns the border graphite.
- **Error:** 2px Fault Red border, red 600 message below, and a red-bordered summary on #fdeceb above the step.
- **Drop zone:** dashed 2px Field Edge on #fafaf7; hover graphite edge; dragging or armed turns it solid yellow with a graphite border.

### Navigation
- **Fascia:** white header band between double aluminium rails with a groove, sticky; logo with yellow cut, 600-weight links, search button with keycap, small ink "Poptávka".
- **Links:** a 4px yellow bar wipes in from the left under the hovered link; the current page holds a graphite bar.
- **Mobile:** a graphite "menu" button opens a white sheet under the fascia, closed by a 6px aluminium edge; links set at panel-title size with hairlines, current page underlined 4px, a yellow call-to-action at the bottom.
- **Rail:** sticky aluminium strip of section links; hover white, current yellow.

### Capacity board (signature)
An eight-week grid per technology: floor-grey cells with a soft-graphite load bar rising from the bottom; free weeks are Signal Yellow cells. Hover or focus draws a 3px graphite outline and a graphite tooltip with tabular dates.

### Search palette
A dialog styled as a counter (white, 10px graphite top) rising 16px into place; the field shows a 4px yellow underline when focused, the selected result fills yellow.

### Sequence axis
Process steps and history sit on a continuous 2px graphite axis with a 12px tick per item; the last year ends in a filled square. On mobile the axis turns vertical.

## Do's and Don'ts

### Do:
- **Do** build every persuasive block as yellow panels inside an aluminium wall with 10px posts and the 2px groove line.
- **Do** put every working tool (tables, forms, checkers) on a white counter with the 10px graphite top.
- **Do** use yellow on white only to mean free, selected or actionable.
- **Do** set headlines at Archivo 800, width 125, line-height about 0.94 to 1, and keep display at or below 6rem.
- **Do** set comparable numbers at width 87 with tabular figures.
- **Do** keep every edge square and draw focus as a 3px graphite outline.
- **Do** keep motion to state changes on `cubic-bezier(0.16, 1, 0.3, 1)` plus the sideways page step, and honour reduced motion.

### Don't:
- **Don't** give a wall panel a shadow; shadows belong to plinths, counters and overlays only.
- **Don't** use hard offset shadows or rounded corners.
- **Don't** set white text on yellow, or use yellow as decoration on a white surface.
- **Don't** add a second typeface, monospace, or all-caps label lines.
- **Don't** add eyebrows or kickers above headlines.
- **Don't** use blueprint devices (title blocks, stamps, dimension-line ornament), a dark "tech" look, or any SETINA grammar (white protocol pages, blue/green measurement accents).
- **Don't** use glyph or emoji icons; icons are stroked SVG with square caps.

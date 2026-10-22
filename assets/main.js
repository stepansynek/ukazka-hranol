/* HRANOL s.r.o. – ukázkový web.
   Hlavička a menu, vyhledávání (⌘K), pult na výkresy v úvodu, technologie, kapacita s týdny podle dnešního data,
   ověření rozměrů dílu, filtr strojů, půdorys haly, poptávka po krocích, směr přechodu mezi stránkami.
   V náhledu v jednom souboru (window.HRANOL_SPA) navíc přepíná stránky přes #. */
(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const SPA = Boolean(window.HRANOL_SPA);
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FILES = { domu: "index.html", vyroba: "vyroba.html", stroje: "stroje.html", reference: "reference.html", "o-firme": "o-firme.html", poptavka: "poptavka.html" };
  const hrefFor = (page, anchor) => (SPA ? `#${anchor || page}` : `${FILES[page]}${anchor ? `#${anchor}` : ""}`);
  const fold = (s) => s.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();

  /* Týdny od pondělí aktuálního týdne, ať ukázka nestárne. Build zapíše data ke dni sestavení. */
  const MONTHS = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"];
  const monday = (() => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d; })();
  const weekStart = (offset) => { const d = new Date(monday); d.setDate(d.getDate() + offset * 7); return d; };
  const isoWeek = (date) => {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    return Math.ceil(((d - Date.UTC(d.getUTCFullYear(), 0, 1)) / 864e5 + 1) / 7);
  };
  const shortDate = (d) => `${d.getDate()}.\u00a0${d.getMonth() + 1}.`;
  const weekRange = (d) => {
    const end = new Date(d); end.setDate(end.getDate() + 4);
    return d.getMonth() === end.getMonth() ? `${d.getDate()}.–${shortDate(end)}` : `${shortDate(d)}–${shortDate(end)}`;
  };

  /* ---------- Výkresy na pultu: soubory z úvodu se přenesou do poptávky (IndexedDB, jinak jen v paměti stránky) ---------- */
  const tray = (() => {
    let memory = [];
    const open = () => new Promise((resolve, reject) => {
      const req = indexedDB.open("hranol", 1);
      req.onupgradeneeded = () => req.result.createObjectStore("tray");
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
    const run = async (mode, fn) => {
      const db = await open();
      return new Promise((resolve, reject) => {
        const tx = db.transaction("tray", mode);
        const req = fn(tx.objectStore("tray"));
        tx.oncomplete = () => { db.close(); resolve(req.result); };
        tx.onerror = () => { db.close(); reject(tx.error); };
      });
    };
    return {
      async get() {
        try { const v = await run("readonly", (store) => store.get("files")); return Array.isArray(v) ? v : memory; } catch { return memory; }
      },
      set(files) {
        memory = [...files];
        run("readwrite", (store) => store.put(memory, "files")).catch(() => {});
      },
    };
  })();

  const MAX_BYTES = 25 * 1024 * 1024;
  const formatSize = (bytes) => (bytes < 1048576 ? `${Math.max(1, Math.round(bytes / 1024))} kB` : `${(bytes / 1048576).toFixed(1).replace(".", ",")} MB`);
  const sizeOf = (list) => list.reduce((s, f) => s + f.size, 0);
  const tooBigText = (list) => `Soubory mají dohromady ${formatSize(sizeOf(list))}, limit je 25 MB. Větší data pošlete přes úschovnu na poptavky@hranol-obrabeni.cz.`;
  const merge = (into, list) => { for (const f of list) if (!into.some((x) => x.name === f.name && x.size === f.size)) into.push(f); return into; };
  const fileRow = (file, onRemove) => {
    const li = document.createElement("li");
    const name = Object.assign(document.createElement("span"), { className: "files__name", textContent: file.name });
    const size = Object.assign(document.createElement("span"), { className: "files__size", textContent: formatSize(file.size) });
    const remove = Object.assign(document.createElement("button"), { type: "button", textContent: "Odebrat" });
    remove.setAttribute("aria-label", `Odebrat soubor ${file.name}`);
    remove.addEventListener("click", onRemove);
    li.append(name, size, remove);
    return li;
  };
  const isVisible = (el) => Boolean(el && el.offsetParent !== null);
  const carriesFiles = (e) => [...(e.dataTransfer?.types || [])].includes("Files");

  /* Přetažení souboru kamkoli do okna: na úvodu skončí na pultu, v poptávce v prvním kroku formuláře. */
  const dropTargets = [];
  let dragDepth = 0;
  const activeTarget = () => dropTargets.find((t) => isVisible(t.el));
  window.addEventListener("dragenter", (e) => {
    const t = carriesFiles(e) && activeTarget();
    if (!t) return;
    e.preventDefault();
    dragDepth += 1;
    t.arm(true);
  });
  window.addEventListener("dragover", (e) => {
    if (!carriesFiles(e) || !activeTarget()) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  });
  window.addEventListener("dragleave", (e) => {
    const t = carriesFiles(e) && activeTarget();
    if (!t) return;
    dragDepth = Math.max(0, dragDepth - 1);
    if (!dragDepth) t.arm(false);
  });
  window.addEventListener("drop", (e) => {
    const t = carriesFiles(e) && activeTarget();
    if (!t) return;
    e.preventDefault();
    dragDepth = 0;
    t.arm(false);
    if (e.dataTransfer.files.length) t.take(e.dataTransfer.files);
  });

  /* ---------- Hlavička ---------- */
  const header = $(".fascia");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 4);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const menuBtn = $(".menu-btn");
  const nav = $("#nav");
  const setMenu = (open) => {
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.textContent = open ? "Zavřít" : "Menu";
    nav.classList.toggle("is-open", open);
  };
  menuBtn.addEventListener("click", () => setMenu(menuBtn.getAttribute("aria-expanded") !== "true"));
  nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });

  /* ---------- Přepínání stránek v náhledu ---------- */
  if (SPA) {
    const pages = $$("main[data-page]");
    const navLinks = $$("[data-nav]");

    const show = (page, target) => {
      const current = pages.find((p) => !p.hidden);
      const back = current && pages.indexOf(page) < pages.indexOf(current);
      const swap = () => {
        pages.forEach((p) => { p.hidden = p !== page; });
        document.title = page.dataset.title;
        navLinks.forEach((a) => {
          if (a.dataset.nav === page.dataset.page) a.setAttribute("aria-current", "page");
          else a.removeAttribute("aria-current");
        });
        const cta = $("[data-ftr-cta]");
        if (cta) cta.hidden = page.dataset.page === "poptavka";
        if (target) target.scrollIntoView({ behavior: current === page && !reduceMotion ? "smooth" : "auto" });
        else window.scrollTo(0, 0);
        document.dispatchEvent(new CustomEvent("hranol:page", { detail: page.dataset.page }));
      };
      if (current === page || reduceMotion || !document.startViewTransition) swap();
      else {
        try { document.startViewTransition({ update: swap, types: [back ? "back" : "forward"] }); } catch { document.startViewTransition(swap); }
      }
    };

    const route = () => {
      const id = decodeURIComponent(window.location.hash.slice(1));
      const home = pages[0];
      if (!id) return show(home);
      const page = pages.find((p) => p.dataset.page === id);
      if (page) return show(page);
      const el = document.getElementById(id);
      if (!el) return show(home);
      const host = el.closest("main[data-page]");
      if (host) return show(host, el);
      el.scrollIntoView();
      if (el.tabIndex >= -1) el.focus({ preventScroll: true });
    };

    window.addEventListener("hashchange", route);
    route();
  }

  /* ---------- Směr přechodu mezi stránkami: vpřed nebo zpět podél stánku ---------- */
  if (!SPA) {
    const order = Object.values(FILES);
    const indexOf = (url) => {
      try { return order.indexOf(new URL(url).pathname.split("/").pop() || "index.html"); } catch { return -1; }
    };
    const direction = (from, to) => (indexOf(to) < indexOf(from) ? "back" : "forward");
    window.addEventListener("pageswap", (e) => {
      if (e.viewTransition && e.activation?.entry) e.viewTransition.types.add(direction(location.href, e.activation.entry.url));
    });
    window.addEventListener("pagereveal", (e) => {
      const from = window.navigation?.activation?.from?.url;
      if (e.viewTransition && from) e.viewTransition.types.add(direction(from, location.href));
    });
  }

  /* ---------- Vyhledávání ⌘K ---------- */
  const palette = $("#palette");
  const indexEl = $("#search-index");
  if (palette && indexEl) {
    const items = JSON.parse(indexEl.textContent).map((item) => ({
      ...item,
      href: hrefFor(item.page, item.anchor),
      haystack: fold(`${item.title} ${item.group} ${item.keys}`),
    }));
    const pageNames = { domu: "Úvod", vyroba: "Výroba", stroje: "Strojový park", reference: "Reference", "o-firme": "O firmě", poptavka: "Poptávka" };
    const input = $("#palette-q");
    const list = $("#palette-list");
    const empty = $("#palette-empty");
    const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
    $$("[data-kbd]").forEach((k) => { k.textContent = isMac ? "⌘K" : "Ctrl K"; });

    let results = [];
    let active = 0;

    const select = (i) => {
      const options = $$('[role="option"]', list);
      if (!options.length) return;
      active = (i + options.length) % options.length;
      options.forEach((o, n) => o.setAttribute("aria-selected", String(n === active)));
      input.setAttribute("aria-activedescendant", options[active].id);
      options[active].scrollIntoView({ block: "nearest" });
    };

    const render = () => {
      const terms = fold(input.value.trim()).split(/\s+/).filter(Boolean);
      results = terms.length ? items.filter((it) => terms.every((t) => it.haystack.includes(t))) : items.filter((it) => it.group !== "Stroje");
      const frag = document.createDocumentFragment();
      let group = "";
      results.forEach((it, i) => {
        if (it.group !== group) {
          group = it.group;
          const g = document.createElement("li");
          g.className = "palette__group";
          g.setAttribute("role", "presentation");
          g.textContent = group;
          frag.append(g);
        }
        const li = document.createElement("li");
        li.className = "palette__item";
        li.id = `palette-opt-${i}`;
        li.setAttribute("role", "option");
        const a = document.createElement("a");
        a.href = it.href;
        a.tabIndex = -1;
        a.textContent = it.title;
        const hint = document.createElement("span");
        hint.textContent = pageNames[it.page];
        a.append(hint);
        li.append(a);
        li.addEventListener("mousemove", () => { if (active !== i) select(i); });
        frag.append(li);
      });
      list.replaceChildren(frag);
      empty.hidden = results.length > 0;
      select(0);
    };

    const open = () => {
      if (palette.open) return;
      setMenu(false);
      input.value = "";
      render();
      palette.showModal();
      input.focus();
    };

    const close = () => { if (palette.open) palette.close(); };

    const go = (i) => {
      const it = results[i];
      if (!it) return;
      close();
      window.location.href = it.href;
    };

    $$("[data-palette-open]").forEach((b) => b.addEventListener("click", open));
    input.addEventListener("input", render);
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); select(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); select(active - 1); }
      else if (e.key === "Enter") { e.preventDefault(); go(active); }
    });
    list.addEventListener("click", (e) => { if (e.target.closest("a")) close(); });
    palette.addEventListener("click", (e) => { if (e.target === palette) close(); });

    document.addEventListener("keydown", (e) => {
      const typing = e.target.closest?.("input, textarea, select, [contenteditable]");
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); palette.open ? close() : open(); }
      else if (e.key === "/" && !typing && !palette.open) { e.preventDefault(); open(); }
      else if (e.key === "Escape" && nav.classList.contains("is-open")) { setMenu(false); menuBtn.focus(); }
    });
  }

  /* ---------- Pult na výkresy v úvodu ---------- */
  const desk = $("[data-desk]");
  if (desk) {
    const input = $("[data-desk-input]", desk);
    const zone = $("[data-desk-drop]", desk);
    const list = $("[data-desk-files]", desk);
    const err = $("[data-desk-err]", desk);
    const pick = $("[data-desk-pick]", desk);
    const go = $("[data-desk-go]", desk);
    let held = [];

    const render = () => {
      list.replaceChildren(...held.map((file, i) => fileRow(file, () => { held.splice(i, 1); save(); pick.focus(); })));
      const big = sizeOf(held) > MAX_BYTES;
      desk.classList.toggle("has-files", held.length > 0);
      err.hidden = !big;
      err.textContent = big ? tooBigText(held) : "";
      go.hidden = !held.length || big;
      pick.textContent = held.length ? "Přidat další výkres" : "Nahrát výkres";
      pick.classList.toggle("btn--sign", !held.length);
      pick.classList.toggle("btn--line", held.length > 0);
    };
    const save = () => { render(); tray.set(held); };
    const take = (files) => {
      merge(held, files);
      save();
      if (desk.getBoundingClientRect().top < 0 || desk.getBoundingClientRect().bottom > window.innerHeight) {
        desk.scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
      }
    };

    tray.get().then((files) => { held = merge(files.slice(), held); render(); });
    pick.addEventListener("click", () => input.click());
    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", () => { take(input.files); input.value = ""; });
    dropTargets.push({ el: desk, arm: (on) => desk.classList.toggle("is-armed", on), take });
  }

  /* ---------- Technologie na úvodu ---------- */
  $$("[data-techlist]").forEach((block) => {
    const images = $$(".techlist__media img", block);
    const set = (key) => images.forEach((img) => img.classList.toggle("is-active", img.dataset.key === key));
    $$("a[data-img]", block).forEach((a) => {
      a.addEventListener("mouseenter", () => set(a.dataset.img));
      a.addEventListener("focus", () => set(a.dataset.img));
    });
  });

  /* ---------- Kapacita: týdny podle dnešního data, popisek u sloupce ---------- */
  $$(".cap__table thead [data-week]").forEach((th) => {
    const d = weekStart(Number(th.dataset.week));
    $(".cap__wk", th).textContent = `T${isoWeek(d)}`;
    $(".cap__date", th).textContent = shortDate(d);
  });
  $$(".cap__when[data-week]").forEach((el) => { el.textContent = `volno od ${shortDate(weekStart(Number(el.dataset.week)))}`; });
  $$("[data-status]").forEach((el) => {
    const d = weekStart(Number(el.dataset.week));
    $("[data-status-date]", el).textContent = `${d.getDate()}.\u00a0${MONTHS[d.getMonth()]}`;
  });

  $$("[data-capacity]").forEach((board) => {
    const tip = $(".cap__tip", board);
    const [title, body] = [$("strong", tip), $("span", tip)];
    const showTip = (cell) => {
      const d = weekStart(Number(cell.dataset.week));
      const name = $(".cap__name", cell.parentElement).textContent;
      title.textContent = `${name}, týden ${isoWeek(d)} (${weekRange(d)})`;
      body.textContent = `Vytížení ${cell.dataset.v} %, volno asi ${cell.dataset.freeH} h`;
      tip.hidden = false;
      const b = board.getBoundingClientRect();
      const c = cell.getBoundingClientRect();
      const half = tip.offsetWidth / 2;
      const x = Math.min(Math.max(c.left - b.left + c.width / 2, half + 8), b.width - half - 8);
      tip.style.left = `${x}px`;
      tip.style.top = `${c.top - b.top + 6}px`;
    };
    const hideTip = () => { tip.hidden = true; };
    $$(".cap__cell", board).forEach((cell) => {
      cell.addEventListener("mouseenter", () => showTip(cell));
      cell.addEventListener("focus", () => showTip(cell));
      cell.addEventListener("mouseleave", hideTip);
      cell.addEventListener("blur", hideTip);
    });
    $(".table-scroll", board)?.addEventListener("scroll", hideTip, { passive: true });
  });

  /* ---------- Výroba: aktivní položka podmenu ---------- */
  $$("[data-subnav]").forEach((sub) => {
    const links = $$("a", sub);
    const targets = links.map((a) => document.getElementById(a.getAttribute("href").split("#")[1])).filter(Boolean);
    if (!("IntersectionObserver" in window) || !targets.length) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => {
          const match = a.getAttribute("href").endsWith(`#${entry.target.id}`);
          if (match) {
            a.setAttribute("aria-current", "true");
            a.scrollIntoView({ block: "nearest", inline: "nearest" });
          } else a.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    targets.forEach((t) => observer.observe(t));
  });

  /* ---------- Strojový park: vejde se díl, filtr ---------- */
  const fit = $("[data-fit]");
  const rows = $$(".mtable tbody tr");

  if (fit && rows.length) {
    let shape = "box";
    const result = $("[data-fit-result]", fit);
    const num = (name) => {
      const v = parseFloat(($(`[data-dim="${name}"]`, fit).value || "").replace(",", ".").replace(/\s/g, ""));
      return Number.isFinite(v) && v > 0 ? v : 0;
    };
    const desc = (a, b) => b - a;
    const nameOf = (row) => $(".mt__name", row).textContent;
    const fmt = (n) => n.toLocaleString("cs-CZ");
    const list = (names) => (names.length < 2 ? names.join("") : `${names.slice(0, -1).join(", ")} a ${names.at(-1)}`);

    const fits = (row) => {
      const kind = row.dataset.kind;
      const env = row.dataset.env.split(",").map(Number);
      if (shape === "box") {
        if (kind !== "box") return false;
        const dims = [num("x"), num("y"), num("z")].sort(desc);
        const box = [...env].sort(desc);
        return dims.every((d, i) => d <= box[i]);
      }
      const d = num("d");
      const l = num("l");
      if (kind === "round") return d <= env[0] && l <= env[1];
      const dims = [l, d, d].sort(desc);
      const box = [...env].sort(desc);
      return dims.every((v, i) => v <= box[i]);
    };

    const update = () => {
      const dims = shape === "box" ? [num("x"), num("y"), num("z")] : [num("d"), num("l")];
      if (dims.some((v) => !v)) {
        rows.forEach((r) => r.classList.remove("is-fit", "is-nofit", "is-na"));
        result.textContent = "Zadejte všechny rozměry v milimetrech.";
        return;
      }
      /* Svařovací zdroje obálku nemají, rozměr dílu se jich netýká: v tabulce zůstanou neutrální. */
      const ok = rows.filter((r) => {
        const na = r.dataset.kind === "weld";
        const f = !na && fits(r);
        r.classList.toggle("is-na", na);
        r.classList.toggle("is-fit", f);
        r.classList.toggle("is-nofit", !na && !f);
        return f;
      });
      const machining = ok.filter((r) => r.dataset.tech !== "mereni");
      const measuring = ok.some((r) => r.dataset.tech === "mereni");
      const label = shape === "box" ? `${fmt(dims[0])} × ${fmt(dims[1])} × ${fmt(dims[2])} mm` : `Ø ${fmt(dims[0])} × ${fmt(dims[1])} mm`;
      result.replaceChildren();
      const strong = document.createElement("strong");
      if (!machining.length) {
        strong.textContent = `Díl ${label} se do našich strojů nevejde.`;
        result.append(strong, " Pošlete výkres, větší díly obrábíme u partnera ve Zlíně.");
        return;
      }
      /* Výsledek podle technologie: u rotačního dílu napřed soustruhy, u hranolového napřed frézky. */
      const groups = [
        ["soustruzeni", "Soustružení"], ["frezovani", "Frézování"], ["brouseni", "Broušení na kulato"],
      ].sort((a, b) => (shape === "box" ? (a[0] === "frezovani" ? -1 : b[0] === "frezovani" ? 1 : 0) : 0));
      const units = machining.reduce((s, r) => s + Number(r.dataset.count), 0);
      strong.textContent = `Díl ${label} obrobíme na ${units} ${units === 1 ? "stroji" : "strojích"}.`;
      const ul = document.createElement("ul");
      ul.className = "fit__groups";
      groups.forEach(([tech, name]) => {
        const hit = machining.filter((r) => r.dataset.tech === tech);
        if (!hit.length) return;
        const li = document.createElement("li");
        const head = document.createElement("span");
        head.textContent = name;
        li.append(head, list(hit.map((r) => `${nameOf(r)}${Number(r.dataset.count) > 1 ? ` (${r.dataset.count}×)` : ""}`)));
        ul.append(li);
      });
      const after = document.createElement("p");
      after.className = "fit__after";
      after.textContent = measuring ? "Rozměry pak ověříme na 3D měřicím stroji." : "Na 3D měřicí stroj je díl příliš velký, měříme ho ručně.";
      result.append(strong, ul, after);
    };

    $$(".seg [data-shape]", fit).forEach((btn) => btn.addEventListener("click", () => {
      shape = btn.dataset.shape;
      $$(".seg [data-shape]", fit).forEach((b) => b.setAttribute("aria-checked", String(b === btn)));
      $$("[data-inputs]", fit).forEach((g) => { g.hidden = g.dataset.inputs !== shape; });
      update();
    }));
    $$("input", fit).forEach((i) => i.addEventListener("input", update));
    update();

    const chips = $$("[data-filter]");
    chips.forEach((chip) => chip.addEventListener("click", () => {
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
      const f = chip.dataset.filter;
      rows.forEach((r) => { r.hidden = f !== "all" && r.dataset.tech !== f; });
    }));
  }

  /* ---------- O firmě: půdorys haly a popisy zón se zvýrazňují navzájem ---------- */
  $$("[data-hall]").forEach((hall) => {
    const items = $$(".zones li", hall);
    const shapes = $$(".hall__zone", hall);
    const set = (zone) => {
      items.forEach((li) => li.classList.toggle("is-active", li.dataset.zone === zone));
      shapes.forEach((g) => g.classList.toggle("is-active", g.dataset.zone === zone));
    };
    [...items, ...shapes].forEach((el) => {
      el.addEventListener("mouseenter", () => set(el.dataset.zone));
      el.addEventListener("mouseleave", () => set(null));
    });
    /* Klávesnicí se zóna zvýrazní přes odkazy na stroje v jejím popisu. */
    items.forEach((li) => {
      li.addEventListener("focusin", () => set(li.dataset.zone));
      li.addEventListener("focusout", () => set(null));
    });
  });

  /* ---------- Poptávka po krocích ---------- */
  const rfq = $("#rfq");
  if (!rfq) return;

  const dateInput = $("#rfq-date");
  const today = new Date();
  dateInput.min = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

  const steps = $$(".rfq__step", rfq);
  const markers = $$(".stepper li", rfq);
  const error = $("#rfq-error");
  const done = $("#rfq-done");
  const fileList = $("[data-file-list]", rfq);
  const fileError = $("#rfq-files-err");
  const sum = (key, value) => { const el = $(`[data-sum="${key}"]`); if (el) el.textContent = value; };
  let files = [];
  let current = 0;

  const carried = $("[data-carried]", rfq);

  const checkFiles = () => {
    const tooBig = sizeOf(files) > MAX_BYTES;
    fileError.hidden = !tooBig;
    fileError.textContent = tooBig ? tooBigText(files) : "";
    return !tooBig;
  };

  const renderFiles = () => {
    fileList.replaceChildren(...files.map((file, i) => fileRow(file, () => { files.splice(i, 1); renderFiles(); $("#rfq-files").focus(); })));
    sum("files", files.length ? `${files.length} (${formatSize(sizeOf(files))})` : "žádné");
    if (!files.length) carried.hidden = true;
    checkFiles();
    tray.set(files);
  };

  const addFiles = (list) => {
    merge(files, list);
    renderFiles();
  };

  tray.get().then((stored) => {
    if (!stored.length) return;
    const before = files.length;
    files = merge(stored.slice(), files);
    renderFiles();
    carried.hidden = before > 0;
  });

  const rfqDrop = $("[data-drop]", rfq);
  dropTargets.push({
    el: rfq,
    arm: (on) => rfqDrop.classList.toggle("is-over", on && !steps[0].hidden),
    take: (list) => { addFiles(list); if (current !== 0) sum("files", `${files.length} (${formatSize(sizeOf(files))})`); },
  });

  $$("[data-drop]", rfq).forEach((zone) => {
    const input = $("[data-file-input]", zone);
    input.addEventListener("change", () => { addFiles(input.files); input.value = ""; });
    zone.addEventListener("click", (e) => { if (!e.target.closest("label, input")) input.click(); });
  });

  /* Živé shrnutí */
  const dateFmt = (v) => { const [y, m, d] = v.split("-"); return y ? `${Number(d)}. ${Number(m)}. ${y}` : "—"; };
  $("#rfq-qty").addEventListener("input", (e) => sum("qty", e.target.value.trim() || "—"));
  $("#rfq-material").addEventListener("change", (e) => sum("material", e.target.value.toLowerCase()));
  $("#rfq-finish").addEventListener("change", (e) => sum("finish", e.target.value.toLowerCase()));
  $("#rfq-date").addEventListener("change", (e) => sum("date", dateFmt(e.target.value)));
  $("#rfq-nda").addEventListener("change", (e) => sum("nda", e.target.checked ? "ano, před zasláním výkresů" : "ne"));
  const repeat = $$("[data-value]", rfq);
  repeat.forEach((btn) => btn.addEventListener("click", () => {
    repeat.forEach((b) => b.setAttribute("aria-checked", String(b === btn)));
    sum("repeat", btn.dataset.value);
  }));

  /* Validace kroků */
  const rules = {
    1: [{ id: "rfq-qty", test: (v) => /\d/.test(v) }],
    2: [
      { id: "rfq-name", test: (v) => v.length > 1 },
      { id: "rfq-company", test: (v) => v.length > 1 },
      { id: "rfq-email", test: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) },
    ],
  };

  const validate = (rule) => {
    const input = document.getElementById(rule.id);
    const ok = rule.test(input.value.trim());
    input.setAttribute("aria-invalid", String(!ok));
    document.getElementById(`${rule.id}-err`).hidden = ok;
    return ok;
  };

  Object.values(rules).flat().forEach((rule) => {
    const input = document.getElementById(rule.id);
    input.addEventListener("input", () => { if (input.getAttribute("aria-invalid") === "true") validate(rule); });
  });

  const fieldsWord = (n) => (n === 1 ? "1 pole" : n < 5 ? `${n} pole` : `${n} polí`);

  const stepValid = (i) => {
    const invalid = (rules[i] || []).filter((r) => !validate(r));
    const filesOk = i !== 0 || checkFiles();
    if (!invalid.length && filesOk) { error.hidden = true; return true; }
    error.textContent = `Než budete pokračovat, opravte ${fieldsWord(invalid.length + (filesOk ? 0 : 1))}.`;
    error.hidden = false;
    (invalid[0] ? document.getElementById(invalid[0].id) : $("#rfq-files")).focus();
    return false;
  };

  const go = (i) => {
    current = i;
    steps.forEach((s, n) => { s.hidden = n !== i; });
    markers.forEach((m, n) => {
      m.classList.toggle("is-done", n < i);
      m.classList.toggle("is-current", n === i);
      if (n === i) m.setAttribute("aria-current", "step"); else m.removeAttribute("aria-current");
    });
    error.hidden = true;
    $(".rfq__legend", steps[i]).focus({ preventScroll: true });
    const top = rfq.getBoundingClientRect().top;
    if (top < 0) rfq.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  };

  $$("[data-next]", rfq).forEach((b) => b.addEventListener("click", () => { if (stepValid(current)) go(current + 1); }));
  $$("[data-back]", rfq).forEach((b) => b.addEventListener("click", () => go(current - 1)));

  rfq.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!stepValid(2)) return;
    steps.forEach((s) => { s.hidden = true; });
    $(".stepper", rfq).hidden = true;
    done.hidden = false;
    tray.set([]);
    $("#rfq-done-title").focus();
  });

  $("#rfq-reset").addEventListener("click", () => {
    rfq.reset();
    files = [];
    renderFiles();
    ["qty", "date"].forEach((k) => sum(k, "—"));
    sum("material", "podle výkresu");
    sum("finish", "bez úpravy");
    sum("nda", "ne");
    repeat.forEach((b, n) => b.setAttribute("aria-checked", String(n === 0)));
    sum("repeat", "jednorázově");
    Object.values(rules).flat().forEach((r) => {
      document.getElementById(r.id).removeAttribute("aria-invalid");
      document.getElementById(`${r.id}-err`).hidden = true;
    });
    done.hidden = true;
    $(".stepper", rfq).hidden = false;
    go(0);
  });
})();

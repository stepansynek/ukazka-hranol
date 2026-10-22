/* HRANOL s.r.o. – 3D model obrobené příruby nad podstavcem v úvodu (three.js r128).
   Studiové prostředí pro odlesky hliníku, pomalé otáčení, otáčení tažením se setrvačností.
   Bez WebGL zůstane nad podstavcem statický render stejné příruby s průhledným pozadím, štítek tak platí dál. */
(() => {
  "use strict";

  const stage = document.getElementById("stage");
  const canvas = document.getElementById("part-canvas");
  if (!stage || !canvas) return;

  const fallback = () => {
    stage.classList.add("stage--fallback");
    stage.style.backgroundImage = 'url("assets/img/priruba-1200.webp")';
  };

  if (!window.THREE) { fallback(); return; }
  const T = window.THREE;

  let renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
  } catch (err) {
    fallback();
    return;
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  renderer.physicallyCorrectLights = true;

  const scene = new T.Scene();
  const camera = new T.PerspectiveCamera(26, 1, 10, 3000);

  /* Studio: místnost se softboxy, z ní předpočítané odrazy */
  const pmrem = new T.PMREMGenerator(renderer);
  const studio = new T.Scene();
  studio.add(new T.Mesh(new T.BoxGeometry(10, 10, 10), new T.MeshBasicMaterial({ color: 0x1b1f23, side: T.BackSide })));
  const softbox = (w, h, pos, intensity) => {
    const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: new T.Color(intensity, intensity, intensity), side: T.DoubleSide }));
    m.position.set(pos[0], pos[1], pos[2]);
    m.lookAt(0, 0, 0);
    studio.add(m);
  };
  softbox(6, 1.6, [0, 4.9, 0.8], 14);
  softbox(1.6, 5.5, [-4.9, 1.4, 1.8], 7);
  softbox(0.9, 5.5, [4.9, 0.8, -0.6], 5);
  softbox(5, 0.7, [0, 2.2, -4.9], 3);
  softbox(4, 0.5, [0, -2.4, 4.9], 1.6);
  softbox(10, 3, [0, -4.9, 0], 0.35);
  scene.environment = pmrem.fromScene(studio, 0.035).texture;
  pmrem.dispose();

  const key = new T.DirectionalLight(0xffffff, 2.2);
  key.position.set(-180, 260, 220);
  scene.add(key);

  /* Soustředné stopy po čelním soustružení na plochách */
  const facing = (() => {
    const size = 1024;
    const c = document.createElement("canvas");
    c.width = c.height = size;
    const g = c.getContext("2d");
    g.fillStyle = "rgb(104,104,104)";
    g.fillRect(0, 0, size, size);
    for (let r = 4; r < size * 0.72; r += 3) {
      const v = 88 + Math.round(Math.random() * 34);
      g.strokeStyle = `rgb(${v},${v},${v})`;
      g.lineWidth = 1.4;
      g.beginPath();
      g.arc(size / 2, size / 2, r, 0, Math.PI * 2);
      g.stroke();
    }
    const tex = new T.CanvasTexture(c);
    tex.wrapS = tex.wrapT = T.ClampToEdgeWrapping;
    tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
    return tex;
  })();

  /* Materiály: plochy (caps) a boky (sides) mají jinou drsnost */
  const faceMat = (radius) => {
    const tex = facing.clone();
    tex.needsUpdate = true;
    tex.repeat.set(1 / (radius * 2.05), 1 / (radius * 2.05));
    tex.offset.set(0.5, 0.5);
    return new T.MeshStandardMaterial({ color: 0xd3d8dc, metalness: 1, roughness: 1, roughnessMap: tex, envMapIntensity: 1.05 });
  };
  const sideMat = new T.MeshStandardMaterial({ color: 0xdfe3e7, metalness: 1, roughness: 0.2, envMapIntensity: 1.2 });
  const grooveMat = new T.MeshStandardMaterial({ color: 0xa9b0b6, metalness: 1, roughness: 0.42 });

  const ring = (outer, inner, depth, bevel, holes = []) => {
    const shape = new T.Shape();
    shape.absarc(0, 0, outer, 0, Math.PI * 2, false);
    const bore = new T.Path();
    bore.absarc(0, 0, inner, 0, Math.PI * 2, true);
    shape.holes.push(bore);
    holes.forEach(([x, y, r]) => {
      const h = new T.Path();
      h.absarc(x, y, r, 0, Math.PI * 2, true);
      shape.holes.push(h);
    });
    return new T.ExtrudeGeometry(shape, {
      depth,
      bevelEnabled: bevel > 0,
      bevelThickness: bevel,
      bevelSize: bevel,
      bevelSegments: 2,
      curveSegments: 160,
    });
  };

  /* Příruba Ø120 × 14, šest děr Ø9 na Ø96, náboj Ø70 s drážkou pro pojistný kroužek, otvor Ø40 */
  const part = new T.Group();
  const holes = Array.from({ length: 6 }, (_, i) => {
    const a = (i * Math.PI) / 3 + Math.PI / 6;
    return [48 * Math.cos(a), 48 * Math.sin(a), 4.5];
  });
  const flange = new T.Mesh(ring(59, 21, 12, 1, holes), [faceMat(60), sideMat]);
  const hubA = new T.Mesh(ring(34, 21, 22, 0.8), [faceMat(35), sideMat]);
  hubA.position.z = 13;
  const groove = new T.Mesh(ring(32.6, 21, 2.2, 0), [grooveMat, grooveMat]);
  groove.position.z = 36.4;
  const hubB = new T.Mesh(ring(34, 21, 12, 0.8), [faceMat(35), sideMat]);
  hubB.position.z = 39.4;
  part.add(flange, hubA, groove, hubB);
  part.position.z = -26;

  const pivot = new T.Group();
  pivot.add(part);
  const holder = new T.Group();
  holder.add(pivot);
  holder.rotation.x = -1.02;
  holder.rotation.z = 0.32;
  const turntable = new T.Group();
  turntable.add(holder);
  scene.add(turntable);

  /* Velikost a kamera */
  let width = 0;
  let height = 0;
  const resize = () => {
    const r = stage.getBoundingClientRect();
    width = Math.round(r.width);
    height = Math.round(r.height);
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    const distance = camera.aspect < 0.95 ? 430 : 330;
    camera.position.set(0, 46, distance);
    camera.lookAt(0, -6, 0);
    camera.updateProjectionMatrix();
    draw();
  };

  /* Otáčení: automaticky kolem osy dílu, tažením kolem svislé osy se setrvačností */
  let spin = 0;
  let yaw = 0.35;
  let velocity = 0;
  let dragging = false;
  let lastX = 0;

  canvas.addEventListener("pointerdown", (e) => {
    dragging = true;
    lastX = e.clientX;
    velocity = 0;
    canvas.setPointerCapture(e.pointerId);
    wake();
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    const dx = e.clientX - lastX;
    lastX = e.clientX;
    yaw += dx * 0.009;
    velocity = dx * 0.009;
  });
  const release = () => { dragging = false; };
  canvas.addEventListener("pointerup", release);
  canvas.addEventListener("pointercancel", release);

  const draw = () => {
    pivot.rotation.z = spin;
    turntable.rotation.y = yaw;
    renderer.render(scene, camera);
  };

  let visible = true;
  let running = false;
  let last = 0;

  const frame = (t) => {
    if (!visible || document.hidden || !width) { running = false; return; }
    const dt = Math.min((t - last) / 1000 || 0, 0.05);
    last = t;
    if (!reduceMotion) spin += dt * 0.22;
    if (!dragging && Math.abs(velocity) > 0.0001) {
      yaw += velocity;
      velocity *= 0.94;
    }
    draw();
    const idle = reduceMotion && !dragging && Math.abs(velocity) <= 0.0001;
    if (idle) { running = false; return; }
    requestAnimationFrame(frame);
  };

  const wake = () => {
    if (running) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(frame);
  };

  new ResizeObserver(() => { resize(); wake(); }).observe(stage);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; if (visible) wake(); }).observe(stage);
  }
  document.addEventListener("visibilitychange", () => { if (!document.hidden) wake(); });
  document.addEventListener("hranol:page", () => { resize(); wake(); });

  resize();
  draw();
  stage.classList.add("is-ready");
  wake();
})();

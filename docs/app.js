// Python Pals — web edition. Runs entirely in the browser via Pyodide
// (real CPython compiled to WASM). No server, no install, no exe.
"use strict";

const CHAPTERS = window.PP_DATA.chapters;
const HINTS = window.PP_DATA.hints;
const QUIZ = window.PP_DATA.quiz;
const ADV_LEVELS = window.PP_ADV_LEVELS;
const THEMES = window.PP_THEMES;
const GRID = window.PP_GRID;

const TOTAL_PUZZLES = CHAPTERS.reduce((n, c) => n + c.puzzles.length, 0);
const TOTAL_ADV = ADV_LEVELS.length;
const TOTAL_TASKS = TOTAL_PUZZLES + TOTAL_ADV;

const SAVE_KEY = "python_pals_progress_v1";

function loadProgress() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) { /* ignore */ }
  return { stars: 0, solved: [], adv_solved: [], name: "", started: "", last: "" };
}
function saveProgress() {
  localStorage.setItem(SAVE_KEY, JSON.stringify(progress));
}

let progress = loadProgress();
let pyodideReady = null;
let view = { mode: "welcome", chIndex: 0, pzIndex: 0, advIndex: 0 };

// ---------- Pyodide bootstrap ----------
async function initPyodide() {
  const status = document.getElementById("boot-status");
  status.textContent = "Waking up the Python engine…";
  const py = await loadPyodide();
  status.textContent = "Almost ready…";
  return py;
}
pyodideReady = initPyodide();

async function runPython(code, heroEngine) {
  const py = await pyodideReady;
  py.globals.set("__pp_code", code);
  py.globals.set("__pp_hero", heroEngine || null);
  const src = `
import io, sys, json
_buf = io.StringIO()
_old_stdout = sys.stdout
sys.stdout = _buf
_err = None
try:
    exec(__pp_code, {"hero": __pp_hero} if __pp_hero is not None else {})
except Exception as _e:
    _err = type(_e).__name__ + ": " + str(_e)
finally:
    sys.stdout = _old_stdout
json.dumps({"output": _buf.getvalue(), "error": _err})
`;
  const resultJson = py.runPython(src);
  return JSON.parse(resultJson);
}

// ---------- Chrome: header stats ----------
function refreshStats() {
  document.getElementById("star-count").textContent = `⭐ ${progress.stars} stars`;
  document.getElementById("badge-count").textContent = `🏅 ${progress.adv_solved.length} badges`;
}

// ---------- Rail ----------
function buildRail() {
  const rail = document.getElementById("rail");
  rail.innerHTML = "";

  const chLabel = document.createElement("div");
  chLabel.className = "rail-label";
  chLabel.textContent = "CHAPTERS";
  rail.appendChild(chLabel);

  CHAPTERS.forEach((ch, i) => {
    const solvedCount = ch.puzzles.filter((_, j) => progress.solved.includes(`${i}-${j}`)).length;
    const done = solvedCount === ch.puzzles.length;
    const btn = document.createElement("button");
    btn.className = "rail-item" + (done ? " done" : "");
    btn.innerHTML = `<span class="rail-emoji">${ch.emoji}</span><span>${i + 1}. ${ch.title}</span>${done ? '<span class="rail-check">✓</span>' : ""}`;
    btn.onclick = () => showChapter(i);
    rail.appendChild(btn);
  });

  let lastWorld = null;
  ADV_LEVELS.forEach((lv, i) => {
    const world = lv.world || "🌳 ADVENTURE MODE";
    if (world !== lastWorld) {
      lastWorld = world;
      const label = document.createElement("div");
      label.className = "rail-label world" + (world.includes("SPACE") ? " space" : "");
      label.textContent = world;
      label.style.marginTop = "14px";
      rail.appendChild(label);
    }
    const done = progress.adv_solved.includes(lv.id);
    const btn = document.createElement("button");
    btn.className = "rail-item" + (done ? " done" : "");
    btn.innerHTML = `<span class="rail-emoji">${lv.emoji}</span><span>${lv.id} ${lv.title}</span>${done ? '<span class="rail-check">✓</span>' : ""}`;
    btn.onclick = () => showAdventure(i);
    rail.appendChild(btn);
  });
}

function highlightRail() {
  const items = document.querySelectorAll(".rail-item");
  items.forEach(el => el.classList.remove("active"));
  const idx = view.mode === "lesson" ? view.chIndex
    : view.mode === "adventure" ? CHAPTERS.length + view.advIndex : -1;
  if (idx >= 0 && items[idx]) items[idx].classList.add("active");
}

// ---------- Home ----------
function showHome() {
  view.mode = "home";
  const main = document.getElementById("main");
  const donePz = new Set(progress.solved).size;
  const doneAdv = new Set(progress.adv_solved).size;
  const done = donePz + doneAdv;
  const pct = TOTAL_TASKS ? Math.round((done / TOTAL_TASKS) * 100) : 0;

  main.innerHTML = `
    <div class="home-wrap">
      <h1>Hi ${escapeHtml(progress.name || "coder")}! 👋</h1>
      <p class="sub">Here is your coding progress:</p>
      <div class="progress-card">
        <div class="progress-head">
          <span>📊 Progress Summary</span>
          <span class="pct">${pct}%</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
        <div class="progress-sub">${done} / ${TOTAL_TASKS} done</div>
        <div class="stat-grid">
          <div class="stat"><div class="stat-label">📅 Started</div><div class="stat-val">${progress.started || "—"}</div></div>
          <div class="stat"><div class="stat-label">📖 Exercises</div><div class="stat-val">${donePz} / ${TOTAL_PUZZLES}</div></div>
          <div class="stat"><div class="stat-label">🏅 Badges</div><div class="stat-val">${doneAdv} / ${TOTAL_ADV}</div></div>
          <div class="stat"><div class="stat-label">⭐ Stars</div><div class="stat-val">${progress.stars}</div></div>
        </div>
      </div>
      <div class="home-actions">
        <button class="btn primary" id="continue-btn">▶ Continue Learning</button>
        <button class="btn green" id="adv-btn">🌳 Adventure Mode</button>
        <button class="btn amber" id="rename-btn">✏️ Change Name</button>
      </div>
    </div>`;

  document.getElementById("continue-btn").onclick = () => {
    const idx = CHAPTERS.findIndex((ch, i) => ch.puzzles.some((_, j) => !progress.solved.includes(`${i}-${j}`)));
    showChapter(idx >= 0 ? idx : 0);
  };
  document.getElementById("adv-btn").onclick = () => {
    const idx = ADV_LEVELS.findIndex(lv => !progress.adv_solved.includes(lv.id));
    showAdventure(idx >= 0 ? idx : 0);
  };
  document.getElementById("rename-btn").onclick = showWelcome;
  highlightRail();
}

// ---------- Welcome ----------
function showWelcome() {
  view.mode = "welcome";
  const main = document.getElementById("main");
  main.innerHTML = `
    <div class="welcome-wrap">
      <div class="welcome-emoji">🐍</div>
      <h1>Welcome to Python Pals!</h1>
      <h2>What is your name, coder?</h2>
      <input id="name-input" type="text" maxlength="18" placeholder="Type your name" value="${escapeHtml(progress.name || "")}" />
      <button class="btn primary" id="start-btn">Let's Go! 🚀</button>
    </div>`;
  const input = document.getElementById("name-input");
  input.focus();
  const go = () => {
    const name = input.value.trim();
    if (!name) { input.focus(); return; }
    progress.name = name;
    if (!progress.started) progress.started = new Date().toDateString();
    progress.last = new Date().toDateString();
    saveProgress();
    refreshStats();
    showHome();
  };
  document.getElementById("start-btn").onclick = go;
  input.addEventListener("keydown", e => { if (e.key === "Enter") go(); });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// ---------- Lesson (chapter + puzzle) ----------
function showChapter(i) {
  view.mode = "lesson"; view.chIndex = i; view.pzIndex = 0;
  renderLesson();
  highlightRail();
}

function renderLesson() {
  const ch = CHAPTERS[view.chIndex];
  const pz = ch.puzzles[view.pzIndex];
  const main = document.getElementById("main");

  main.innerHTML = `
    <div class="lesson-wrap">
      <div class="lesson-head">
        <h1>${ch.emoji} ${escapeHtml(ch.title)}</h1>
        <button class="btn small" id="hint-btn">💡 Hint</button>
      </div>
      <div class="theory-card">
        ${ch.theory.map(line => `<div class="theory-line">${formatTheory(line)}</div>`).join("")}
      </div>
      <div class="puzzle-card">
        <div class="puzzle-prompt">${escapeHtml(pz.prompt)}</div>
        <textarea id="code-editor" class="code-editor" spellcheck="false">${escapeHtml(pz.starter)}</textarea>
        <div class="puzzle-actions">
          <button class="btn primary" id="run-btn">▶ Run</button>
          <span class="puzzle-counter">Puzzle ${view.pzIndex + 1} / ${ch.puzzles.length}</span>
          <div class="spacer"></div>
          <button class="btn small" id="prev-btn" ${view.pzIndex === 0 ? "disabled" : ""}>← Prev</button>
          <button class="btn small" id="next-btn" ${view.pzIndex === ch.puzzles.length - 1 ? "disabled" : ""}>Next →</button>
        </div>
        <div id="output-box" class="output-box empty">Press ▶ Run to see your output here.</div>
      </div>
    </div>`;

  document.getElementById("run-btn").onclick = runPuzzle;
  document.getElementById("prev-btn").onclick = () => { if (view.pzIndex > 0) { view.pzIndex--; renderLesson(); } };
  document.getElementById("next-btn").onclick = () => { if (view.pzIndex < ch.puzzles.length - 1) { view.pzIndex++; renderLesson(); } };
  document.getElementById("hint-btn").onclick = showHint;

  const editor = document.getElementById("code-editor");
  editor.addEventListener("keydown", e => {
    if (e.key === "Tab") { e.preventDefault(); insertAtCursor(editor, "    "); }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runPuzzle();
  });
}

function formatTheory(line) {
  const isExample = /^\s{3}/.test(line);
  return `<div class="${isExample ? "theory-code" : ""}">${escapeHtml(line)}</div>`;
}

function insertAtCursor(el, text) {
  const start = el.selectionStart, end = el.selectionEnd;
  el.value = el.value.slice(0, start) + text + el.value.slice(end);
  el.selectionStart = el.selectionEnd = start + text.length;
}

async function runPuzzle() {
  const ch = CHAPTERS[view.chIndex];
  const pz = ch.puzzles[view.pzIndex];
  const editor = document.getElementById("code-editor");
  const out = document.getElementById("output-box");
  const runBtn = document.getElementById("run-btn");
  runBtn.disabled = true; runBtn.textContent = "Running…";
  out.className = "output-box";
  out.textContent = "Running…";

  const result = await runPython(editor.value, null);
  runBtn.disabled = false; runBtn.textContent = "▶ Run";

  if (result.error) {
    out.className = "output-box bad";
    out.textContent = `Oops! Little bug: ${result.error}\n💡 Check your spelling and quotes, then try again!`;
    return;
  }

  const got = result.output.trim().replace(/\r\n/g, "\n");
  const shown = got || "(nothing printed yet)";
  const correct = pz.expect_any ? Boolean(got) : got === pz.expect.trim();

  if (correct) {
    const key = `${view.chIndex}-${view.pzIndex}`;
    const first = !progress.solved.includes(key);
    if (first) {
      progress.solved.push(key);
      progress.stars += 1;
      progress.last = new Date().toDateString();
      saveProgress();
      refreshStats();
      buildRail();
      highlightRail();
    }
    out.className = "output-box good";
    out.textContent = `Output:\n${shown}\n\n✅ Great job! ${first ? "🌟 +1 star!" : "🌟 Nice!"}  Press Next → to keep going.`;
  } else {
    out.className = "output-box warn";
    const hint = pz.expect_any ? "" : `\n🎯 We were hoping to see:\n${pz.expect}`;
    out.textContent = `Output:\n${shown}\n\n🤏 Almost! Try again.${hint}`;
  }
}

// ---------- Hint / quiz popup ----------
function showHint() {
  const i = view.chIndex;
  const hint = HINTS[i];
  const quiz = QUIZ[i] || [];
  const modal = document.getElementById("modal");
  modal.classList.remove("hidden");
  modal.innerHTML = `
    <div class="modal-card">
      <div class="modal-head">💡 Quick Reminder <button class="modal-close" id="modal-close">✕</button></div>
      <p class="modal-hint">${escapeHtml(hint)}</p>
      ${quiz.map((q, qi) => `
        <div class="quiz-q">
          <div class="quiz-question">${escapeHtml(q.q)}</div>
          <div class="quiz-opts">
            ${q.opts.map((opt, oi) => `<button class="quiz-opt" data-qi="${qi}" data-oi="${oi}">${escapeHtml(opt)}</button>`).join("")}
          </div>
        </div>`).join("")}
    </div>`;
  document.getElementById("modal-close").onclick = closeModal;
  modal.querySelectorAll(".quiz-opt").forEach(btn => {
    btn.onclick = () => {
      const qi = Number(btn.dataset.qi), oi = Number(btn.dataset.oi);
      const correct = quiz[qi].a === oi;
      const group = modal.querySelectorAll(`.quiz-opt[data-qi="${qi}"]`);
      group.forEach(b => b.disabled = true);
      btn.classList.add(correct ? "correct" : "wrong");
      if (!correct) group[quiz[qi].a].classList.add("correct");
    };
  });
}
function closeModal() {
  const modal = document.getElementById("modal");
  modal.classList.add("hidden");
  modal.innerHTML = "";
}

// ---------- Adventure mode ----------
function showAdventure(i) {
  view.mode = "adventure"; view.advIndex = i;
  renderAdventure();
  highlightRail();
}

function renderAdventure() {
  const lv = ADV_LEVELS[view.advIndex];
  const theme = THEMES[lv.theme || "forest"];
  const main = document.getElementById("main");

  main.innerHTML = `
    <div class="adv-wrap">
      <div class="lesson-head">
        <h1>${lv.emoji} ${lv.id} — ${escapeHtml(lv.title)}</h1>
      </div>
      <div class="adv-mission">
        ${lv.mission.map(l => `<div class="mission-line ${/^\s{2,}|^[a-zA-Z_]+\(|^for |^if |^   /.test(l) ? "mission-code" : ""}">${escapeHtml(l)}</div>`).join("")}
      </div>
      <div class="adv-stage">
        <div class="adv-left">
          <div class="adv-tools">${lv.tools.map(t => `<span class="tool-chip">${escapeHtml(t)}</span>`).join("")}</div>
          <textarea id="adv-editor" class="code-editor" spellcheck="false">${escapeHtml(lv.starter)}</textarea>
          <div class="puzzle-actions">
            <button class="btn primary" id="adv-run-btn">▶ Run</button>
            <div class="spacer"></div>
            <button class="btn small" id="adv-prev-btn" ${view.advIndex === 0 ? "disabled" : ""}>← Prev</button>
            <button class="btn small" id="adv-next-btn" ${view.advIndex === ADV_LEVELS.length - 1 ? "disabled" : ""}>Next →</button>
          </div>
        </div>
        <div class="adv-right">
          <canvas id="adv-canvas" width="360" height="360"></canvas>
          <div id="adv-output" class="output-box empty">Press ▶ Run to send your hero!</div>
        </div>
      </div>
    </div>`;

  drawGrid(lv, { x: lv.start[0], y: lv.start[1], dir: lv.start[2], trees: new Set(lv.trees.map(([x, y]) => x + "," + y)), gems: new Set(lv.gems.map(([x, y]) => x + "," + y)), collected: 0, painted: {} });

  document.getElementById("adv-run-btn").onclick = runAdventure;
  document.getElementById("adv-prev-btn").onclick = () => { if (view.advIndex > 0) showAdventure(view.advIndex - 1); };
  document.getElementById("adv-next-btn").onclick = () => { if (view.advIndex < ADV_LEVELS.length - 1) showAdventure(view.advIndex + 1); };

  const editor = document.getElementById("adv-editor");
  editor.addEventListener("keydown", e => {
    if (e.key === "Tab") { e.preventDefault(); insertAtCursor(editor, "    "); }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runAdventure();
  });
}

function drawGrid(lv, frame) {
  const theme = THEMES[lv.theme || "forest"];
  const canvas = document.getElementById("adv-canvas");
  const ctx = canvas.getContext("2d");
  const size = canvas.width / GRID;

  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      ctx.fillStyle = (x + y) % 2 === 0 ? theme.bg1 : theme.bg2;
      ctx.fillRect(x * size, y * size, size, size);
    }
  }

  const wallSet = new Set(lv.walls.map(([x, y]) => x + "," + y));
  wallSet.forEach(k => {
    const [x, y] = k.split(",").map(Number);
    ctx.fillStyle = theme.wall;
    ctx.fillRect(x * size, y * size, size, size);
  });

  Object.entries(frame.painted).forEach(([k, color]) => {
    const [x, y] = k.split(",").map(Number);
    ctx.fillStyle = color;
    ctx.globalAlpha = 0.55;
    ctx.fillRect(x * size, y * size, size, size);
    ctx.globalAlpha = 1;
  });

  ctx.strokeStyle = theme.grid;
  ctx.lineWidth = 1;
  for (let i = 0; i <= GRID; i++) {
    ctx.beginPath(); ctx.moveTo(i * size, 0); ctx.lineTo(i * size, canvas.height); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i * size); ctx.lineTo(canvas.width, i * size); ctx.stroke();
  }

  if (lv.flag) {
    ctx.font = `${size * 0.6}px serif`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(theme.flag, lv.flag[0] * size + size / 2, lv.flag[1] * size + size / 2);
  }
  frame.trees.forEach(k => {
    const [x, y] = k.split(",").map(Number);
    ctx.font = `${size * 0.6}px serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(theme.tree, x * size + size / 2, y * size + size / 2);
  });
  frame.gems.forEach(k => {
    const [x, y] = k.split(",").map(Number);
    ctx.font = `${size * 0.5}px serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(theme.gem, x * size + size / 2, y * size + size / 2);
  });

  const rot = { right: 0, down: 90, left: 180, up: 270 }[frame.dir] || 0;
  ctx.save();
  ctx.translate(frame.x * size + size / 2, frame.y * size + size / 2);
  ctx.rotate((rot * Math.PI) / 180);
  ctx.font = `${size * 0.65}px serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText(theme.hero, 0, 0);
  ctx.restore();
}

async function runAdventure() {
  const lv = ADV_LEVELS[view.advIndex];
  const editor = document.getElementById("adv-editor");
  const out = document.getElementById("adv-output");
  const runBtn = document.getElementById("adv-run-btn");
  runBtn.disabled = true; runBtn.textContent = "Running…";
  out.className = "output-box"; out.textContent = "Running…";

  const engine = new HeroEngine(lv);
  const result = await runPython(editor.value, engine);
  runBtn.disabled = false; runBtn.textContent = "▶ Run";

  // Replay frames on the canvas.
  let fi = 0;
  const timer = setInterval(() => {
    if (fi >= engine.frames.length) {
      clearInterval(timer);
      finishAdventure(lv, engine, result, out);
      return;
    }
    drawGrid(lv, engine.frames[fi]);
    fi++;
  }, 220);
}

function finishAdventure(lv, engine, result, out) {
  if (result.error) {
    out.className = "output-box bad";
    out.textContent = `Oops! Little bug: ${result.error}\n💡 Fix it and press ▶ Run again.`;
    return;
  }
  const solved = lv.check(engine);
  if (solved) {
    const first = !progress.adv_solved.includes(lv.id);
    if (first) {
      progress.adv_solved.push(lv.id);
      saveProgress();
      refreshStats();
      buildRail();
      highlightRail();
    }
    out.className = "output-box good";
    out.textContent = `🏅 MISSION COMPLETE! ${first ? "New badge earned!" : "Nice!"}  Press Next → for the next adventure.`;
  } else {
    out.className = "output-box warn";
    out.textContent = "🤏 Not quite there yet! Look at where the hero stopped, fix your code, and press ▶ Run again.";
  }
}

// ---------- Boot ----------
async function boot() {
  refreshStats();
  buildRail();
  await pyodideReady;
  document.getElementById("boot-overlay").classList.add("hidden");
  if (progress.name) showHome(); else showWelcome();
}
boot();

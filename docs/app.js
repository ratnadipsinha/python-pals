// Python Pals — web edition. Runs entirely in the browser via Pyodide
// (real CPython compiled to WASM). No server, no install, no exe.
"use strict";

const CHAPTERS = window.PP_DATA.chapters;
const HINTS = window.PP_DATA.hints;
const QUIZ = window.PP_DATA.quiz;
const PROJECTS = window.PP_PROJECTS;

const TOTAL_PUZZLES = CHAPTERS.reduce((n, c) => n + c.puzzles.length, 0);
const TOTAL_PROJECTS = PROJECTS.length;

const SAVE_KEY = "python_pals_progress_v2";

function loadProgress() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) { /* ignore */ }
  return { stars: 0, solved: [], projects_done: [], name: "", started: "", last: "" };
}
function saveProgress() {
  localStorage.setItem(SAVE_KEY, JSON.stringify(progress));
}

let progress = loadProgress();
let pyodideReady = null;
let view = { mode: "welcome", chIndex: 0, pzIndex: 0, projIndex: 0, projStage: 0 };

// ---------- Pyodide bootstrap ----------
async function initPyodide() {
  const status = document.getElementById("boot-status");
  status.textContent = "Waking up the Python engine…";
  const py = await loadPyodide();
  status.textContent = "Almost ready…";
  return py;
}
pyodideReady = initPyodide();

// input() in a puzzle/project is bridged to a real browser prompt() so
// projects like the Number Guessing Game are genuinely interactive.
function jsInputBridge(promptText) {
  const answer = window.prompt(promptText || "");
  return answer === null ? "" : answer;
}

async function runPython(code) {
  const py = await pyodideReady;
  py.globals.set("__pp_code", code);
  py.globals.set("__pp_input", jsInputBridge);
  const src = `
import io, sys, json, builtins
_buf = io.StringIO()
_old_stdout = sys.stdout
_old_input = builtins.input
sys.stdout = _buf
builtins.input = lambda prompt="": __pp_input(prompt)
_err = None
try:
    exec(__pp_code, {})
except Exception as _e:
    _err = type(_e).__name__ + ": " + str(_e)
finally:
    sys.stdout = _old_stdout
    builtins.input = _old_input
json.dumps({"output": _buf.getvalue(), "error": _err})
`;
  const resultJson = py.runPython(src);
  return JSON.parse(resultJson);
}

// ---------- Chrome: header stats ----------
function refreshStats() {
  document.getElementById("star-count").textContent = `⭐ ${progress.stars} stars`;
  document.getElementById("badge-count").textContent = `🚀 ${progress.projects_done.length} projects`;
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

  const projLabel = document.createElement("div");
  projLabel.className = "rail-label";
  projLabel.textContent = "🚀 PROJECTS";
  projLabel.style.marginTop = "14px";
  rail.appendChild(projLabel);

  PROJECTS.forEach((p, i) => {
    const done = progress.projects_done.includes(p.id);
    const btn = document.createElement("button");
    btn.className = "rail-item" + (done ? " done" : "");
    btn.innerHTML = `<span class="rail-emoji">${p.emoji}</span><span>${p.title}</span>${done ? '<span class="rail-check">✓</span>' : ""}`;
    btn.onclick = () => showProject(i);
    rail.appendChild(btn);
  });
}

function highlightRail() {
  const items = document.querySelectorAll(".rail-item");
  items.forEach(el => el.classList.remove("active"));
  const idx = view.mode === "lesson" ? view.chIndex
    : view.mode === "project" ? CHAPTERS.length + view.projIndex : -1;
  if (idx >= 0 && items[idx]) items[idx].classList.add("active");
}

// ---------- Home ----------
function showHome() {
  view.mode = "home";
  const main = document.getElementById("main");
  const donePz = new Set(progress.solved).size;
  const doneProj = new Set(progress.projects_done).size;
  const pct = TOTAL_PUZZLES ? Math.round((donePz / TOTAL_PUZZLES) * 100) : 0;

  const todayStr = new Date().toDateString();
  if (!progress.started) progress.started = todayStr;

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
        <div class="progress-sub">${donePz} / ${TOTAL_PUZZLES} exercises done</div>
        <div class="stat-grid">
          <div class="stat"><div class="stat-label">📅 Started</div><div class="stat-val">${progress.started}</div></div>
          <div class="stat"><div class="stat-label">🕒 Today</div><div class="stat-val">${todayStr}</div></div>
          <div class="stat"><div class="stat-label">📖 Exercises</div><div class="stat-val">${donePz} / ${TOTAL_PUZZLES}</div></div>
          <div class="stat"><div class="stat-label">🚀 Projects</div><div class="stat-val">${doneProj} / ${TOTAL_PROJECTS}</div></div>
        </div>
      </div>
      ${pct >= 100 ? `<div class="win-banner">🎉 WOW! You finished every chapter! You are a Python star! 🌟</div>` : ""}
      <div class="home-actions">
        <button class="btn primary" id="continue-btn">▶ Continue Learning</button>
        <button class="btn green" id="proj-btn">🚀 Try a Project</button>
        <button class="btn amber" id="rename-btn">✏️ Change Name</button>
        <button class="btn danger" id="reset-btn">🔄 Reset Progress</button>
      </div>
    </div>`;

  document.getElementById("continue-btn").onclick = () => {
    const idx = CHAPTERS.findIndex((ch, i) => ch.puzzles.some((_, j) => !progress.solved.includes(`${i}-${j}`)));
    showChapter(idx >= 0 ? idx : 0);
  };
  document.getElementById("proj-btn").onclick = () => {
    const idx = PROJECTS.findIndex(p => !progress.projects_done.includes(p.id));
    showProject(idx >= 0 ? idx : 0);
  };
  document.getElementById("rename-btn").onclick = showWelcome;
  document.getElementById("reset-btn").onclick = confirmReset;
  progress.last = todayStr;
  saveProgress();
  highlightRail();
}

function confirmReset() {
  const modal = document.getElementById("modal");
  modal.classList.remove("hidden");
  modal.innerHTML = `
    <div class="modal-card">
      <div class="modal-head" style="color:#d32f2f">⚠️ Are you sure?</div>
      <p><b>This will erase ALL your progress:</b></p>
      <ul class="reset-list">
        <li>All ⭐ stars will be gone</li>
        <li>All 🚀 finished projects will be gone</li>
        <li>You will go back to 0%</li>
      </ul>
      <p class="modal-hint" style="margin-top:0">Your name and start date will stay.</p>
      <div class="modal-actions">
        <button class="btn small" id="reset-cancel">Cancel</button>
        <button class="btn danger small" id="reset-confirm">Yes, reset</button>
      </div>
    </div>`;
  document.getElementById("reset-cancel").onclick = closeModal;
  document.getElementById("reset-confirm").onclick = () => {
    progress.solved = [];
    progress.projects_done = [];
    progress.stars = 0;
    progress.last = new Date().toDateString();
    saveProgress();
    refreshStats();
    buildRail();
    closeModal();
    showHome();
  };
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
        <div class="lesson-head-actions">
          ${ch.youtube ? `<button class="btn small yt" id="yt-btn">📺 Watch on YouTube</button>` : ""}
          <button class="btn small" id="hint-btn">💡 Hint</button>
        </div>
      </div>
      <div class="lesson-stage">
        <div class="lesson-left">
          <div class="theory-card">
            ${ch.theory.map(line => `<div class="theory-line">${formatTheory(line)}</div>`).join("")}
          </div>
          <div class="puzzle-card">
            <div class="puzzle-prompt">${escapeHtml(pz.prompt)}</div>
            <textarea id="code-editor" class="code-editor" spellcheck="false" placeholder="Write your code here…"></textarea>
            <div class="puzzle-actions">
              <button class="btn primary" id="run-btn">▶ Run</button>
              <span class="puzzle-counter">Puzzle ${view.pzIndex + 1} / ${ch.puzzles.length}</span>
              <div class="spacer"></div>
              <button class="btn small" id="prev-btn" ${view.pzIndex === 0 ? "disabled" : ""}>← Prev</button>
              <button class="btn small" id="next-btn" ${view.pzIndex === ch.puzzles.length - 1 ? "disabled" : ""}>Next →</button>
            </div>
            <div id="output-box" class="output-box empty">Press ▶ Run to see your output here.</div>
          </div>
        </div>
        <div id="side-panel" class="side-panel">${sidePanelPlaceholder(ch)}</div>
      </div>
    </div>`;

  document.getElementById("run-btn").onclick = runPuzzle;
  document.getElementById("prev-btn").onclick = () => { if (view.pzIndex > 0) { view.pzIndex--; renderLesson(); } };
  document.getElementById("next-btn").onclick = () => { if (view.pzIndex < ch.puzzles.length - 1) { view.pzIndex++; renderLesson(); } };
  document.getElementById("hint-btn").onclick = showHintInPanel;
  const ytBtn = document.getElementById("yt-btn");
  if (ytBtn) ytBtn.onclick = () => showVideoInPanel(ch);

  const editor = document.getElementById("code-editor");
  editor.addEventListener("keydown", e => {
    if (e.key === "Tab") { e.preventDefault(); insertAtCursor(editor, "    "); }
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runPuzzle();
  });
}

function sidePanelPlaceholder(ch) {
  return `
    <div class="side-empty">
      <div class="side-empty-emoji">👋</div>
      <p>${ch.youtube ? "Press 📺 <b>Watch on YouTube</b> to play the video here," : ""} ${ch.youtube ? "or press" : "Press"} 💡 <b>Hint</b> for a quick reminder and a mini quiz.</p>
    </div>`;
}

function youtubeEmbedUrl(url) {
  try {
    const u = new URL(url);
    const id = u.searchParams.get("v");
    const list = u.searchParams.get("list");
    let embed = `https://www.youtube-nocookie.com/embed/${id}`;
    if (list) embed += `?list=${list}`;
    return embed;
  } catch (e) { return null; }
}

function showVideoInPanel(ch) {
  const panel = document.getElementById("side-panel");
  const embed = youtubeEmbedUrl(ch.youtube);
  panel.innerHTML = `
    <div class="side-head">📺 ${escapeHtml(ch.title)}</div>
    <div class="video-frame">
      ${embed
        ? `<iframe src="${embed}" title="${escapeHtml(ch.title)} video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`
        : `<div class="side-empty"><p>Couldn't load that video here — <a href="${escapeHtml(ch.youtube)}" target="_blank" rel="noopener">open it on YouTube</a> instead.</p></div>`}
    </div>`;
}

function showHintInPanel() {
  const i = view.chIndex;
  const hint = HINTS[i];
  const quiz = QUIZ[i] || [];
  const panel = document.getElementById("side-panel");
  panel.innerHTML = `
    <div class="side-head">💡 Quick Reminder</div>
    <p class="modal-hint">${escapeHtml(hint)}</p>
    ${quiz.map((q, qi) => `
      <div class="quiz-q">
        <div class="quiz-question">${escapeHtml(q.q)}</div>
        <div class="quiz-opts">
          ${q.opts.map((opt, oi) => `<button class="quiz-opt" data-qi="${qi}" data-oi="${oi}">${escapeHtml(opt)}</button>`).join("")}
        </div>
      </div>`).join("")}`;
  panel.querySelectorAll(".quiz-opt").forEach(btn => {
    btn.onclick = () => {
      const qi = Number(btn.dataset.qi), oi = Number(btn.dataset.oi);
      const correct = quiz[qi].a === oi;
      const group = panel.querySelectorAll(`.quiz-opt[data-qi="${qi}"]`);
      group.forEach(b => b.disabled = true);
      btn.classList.add(correct ? "correct" : "wrong");
      if (!correct) group[quiz[qi].a].classList.add("correct");
    };
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

  const result = await runPython(editor.value);
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

function closeModal() {
  const modal = document.getElementById("modal");
  modal.classList.add("hidden");
  modal.innerHTML = "";
}

// ---------- Projects ----------
// Each project walks through stages: 0 = problem statement,
// 1..N = numbered steps, N+1 = the code editor itself.
function showProject(i) {
  view.mode = "project"; view.projIndex = i; view.projStage = 0;
  renderProject();
  highlightRail();
}

function projectStageCount(p) { return p.steps.length + 2; } // problem + steps + code

function gotoProjectStage(delta) {
  const p = PROJECTS[view.projIndex];
  const next = view.projStage + delta;
  if (next < 0 || next >= projectStageCount(p)) return;
  view.projStage = next;
  renderProject();
}

function renderProject() {
  const p = PROJECTS[view.projIndex];
  const stage = view.projStage;
  const lastStage = projectStageCount(p) - 1;
  const main = document.getElementById("main");
  const done = progress.projects_done.includes(p.id);

  main.innerHTML = `
    <div class="lesson-wrap">
      <div class="lesson-head">
        <h1>${p.emoji} ${escapeHtml(p.title)}${done ? " ✓" : ""}</h1>
        <div class="proj-stage-track">${projectStageDots(p, stage)}</div>
      </div>
      <div class="lesson-stage">
        <div class="lesson-left">
          ${stage === 0 ? renderProblemStage(p) : stage === lastStage ? renderCodeStage(p, done) : renderStepStage(p, stage)}
        </div>
        <div class="side-panel">
          <div class="side-head">${stage === 0 ? "🧠 What you'll practice" : stage === lastStage ? "💡 Tips" : "🗺 Where you are"}</div>
          ${stage === 0
            ? `<p class="modal-hint">${p.learn.map(escapeHtml).join(", ")}</p>`
            : stage === lastStage
              ? `<p class="modal-hint">This is an open project — there's no single right answer! Follow the TODOs, run often, and tinker until it works the way you want.</p>
                 <p class="modal-hint">Stuck? Scroll back through the steps with ← Prev to re-read the plan.</p>`
              : `<p class="modal-hint">Step ${stage} of ${p.steps.length}. Read it, then press Next when you understand the idea — you'll write the actual code on the last screen.</p>`}
        </div>
      </div>
    </div>`;

  const prevBtn = document.getElementById("proj-prev-btn");
  const nextBtn = document.getElementById("proj-next-btn");
  if (prevBtn) prevBtn.onclick = () => gotoProjectStage(-1);
  if (nextBtn) nextBtn.onclick = () => gotoProjectStage(1);

  if (stage === lastStage) {
    document.getElementById("proj-run-btn").onclick = runProject;
    document.getElementById("proj-done-btn").onclick = markProjectDone;
    const editor = document.getElementById("proj-editor");
    editor.addEventListener("keydown", e => {
      if (e.key === "Tab") { e.preventDefault(); insertAtCursor(editor, "    "); }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runProject();
    });
  }
}

function projectStageDots(p, stage) {
  const total = projectStageCount(p);
  let dots = "";
  for (let i = 0; i < total; i++) {
    dots += `<span class="stage-dot${i === stage ? " active" : ""}${i < stage ? " past" : ""}"></span>`;
  }
  return dots;
}

function projectNavRow(prevLabel, nextLabel, prevDisabled) {
  return `
    <div class="puzzle-actions">
      <button class="btn small" id="proj-prev-btn" ${prevDisabled ? "disabled" : ""}>${prevLabel}</button>
      <div class="spacer"></div>
      <button class="btn primary" id="proj-next-btn">${nextLabel}</button>
    </div>`;
}

function renderProblemStage(p) {
  return `
    <div class="theory-card">
      <div class="side-head" style="margin-bottom:8px">📋 Problem Statement</div>
      <div class="theory-line">${escapeHtml(p.problem)}</div>
    </div>
    <div class="puzzle-card">
      ${projectNavRow("← Prev", `See the steps →`, true)}
    </div>`;
}

function renderStepStage(p, stage) {
  const step = p.steps[stage - 1];
  return `
    <div class="theory-card">
      <div class="side-head" style="margin-bottom:8px">Step ${stage} of ${p.steps.length}: ${escapeHtml(step.title)}</div>
      <div class="theory-line">${escapeHtml(step.text)}</div>
    </div>
    <div class="puzzle-card">
      ${projectNavRow("← Prev", stage === p.steps.length ? "Let's code! →" : "Next step →", false)}
    </div>`;
}

function renderCodeStage(p, done) {
  return `
    <div class="puzzle-card">
      <div class="puzzle-prompt">Finish the code below. Click ▶ Run whenever you want to test it — input() will pop up a real prompt box.</div>
      <textarea id="proj-editor" class="code-editor proj-editor" spellcheck="false">${escapeHtml(p.starter)}</textarea>
      <div class="puzzle-actions">
        <button class="btn small" id="proj-prev-btn">← Prev</button>
        <button class="btn primary" id="proj-run-btn">▶ Run</button>
        <button class="btn green" id="proj-done-btn">${done ? "✓ Marked Complete" : "✅ Mark Complete"}</button>
        <div class="spacer"></div>
      </div>
      <div id="proj-output" class="output-box empty">Press ▶ Run to see your output here.</div>
    </div>`;
}

async function runProject() {
  const editor = document.getElementById("proj-editor");
  const out = document.getElementById("proj-output");
  const runBtn = document.getElementById("proj-run-btn");
  runBtn.disabled = true; runBtn.textContent = "Running…";
  out.className = "output-box";
  out.textContent = "Running…";

  const result = await runPython(editor.value);
  runBtn.disabled = false; runBtn.textContent = "▶ Run";

  if (result.error) {
    out.className = "output-box bad";
    out.textContent = `Oops! Little bug: ${result.error}\n💡 Check your spelling and indentation, then try again!`;
    return;
  }
  const shown = result.output.trim() || "(nothing printed yet — add some print() calls!)";
  out.className = "output-box good";
  out.textContent = `Output:\n${shown}`;
}

function markProjectDone() {
  const p = PROJECTS[view.projIndex];
  const first = !progress.projects_done.includes(p.id);
  if (first) {
    progress.projects_done.push(p.id);
    progress.stars += 1;
    progress.last = new Date().toDateString();
    saveProgress();
    refreshStats();
    buildRail();
    highlightRail();
  }
  renderProject();
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

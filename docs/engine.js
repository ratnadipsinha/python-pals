// Faithful JS port of app.py's HeroEngine — grid movement, walls/trees,
// pen/paint, gem pickup. Every action records a frame for step-by-step replay.
const PP_DIRS = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
const PP_LEFT_TURN = { up: "left", left: "down", down: "right", right: "up" };
const PP_RIGHT_TURN = { up: "right", right: "down", down: "left", left: "up" };

function keyOf(x, y) { return x + "," + y; }

class HeroEngine {
  constructor(level) {
    [this.x, this.y, this.dir] = level.start;
    this.trees = new Set(level.trees.map(([x, y]) => keyOf(x, y)));
    this.gems = new Set(level.gems.map(([x, y]) => keyOf(x, y)));
    this.walls = new Set(level.walls.map(([x, y]) => keyOf(x, y)));
    this.flag = level.flag;
    this.collected = 0;
    this.painted = {};
    this.pen = false;
    this.penColor = "#4cc9f0";
    this.frames = [];
    this._snap();
  }

  _snap() {
    this.frames.push({
      x: this.x, y: this.y, dir: this.dir,
      trees: new Set(this.trees), gems: new Set(this.gems),
      collected: this.collected, painted: { ...this.painted },
    });
  }

  _blocked(x, y) {
    return !(x >= 0 && x < window.PP_GRID && y >= 0 && y < window.PP_GRID)
      || this.walls.has(keyOf(x, y)) || this.trees.has(keyOf(x, y));
  }

  _step(dx, dy) {
    const nx = this.x + dx, ny = this.y + dy;
    if (this._blocked(nx, ny)) return; // bump: stay put
    this.x = nx; this.y = ny;
    if (this.pen) this.painted[keyOf(this.x, this.y)] = this.penColor;
    this._snap();
  }

  _move(direction, n) {
    const [dx, dy] = PP_DIRS[direction];
    const steps = Math.max(1, Math.trunc(n));
    for (let i = 0; i < steps; i++) this._step(dx, dy);
  }

  move_right(n = 1) { this._move("right", n); }
  move_left(n = 1) { this._move("left", n); }
  move_up(n = 1) { this._move("up", n); }
  move_down(n = 1) { this._move("down", n); }

  face_up() { this.dir = "up"; this._snap(); }
  face_down() { this.dir = "down"; this._snap(); }
  face_left() { this.dir = "left"; this._snap(); }
  face_right() { this.dir = "right"; this._snap(); }

  turn_left() { this.dir = PP_LEFT_TURN[this.dir]; this._snap(); }
  turn_right() { this.dir = PP_RIGHT_TURN[this.dir]; this._snap(); }

  forward(n = 1) { this._move(this.dir, n); }

  pen_down() {
    this.pen = true;
    this.painted[keyOf(this.x, this.y)] = this.penColor;
    this._snap();
  }

  pen_up() { this.pen = false; this._snap(); }

  paint(color = "red") {
    this.penColor = color;
    this.painted[keyOf(this.x, this.y)] = color;
    this._snap();
  }

  tree_ahead() {
    const [dx, dy] = PP_DIRS[this.dir];
    return this.trees.has(keyOf(this.x + dx, this.y + dy));
  }

  chop() {
    const [dx, dy] = PP_DIRS[this.dir];
    this.trees.delete(keyOf(this.x + dx, this.y + dy));
    this._snap();
  }

  pickup() {
    const k = keyOf(this.x, this.y);
    if (this.gems.has(k)) { this.gems.delete(k); this.collected += 1; }
    this._snap();
  }

  // Snapshot shape used by each level's `check(e)` predicate — matches
  // the (x, y, trees.length, collected, painted) surface the Python
  // check lambdas read.
  get trees_arr() { return [...this.trees]; }
}

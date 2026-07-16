# Python Pals Installer & Deployment

This directory contains the one-click installer and deployment scripts for Python Pals.

## Quick Start

### For users (one-click install)
1. Download `python-pals-setup.exe` from GitHub Releases
2. Double-click it
3. Follow the prompts (admin required)
4. Click the "Python Pals" shortcut to play

### For developers (build the installer locally)

**Prerequisites:**
- Inno Setup 6+ (download from https://jrsoftware.org/isdl.php)
- Python Pals app fully built (`dist\Python Pals.exe`)

**Build:**
```powershell
# From the root directory
ISCC.exe installer\python-pals-setup.iss
```

This produces `installer\output\python-pals-setup.exe` (~12 MB, standalone, includes the bundled .exe).

---

## How it works

### Installation flow

1. **Check prerequisites** (Git, Python) — skip if already present
2. **Copy app to** `%ProgramFiles%\PythonPals`
3. **Link to GitHub** — `git remote add origin <repo>`
4. **Fetch latest** — `git fetch origin main` (allows updates even if installer is older)
5. **Create shortcuts** — Desktop + Start Menu
6. **Done** — app is ready to play

### Launching

Double-click the "Python Pals" shortcut → runs `scripts\launch.ps1` → opens the app.

### Updates

In the app, click **🔄 Check for Updates** → if available, click **Update Now** → app restarts with new code.

---

## Security notes

**API Key in the installer:** The GitHub token (if needed for private repos) is embedded in the `.iss` file and ends up in the compiled `.exe`. This is acceptable for a personal/local deployment, but:

- **Never share the installer with untrusted parties** (the token is extractable)
- **Rotate the token periodically** (invalidate old .exe builds)
- For production: use environment variables on the target PC instead (set them before running the installer)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Administrator privileges required" | Right-click installer → Run as Administrator |
| Installer hangs on "Installing..." | Check internet connection; installer downloads Git/Python if needed |
| App won't start after install | Check `%ProgramFiles%\PythonPals\app.log` for errors |
| Updates fail | Run `scripts\update.ps1` manually from the app directory |

---

## Files in this directory

- `python-pals-setup.iss` — Inno Setup script (compiles to `.exe`)
- `post-install.ps1` — Runs after installer copies files
- `output/` — Contains the built `.exe` (not in git, created by compilation)
- `vendor/` — Cached prerequisite installers (not in git, downloaded once)

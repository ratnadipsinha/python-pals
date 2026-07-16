# Python Pals — Deployment & Update Mechanism

Complete guide to building, distributing, and updating Python Pals.

---

## Overview: The three machines

| Machine | Role |
|---|---|
| **Source PC** | This dev machine. Write code, test, commit to GitHub. |
| **GitHub** | Single source of truth (`https://github.com/ratnadipsinha/python-pals`). No CI, purely passive. |
| **Target PC** | Kid's machine. One-click install, auto-updates on demand. |

**Data flow:** Source → GitHub → Target pulls when asked (never pushed to).

---

## 1. Building the installer (on source PC)

### Prerequisites
- Inno Setup 6+ (https://jrsoftware.org/isdl.php)
- `dist\Python Pals.exe` already built (via PyInstaller)

### Build command
```bash
ISCC.exe installer\python-pals-setup.iss
```

**Output:** `installer\output\python-pals-setup.exe` (~12 MB, standalone)

**What's bundled:**
- The compiled Python Pals app (`dist\Python Pals.exe`)
- `post-install.ps1` — initialization script
- `scripts\launch.ps1`, `update.ps1` — helper scripts

**What's NOT bundled (stay in git as gitignore):**
- `installer\output\` — the compiled .exe (built, not committed)
- `installer\vendor\` — cached prerequisites (downloaded, not committed)

### Workflow
```
1. Edit code in source/
2. Build with PyInstaller → dist\Python Pals.exe
3. Commit to GitHub
4. Run ISCC.exe to rebuild installer
5. Upload installer to GitHub Releases
```

---

## 2. Installing (on target PC)

**User experience:**
1. Download `python-pals-setup.exe` from GitHub Releases
2. Double-click it
3. UAC prompt → "Yes"
4. Wait for "Setup Complete"
5. Done — "Python Pals" shortcut appears on Desktop & Start Menu

**What happens behind the scenes:**
```
1. Inno Setup checks prerequisites
   ├─ Git installed? (skip if yes)
   ├─ Python? (skip if yes)
   └─ Other frameworks? (skip if yes)

2. Copy bundled app to %ProgramFiles%\PythonPals

3. Run post-install.ps1
   ├─ git init
   ├─ git remote add origin https://github.com/ratnadipsinha/python-pals
   ├─ git fetch origin main
   └─ git checkout -B main origin/main
       (ensures target PC gets LATEST code, even if
        the .exe was built weeks ago)

4. Create shortcuts
   └─ %DESKTOP%\Python Pals.lnk → scripts\launch.ps1
```

**No auto-start.** App only runs when clicked. No background processes, no scheduled tasks.

---

## 3. Playing (launch-on-demand)

**User clicks "Python Pals" shortcut** → `scripts\launch.ps1` → starts the app

The `.exe` runs as a normal desktop application (Tkinter window). On close, the process exits cleanly.

---

## 4. Updating (in-app, on-demand)

**User sees "🔄 Check for Updates" button in the app footer**

### Check for updates
```
Click "Check for Updates"
  ↓
App calls: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/update.ps1 -CheckOnly
  ↓
update.ps1 runs:
  ├─ git fetch origin
  ├─ compare local HEAD vs origin/main
  └─ return { UpdateAvailable: true/false, LocalCommit, RemoteCommit }
  ↓
App displays: "A new version is available. Update now?"
```

### Apply update
```
User clicks "Update Now"
  ↓
App calls: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/update.ps1
  ↓
update.ps1 runs (in background):
  ├─ git pull origin main
  └─ (app process stays alive, download happens in parallel)
  ↓
App polls for completion
App displays: "Update complete! Restart to apply."
  ↓
User closes app (normal exit)
  ↓
Next launch: new code is running
```

**Why this works on Windows:**
- `git pull` is fast (small repo, incremental fetch)
- PowerShell spawns the update as a true background job (survives parent process death)
- App doesn't wait for the update to finish — returns immediately ("started")
- Next time app is launched, the new code is there

---

## 5. GitHub setup (one-time)

### Create the repo
```bash
# On source PC
cd c:\Users\ratna\apps\python project\python_pals
git init
git remote add origin https://github.com/ratnadipsinha/python-pals
git add -A
git commit -m "Initial commit: Python Pals app"
git branch -M main
git push -u origin main
```

### Update the installer script
Edit `installer\python-pals-setup.iss`:
```iss
#define GitHubRepoURL "https://github.com/ratnadipsinha/python-pals.git"
```

Edit `installer\post-install.ps1`:
```powershell
[string]$GitHubRepo = "https://github.com/ratnadipsinha/python-pals.git"
```

### Create a GitHub Release
1. Go to your repo → **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: `Python Pals v1.0.0`
4. Upload: `installer\output\python-pals-setup.exe`
5. Publish

Users can now download the installer directly from the release page.

---

## 6. Rollout workflow

### First-time users (new install)
1. Download latest `python-pals-setup.exe` from GitHub Releases
2. Run installer
3. Play (latest code downloaded during install, even if .exe is older)

### Existing users (updates)
1. Play app normally
2. See "Update available" message (from in-app check)
3. Click "Update Now"
4. Close app
5. Next launch: new code is running

### Emergency rollback (if new version breaks)
Target PC user:
```powershell
cd "%ProgramFiles%\Python Pals"
git log --oneline
git checkout <old-commit-hash>
# Restart app — old version runs
```

---

## 7. File layout

```
python_pals/
├── app.py                          ← Main Tkinter app
├── dist/
│   └── Python Pals.exe            ← Built standalone exe (PyInstaller output)
├── installer/
│   ├── README.md
│   ├── python-pals-setup.iss      ← Inno Setup script (→ compiles to .exe installer)
│   ├── post-install.ps1           ← Runs after installer
│   ├── output/                    ← Compiled .exe (gitignore)
│   └── vendor/                    ← Cached prerequisites (gitignore)
├── scripts/
│   ├── launch.ps1                 ← User clicks shortcut → runs this
│   └── update.ps1                 ← In-app update checker/applier
├── DEPLOYMENT_GUIDE.md            ← This file
├── .gitignore
└── README.txt
```

---

## 8. Troubleshooting

| Issue | Solution |
|---|---|
| **Installer says "administrator required"** | Right-click `.exe` → Run as Administrator |
| **"Git is not installed" during install** | Installer auto-downloads Git; check internet connection |
| **Update fails with "git pull failed"** | Check internet; try manual: `cd "%ProgramFiles%\Python Pals"` then `git pull origin main` |
| **App crashes after update** | Check `%ProgramFiles%\Python Pals\app.log` for errors; rollback with `git checkout <old-hash>` |
| **Shortcut doesn't work** | Recreate: right-click Desktop → New → Shortcut → `%ProgramFiles%\Python Pals\python-pals.exe` |

---

## 9. Security considerations

**API keys in the installer:**
- If you need to embed anything (GitHub token, API key), it goes in the `.iss` file and ends up in the compiled `.exe`.
- It's **extractable** via hex dump / strings search.
- **OK for:** personal/local distribution, trusted machines only.
- **Not OK for:** public, untrusted, or production apps.

**Mitigations:**
- Use GitHub **Personal Access Tokens** (not your main account password) for any auth.
- Rotate tokens periodically (invalidate old .exe builds).
- For production: deploy tokens via environment variables instead of baking them in.

---

## 10. Quick reference

| Task | Command |
|---|---|
| Build app (PyInstaller) | `python -m PyInstaller ... app.py` |
| Build installer | `ISCC.exe installer\python-pals-setup.iss` |
| Check update (manual) | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\update.ps1 -CheckOnly` |
| Apply update (manual) | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\update.ps1` |
| Push to GitHub | `git push origin main` |
| Publish release on GitHub | Go to Releases → Create new → upload `installer\output\python-pals-setup.exe` |

---

**That's it!** Users get one-click installs, automatic update checks, and your code flows cleanly from source → GitHub → their machines.

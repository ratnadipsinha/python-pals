# launch.ps1 — Main entry point for Python Pals
# Double-clicking "Python Pals" shortcut runs this
# Handles startup, window management, and graceful shutdown

param(
    [string]$AppDir = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Paths
$ExePath = "$AppDir\python-pals.exe"
$LogPath = "$AppDir\app.log"

Write-Host "🐍 Python Pals starting..." -ForegroundColor Green

# Check if app exists
if (-not (Test-Path $ExePath)) {
    Write-Host "❌ Error: Python Pals app not found at $ExePath" -ForegroundColor Red
    Write-Host "   Reinstall from the Setup wizard." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the app
try {
    & $ExePath
    exit 0
} catch {
    Write-Host "❌ Error launching Python Pals:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "   See $LogPath for details." -ForegroundColor Yellow
    exit 1
}

# Post-install script for Python Pals
# Runs after the installer copies files
# Sets up the app directory with git, checks for updates, etc.

param(
    [string]$AppDir = (Split-Path -Parent $MyInvocation.MyCommand.Path),
    [string]$GitHubRepo = "https://github.com/ratnadipsinha/python-pals.git"
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

Write-Host "🐍 Setting up Python Pals..." -ForegroundColor Green

# 1. Initialize git if needed
if (-not (Test-Path "$AppDir\.git")) {
    Write-Host "  • Initializing git repository..." -ForegroundColor Gray
    Push-Location $AppDir
    & git init *> $null
    & git remote add origin $GitHubRepo *> $null
    & git fetch origin main *> $null
    & git checkout -B main origin/main *> $null
    Pop-Location
}

# 2. Fetch latest from GitHub (allows newer app even if installer is older)
Write-Host "  • Checking for latest version..." -ForegroundColor Gray
Push-Location $AppDir
& git fetch origin *> $null
Pop-Location

Write-Host "✅ Python Pals is ready!" -ForegroundColor Green
Write-Host "   Click 'Python Pals' on your Desktop or Start Menu to play." -ForegroundColor Cyan
Write-Host "   (You can check for updates inside the app.)" -ForegroundColor Cyan

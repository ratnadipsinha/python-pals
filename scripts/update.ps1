# update.ps1 — Check for and apply updates
# Called from the app's "Check for Updates" / "Update Now" buttons

param(
    [string]$AppDir = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)),
    [switch]$CheckOnly = $false
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

function Check-Updates {
    Push-Location $AppDir

    # Fetch latest from GitHub
    & git fetch origin 2> $null | Out-Null

    # Get local and remote commit hashes
    $LocalCommit = & git rev-parse HEAD
    $RemoteCommit = & git rev-parse origin/main

    Pop-Location

    $UpdateAvailable = $LocalCommit -ne $RemoteCommit

    @{
        UpdateAvailable = $UpdateAvailable
        LocalCommit = $LocalCommit.Substring(0, 8)
        RemoteCommit = $RemoteCommit.Substring(0, 8)
    }
}

function Apply-Update {
    Write-Host "🔄 Updating Python Pals..." -ForegroundColor Green

    Push-Location $AppDir

    # Pull latest code
    & git pull origin main 2> $null | Out-Null

    $Success = $?

    Pop-Location

    if ($Success) {
        Write-Host "✅ Update complete! Python Pals will restart on next launch." -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Update failed. Check your internet connection and try again." -ForegroundColor Red
        return $false
    }
}

# Main logic
if ($CheckOnly) {
    $Status = Check-Updates
    Write-Host ($Status | ConvertTo-Json)
} else {
    Apply-Update
}

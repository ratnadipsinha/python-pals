; Inno Setup script for Python Pals
; Compiles to python-pals-setup.exe — a one-click installer
; Usage: ISCC.exe python-pals-setup.iss

#define MyAppName "Python Pals"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Python Pals"
#define MyAppURL "https://github.com/ratnadipsinha/python-pals"
#define MyAppExeName "python-pals.exe"
#define GitHubRepoURL "https://github.com/ratnadipsinha/python-pals.git"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=output
OutputBaseFilename=python-pals-setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
ChangesEnvironment=no
SetupLogging=yes
LogFileName={tmp}\python-pals-setup.log

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Bundle the pre-built .exe from dist/
Source: "..\dist\Python Pals.exe"; DestDir: "{app}"; DestName: "python-pals.exe"; Flags: ignoreversion
Source: "..\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Include the post-install script
Source: "post-install.ps1"; DestDir: "{app}"; Flags: ignoreversion

; Include launch and update scripts
Source: "..\scripts\launch.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "..\scripts\setup.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "..\scripts\update.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\python-pals.exe"; Comment: "Play Python Pals"
Name: "{commonprograms}\{#MyAppName}\{#MyAppName}"; Filename: "{app}\python-pals.exe"; Comment: "Play Python Pals"
Name: "{commonprograms}\{#MyAppName}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; Comment: "Uninstall Python Pals"

[Run]
; Run post-install script
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\post-install.ps1"" -GitHubRepo ""{#GitHubRepoURL}"""; Flags: runhidden; Description: "Setting up Python Pals..."

[UninstallDelete]
Type: filesandordirs; Name: "{app}\__pycache__"
Type: filesandordirs; Name: "{app}\.git"
Type: filesandordirs; Name: "{app}\progress.json"
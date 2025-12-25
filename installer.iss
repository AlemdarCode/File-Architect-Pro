; ============================================================
; File Architect Pro - Inno Setup Installer Script
; Ahmet Alemdar - 2025
; ============================================================

[Setup]
AppName=File Architect Pro
AppVersion=1.0.0
AppVerName=File Architect Pro 1.0.0
AppPublisher=Ahmet Alemdar
AppPublisherURL=https://github.com/AhmetAlemdar
AppSupportURL=https://github.com/AhmetAlemdar
AppUpdatesURL=https://github.com/AhmetAlemdar
DefaultDirName={autopf}\File Architect Pro
DefaultGroupName=File Architect Pro
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=FileArchitectPro_Setup_v1.0
SetupIconFile=icons\app.ico
UninstallDisplayIcon={app}\FileArchitectPro.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Windows 10+ gereksinimi
MinVersion=10.0

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; PyInstaller ciktisi (dist\FileArchitectPro klasoru)
Source: "dist\FileArchitectPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\File Architect Pro"; Filename: "{app}\FileArchitectPro.exe"
Name: "{group}\{cm:UninstallProgram,File Architect Pro}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\File Architect Pro"; Filename: "{app}\FileArchitectPro.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FileArchitectPro.exe"; Description: "{cm:LaunchProgram,File Architect Pro}"; Flags: nowait postinstall skipifsilent

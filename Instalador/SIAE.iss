#define MyAppName "SIAE"
#define MyAppVersion "1.5"
#define MyAppPublisher "Lincon.Dev"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "app.exe"

[Setup]
AppId={{F0F12E0A-FD1D-4FCF-A03E-EA99483A53DC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes

OutputDir=C:\Users\lincon.silva.estagio\Desktop\Instalador
OutputBaseFilename=SIAE_Setup_v1.5

SetupIconFile=C:\Users\lincon.silva.estagio\Documents\projeto\assets\logo.ico

Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Files]
; 🔥 AQUI ESTÁ A CORREÇÃO PRINCIPAL
Source: "C:\Users\lincon.silva.estagio\Documents\projeto\dist\app\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName}"; Flags: nowait postinstall skipifsilent
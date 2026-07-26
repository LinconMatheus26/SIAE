; =============================
; CONFIGURAÇÃO GERAL
; =============================

[Setup]
AppName=Sistema de Faturas
AppVersion=1.0
DefaultDirName={pf}\SistemaFaturas
DefaultGroupName=Sistema de Faturas
OutputDir=output_installer
OutputBaseFilename=Setup_Sistema_Faturas
Compression=lzma
SolidCompression=yes

; ÍCONE DO INSTALADOR
SetupIconFile=assets\logo.ico

; IMAGEM LATERAL (OPCIONAL)
WizardImageFile=assets\logo.bmp
WizardSmallImageFile=assets\logo.bmp

; NÃO PRECISA ADMIN DEPOIS
PrivilegesRequired=admin

; =============================
; ARQUIVOS
; =============================

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

; =============================
; ATALHOS
; =============================

[Icons]
Name: "{group}\Sistema de Faturas"; Filename: "{app}\app.exe"
Name: "{commondesktop}\Sistema de Faturas"; Filename: "{app}\app.exe"

; =============================
; EXECUTAR APÓS INSTALAÇÃO
; =============================

[Run]
Filename: "{app}\app.exe"; Description: "Abrir Sistema de Faturas"; Flags: nowait postinstall skipifsilent
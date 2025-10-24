@echo off
REM Respaldo automatico sin interaccion

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "Min=%dt:~10,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%"

set "backup_name=Pods_DAS_Backup_%timestamp%"
set "backup_path=..\%backup_name%"

echo Creando respaldo: %backup_name%

mkdir "%backup_path%" 2>nul

xcopy /E /I /Y /Q "src" "%backup_path%\src\" >nul
xcopy /E /I /Y /Q "config" "%backup_path%\config\" >nul
copy /Y "*.md" "%backup_path%\" >nul 2>&1
copy /Y "*.txt" "%backup_path%\" >nul 2>&1
copy /Y "requirements.txt" "%backup_path%\" >nul
copy /Y "*.bat" "%backup_path%\" >nul 2>&1
copy /Y "*.sh" "%backup_path%\" >nul 2>&1
copy /Y "*.py" "%backup_path%\" >nul 2>&1

mkdir "%backup_path%\documentos\entrada" 2>nul
mkdir "%backup_path%\documentos\procesados" 2>nul
mkdir "%backup_path%\logs" 2>nul
mkdir "%backup_path%\resultados" 2>nul

echo Comprimiendo...
powershell -command "Compress-Archive -Path '%backup_path%' -DestinationPath '..\%backup_name%.zip' -Force"

if exist "..\%backup_name%.zip" (
    rmdir /S /Q "%backup_path%"
    echo.
    echo [OK] Respaldo creado: %backup_name%.zip
    echo Ubicacion: ..\%backup_name%.zip
    echo.
) else (
    echo [ERROR] No se pudo crear el ZIP
)



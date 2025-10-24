@echo off
color 0B
echo ========================================
echo   RESPALDO DEL PROYECTO PODs_DAS
echo ========================================
echo.

REM Crear nombre de archivo con fecha
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
echo.

REM Crear carpeta de respaldo
mkdir "%backup_path%" 2>nul

echo [1/5] Copiando codigo fuente...
xcopy /E /I /Y "src" "%backup_path%\src\" >nul
echo [OK] Codigo fuente copiado

echo [2/5] Copiando configuracion...
xcopy /E /I /Y "config" "%backup_path%\config\" >nul
echo [OK] Configuracion copiada

echo [3/5] Copiando documentacion...
copy /Y "*.md" "%backup_path%\" >nul 2>&1
copy /Y "*.txt" "%backup_path%\" >nul 2>&1
echo [OK] Documentacion copiada

echo [4/5] Copiando archivos de configuracion...
copy /Y "requirements.txt" "%backup_path%\" >nul
copy /Y ".gitignore" "%backup_path%\" >nul 2>&1
copy /Y "*.bat" "%backup_path%\" >nul 2>&1
copy /Y "*.sh" "%backup_path%\" >nul 2>&1
copy /Y "*.py" "%backup_path%\" >nul 2>&1
echo [OK] Archivos de configuracion copiados

echo [5/5] Copiando documentos de ejemplo (si existen)...
if exist "documentos\ejemplos" (
    xcopy /E /I /Y "documentos\ejemplos" "%backup_path%\documentos\ejemplos\" >nul
    echo [OK] Documentos de ejemplo copiados
) else (
    echo [INFO] No hay documentos de ejemplo
)

REM Opcional: Crear estructura de directorios
mkdir "%backup_path%\documentos\entrada" 2>nul
mkdir "%backup_path%\documentos\procesados" 2>nul
mkdir "%backup_path%\logs" 2>nul
mkdir "%backup_path%\resultados\reportes" 2>nul
mkdir "%backup_path%\resultados\imagenes_anotadas" 2>nul

echo.
echo ========================================
echo   RESPALDO COMPLETADO EXITOSAMENTE!
echo ========================================
echo.
echo Ubicacion del respaldo:
echo %backup_path%
echo.
echo Contenido respaldado:
echo   - Todo el codigo fuente (src/)
echo   - Configuracion (config/)
echo   - Documentacion (*.md, *.txt)
echo   - Scripts de instalacion y ejecucion
echo   - Archivos de Python
echo.
echo NO incluye (por seguridad/tamano):
echo   - Entorno virtual (venv/)
echo   - PODs procesados (documentos/)
echo   - Resultados generados (resultados/)
echo   - Logs (logs/)
echo   - Archivos temporales
echo.
echo Para restaurar:
echo   1. Copia la carpeta a donde quieras
echo   2. Ejecuta install.bat
echo   3. Listo!
echo.

REM Preguntar si comprimir
set /p COMPRIMIR="Deseas comprimir el respaldo en ZIP? (S/N): "
if /i "%COMPRIMIR%"=="S" (
    echo.
    echo Comprimiendo respaldo...
    powershell -command "Compress-Archive -Path '%backup_path%' -DestinationPath '..\%backup_name%.zip' -Force"
    if errorlevel 0 (
        echo.
        echo [OK] Archivo ZIP creado: %backup_name%.zip
        echo.
        set /p ELIMINAR="Eliminar carpeta sin comprimir? (S/N): "
        if /i "!ELIMINAR!"=="S" (
            rmdir /S /Q "%backup_path%"
            echo Carpeta eliminada, ZIP conservado
        )
    ) else (
        echo [ERROR] No se pudo crear el ZIP
    )
)

echo.
echo ========================================
pause


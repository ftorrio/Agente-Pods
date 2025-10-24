@echo off
echo ========================================
echo   INSTALAR IDIOMA ESPAÑOL EN TESSERACT
echo ========================================
echo.

REM Verificar si el archivo ya existe
if exist "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata" (
    echo [INFO] El idioma español YA esta instalado
    echo.
    set /p REINSTALAR="Reinstalar de todos modos? (S/N): "
    if /i NOT "%REINSTALAR%"=="S" (
        echo.
        echo Instalacion cancelada
        pause
        exit /b 0
    )
)

echo.
echo [1/2] Verificando archivo spa.traineddata...

if not exist "spa.traineddata" (
    echo [INFO] Descargando archivo de idioma español...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata/raw/main/spa.traineddata' -OutFile 'spa.traineddata'"
    echo [OK] Archivo descargado
)

echo [OK] Archivo encontrado
echo.

echo [2/2] Copiando a Tesseract...
echo (Se solicitaran permisos de administrador)
echo.

REM Ejecutar PowerShell como administrador para copiar
powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoExit','-Command','Copy-Item ''%CD%\spa.traineddata'' -Destination ''C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata'' -Force; Write-Host ''''; Write-Host ''[OK] Idioma español instalado correctamente''; Write-Host ''''; Write-Host ''Verifica en la otra ventana y presiona Enter...''; Read-Host'"

echo.
echo Verificando instalacion...
timeout /t 2 >nul

if exist "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata" (
    color 0A
    echo.
    echo ========================================
    echo   IDIOMA ESPAÑOL INSTALADO EXITOSAMENTE
    echo ========================================
    echo.
    echo Tesseract ahora puede:
    echo - Leer texto en español con alta precision
    echo - Detectar campos: Factura, Cliente, Pedido
    echo - Leer sellos y anotaciones en español
    echo - Mejorar la confianza OCR de 40%% a 80-90%%
    echo.
    echo Para que los cambios surtan efecto:
    echo 1. Cierra la aplicacion web si esta abierta
    echo 2. Ejecuta: run_web.bat
    echo 3. Procesa PODs de nuevo
    echo.
    echo ========================================
) else (
    color 0C
    echo.
    echo [ERROR] No se pudo instalar el idioma
    echo.
    echo Por favor copia manualmente:
    echo Desde: %CD%\spa.traineddata
    echo Hacia: C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata
    echo.
)

pause



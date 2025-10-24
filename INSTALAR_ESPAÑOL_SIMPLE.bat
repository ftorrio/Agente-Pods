@echo off
echo ========================================
echo INSTALAR IDIOMA ESPAÑOL EN TESSERACT
echo ========================================
echo.
echo Este script copiara el archivo de idioma español
echo a la carpeta de Tesseract.
echo.
echo Se solicitaran permisos de administrador.
echo.
pause

powershell -ExecutionPolicy Bypass -File "copiar_español.ps1" -Verb RunAs

echo.
echo Verificando...
timeout /t 2 >nul

if exist "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata" (
    echo.
    echo [OK] INSTALADO CORRECTAMENTE!
    echo.
    echo Ahora el OCR funcionara mucho mejor.
    echo Reinicia la aplicacion web para ver los cambios.
) else (
    echo.
    echo [INFO] Copia manual requerida:
    echo.
    echo 1. Abre el explorador de archivos
    echo 2. Ve a: C:\Fabian\Cursor\Pods_DAS
    echo 3. Busca: spa.traineddata
    echo 4. Copialo (Ctrl+C)
    echo 5. Ve a: C:\Program Files\Tesseract-OCR\tessdata
    echo 6. Pegalo (Ctrl+V) - acepta permisos de administrador
)

echo.
pause



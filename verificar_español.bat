@echo off
echo Verificando idioma español en Tesseract...
echo.

if exist "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata" (
    echo [OK] Idioma español INSTALADO correctamente
    echo Archivo encontrado en: C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata
    echo.
    echo El sistema ahora puede:
    echo - Leer texto en español con alta confianza
    echo - Detectar campos: Factura, Cliente, Pedido, Productos
    echo - Leer sellos y anotaciones en español
    echo - Mejorar la precisión general
) else (
    echo [X] Idioma español NO instalado
    echo.
    echo Por favor copia manualmente:
    echo Desde: C:\Fabian\Cursor\Pods_DAS\spa.traineddata
    echo Hacia: C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata
    echo.
    echo Necesitas permisos de administrador.
)

echo.
pause



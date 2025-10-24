@echo off
REM Script de instalación para Windows

echo ========================================
echo Sistema de Validación de PODs
echo Instalación en Windows
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instale Python 3.8 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python detectado correctamente
echo.

REM Crear entorno virtual
echo [2/4] Creando entorno virtual...
if not exist venv (
    python -m venv venv
    echo Entorno virtual creado
) else (
    echo Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo [3/4] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [4/4] Instalando dependencias de Python...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Instalación completada!
echo ========================================
echo.
echo IMPORTANTE: Debes instalar Tesseract OCR manualmente
echo.
echo Descárgalo desde:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Instala y asegúrate de agregarlo al PATH del sistema
echo o actualiza la configuración para indicar la ruta.
echo.
echo Para usar el sistema, ejecuta:
echo   venv\Scripts\activate
echo   python src/main.py --help
echo.
pause


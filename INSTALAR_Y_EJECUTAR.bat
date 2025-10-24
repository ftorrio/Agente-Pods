@echo off
echo ========================================
echo Sistema de Validacion de PODs
echo Instalacion y Ejecucion Automatica
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo.
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante la instalacion, marca la casilla
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Crear entorno virtual si no existe
if not exist venv (
    echo [1/4] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [1/4] Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno activado
echo.

REM Instalar dependencias
echo [3/4] Instalando dependencias...
echo (Esto puede tomar unos minutos la primera vez)
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo [OK] Dependencias instaladas
echo.

REM Ejecutar GUI
echo [4/4] Iniciando interfaz grafica...
echo.
echo ========================================
echo La interfaz se abrira en unos segundos
echo ========================================
echo.

python src/gui.py

pause


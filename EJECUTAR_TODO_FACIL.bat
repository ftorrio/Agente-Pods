@echo off
color 0B
title Sistema de Validacion PODs - Instalacion Automatica

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                                                      ║
echo ║     SISTEMA DE VALIDACION DE PODs                   ║
echo ║     Instalacion y Ejecucion Automatica              ║
echo ║                                                      ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo Verificando Python...
python --version >nul 2>&1

if errorlevel 1 (
    color 0E
    echo.
    echo [!] Python NO esta instalado
    echo.
    echo Voy a ayudarte a instalarlo de 2 formas:
    echo.
    echo OPCION 1: Microsoft Store (MAS FACIL - Recomendada)
    echo   - Instalacion con 1 clic
    echo   - Se configura automaticamente
    echo.
    echo OPCION 2: Sitio oficial Python.org
    echo   - Mas control
    echo   - Requiere marcar "Add to PATH"
    echo.
    set /p OPCION="Elige opcion (1 o 2): "
    
    if "%OPCION%"=="1" (
        echo.
        echo Abriendo Microsoft Store...
        start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
        echo.
        echo 1. Haz clic en "Obtener" o "Instalar"
        echo 2. Espera a que termine
        echo 3. Cierra la tienda
        echo 4. Presiona una tecla aqui...
        pause >nul
    ) else (
        echo.
        echo Abriendo pagina de descarga de Python...
        start https://www.python.org/downloads/
        echo.
        echo IMPORTANTE:
        echo 1. Descarga Python 3.11
        echo 2. Ejecuta el instalador
        echo 3. MARCA: [X] Add Python to PATH
        echo 4. Haz clic en "Install Now"
        echo 5. Espera a que termine
        echo 6. REINICIA TU PC
        echo 7. Ejecuta este archivo de nuevo
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo Verificando instalacion...
    python --version >nul 2>&1
    if errorlevel 1 (
        color 0C
        echo.
        echo [X] Python aun no esta disponible
        echo.
        echo Por favor:
        echo 1. Cierra TODAS las ventanas de CMD/PowerShell
        echo 2. Abre una NUEVA ventana
        echo 3. Ejecuta este archivo de nuevo
        echo.
        echo Si el problema persiste, REINICIA TU PC
        echo.
        pause
        exit /b 1
    )
)

color 0A
echo.
echo [OK] Python detectado!
python --version
echo.

REM Verificar si ya existe el entorno virtual
if exist venv (
    echo [INFO] Entorno virtual ya existe
    goto :activar
)

echo Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    color 0C
    echo [ERROR] No se pudo crear entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

:activar
echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
echo (Esto puede tardar 2-3 minutos la primera vez)
echo.

python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if errorlevel 1 (
    color 0C
    echo [ERROR] Problema al instalar dependencias
    echo.
    echo Intentando de nuevo con mas detalles...
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
color 0A
echo ╔══════════════════════════════════════════════════════╗
echo ║                                                      ║
echo ║     ¡INSTALACION COMPLETA!                          ║
echo ║                                                      ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo Iniciando servidor web...
echo.
echo La aplicacion se abrira en tu navegador en:
echo.
echo     http://localhost:8501
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

timeout /t 3

streamlit run src/web_app.py --server.port 8501 --server.headless false

pause


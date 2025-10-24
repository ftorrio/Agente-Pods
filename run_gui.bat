@echo off
REM Script para ejecutar la interfaz gráfica en Windows

echo ========================================
echo Sistema de Validacion de PODs - GUI
echo ========================================
echo.

REM Verificar si el entorno virtual existe
if not exist venv (
    echo ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta install.bat primero
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar GUI
python src/gui.py

pause


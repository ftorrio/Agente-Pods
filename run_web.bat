@echo off
REM Script para ejecutar la interfaz web en Windows

echo ========================================
echo Sistema de Validacion de PODs - Web
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

echo Iniciando servidor web...
echo.
echo La aplicacion se abrira automaticamente en tu navegador
echo URL: http://localhost:8501
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar aplicación web con Streamlit
streamlit run src/web_app.py --server.port 8501 --server.headless false

pause


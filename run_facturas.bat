@echo off
echo ========================================
echo   SISTEMA DE FACTURAS CON PODs
echo ========================================
echo.
echo Iniciando aplicacion de facturas...
echo.

REM Activar entorno virtual
call .\venv\Scripts\activate.bat

REM Ejecutar aplicación
streamlit run src/facturas_pods.py --server.port 8502

pause


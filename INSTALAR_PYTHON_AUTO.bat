@echo off
echo ========================================
echo   INSTALADOR AUTOMATICO DE PYTHON
echo ========================================
echo.

echo Intentando instalar Python desde Microsoft Store...
echo.

REM Intentar abrir Python desde Microsoft Store (esto abrira la tienda)
start ms-windows-store://pdp/?ProductId=9NRWMJP3717K

echo.
echo Se ha abierto Microsoft Store para instalar Python.
echo.
echo IMPORTANTE:
echo 1. Haz clic en "Obtener" o "Instalar" en la tienda
echo 2. Espera a que termine la instalacion
echo 3. Cierra la tienda
echo 4. Presiona cualquier tecla aqui para continuar...
echo.
pause

echo.
echo Verificando si Python se instalo...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python no se instalo correctamente.
    echo.
    echo PLAN B - Instalacion Manual:
    echo 1. Ve a: https://www.python.org/downloads/
    echo 2. Descarga Python 3.11
    echo 3. Ejecuta el instalador
    echo 4. MARCA la casilla: Add Python to PATH
    echo 5. Instala
    echo 6. Reinicia tu PC
    echo 7. Ejecuta este archivo de nuevo
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Python instalado!
echo.
echo Ahora ejecutando instalacion completa...
timeout /t 3
call INSTALAR_TODO.bat


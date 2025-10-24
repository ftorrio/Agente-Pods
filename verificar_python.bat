@echo off
echo.
echo Verificando instalacion de Python...
echo.

python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python NO esta instalado correctamente
    echo.
    echo Por favor:
    echo 1. Verifica que marcaste "Add Python to PATH"
    echo 2. Reinicia tu computadora
    echo 3. Ejecuta este archivo de nuevo
    echo.
) else (
    echo.
    echo [OK] Python esta instalado correctamente!
    echo.
    echo Ahora puedes ejecutar: INSTALAR_TODO.bat
    echo.
)

pause


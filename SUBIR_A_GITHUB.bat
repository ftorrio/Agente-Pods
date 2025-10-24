@echo off
echo ========================================
echo   SUBIR PROYECTO A GITHUB
echo ========================================
echo.

REM Reemplaza esta URL con la de tu repositorio
set REPO_URL=https://github.com/TU_USUARIO/pods-validation-system.git

echo URL del repositorio: %REPO_URL%
echo.
echo Si es correcta, presiona Enter
echo Si NO, cierra esta ventana y edita SUBIR_A_GITHUB.bat
pause

echo.
echo Conectando con GitHub...
git remote add origin %REPO_URL%

echo.
echo Subiendo código...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   CODIGO SUBIDO A GITHUB!
echo ========================================
echo.
echo Ahora puedes:
echo 1. Ir a https://share.streamlit.io
echo 2. Conectar tu cuenta de GitHub
echo 3. Seleccionar tu repositorio
echo 4. Deploy!
echo.
pause


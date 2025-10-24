@echo off
color 0A
echo.
echo ========================================================
echo     INSTALADOR AUTOMATICO - Sistema de Validacion PODs
echo ========================================================
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Python no esta instalado!
    echo.
    echo Por favor sigue estos pasos:
    echo.
    echo 1. Ve a: https://www.python.org/downloads/
    echo 2. Descarga Python 3.11 o superior
    echo 3. Durante la instalacion, MARCA la casilla:
    echo    [X] Add Python to PATH
    echo 4. Instala Python
    echo 5. Reinicia esta ventana y ejecuta este script de nuevo
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python detectado correctamente
echo.

REM Verificar Tesseract
echo [2/5] Verificando Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    color 0E
    echo.
    echo [ADVERTENCIA] Tesseract OCR no esta instalado!
    echo.
    echo El sistema funcionara pero sin reconocimiento de texto (OCR).
    echo.
    echo Para instalar Tesseract:
    echo 1. Ve a: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Descarga el instalador para Windows
    echo 3. Instala en: C:\Program Files\Tesseract-OCR
    echo 4. Agrega al PATH: C:\Program Files\Tesseract-OCR
    echo 5. Reinicia esta ventana
    echo.
    echo Presiona cualquier tecla para continuar sin Tesseract...
    pause >nul
    color 0A
) else (
    echo [OK] Tesseract OCR detectado
)
echo.

REM Crear entorno virtual
echo [3/5] Creando entorno virtual...
if exist venv (
    echo [INFO] El entorno virtual ya existe
) else (
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [4/5] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo [ERROR] No se pudo activar el entorno virtual
    echo.
    echo Intenta ejecutar esto manualmente:
    echo Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo.
    pause
    exit /b 1
)
echo [OK] Entorno activado
echo.

REM Instalar dependencias
echo [5/5] Instalando dependencias...
echo (Esto puede tomar 2-3 minutos)
echo.

python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    color 0C
    echo [ERROR] No se pudo actualizar pip
    pause
    exit /b 1
)

pip install -r requirements.txt --quiet --no-warn-script-location
if errorlevel 1 (
    color 0C
    echo [ERROR] No se pudieron instalar las dependencias
    echo.
    echo Intenta instalar manualmente:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas correctamente
echo.

REM Crear directorios necesarios
echo Creando directorios...
if not exist "documentos\entrada" mkdir "documentos\entrada"
if not exist "documentos\procesados" mkdir "documentos\procesados"
if not exist "documentos\ejemplos" mkdir "documentos\ejemplos"
if not exist "resultados" mkdir "resultados"
if not exist "resultados\reportes" mkdir "resultados\reportes"
if not exist "resultados\imagenes_anotadas" mkdir "resultados\imagenes_anotadas"
if not exist "logs" mkdir "logs"
echo [OK] Directorios creados
echo.

REM Resumen final
color 0A
echo ========================================================
echo     INSTALACION COMPLETADA CON EXITO!
echo ========================================================
echo.
echo Todo esta listo para usar el sistema.
echo.
echo Tienes 3 opciones de interfaz:
echo.
echo 1. INTERFAZ WEB (Recomendada - Mas moderna)
echo    Ejecuta: run_web.bat
echo    Se abrira en: http://localhost:8501
echo.
echo 2. INTERFAZ GRAFICA (App de escritorio)
echo    Ejecuta: run_gui.bat
echo.
echo 3. LINEA DE COMANDOS (Para automatizacion)
echo    Ejecuta: python src/main.py
echo.
echo ========================================================
echo.
echo Documentacion disponible:
echo - INSTALACION_COMPLETA.md (esta guia completa)
echo - GUIA_INTERFAZ_WEB.md (manual de la interfaz web)
echo - INICIO_RAPIDO.md (guia de 5 minutos)
echo - README.md (documentacion completa)
echo.
echo ========================================================
echo.

REM Preguntar si quiere ejecutar la interfaz web ahora
set /p EJECUTAR="Quieres ejecutar la interfaz web ahora? (S/N): "
if /i "%EJECUTAR%"=="S" (
    echo.
    echo Iniciando interfaz web...
    echo La aplicacion se abrira en tu navegador
    echo Presiona Ctrl+C para detener el servidor
    echo.
    streamlit run src/web_app.py --server.port 8501 --server.headless false
) else (
    echo.
    echo Para ejecutar mas tarde, usa: run_web.bat
    echo.
)

pause


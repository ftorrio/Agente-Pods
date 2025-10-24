#!/bin/bash

# Script para ejecutar la interfaz web en Linux/Mac

echo "========================================"
echo "Sistema de Validación de PODs - Web"
echo "========================================"
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Por favor ejecuta install.sh primero"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

echo "Iniciando servidor web..."
echo ""
echo "La aplicación se abrirá automáticamente en tu navegador"
echo "URL: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Ejecutar aplicación web con Streamlit
streamlit run src/web_app.py --server.port 8501 --server.headless false


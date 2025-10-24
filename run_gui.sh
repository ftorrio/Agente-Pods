#!/bin/bash

# Script para ejecutar la interfaz gráfica en Linux/Mac

echo "========================================"
echo "Sistema de Validación de PODs - GUI"
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

# Ejecutar GUI
python src/gui.py


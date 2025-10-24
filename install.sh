#!/bin/bash

# Script de instalación para Linux/Mac

echo "========================================"
echo "Sistema de Validación de PODs"
echo "Instalación en Linux/Mac"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instale Python 3.8 o superior"
    exit 1
fi

echo "[1/5] Python detectado correctamente"
echo ""

# Verificar Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "ADVERTENCIA: Tesseract OCR no está instalado"
    echo "Instalando Tesseract..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr tesseract-ocr-spa
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac
        if command -v brew &> /dev/null; then
            brew install tesseract tesseract-lang
        else
            echo "ERROR: Homebrew no está instalado"
            echo "Instala Tesseract manualmente desde: https://github.com/tesseract-ocr/tesseract"
            exit 1
        fi
    fi
else
    echo "[2/5] Tesseract OCR detectado correctamente"
fi
echo ""

# Crear entorno virtual
echo "[3/5] Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Entorno virtual creado"
else
    echo "Entorno virtual ya existe"
fi
echo ""

# Activar entorno virtual
echo "[4/5] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[5/5] Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Instalación completada!"
echo "========================================"
echo ""
echo "Para usar el sistema, ejecuta:"
echo "  source venv/bin/activate"
echo "  python src/main.py --help"
echo ""


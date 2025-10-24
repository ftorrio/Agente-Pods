#!/bin/bash

echo "========================================"
echo "  RESPALDO DEL PROYECTO PODs_DAS"
echo "========================================"
echo ""

# Crear nombre con timestamp
timestamp=$(date +%Y%m%d_%H%M%S)
backup_name="Pods_DAS_Backup_${timestamp}"
backup_path="../${backup_name}"

echo "Creando respaldo: ${backup_name}"
echo ""

# Crear carpeta de respaldo
mkdir -p "${backup_path}"

echo "[1/5] Copiando código fuente..."
cp -r src "${backup_path}/"
echo "[OK] Código fuente copiado"

echo "[2/5] Copiando configuración..."
cp -r config "${backup_path}/"
echo "[OK] Configuración copiada"

echo "[3/5] Copiando documentación..."
cp *.md "${backup_path}/" 2>/dev/null || true
cp *.txt "${backup_path}/" 2>/dev/null || true
echo "[OK] Documentación copiada"

echo "[4/5] Copiando archivos de configuración..."
cp requirements.txt "${backup_path}/"
cp .gitignore "${backup_path}/" 2>/dev/null || true
cp *.bat "${backup_path}/" 2>/dev/null || true
cp *.sh "${backup_path}/" 2>/dev/null || true
cp *.py "${backup_path}/" 2>/dev/null || true
echo "[OK] Archivos de configuración copiados"

echo "[5/5] Copiando documentos de ejemplo..."
if [ -d "documentos/ejemplos" ]; then
    mkdir -p "${backup_path}/documentos/ejemplos"
    cp -r documentos/ejemplos/* "${backup_path}/documentos/ejemplos/" 2>/dev/null || true
    echo "[OK] Documentos de ejemplo copiados"
else
    echo "[INFO] No hay documentos de ejemplo"
fi

# Crear estructura de directorios
mkdir -p "${backup_path}/documentos/entrada"
mkdir -p "${backup_path}/documentos/procesados"
mkdir -p "${backup_path}/logs"
mkdir -p "${backup_path}/resultados/reportes"
mkdir -p "${backup_path}/resultados/imagenes_anotadas"

echo ""
echo "========================================"
echo "  RESPALDO COMPLETADO EXITOSAMENTE!"
echo "========================================"
echo ""
echo "Ubicación del respaldo:"
echo "${backup_path}"
echo ""
echo "Contenido respaldado:"
echo "  - Todo el código fuente (src/)"
echo "  - Configuración (config/)"
echo "  - Documentación (*.md, *.txt)"
echo "  - Scripts de instalación y ejecución"
echo ""
echo "NO incluye:"
echo "  - Entorno virtual (venv/)"
echo "  - PODs procesados"
echo "  - Resultados generados"
echo "  - Logs"
echo ""

# Preguntar si comprimir
read -p "¿Deseas comprimir el respaldo en .tar.gz? (s/n): " COMPRIMIR

if [[ "$COMPRIMIR" == "s" || "$COMPRIMIR" == "S" ]]; then
    echo ""
    echo "Comprimiendo respaldo..."
    tar -czf "../${backup_name}.tar.gz" -C ".." "${backup_name}"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "[OK] Archivo comprimido creado: ${backup_name}.tar.gz"
        echo ""
        read -p "¿Eliminar carpeta sin comprimir? (s/n): " ELIMINAR
        
        if [[ "$ELIMINAR" == "s" || "$ELIMINAR" == "S" ]]; then
            rm -rf "${backup_path}"
            echo "Carpeta eliminada, archivo .tar.gz conservado"
        fi
    else
        echo "[ERROR] No se pudo crear el archivo comprimido"
    fi
fi

echo ""
echo "========================================"
echo ""


# 🚀 Inicio Rápido

Guía de 5 minutos para comenzar a usar el Sistema de Validación de PODs.

---

## ⚡ Instalación Rápida

### Windows
```bash
# 1. Instalar Tesseract OCR
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
# Ejecutar el instalador y agregar al PATH

# 2. Instalar el sistema
.\install.bat
```

### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

---

## 📁 Preparar Documentos

1. Coloca tus archivos POD (PDF, GIF, PNG, JPG) en:
   ```
   documentos/entrada/
   ```

2. Asegúrate de que los documentos:
   - Tengan buena calidad (mínimo 150 DPI)
   - Estén completos (no cortados)
   - Estén en orientación correcta

---

## ▶️ Ejecutar

### Opción 1: Interfaz Gráfica (Recomendado) 🖥️

```bash
# Windows
run_gui.bat

# Linux/Mac
./run_gui.sh
```

### Opción 2: Línea de Comandos 💻

```bash
# Activar entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Procesar todos los documentos
python src/main.py
```

---

## 📊 Ver Resultados

### 1. Consola
Los resultados se muestran en tiempo real mientras procesa.

### 2. Reportes
```
resultados/reportes/
  ├── reporte_pods_TIMESTAMP.xlsx    ← Abrir con Excel
  ├── reporte_pods_TIMESTAMP.csv
  └── resumen_TIMESTAMP.txt
```

### 3. Imágenes Anotadas
```
resultados/imagenes_anotadas/
  └── documento_anotado.jpg          ← Ver detecciones visuales
```

---

## 🎯 Interpretación Rápida

| Clasificación | Significado | Acción |
|---------------|-------------|--------|
| ✅ **OK** | Válido con firma/sello | ✓ Aprobar |
| 📝 **CON ANOTACIONES** | Tiene comentarios | → Revisar |
| ⚠️ **SIN ACUSE** | Sin firma ni sello | ✗ Solicitar firma |
| ❌ **POCO LEGIBLE** | No se distinguen campos | ✗ Re-digitalizar |
| ❌ **INCORRECTO** | Documento cortado | ✗ Escanear completo |

---

## 🔧 Comandos Útiles

```bash
# Procesar un directorio específico
python src/main.py --input "C:\ruta\a\documentos"

# Procesar un solo archivo
python src/main.py --file "documento.pdf"

# Sin generar imágenes anotadas (más rápido)
python src/main.py --no-annotated

# Ver ayuda completa
python src/main.py --help
```

---

## ❓ Problemas Comunes

### "Tesseract not found"
```bash
# Windows: Agregar al PATH
# Panel de Control → Sistema → Variables de entorno
# Agregar: C:\Program Files\Tesseract-OCR

# Linux
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# Mac
brew install tesseract tesseract-lang
```

### No detecta firmas/sellos
1. Abrir `config/settings.yaml`
2. Reducir `signature_confidence` de 0.7 a 0.5
3. Reducir `stamp_circularity` de 0.6 a 0.4
4. Ejecutar de nuevo

### Muchos "Poco Legible"
1. Mejorar calidad de escaneo (300 DPI)
2. O reducir `min_text_quality` en config (de 0.6 a 0.4)

---

## 📚 Documentación Completa

- `README.md` - Documentación técnica completa
- `GUIA_USO.md` - Guía detallada paso a paso
- `ejemplo_uso.py` - Ejemplos de código

---

## ✅ Checklist de Primer Uso

- [ ] Tesseract OCR instalado y en PATH
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`install.bat` / `install.sh`)
- [ ] Documentos POD en `documentos/entrada/`
- [ ] Entorno virtual activado
- [ ] Primer ejecución: `python src/main.py`
- [ ] Resultados revisados en `resultados/reportes/`

---

¡Listo! Ya estás validando PODs automáticamente. 🎉

Para más detalles, consulta `GUIA_USO.md`.


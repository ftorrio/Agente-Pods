# Guía de Uso - Sistema de Validación de PODs

## Tabla de Contenidos
1. [Instalación](#instalación)
2. [Preparación de Documentos](#preparación-de-documentos)
3. [Uso Básico](#uso-básico)
4. [Interpretación de Resultados](#interpretación-de-resultados)
5. [Configuración Avanzada](#configuración-avanzada)
6. [Solución de Problemas](#solución-de-problemas)

---

## Instalación

### Windows

1. **Instalar Python 3.8 o superior**
   - Descargar desde: https://www.python.org/downloads/
   - Durante la instalación, marcar "Add Python to PATH"

2. **Instalar Tesseract OCR**
   - Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
   - Ejecutar el instalador
   - Agregar al PATH del sistema: `C:\Program Files\Tesseract-OCR`

3. **Instalar el sistema**
   ```bash
   # Doble clic en install.bat o ejecutar en PowerShell:
   .\install.bat
   ```

### Linux/Mac

1. **Ejecutar script de instalación**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

---

## Preparación de Documentos

### Ubicación de Archivos

1. Coloca tus documentos POD en: `documentos/entrada/`
2. Formatos soportados: PDF, GIF, PNG, JPG, TIFF, BMP

### Recomendaciones de Calidad

Para mejores resultados:
- **Resolución mínima**: 150 DPI (recomendado: 300 DPI)
- **Formato preferido**: PDF con buena calidad
- **Tamaño**: Documentos completos, sin cortes
- **Contraste**: Alto contraste entre texto y fondo
- **Orientación**: Correcta (no rotados)

---

## Uso Básico

### Activar el Entorno

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Casos de Uso Comunes

#### 1. Procesar todos los documentos del directorio
```bash
python src/main.py
```

#### 2. Procesar un directorio específico
```bash
python src/main.py --input "C:\ruta\a\documentos"
```

#### 3. Procesar un solo archivo
```bash
python src/main.py --file "documento.pdf"
```

#### 4. Procesar sin generar imágenes anotadas
```bash
python src/main.py --no-annotated
```

#### 5. Ver ayuda completa
```bash
python src/main.py --help
```

---

## Interpretación de Resultados

### Clasificaciones

El sistema clasifica cada POD en una de estas 5 categorías:

#### ✅ **OK** (Válido)
**Significado**: Documento válido con evidencia de recepción

**Criterios**:
- Tiene firma manuscrita del cliente en zonas 6, 7 u 8
- O tiene sello válido del cliente (no de Deacero o Ingetek)

**Acción**: Ninguna, documento aprobado

---

#### 📝 **CON ANOTACIONES**
**Significado**: Tiene comentarios escritos a mano

**Subtipos**:
- **Positivo**: Anotaciones confirman recepción ("recibido", "conforme", "OK")
- **Negativo**: Anotaciones indican reclamación ("dañado", "incompleto", "reclamo")
- **Neutral**: Anotaciones sin sentimiento claro

**Acción**:
- Positivo: Revisar manualmente, probablemente válido
- Negativo: **Revisión urgente** - posible problema
- Neutral: Revisar para interpretar

---

#### ⚠️ **SIN ACUSE**
**Significado**: Es solo la remisión, sin evidencia de recepción

**Criterios**:
- No tiene firma del cliente
- No tiene sello del cliente
- No tiene anotaciones manuscritas

**Acción**: Solicitar documento con firma o sello del cliente

---

#### ❌ **POCO LEGIBLE**
**Significado**: Los campos clave no son distinguibles

**Causas comunes**:
- Imagen borrosa o de baja calidad
- Campos importantes no detectables (Factura, Cliente, Pedido, Productos, Firma)
- Confianza OCR muy baja

**Acción**: Re-digitalizar con mejor calidad

---

#### ❌ **INCORRECTO**
**Significado**: Documento no completamente digitalizado

**Causas**:
- Documento cortado
- Digitalización parcial
- Faltan secciones importantes

**Acción**: Re-digitalizar el documento completo

---

### Estructura de Resultados

El sistema genera tres tipos de salida:

#### 1. **Consola** (Tiempo real)
```
============================================================
RESULTADO DE CLASIFICACIÓN
============================================================
Archivo: POD_12345.pdf
Página: 1

Clasificación: OK
Código: OK
Confianza: 95.0%
Válido: ✓ SÍ

Detalles:
  • Firma válida detectada (2 firma(s))
  • Contiene anotaciones positivas confirmando recepción
============================================================
```

#### 2. **Reportes Excel/CSV** (`resultados/reportes/`)
Columnas principales:
- Archivo, Ruta, Página
- Clasificación, Código, Válido
- Confianza
- Firmas/Sellos/Anotaciones detectados
- Calidad del texto y legibilidad
- Campos detectados/faltantes
- Problemas y recomendaciones

#### 3. **Imágenes Anotadas** (`resultados/imagenes_anotadas/`)
Muestran visualmente:
- Zonas de firma (6, 7, 8) en azul/amarillo
- Firmas detectadas en verde/amarillo/rojo según confianza
- Sellos detectados en verde (válido) o rojo (inválido)
- Anotaciones en verde (positivo), rojo (negativo) o azul (neutral)

---

## Configuración Avanzada

### Archivo `config/settings.yaml`

#### Ajustar Umbrales de Detección

```yaml
thresholds:
  # Legibilidad
  min_text_quality: 0.6       # Reducir si muchos son "Poco Legible"
  min_fields_detected: 3      # Campos mínimos requeridos
  blur_threshold: 100         # Aumentar si muchos son "borrosos"
  
  # Firmas
  signature_min_area: 500     # Área mínima en píxeles
  signature_confidence: 0.7   # Reducir si no detecta firmas
  
  # Sellos
  stamp_min_area: 1000
  stamp_circularity: 0.6      # Reducir para detectar sellos irregulares
```

#### Agregar Palabras Clave para Anotaciones

```yaml
annotation_keywords:
  positive:
    - "recibido"
    - "conforme"
    - "ok"
    - "correcto"
    - "aceptado"
    - "tu_palabra_personalizada"  # Agregar aquí
  
  negative:
    - "reclamación"
    - "dañado"
    - "tu_palabra_negativa"  # Agregar aquí
```

#### Modificar Zonas de Firma

Las zonas usan coordenadas relativas (0.0 a 1.0):

```yaml
zones:
  zone_6:  # Parte inferior izquierda
    x_start: 0.0   # 0% del ancho
    x_end: 0.33    # 33% del ancho
    y_start: 0.75  # 75% del alto
    y_end: 1.0     # 100% del alto
```

---

## Solución de Problemas

### Problema: "Tesseract not found"

**Windows:**
1. Verificar instalación: Abrir CMD y ejecutar `tesseract --version`
2. Si no funciona, agregar al PATH:
   - Panel de Control → Sistema → Variables de entorno
   - Editar PATH, agregar: `C:\Program Files\Tesseract-OCR`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# Mac
brew install tesseract tesseract-lang
```

---

### Problema: No detecta firmas

**Soluciones**:
1. Reducir `signature_confidence` en `config/settings.yaml`
2. Verificar que las firmas estén en zonas 6, 7 u 8
3. Ajustar coordenadas de zonas si el formato del POD es diferente
4. Revisar que la imagen tenga suficiente contraste

---

### Problema: Muchos documentos clasificados como "Poco Legible"

**Soluciones**:
1. Mejorar calidad de digitalización (aumentar DPI)
2. Reducir `min_text_quality` en configuración
3. Reducir `min_fields_detected` si el formato es minimal
4. Verificar que el OCR tenga idioma español configurado

---

### Problema: No detecta sellos

**Soluciones**:
1. Reducir `stamp_circularity` para sellos irregulares
2. Ajustar `stamp_min_area` y `stamp_max_area`
3. Verificar que el sello no esté en la lista de inválidos

---

### Problema: Error "No se encontraron archivos"

**Verificar**:
1. Los archivos están en `documentos/entrada/` (o directorio especificado)
2. Los formatos son soportados (.pdf, .gif, .png, .jpg, etc.)
3. Los archivos no están en subdirectorios (el sistema busca en el nivel superior)

---

### Problema: Rendimiento lento

**Optimizaciones**:
1. Reducir `max_dimension` en configuración (default: 3000 px)
2. Desactivar imágenes anotadas: `--no-annotated`
3. Procesar archivos en lotes pequeños
4. Verificar que los archivos no sean extremadamente grandes

---

## Contacto y Soporte

Para preguntas adicionales o problemas no resueltos, consultar la documentación técnica en `README.md` o revisar los logs en `logs/`.

### Logs

Los logs detallados se guardan en:
- `logs/pod_validation_FECHA.log`

Revisar estos archivos para diagnosticar problemas específicos.

---

## Ejemplos de Flujo de Trabajo

### Flujo Típico de Validación

1. **Preparación**
   ```bash
   # Colocar PODs en documentos/entrada/
   cp /ruta/original/POD*.pdf documentos/entrada/
   ```

2. **Procesamiento**
   ```bash
   # Activar entorno
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   
   # Procesar
   python src/main.py
   ```

3. **Revisión de Resultados**
   - Abrir `resultados/reportes/reporte_pods_TIMESTAMP.xlsx`
   - Filtrar por "Válido = NO"
   - Revisar recomendaciones

4. **Acciones Correctivas**
   - **SIN ACUSE**: Solicitar firma/sello
   - **POCO LEGIBLE/INCORRECTO**: Re-digitalizar
   - **CON ANOTACIONES (negativas)**: Investigar reclamación

5. **Verificación Manual**
   - Revisar imágenes anotadas en `resultados/imagenes_anotadas/`
   - Confirmar detecciones automáticas

6. **Mover documentos procesados**
   ```bash
   move documentos\entrada\* documentos\procesados\
   ```

---

¡Listo! Ahora estás preparado para usar el sistema de validación de PODs de manera efectiva.


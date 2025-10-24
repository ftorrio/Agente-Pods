# 🖥️ Guía de la Interfaz Gráfica

Manual completo para usar la interfaz gráfica del Sistema de Validación de PODs.

---

## 🚀 Iniciar la Interfaz

### Windows
```bash
run_gui.bat
```

### Linux/Mac
```bash
chmod +x run_gui.sh
./run_gui.sh
```

O manualmente:
```bash
# Activar entorno
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Ejecutar GUI
python src/gui.py
```

---

## 📊 Descripción de la Interfaz

La interfaz se divide en 6 secciones principales:

### 1️⃣ ENCABEZADO
```
🔍 Sistema de Validación de PODs
Proof of Delivery - Análisis Automático de Documentos
```
Título y descripción del sistema.

---

### 2️⃣ CONTROLES

#### Selector de Directorio
- **Campo de texto**: Muestra la ruta del directorio con los PODs
- **Botón "📁 Explorar"**: Abre un diálogo para seleccionar el directorio

#### Botones de Acción
- **▶️ Procesar PODs**: Inicia el análisis de todos los documentos
- **⏹️ Detener**: Interrumpe el procesamiento en curso
- **🗑️ Limpiar**: Borra todos los resultados mostrados

---

### 3️⃣ ESTADÍSTICAS

Muestra un resumen visual con 7 indicadores:

| Indicador | Descripción |
|-----------|-------------|
| **Total PODs** | Número total de documentos procesados |
| **✓ Válidos** | Documentos que pasaron la validación (verde) |
| **✗ Con Defectos** | Documentos con problemas (rojo) |
| **OK** | Documentos clasificados como OK |
| **Con Anotaciones** | Documentos con comentarios manuscritos |
| **Sin Acuse** | Documentos sin firma ni sello |
| **Tasa Validación** | Porcentaje de documentos válidos (azul) |

Las estadísticas se actualizan **en tiempo real** mientras se procesan los documentos.

---

### 4️⃣ TABLA DE RESULTADOS DETALLADOS

Tabla interactiva con 8 columnas:

| Columna | Contenido |
|---------|-----------|
| **Archivo** | Nombre del archivo POD |
| **Clasificación** | Categoría asignada (OK, SIN ACUSE, etc.) |
| **Estado** | ✓ Válido o ✗ Defecto |
| **Confianza** | Porcentaje de confianza del análisis |
| **Firmas** | Número de firmas detectadas |
| **Sellos** | Número de sellos detectados |
| **Anotaciones** | Estado de anotaciones (✓/✗/○ + sentimiento) |
| **Problemas/Detalles** | Resumen de problemas encontrados |

#### Códigos de Color de Filas:
- 🟢 **Verde claro**: Documento válido
- 🔴 **Rojo claro**: Documento con defectos
- 🟡 **Amarillo claro**: Documento con anotaciones (requiere revisión)

#### Interacción:
- **Doble clic** en una fila para ver **detalles completos**

---

### 5️⃣ LOG DE PROCESAMIENTO

Consola en tiempo real que muestra:
- Inicio del procesamiento
- Progreso de cada archivo
- Resultados individuales
- Errores o advertencias
- Finalización del proceso

#### Códigos de Color del Log:
- ⚫ **Negro**: Información general
- 🟢 **Verde**: Operaciones exitosas
- 🟡 **Amarillo**: Advertencias
- 🔴 **Rojo**: Errores

---

### 6️⃣ BOTONES DE ACCIÓN INFERIOR

- **📊 Abrir Reportes**: Abre la carpeta con los reportes Excel/CSV
- **🖼️ Ver Imágenes Anotadas**: Abre la carpeta con las imágenes procesadas
- **📋 Exportar Excel**: Genera y guarda un reporte Excel
- **❓ Ayuda**: Muestra información de ayuda rápida

---

## 🎯 Flujo de Trabajo Típico

### Paso 1: Preparar Documentos
```
1. Coloca tus archivos POD en: documentos/entrada/
2. Formatos soportados: PDF, GIF, PNG, JPG, TIFF, BMP
```

### Paso 2: Iniciar la Aplicación
```bash
run_gui.bat  # Windows
./run_gui.sh # Linux/Mac
```

### Paso 3: Seleccionar Directorio
```
1. Haz clic en "📁 Explorar"
2. Selecciona la carpeta con los PODs
   (por defecto: documentos/entrada/)
3. Haz clic en "Seleccionar carpeta"
```

### Paso 4: Procesar
```
1. Haz clic en "▶️ Procesar PODs"
2. Espera mientras se procesan los documentos
3. Observa el progreso en el log y las estadísticas
```

### Paso 5: Revisar Resultados
```
1. Consulta las estadísticas en la sección superior
2. Revisa la tabla de resultados
3. Doble clic en cualquier POD para ver detalles
```

### Paso 6: Análisis Detallado
```
Para cada documento con defectos:
1. Doble clic en la fila
2. Lee los problemas detectados
3. Revisa las recomendaciones
4. Haz clic en "Ver Imagen Anotada" si está disponible
```

### Paso 7: Exportar
```
1. Haz clic en "📊 Abrir Reportes" para ver Excel/CSV
2. O haz clic en "📋 Exportar Excel" para generar nuevo reporte
3. Haz clic en "🖼️ Ver Imágenes Anotadas" para revisar visualmente
```

---

## 🔍 Ventana de Detalles

Al hacer **doble clic** en un resultado, se abre una ventana con información completa:

### Información Mostrada:

#### 📋 Clasificación
- Categoría asignada
- Estado (Válido/Con Defectos)
- Porcentaje de confianza

#### ✍️ Firmas
- Lista de firmas detectadas
- Región donde se encontró cada firma
- Confianza de cada detección

#### 🔖 Sellos
- Tipo de sello (circular/rectangular)
- Estado (Válido/Inválido)
- Si es inválido, razón (ej: sello de Deacero)

#### 📝 Anotaciones
- Cantidad de anotaciones detectadas
- Sentimiento (positivo/negativo/neutral)
- Texto extraído de las anotaciones

#### 📖 Legibilidad
- Calidad del texto (0-1)
- Confianza del OCR
- Campos detectados (Factura, Cliente, etc.)

#### ⚠️ Problemas
- Lista detallada de todos los problemas encontrados

#### 💡 Recomendaciones
- Acciones sugeridas para resolver problemas

#### 🖼️ Imagen Anotada
- Botón para abrir la imagen con marcas visuales

---

## 📊 Interpretación de Resultados

### ✅ Documento Válido (Verde)
```
Clasificación: OK
Estado: ✓ Válido
Confianza: 95%

Acción: Ninguna, documento aprobado
```

### 📝 Con Anotaciones (Amarillo)
```
Clasificación: CON ANOTACIONES
Anotaciones: ✓ positive

Acción: Revisar manualmente las anotaciones
- Si es positivo: Probablemente válido
- Si es negativo: Atención urgente (posible reclamo)
```

### ⚠️ Sin Acuse (Rojo)
```
Clasificación: SIN ACUSE
Estado: ✗ Defecto

Acción: Solicitar POD con firma o sello del cliente
```

### ❌ Poco Legible (Rojo)
```
Clasificación: POCO LEGIBLE
Problemas: Campos insuficientes detectados: 2/3

Acción: Re-digitalizar con mejor calidad (300 DPI)
```

### ❌ Incorrecto (Rojo)
```
Clasificación: INCORRECTO
Problemas: Documento no completamente digitalizado

Acción: Escanear el documento completo sin cortes
```

---

## 💡 Consejos y Trucos

### ⚡ Procesamiento Rápido
1. Si solo necesitas clasificaciones sin imágenes anotadas, modifica la configuración
2. Procesa documentos en lotes de 50-100 para mejor rendimiento

### 🔍 Revisión Eficiente
1. Ordena la tabla por "Estado" para ver primero los defectuosos
2. Usa el scroll horizontal si la ventana es pequeña
3. El log guarda historial completo del procesamiento

### 📁 Organización
1. Después de procesar, mueve los PODs de `entrada/` a `procesados/`
2. Los reportes incluyen la fecha/hora en el nombre
3. Las imágenes anotadas tienen el mismo nombre que el original

### 🐛 Solución de Problemas
1. Si la GUI no inicia, verifica que el entorno virtual esté activado
2. Si no detecta archivos, verifica los formatos soportados
3. Si hay errores de procesamiento, revisa el log en rojo

---

## ⌨️ Atajos de Teclado

| Acción | Atajo |
|--------|-------|
| Abrir ventana de detalles | Doble clic en fila |
| Scroll en tabla | Rueda del ratón |
| Scroll en detalles | Rueda del ratón |

---

## 🎨 Códigos de Color

### Estados:
- 🟢 **Verde**: Válido, correcto, positivo
- 🔴 **Rojo**: Inválido, error, negativo
- 🟡 **Amarillo**: Advertencia, revisar
- 🔵 **Azul**: Información, neutral

### Sentimientos de Anotaciones:
- ✓ **Positivo**: Confirma recepción (verde)
- ✗ **Negativo**: Posible reclamo (rojo)
- ○ **Neutral**: Sin sentimiento claro (azul)

---

## 📋 Ejemplo Práctico

### Escenario: Validar 10 PODs

1. **Inicio**
   ```
   Total PODs: 0
   Válidos: 0
   Con Defectos: 0
   ```

2. **Durante Procesamiento**
   ```
   [10:30:15] Iniciando procesamiento de 10 archivo(s)...
   [10:30:16] [1/10] Procesando: POD_001.pdf
   [10:30:17] ✓ POD_001.pdf: OK
   [10:30:18] [2/10] Procesando: POD_002.pdf
   [10:30:19] ✗ POD_002.pdf: SIN ACUSE
   ...
   ```

3. **Resultado Final**
   ```
   Total PODs: 10
   Válidos: 7 (70%)
   Con Defectos: 3 (30%)
   
   Desglose:
   - OK: 6
   - Con Anotaciones: 1
   - Sin Acuse: 2
   - Poco Legible: 1
   ```

4. **Acción**
   - Los 6 OK están aprobados ✓
   - 1 con anotaciones positivas → Revisar y aprobar
   - 2 sin acuse → Solicitar firma
   - 1 poco legible → Re-escanear

---

## 🆘 Soporte

Si tienes problemas con la interfaz:

1. **Revisa el log** en la ventana inferior
2. **Consulta los logs del sistema** en `logs/`
3. **Verifica la configuración** en `config/settings.yaml`
4. **Lee la documentación** completa en `GUIA_USO.md`

---

## 🔄 Actualizaciones

Para actualizar el sistema:
```bash
git pull
pip install -r requirements.txt --upgrade
```

---

¡Disfruta validando PODs de forma visual y eficiente! 🎉


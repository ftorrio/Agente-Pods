# 🌐 Guía de la Interfaz Web

Manual completo para usar la interfaz web del Sistema de Validación de PODs.

---

## 🚀 Iniciar la Interfaz Web

### Windows
```bash
run_web.bat
```

### Linux/Mac
```bash
chmod +x run_web.sh
./run_web.sh
```

### Manualmente
```bash
# Activar entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Ejecutar aplicación web
streamlit run src/web_app.py
```

---

## 🌐 Acceder a la Aplicación

Una vez iniciado el servidor, se abrirá automáticamente en tu navegador:

```
🌐 URL: http://localhost:8501
```

Si no se abre automáticamente, copia y pega esa URL en tu navegador.

---

## 🖥️ Vista de la Interfaz Web

### Panel Lateral (Izquierda)

```
╔═══════════════════════════════╗
║ ⚙️ CONTROL                    ║
╠═══════════════════════════════╣
║ 📁 Directorio de PODs:        ║
║ [documentos/entrada/]         ║
║                               ║
║ 📊 15 archivo(s) encontrados  ║
║                               ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                               ║
║ [▶️ Procesar PODs]            ║
║                               ║
║ [🗑️ Limpiar Resultados]       ║
║                               ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                               ║
║ 🔗 Accesos Rápidos            ║
║ [📊 Abrir Reportes]           ║
║ [🖼️ Ver Imágenes]             ║
║                               ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                               ║
║ ℹ️ Información                ║
║ Clasificaciones:              ║
║ • ✅ OK: Válido               ║
║ • 📝 Con Anotaciones          ║
║ • ⚠️ Sin Acuse                ║
║ • ❌ Poco Legible             ║
║ • ❌ Incorrecto               ║
╚═══════════════════════════════╝
```

---

### Área Principal (Centro/Derecha)

#### 1. Dashboard de Métricas

```
╔═══════════════════════════════════════════════════════╗
║ 📊 DASHBOARD DE MÉTRICAS                              ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ ║
║  │📊 Total │  │✅ Válidos│  │❌ Defect│  │📈 Tasa  │ ║
║  │   15    │  │    12    │  │    3    │  │  80%    │ ║
║  │ PODs    │  │   ↑80%   │  │   ↓20%  │  │         │ ║
║  └─────────┘  └─────────┘  └─────────┘  └─────────┘ ║
║                                                       ║
║  ┌─────┐  ┌─────────┐  ┌─────────┐  ┌──────┐  ┌────┐║
║  │✅ OK│  │📝 Anotac│  │⚠️ Sin   │  │❌ Poco│  │❌ In│║
║  │  10 │  │    2    │  │  Acuse  │  │Legible│  │corr│║
║  │     │  │         │  │    2    │  │   1   │  │ 0  │║
║  └─────┘  └─────────┘  └─────────┘  └──────┘  └────┘║
╚═══════════════════════════════════════════════════════╝
```

#### 2. Visualizaciones

```
╔═══════════════════════════════════════════════════════╗
║ 📈 VISUALIZACIONES                                    ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  ┌─────────────────────┐  ┌──────────────────────┐  ║
║  │  DISTRIBUCIÓN POR   │  │  ESTADO DE          │  ║
║  │   CLASIFICACIÓN     │  │   VALIDACIÓN        │  ║
║  │                     │  │                      │  ║
║  │     [Gráfico       │  │    [Gráfico         │  ║
║  │      de Torta]     │  │     de Barras]      │  ║
║  │                     │  │                      │  ║
║  └─────────────────────┘  └──────────────────────┘  ║
╚═══════════════════════════════════════════════════════╝
```

#### 3. Tabla Interactiva

```
╔═══════════════════════════════════════════════════════╗
║ 📋 TABLA DE RESULTADOS DETALLADOS                     ║
╠═══════════════════════════════════════════════════════╣
║ Filtrar por Clasificación: [▼ Todas]                 ║
║ Filtrar por Estado: [▼ Todos]                        ║
║ 🔍 Buscar archivo: [____________]                     ║
║                                                       ║
║ ┌──────────┬─────────┬────────┬──────────┬──────┐   ║
║ │ Archivo  │Clasificac│ Estado │Confianza │Firmas│   ║
║ ├──────────┼─────────┼────────┼──────────┼──────┤   ║
║ │POD_001   │ OK      │✓ Válido│   95%    │  2   │   ║
║ │POD_002   │SIN ACUSE│✗Defecto│   90%    │  0   │   ║
║ │POD_003   │ANOTACION│⚠Revisar│   85%    │  1   │   ║
║ └──────────┴─────────┴────────┴──────────┴──────┘   ║
║                                                       ║
║ [📥 Descargar tabla como CSV]                        ║
╚═══════════════════════════════════════════════════════╝
```

#### 4. Vista Detallada

```
╔═══════════════════════════════════════════════════════╗
║ 🔍 VISTA DETALLADA                                    ║
╠═══════════════════════════════════════════════════════╣
║ Selecciona un POD: [▼ POD_001.pdf]                   ║
║                                                       ║
║ ┌───────────────────────────────────────────────────┐║
║ │ 📄 POD_001.pdf                          [VÁLIDO]  │║
║ ├───────────────────────────────────────────────────┤║
║ │ Clasificación  │  Estado    │  Confianza          │║
║ │     OK         │ ✓ Válido   │    95%              │║
║ └───────────────────────────────────────────────────┘║
║                                                       ║
║ [✍️ Firmas] [🔖 Sellos] [📝 Anotaciones] [📖 ...] [ ]║
║ ┌───────────────────────────────────────────────────┐║
║ │ ✍️ FIRMAS                                         │║
║ │                                                   │║
║ │ Detectadas 2 firma(s):                           │║
║ │ • Firma 1: Región zone_7, Confianza: 0.87       │║
║ │ • Firma 2: Región zone_8, Confianza: 0.92       │║
║ └───────────────────────────────────────────────────┘║
║                                                       ║
║ 🖼️ IMAGEN ANOTADA                                    ║
║ [Imagen del POD con marcas visuales]                 ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🎯 Flujo de Trabajo Típico

### 1️⃣ Iniciar la Aplicación
```bash
run_web.bat  # Se abrirá en tu navegador
```

### 2️⃣ Verificar Directorio
- El panel lateral muestra el directorio configurado
- Verás cuántos archivos se encontraron
- Si es incorrecto, puedes cambiarlo en el campo de texto

### 3️⃣ Procesar PODs
- Haz clic en **▶️ Procesar PODs**
- Verás una barra de progreso
- El procesamiento ocurre en tiempo real

### 4️⃣ Revisar Dashboard
- Las métricas se actualizan automáticamente
- Observa:
  - Total procesados
  - Válidos vs Con Defectos
  - Tasa de validación
  - Distribución por clasificación

### 5️⃣ Analizar Gráficos
- **Gráfico de Torta**: Distribución por clasificación
- **Gráfico de Barras**: Válidos vs Con Defectos

### 6️⃣ Explorar la Tabla
- Usa los filtros para mostrar solo ciertos tipos
- Busca por nombre de archivo
- Ordena por cualquier columna (clic en el encabezado)
- Descarga la tabla filtrada como CSV

### 7️⃣ Ver Detalles Individuales
- Selecciona un POD del desplegable
- Navega por las pestañas:
  - ✍️ **Firmas**: Detecciones de firmas
  - 🔖 **Sellos**: Detecciones de sellos
  - 📝 **Anotaciones**: Comentarios manuscritos
  - 📖 **Legibilidad**: Análisis OCR
  - ⚠️ **Problemas**: Problemas y recomendaciones
- Ve la imagen anotada al final

### 8️⃣ Exportar Resultados
- Descarga la tabla como CSV
- O usa **📊 Abrir Reportes** para ver los Excel
- O usa **🖼️ Ver Imágenes** para ver las anotadas

---

## 🎨 Características Interactivas

### Filtros Dinámicos
```
✅ Filtrar por clasificación (múltiple selección)
✅ Filtrar por estado (Válido/Defecto)
✅ Búsqueda por texto libre
✅ Combinación de filtros
```

### Gráficos Interactivos
```
✅ Zoom in/out
✅ Hover para ver detalles
✅ Exportar como imagen
✅ Responsive (se adapta al tamaño)
```

### Tabla Dinámica
```
✅ Ordenamiento por columna
✅ Scroll horizontal/vertical
✅ Descarga como CSV
✅ Búsqueda instantánea
```

### Navegación por Pestañas
```
✅ Organización clara de información
✅ Acceso rápido a detalles
✅ Sin recargar la página
```

---

## 💡 Ventajas de la Interfaz Web

### 🌐 Acceso Remoto
- Puede ejecutarse en un servidor
- Acceso desde cualquier dispositivo con navegador
- Múltiples usuarios simultáneos (con servidor apropiado)

### 📱 Responsive
- Se adapta a diferentes tamaños de pantalla
- Funciona en tablets y móviles
- Layout flexible

### 🎨 Moderna y Visual
- Gráficos interactivos con Plotly
- Métricas grandes y claras
- Colores según estado (verde/rojo/amarillo)

### 🚀 Rápida y Eficiente
- Actualización automática
- Sin recargar página completa
- Procesamiento con barra de progreso

### 📊 Análisis Integrado
- Dashboard completo en una vista
- Gráficos generados automáticamente
- Filtros en tiempo real

---

## 🔧 Configuración Avanzada

### Cambiar Puerto

Edita `run_web.bat` o `run_web.sh`:
```bash
streamlit run src/web_app.py --server.port 8080
```

### Modo Headless (Sin abrir navegador)

```bash
streamlit run src/web_app.py --server.headless true
```

### Permitir Acceso Externo

```bash
streamlit run src/web_app.py --server.address 0.0.0.0
```

---

## 🆚 Comparación: Web vs Escritorio

| Característica | Interfaz Web | Interfaz Escritorio |
|----------------|--------------|---------------------|
| **Instalación** | Streamlit | Tkinter (incluido) |
| **Acceso** | Navegador | App local |
| **Plataforma** | Cualquiera con navegador | Windows/Linux/Mac |
| **Gráficos** | Plotly (interactivos) | Básicos |
| **Actualización** | Automática | Manual |
| **Multi-usuario** | ✅ Sí (con servidor) | ❌ No |
| **Responsive** | ✅ Sí | ❌ Fijo |
| **Filtros** | Avanzados | Básicos |
| **Deploy** | Cloud posible | Solo local |

---

## 🌍 Desplegar en la Nube (Opcional)

### Streamlit Cloud (Gratis)

1. Sube el proyecto a GitHub
2. Ve a https://streamlit.io/cloud
3. Conecta tu repositorio
4. Selecciona `src/web_app.py`
5. ¡Deploy!

### Heroku

```bash
# Crear Procfile
echo "web: streamlit run src/web_app.py --server.port $PORT" > Procfile

# Deploy
heroku create mi-validador-pods
git push heroku main
```

---

## ❓ Problemas Comunes

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Solución:**
```bash
pip install streamlit plotly
```

### ❌ El navegador no se abre automáticamente

**Solución:**
- Abre manualmente: http://localhost:8501
- O usa `--server.headless false` en el comando

### ❌ Puerto ya en uso

**Solución:**
```bash
# Cambiar puerto
streamlit run src/web_app.py --server.port 8502
```

### ❌ "Address already in use"

**Solución:**
- Cierra otras instancias de Streamlit
- O usa un puerto diferente

---

## 🎉 ¡Listo para Usar!

Ahora tienes una interfaz web moderna y profesional para validar PODs con:
- ✅ Dashboard interactivo
- ✅ Gráficos visuales
- ✅ Filtros avanzados
- ✅ Tabla exportable
- ✅ Vista detallada
- ✅ Responsive design
- ✅ Fácil de usar

**Para empezar:**
```bash
run_web.bat  # ¡Ejecuta y abre tu navegador! 🚀
```

---

**¡Disfruta validando PODs desde tu navegador!** 🌐


# 🖥️ Cómo Ver la Interfaz Gráfica

Guía paso a paso para ejecutar la interfaz gráfica del Sistema de Validación de PODs.

---

## ✅ MÉTODO RÁPIDO (Windows)

### Opción A: Si ya tienes Python instalado

1. **Doble clic en este archivo:**
   ```
   INSTALAR_Y_EJECUTAR.bat
   ```

2. **Espera** mientras se instalan las dependencias (primera vez: 2-3 minutos)

3. **¡Listo!** La interfaz se abrirá automáticamente

---

### Opción B: Si NO tienes Python

#### Paso 1: Instalar Python (5 minutos)

1. Ve a: **https://www.python.org/downloads/**

2. Descarga **Python 3.11** (o la última versión)

3. Ejecuta el instalador descargado

4. ⚠️ **MUY IMPORTANTE:** 
   - Marca la casilla: ☑️ **"Add Python to PATH"**
   - Esto es ESENCIAL

5. Haz clic en **"Install Now"**

6. Espera a que termine (2-3 minutos)

7. **Verifica la instalación:**
   - Abre **PowerShell** (busca "PowerShell" en el menú inicio)
   - Escribe: `python --version`
   - Deberías ver algo como: `Python 3.11.x`
   - Si ves esto, ¡todo bien! ✅

#### Paso 2: Instalar Tesseract OCR (5 minutos)

1. Ve a: **https://github.com/UB-Mannheim/tesseract/wiki**

2. Descarga el instalador para Windows

3. Ejecuta el instalador

4. Durante la instalación:
   - Acepta la ubicación por defecto: `C:\Program Files\Tesseract-OCR`
   - Asegúrate de instalar los datos de idioma español

5. **Agregar al PATH:**
   - Abre **Panel de Control**
   - Ve a **Sistema y Seguridad → Sistema → Configuración avanzada del sistema**
   - Haz clic en **"Variables de entorno"**
   - En "Variables del sistema", busca **Path** y haz clic en **Editar**
   - Haz clic en **Nuevo** y agrega: `C:\Program Files\Tesseract-OCR`
   - Haz clic en **Aceptar** en todas las ventanas

6. **Verifica la instalación:**
   - Abre una **NUEVA** ventana de PowerShell
   - Escribe: `tesseract --version`
   - Deberías ver la versión de Tesseract

#### Paso 3: Ejecutar la Interfaz

1. **Navega a la carpeta del proyecto:**
   ```
   C:\Fabian\Cursor\Pods_DAS
   ```

2. **Doble clic en:**
   ```
   INSTALAR_Y_EJECUTAR.bat
   ```

3. **Espera** mientras se instala (primera vez: 2-3 minutos)

4. **¡La interfaz se abrirá!** 🎉

---

## 🖥️ Vista de la Interfaz

Una vez que se abra, verás algo así:

```
┌──────────────────────────────────────────────────────────┐
│      🔍 Sistema de Validación de PODs                    │
│      Proof of Delivery - Análisis Automático            │
├──────────────────────────────────────────────────────────┤
│  CONTROL                                                 │
│  Directorio: [documentos/entrada/    ] [📁 Explorar]    │
│  [▶️ Procesar PODs] [⏹️ Detener] [🗑️ Limpiar]           │
├──────────────────────────────────────────────────────────┤
│  ESTADÍSTICAS                                            │
│  ┌────────┬────────┬──────────┬─────┬──────────┬───────┐│
│  │ Total  │Válidos │ Defectos │ OK  │Anotacion.│Sin Ac.││
│  │   0    │   0    │    0     │  0  │    0     │   0   ││
│  │        │        │          │Tasa: 0%                ││
│  └────────┴────────┴──────────┴─────┴──────────┴───────┘│
├──────────────────────────────────────────────────────────┤
│  RESULTADOS DETALLADOS                                   │
│  ┌─────────┬──────────┬────────┬──────────┬─────┬─────┐ │
│  │ Archivo │Clasific. │ Estado │Confianza │Firma│Sello│ │
│  ├─────────┼──────────┼────────┼──────────┼─────┼─────┤ │
│  │         │          │        │          │     │     │ │
│  │    (vacío hasta que proceses documentos)            │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────┤
│  LOG DE PROCESAMIENTO                                    │
│  Sistema iniciado. Listo para procesar PODs...          │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  [📊 Abrir Reportes] [🖼️ Ver Imágenes] [❓ Ayuda]        │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 Probar con Documentos de Ejemplo

Si quieres probar la interfaz pero no tienes PODs reales:

1. **Coloca cualquier PDF o imagen** en:
   ```
   C:\Fabian\Cursor\Pods_DAS\documentos\entrada\
   ```

2. **En la interfaz:**
   - Haz clic en **"▶️ Procesar PODs"**
   - Observa cómo se procesa
   - Ve los resultados en la tabla

---

## 🎯 Usar la Interfaz (Guía Rápida)

### 1. Seleccionar Directorio
```
Haz clic en [📁 Explorar] → Selecciona carpeta con PODs
```

### 2. Procesar
```
Haz clic en [▶️ Procesar PODs]
```

### 3. Observar
```
- Las estadísticas se actualizan en tiempo real
- La tabla se llena con cada POD procesado
- El log muestra el progreso
```

### 4. Ver Detalles
```
Doble clic en cualquier fila de la tabla
→ Se abre ventana con información completa
```

### 5. Exportar
```
Haz clic en [📊 Abrir Reportes] para ver los Excel generados
```

---

## ❓ Problemas Comunes

### ❌ "Python no se reconoce..."
**Solución:** No marcaste "Add Python to PATH" durante la instalación
- Desinstala Python
- Reinstala y MARCA la casilla "Add Python to PATH"

### ❌ "Tesseract not found"
**Solución:** Tesseract no está en el PATH
- Ve a Panel de Control → Variables de entorno
- Agrega `C:\Program Files\Tesseract-OCR` al PATH
- Abre una NUEVA ventana de PowerShell

### ❌ "No se encontraron archivos"
**Solución:** No hay PODs en el directorio
- Asegúrate de tener archivos PDF/GIF/PNG/JPG en la carpeta
- Verifica que estés seleccionando el directorio correcto

### ❌ La interfaz no se abre
**Solución:** Ejecuta manualmente:
```bash
# Abre PowerShell en la carpeta del proyecto
cd C:\Fabian\Cursor\Pods_DAS
venv\Scripts\activate
python src/gui.py
```

---

## 📞 ¿Necesitas Ayuda?

Si tienes algún problema:
1. Lee los mensajes de error en la ventana
2. Revisa este archivo paso a paso
3. Verifica que Python y Tesseract estén instalados
4. Abre una nueva ventana de PowerShell después de instalar

---

## 🎉 ¡Listo!

Una vez que veas la interfaz, ya puedes:
- ✅ Procesar PODs automáticamente
- ✅ Ver estadísticas en tiempo real
- ✅ Revisar cada POD en detalle
- ✅ Exportar reportes a Excel
- ✅ Ver imágenes anotadas

---

**Tiempo total de instalación:** 10-15 minutos (primera vez)  
**Tiempo para ejecutar después:** 5 segundos

¡Disfruta validando PODs! 🚀


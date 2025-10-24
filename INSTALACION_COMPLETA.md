# 📦 Instalación Completa - Paso a Paso

Guía visual completa para instalar y ejecutar el Sistema de Validación de PODs.

---

## ✅ PASO 1: Instalar Python (10 minutos)

### 1.1 Descargar Python

1. **Abre tu navegador**
2. **Ve a**: https://www.python.org/downloads/
3. **Descarga**: Haz clic en el botón amarillo grande "Download Python 3.11.x"
4. **Espera** a que termine la descarga (≈30 MB)

### 1.2 Instalar Python

1. **Ejecuta el archivo descargado** (doble clic)
2. **⚠️ MUY IMPORTANTE**: 
   ```
   ☑️ MARCA esta casilla: "Add Python to PATH"
   ```
   Esta casilla está **abajo** en la primera pantalla. ¡Es CRUCIAL marcarla!

3. **Haz clic** en "Install Now"
4. **Espera** 2-3 minutos mientras se instala
5. **Clic** en "Close" cuando termine

### 1.3 Verificar Instalación

1. **Abre PowerShell**:
   - Presiona `Windows + X`
   - Selecciona "Windows PowerShell" o "Terminal"

2. **Escribe** este comando y presiona Enter:
   ```powershell
   python --version
   ```

3. **Deberías ver** algo como:
   ```
   Python 3.11.7
   ```

✅ Si ves esto, **Python está instalado correctamente**

❌ Si ves un error, **reinicia tu computadora** e intenta de nuevo

---

## ✅ PASO 2: Instalar Tesseract OCR (10 minutos)

### 2.1 Descargar Tesseract

1. **Abre tu navegador**
2. **Ve a**: https://github.com/UB-Mannheim/tesseract/wiki
3. **Descarga**: Haz clic en el enlace del instalador para Windows (64-bit)
   - Busca: "tesseract-ocr-w64-setup-xxx.exe"

### 2.2 Instalar Tesseract

1. **Ejecuta el instalador** descargado
2. **Acepta** la ubicación por defecto: `C:\Program Files\Tesseract-OCR`
3. **Asegúrate** de instalar el idioma español:
   - En "Choose Components" → Marca "Spanish"
4. **Haz clic** en "Install"
5. **Espera** a que termine

### 2.3 Agregar al PATH

1. **Abre Panel de Control**:
   - Presiona `Windows + R`
   - Escribe: `sysdm.cpl`
   - Presiona Enter

2. **Ve a** la pestaña "Opciones avanzadas"

3. **Haz clic** en "Variables de entorno"

4. **En "Variables del sistema"**:
   - Busca y selecciona "Path"
   - Haz clic en "Editar"

5. **Haz clic** en "Nuevo"

6. **Escribe**: 
   ```
   C:\Program Files\Tesseract-OCR
   ```

7. **Haz clic** en "Aceptar" en todas las ventanas

8. **Cierra** todas las ventanas de PowerShell abiertas

### 2.4 Verificar Instalación

1. **Abre una NUEVA ventana de PowerShell**

2. **Escribe**:
   ```powershell
   tesseract --version
   ```

3. **Deberías ver**:
   ```
   tesseract 5.x.x
   ```

✅ Si ves esto, **Tesseract está instalado correctamente**

---

## ✅ PASO 3: Instalar Dependencias del Proyecto (5 minutos)

### 3.1 Método Automático (Recomendado)

1. **Navega** a la carpeta del proyecto:
   ```
   C:\Fabian\Cursor\Pods_DAS
   ```

2. **Doble clic** en:
   ```
   INSTALAR_Y_EJECUTAR.bat
   ```

3. **Espera** mientras se instala todo (2-3 minutos)

4. **¡La interfaz se abrirá automáticamente!** 🎉

### 3.2 Método Manual (Si el automático falla)

1. **Abre PowerShell** en la carpeta del proyecto:
   - `Shift + Clic derecho` en la carpeta
   - "Abrir ventana de PowerShell aquí"

2. **Ejecuta estos comandos** uno por uno:

   ```powershell
   # Crear entorno virtual
   python -m venv venv
   
   # Activar entorno virtual
   .\venv\Scripts\Activate.ps1
   
   # Actualizar pip
   python -m pip install --upgrade pip
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

3. **Si da error de permisos** al activar:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Luego intenta de nuevo el paso 2.

---

## ✅ PASO 4: Ejecutar la Interfaz Web (30 segundos)

### 4.1 Primera Vez

**Doble clic** en:
```
run_web.bat
```

Se abrirá automáticamente en tu navegador en: `http://localhost:8501`

### 4.2 Siguientes Veces

Simplemente **doble clic** en `run_web.bat` ¡y listo!

---

## 🎨 ¿Qué verás?

### Pantalla Inicial

```
┌────────────────────────────────────────────────┐
│ 🔍 Sistema de Validación de PODs               │
│ Proof of Delivery - Análisis Automático       │
├────────────────────────────────────────────────┤
│                                                │
│ 👋 Bienvenido al Sistema de Validación        │
│                                                │
│ Para comenzar:                                 │
│ 1. Coloca tus archivos POD en la carpeta      │
│    documentos/entrada/                         │
│ 2. Verifica el directorio en el panel         │
│ 3. Haz clic en ▶️ Procesar PODs                │
│ 4. Revisa los resultados                      │
│                                                │
│ Formatos soportados:                          │
│ PDF, GIF, PNG, JPG, TIFF, BMP                 │
│                                                │
└────────────────────────────────────────────────┘
```

### Después de Procesar

```
┌────────────────────────────────────────────────┐
│ 📊 DASHBOARD DE MÉTRICAS                       │
│                                                │
│  Total: 10  Válidos: 8  Defectos: 2  (80%)   │
│                                                │
│ 📈 GRÁFICOS INTERACTIVOS                       │
│  [Gráfico Torta]  [Gráfico Barras]           │
│                                                │
│ 📋 TABLA DE RESULTADOS                         │
│  [Filtros]  [Búsqueda]                        │
│  Lista completa de PODs...                    │
│                                                │
│ 🔍 VISTA DETALLADA                             │
│  Información completa de cada POD...          │
└────────────────────────────────────────────────┘
```

---

## ❓ Problemas Comunes

### ❌ "python no se reconoce..."

**Problema**: Python no está en el PATH

**Solución**:
1. Desinstala Python
2. Reinstala y **MARCA** la casilla "Add Python to PATH"
3. Reinicia la computadora

### ❌ "tesseract not found"

**Problema**: Tesseract no está en el PATH

**Solución**:
1. Sigue el Paso 2.3 para agregar al PATH
2. Cierra TODAS las ventanas de PowerShell
3. Abre una NUEVA ventana
4. Intenta de nuevo

### ❌ "cannot be loaded because running scripts is disabled"

**Problema**: PowerShell no permite ejecutar scripts

**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Problema**: Las dependencias no se instalaron

**Solución**:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 Checklist de Instalación

Marca cada item cuando lo completes:

- [ ] Python 3.8+ instalado
- [ ] Python agregado al PATH
- [ ] Python verificado con `python --version`
- [ ] Tesseract OCR instalado
- [ ] Tesseract agregado al PATH
- [ ] Tesseract verificado con `tesseract --version`
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Script `run_web.bat` ejecutado
- [ ] Interfaz web abierta en el navegador

---

## 🎉 ¡Listo!

Una vez completados todos los pasos:

1. **Coloca algunos PODs** en `documentos/entrada/`
2. **Ejecuta** `run_web.bat`
3. **Haz clic** en "▶️ Procesar PODs"
4. **Disfruta** viendo los resultados en tiempo real

---

## 🆘 ¿Necesitas Ayuda?

Si algo no funciona:
1. Lee la sección "Problemas Comunes"
2. Verifica el checklist completo
3. Revisa los logs en la consola

---

## 📚 Documentación

Después de instalar, consulta:
- `GUIA_INTERFAZ_WEB.md` - Cómo usar la interfaz web
- `COMPARACION_INTERFACES.md` - Comparar interfaces
- `README.md` - Documentación completa

---

**Tiempo total estimado**: 25-30 minutos
**Una sola vez**: Sí, después solo ejecutas `run_web.bat`


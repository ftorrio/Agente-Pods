# 💾 Guía de Respaldo y Restauración

Cómo hacer respaldos del sistema y restaurarlos cuando sea necesario.

---

## 🚀 Hacer un Respaldo Rápido

### Windows
```bash
# Doble clic en:
HACER_RESPALDO.bat
```

### Linux/Mac
```bash
chmod +x HACER_RESPALDO.sh
./HACER_RESPALDO.sh
```

---

## 📦 ¿Qué Incluye el Respaldo?

### ✅ SÍ se Respalda:
- ✅ Todo el código fuente (`src/`)
- ✅ Configuración (`config/settings.yaml`)
- ✅ Documentación (todos los `.md` y `.txt`)
- ✅ Scripts de instalación (`install.bat`, `run_web.bat`, etc.)
- ✅ Archivos Python de ejemplo
- ✅ Estructura de carpetas vacías

### ❌ NO se Respalda (por tamaño/seguridad):
- ❌ Entorno virtual (`venv/`) - se puede recrear
- ❌ PODs procesados (`documentos/`) - datos temporales
- ❌ Resultados (`resultados/`) - se pueden regenerar
- ❌ Logs (`logs/`) - datos temporales
- ❌ Archivos temporales

---

## 📁 Estructura del Respaldo

```
Pods_DAS_Backup_20251023_1530/
├── src/                    # Código fuente completo
├── config/                 # Configuración
├── documentos/             # Estructura de carpetas
├── logs/                   # (vacío)
├── resultados/             # (vacío)
├── *.md                    # Documentación
├── *.bat                   # Scripts Windows
├── *.sh                    # Scripts Linux/Mac
├── requirements.txt        # Dependencias
└── .gitignore             # Configuración Git
```

---

## 💿 Opciones de Respaldo

### Opción 1: Carpeta (Sin Comprimir)
```
📁 Pods_DAS_Backup_20251023_1530/
   (≈5-10 MB)
```

**Ventajas:**
- Rápido de crear
- Fácil de inspeccionar
- Fácil de modificar

**Uso:** Respaldos locales frecuentes

---

### Opción 2: ZIP/TAR.GZ (Comprimido)
```
📦 Pods_DAS_Backup_20251023_1530.zip
   (≈2-3 MB)
```

**Ventajas:**
- Ocupa menos espacio
- Fácil de transferir
- Un solo archivo

**Uso:** Respaldos para almacenar/compartir

---

## 🔄 Restaurar un Respaldo

### Paso 1: Descomprimir (si está comprimido)
```bash
# Windows: Click derecho → Extraer todo

# Linux/Mac:
tar -xzf Pods_DAS_Backup_20251023_1530.tar.gz
```

### Paso 2: Entrar a la carpeta
```bash
cd Pods_DAS_Backup_20251023_1530
```

### Paso 3: Instalar dependencias
```bash
# Windows
install.bat

# Linux/Mac
./install.sh
```

### Paso 4: Ejecutar
```bash
# Windows
run_web.bat

# Linux/Mac
./run_web.sh
```

---

## 📅 Estrategia de Respaldos Recomendada

### Respaldos Automáticos

**Diarios (Durante desarrollo):**
- Ejecuta `HACER_RESPALDO.bat` al final del día
- Guarda en carpeta local

**Semanales (En producción):**
- Respaldo completo comprimido
- Guardar en carpeta compartida/cloud

**Antes de cambios importantes:**
- Respaldo inmediato
- Con nombre descriptivo

---

## 💾 Dónde Guardar los Respaldos

### Opción 1: Carpeta Local
```
C:\Respaldos\PODs_DAS\
└── Pods_DAS_Backup_20251023_1530.zip
```

### Opción 2: Unidad de Red
```
\\servidor\respaldos\PODs_DAS\
```

### Opción 3: Cloud (OneDrive, Google Drive, etc.)
- Sube el archivo ZIP
- Fácil acceso desde cualquier lugar

### Opción 4: Repositorio Git
```bash
git init
git add .
git commit -m "Respaldo del proyecto"
git push origin main
```

---

## 🔐 Respaldo de Datos Sensibles

### Credenciales (credentials.json)
⚠️ **NO incluir en respaldos compartidos**

Si necesitas respaldar credenciales:
1. Copia `config/credentials.json` aparte
2. Guárdalo en ubicación segura
3. NO lo subas a repositorios públicos

### Configuración Personalizada
✅ `config/settings.yaml` SÍ se incluye en respaldos

---

## 📊 Respaldo de Resultados (Opcional)

Si quieres respaldar resultados generados:

### Manual:
```bash
# Copiar resultados a carpeta de respaldo
xcopy /E /I resultados "%backup_path%\resultados\"
```

### Automático:
Edita `HACER_RESPALDO.bat` y descomenta la sección de resultados.

---

## ✅ Verificar un Respaldo

Después de crear un respaldo:

1. **Abre** la carpeta del respaldo
2. **Verifica** que contiene:
   - ✅ Carpeta `src/` con archivos .py
   - ✅ Carpeta `config/` con settings.yaml
   - ✅ Archivos .md de documentación
   - ✅ requirements.txt
   - ✅ Scripts .bat/.sh

3. **Si algo falta**, ejecuta el script de respaldo de nuevo

---

## 🆘 Recuperación de Desastres

Si pierdes el proyecto original:

1. **Descomprime** el respaldo más reciente
2. **Navega** a la carpeta
3. **Ejecuta** `install.bat` (o `install.sh`)
4. **Espera** 2-3 minutos
5. **Ejecuta** `run_web.bat` (o `run_web.sh`)
6. **¡Recuperado!** 🎉

---

## 📝 Registro de Respaldos

Crea un archivo `RESPALDOS.txt` para llevar control:

```
Fecha       | Versión | Ubicación              | Notas
------------|---------|------------------------|------------------
2025-10-23  | 1.0.0   | C:\Respaldos\...       | Versión inicial
2025-10-24  | 1.0.1   | OneDrive/...           | Agregado OCR
...
```

---

## 🎯 Resumen Rápido

**Hacer respaldo:**
```bash
HACER_RESPALDO.bat  # Doble clic
```

**Restaurar:**
```bash
1. Descomprimir
2. install.bat
3. run_web.bat
```

**Frecuencia recomendada:**
- Durante desarrollo: Diario
- En producción: Semanal
- Antes de cambios: Siempre

---

¡Tus respaldos están seguros! 💾✨


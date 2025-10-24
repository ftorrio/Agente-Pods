# ☁️ Guía de Google Cloud Storage

Cómo leer y procesar PODs directamente desde Google Cloud Storage.

---

## 🌐 Nueva Funcionalidad: Leer PODs desde la Nube

El sistema ahora puede **descargar y procesar PODs** directamente desde tu bucket de Google Cloud Storage sin necesidad de descargarlos manualmente.

---

## 🚀 Cómo Usar

### En la Interfaz Web (localhost:8501):

1. **Abre** la aplicación web (run_web.bat)

2. **En el Panel Lateral** verás una nueva sección:
   ```
   ╔════════════════════════════╗
   ║ 📂 Fuente de Datos         ║
   ║                            ║
   ║ ○ 💻 Archivos Locales      ║
   ║ ● ☁️ Google Cloud Storage  ║  ← Selecciona esta opción
   ╚════════════════════════════╝
   ```

3. **Configura** los parámetros:
   ```
   🌐 URL Base:
   https://storage.cloud.google.com/dea-documents-das/pod
   
   📁 Carpeta/Prefijo:
   IES161108I36  ← Tu carpeta en el bucket
   
   📝 Lista de archivos:
   pod_IES161108I36_QC8261_1024008261.jpg
   pod_IES161108I36_QM2015_1033002015.jpg
   pod_IES161108I36_QP7957_1036007957.jpg
   ...
   ```

4. **Haz clic** en "▶️ Procesar PODs"

5. **El sistema hará automáticamente:**
   - 📥 Descarga los archivos desde la nube (50% progreso)
   - ⚙️ Procesa cada POD (50-100% progreso)
   - 📊 Muestra resultados en el dashboard

---

## 📋 Estructura de URL

Tus PODs están en:
```
https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/NOMBRE_ARCHIVO.ext
│                                                │          │           │
└─ Bucket                                        └─ Bucket  └─ Carpeta  └─ Archivo
```

**Ejemplo completo:**
```
https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/pod_IES161108I36_QC8261_1024008261.jpg
```

---

## 📝 Cómo Agregar Archivos a la Lista

### Opción 1: Manual (uno por línea)

En el campo "Lista de archivos", escribe los nombres:
```
pod_IES161108I36_QC8261_1024008261.jpg
pod_IES161108I36_QM2015_1033002015.jpg
pod_IES161108I36_QP7957_1036007957.jpg
pod_IES161108I36_QP7960_1036007960.jpg
```

### Opción 2: Copiar y Pegar

Si tienes la lista en Excel o un archivo de texto, cópiala y pégala directamente.

---

## ⚙️ Ventajas de Usar Cloud Storage

✅ **No necesitas descargar manualmente** los PODs  
✅ **Procesa directamente** desde la nube  
✅ **Ahorra espacio** en disco local  
✅ **Acceso centralizado** a los documentos  
✅ **Múltiples usuarios** pueden procesar desde el mismo bucket  
✅ **Actualización automática** - siempre procesas la versión más reciente  

---

## 🔄 Flujo de Trabajo con Cloud

```
1. Usuario selecciona "☁️ Google Cloud Storage"
           ↓
2. Configura carpeta: IES161108I36
           ↓
3. Lista los archivos a procesar
           ↓
4. Clic en "▶️ Procesar PODs"
           ↓
5. Sistema descarga archivos (temporal)
           ↓
6. Sistema procesa cada POD
           ↓
7. Muestra resultados en dashboard
           ↓
8. Limpia archivos temporales
```

---

## 📊 Progreso en Pantalla

Cuando procesas desde la nube verás:

```
Barra de Progreso:

0-50%:  📥 Descargando archivos desde Google Cloud
         "Descargando 1/4: pod_xxx.jpg"
         "Descargando 2/4: pod_yyy.jpg"
         ...

50-100%: ⚙️ Procesando PODs
         "Procesando 1/4: pod_xxx.jpg"
         "Procesando 2/4: pod_yyy.jpg"
         ...

100%:   ✅ Procesamiento completado
```

---

## 🔒 Seguridad y Permisos

### Para Buckets Públicos:
- ✅ Funciona directamente
- ✅ No requiere autenticación
- ✅ Solo lectura

### Para Buckets Privados:
Necesitarás configurar credenciales:
```python
# Configurar variable de entorno
GOOGLE_APPLICATION_CREDENTIALS="ruta/a/credenciales.json"
```

---

## 💡 Casos de Uso

### 1. Procesamiento Centralizado
```
Múltiples usuarios → Mismo bucket → Procesan PODs compartidos
```

### 2. Auditoría sin Descarga
```
Auditor → Accede a PODs en la nube → Procesa → Genera reportes
```

### 3. Automatización Cloud
```
PODs suben a bucket → Sistema detecta → Procesa automáticamente
```

---

## 🆚 Comparación: Local vs Cloud

| Aspecto | Archivos Locales | Google Cloud Storage |
|---------|------------------|---------------------|
| **Descarga** | Manual | Automática |
| **Espacio** | Requiere espacio local | Solo temporal |
| **Acceso** | Solo local | Desde cualquier lugar |
| **Actualización** | Manual | Siempre actualizado |
| **Multi-usuario** | Copias separadas | Fuente compartida |
| **Velocidad** | Muy rápido | Depende de internet |

---

## ❓ Preguntas Frecuentes

### ¿Necesito descargar los PODs manualmente?
**No.** El sistema los descarga automáticamente en temporal y los procesa.

### ¿Los archivos descargados se quedan en mi PC?
**No.** Se guardan en una carpeta temporal y se pueden limpiar después.

### ¿Puedo procesar PODs de diferentes carpetas?
**Sí.** Solo cambia el "Carpeta/Prefijo" en la interfaz.

### ¿Qué pasa si no tengo internet?
Usa la opción "💻 Archivos Locales" en lugar de Cloud Storage.

### ¿Funciona con otros servicios cloud (AWS, Azure)?
Por ahora solo Google Cloud Storage, pero se puede extender.

---

## 🔧 Configuración Avanzada

### Cambiar URL Base del Bucket

En la interfaz web, el campo "URL Base" está deshabilitado por defecto, pero puedes modificarlo en el código:

```python
# En src/cloud_storage.py
self.base_url = "https://storage.cloud.google.com/TU-BUCKET/TU-RUTA"
```

### Agregar Autenticación

Para buckets privados, configura las credenciales:

```python
from google.cloud import storage

# Usar cliente autenticado
client = storage.Client.from_service_account_json('credenciales.json')
bucket = client.bucket('dea-documents-das')
```

---

## ✨ Próximas Mejoras

- [ ] Autodetección de archivos en el bucket
- [ ] Soporte para AWS S3
- [ ] Soporte para Azure Blob Storage
- [ ] Caché de archivos descargados
- [ ] Procesamiento directo sin descarga (streaming)

---

**¡Ahora puedes procesar PODs directamente desde la nube!** 🎉

Para empezar:
1. Abre la aplicación web
2. Selecciona "☁️ Google Cloud Storage"
3. Configura tu carpeta
4. Lista los archivos
5. ¡Procesa!


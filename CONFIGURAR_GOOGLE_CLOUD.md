# ☁️ Configurar Acceso a Google Cloud Storage

Guía para configurar el acceso autenticado a tu bucket de Google Cloud Storage.

---

## 🔐 Opción 1: Service Account (Recomendado para Automatización)

### Paso 1: Crear Service Account

1. **Ve a Google Cloud Console:**
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts
   ```

2. **Selecciona tu proyecto**

3. **Haz clic en** "Crear cuenta de servicio"

4. **Configura:**
   - Nombre: `pod-validator-reader`
   - Descripción: `Lector para validación de PODs`
   - Haz clic en "Crear y continuar"

5. **Asigna roles:**
   - Rol: `Storage Object Viewer` (solo lectura)
   - Haz clic en "Continuar"

6. **Omite** el paso 3 (opcional)

7. **Haz clic** en "Listo"

### Paso 2: Crear Clave JSON

1. **En la lista de service accounts**, haz clic en la cuenta que creaste

2. **Ve a** la pestaña "Claves"

3. **Haz clic en** "Agregar clave" → "Crear clave nueva"

4. **Selecciona** tipo: JSON

5. **Haz clic** en "Crear"

6. **Se descargará** un archivo JSON (ej: `proyecto-123456-abc.json`)

### Paso 3: Guardar Credenciales

1. **Mueve** el archivo JSON descargado a:
   ```
   C:\Fabian\Cursor\Pods_DAS\config\credentials.json
   ```

2. **Renómbralo** a `credentials.json` (si tiene otro nombre)

---

## 🌐 Opción 2: Hacer el Bucket Público (Más Fácil)

Si los PODs no son confidenciales:

### Paso 1: Hacer Público el Bucket

1. **Ve a:**
   ```
   https://console.cloud.google.com/storage/browser
   ```

2. **Selecciona** tu bucket: `dea-documents-das`

3. **Ve a** la pestaña "Permisos"

4. **Haz clic** en "Conceder acceso"

5. **Agrega:**
   - Nuevos principales: `allUsers`
   - Rol: `Storage Object Viewer`

6. **Guarda**

7. **Confirma** que quieres hacer público

### Paso 2: Probar

Abre en tu navegador:
```
https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/pod_IES161108I36_QC8261_1024008261.jpg
```

Si ves la imagen directamente → ¡Funciona!

---

## ⚙️ Configurar en la Aplicación

Una vez que tengas credenciales O bucket público:

### Con Service Account:

1. **Coloca** `credentials.json` en `config/`

2. **En la aplicación web**, verás opción para cargar credenciales

### Con Bucket Público:

¡Ya funciona! Solo selecciona "☁️ Google Cloud Storage" y procesa.

---

## 📋 Resumen de Opciones

| Opción | Dificultad | Seguridad | Mejor Para |
|--------|------------|-----------|------------|
| **Service Account** | Media | Alta | Producción, múltiples usuarios |
| **Bucket Público** | Fácil | Baja | PODs no confidenciales |
| **Archivos Locales** | Muy Fácil | Alta | Pocos archivos, uso local |

---

## 🎯 ¿Qué Opción Elegir?

### Si los PODs son confidenciales:
→ **Service Account** (Opción 1)

### Si los PODs NO son confidenciales:
→ **Bucket Público** (Opción 2)

### Si tienes pocos archivos o quieres probar rápido:
→ **Archivos Locales**

---

## 💡 Mi Recomendación para Ti:

Como tienes MUCHOS PODs en el bucket:

1. **Hacer el bucket público** (más rápido)
2. O **crear service account** (más seguro)
3. Luego usar la opción "☁️ Google Cloud Storage" en la app

---

**¿Cuál prefieres?** Te guío paso a paso. 😊


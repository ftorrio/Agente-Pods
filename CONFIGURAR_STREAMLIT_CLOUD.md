# ☁️ Configurar Streamlit Cloud para Acceso a Google Cloud Storage

Guía paso a paso para que tu demo pueda leer PODs automáticamente desde el bucket.

---

## 🔑 PASO 1: Copiar Credenciales

**Abre el archivo:**
```
C:\Fabian\Cursor\Pods_DAS\config\credentials.json
```

**Copia TODO el contenido** (es un JSON grande)

---

## ⚙️ PASO 2: Ir a Secrets en Streamlit Cloud

1. **Ve a:** https://share.streamlit.io/
2. **Encuentra tu app:** `agentepods`
3. **Haz clic en** el menú **⋮** (3 puntos)
4. **Selecciona** "Settings"
5. **Ve a** la pestaña "**Secrets**"

---

## 📝 PASO 3: Agregar este Contenido

**En el editor de secrets, pega esto:**

```toml
# Credenciales de Google Cloud Storage
[gcp_service_account]
type = "service_account"
project_id = "deasol-prj-sandbox"
private_key_id = "TU_PRIVATE_KEY_ID_AQUI"
private_key = "-----BEGIN PRIVATE KEY-----\nTU_PRIVATE_KEY_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "deasol-prj-sandbox-sa@deasol-prj-sandbox.iam.gserviceaccount.com"
client_id = "TU_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "TU_CLIENT_CERT_URL"
universe_domain = "googleapis.com"

# API Key de Gemini
GEMINI_API_KEY = "AIzaSyC_MX_qKv-gJDFA3Te9BHG8Qv-3B53BFfE"
```

**⚠️ IMPORTANTE:** Reemplaza los valores desde tu `credentials.json` local.

---

## 📋 FORMATO CORRECTO DEL PRIVATE KEY:

El `private_key` debe tener `\n` para saltos de línea:

```toml
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n...\n-----END PRIVATE KEY-----\n"
```

---

## ✅ PASO 4: Guardar y Esperar

1. **Haz clic en** "Save"
2. **Espera 30-60 segundos**
3. **Streamlit reiniciará** la app automáticamente

---

## 🎯 RESULTADO:

**Después de configurar:**

✅ El mensaje "Sin credenciales" desaparecerá  
✅ Verá "✅ Credenciales encontradas"  
✅ Podrá hacer clic en "🔄 Listar PODs por Fecha"  
✅ Descargará PODs del bucket automáticamente  
✅ Procesará y mostrará resultados  

---

## 📊 DEMO LISTA:

**Usuario podrá:**
1. Seleccionar rango de fechas
2. Listar PODs del bucket
3. Procesar (límite: 10 PODs)
4. Ver dashboard completo
5. Explorar resultados

---

## 🎬 FLUJO DE LA DEMO:

```
1. Entra a https://agentepods.streamlit.app
2. Selecciona "☁️ Google Cloud Storage"
3. Ajusta fecha: HOY
4. Límite: 10 archivos
5. Clic "🔄 Listar PODs por Fecha"
6. Clic "▶️ Procesar PODs"
7. Ve resultados en vivo
8. Dashboard + Gráficos + Tabla
```

---

## ⚠️ ALTERNATIVA RÁPIDA:

Si no quieres configurar credenciales ahora:

**Usa el botón "🎬 Ver Demo"** que ya agregué:
- Muestra resultados pre-cargados
- Sin necesidad de credenciales
- Instantáneo
- Perfecto para presentación rápida

---

**¿Quieres configurar las credenciales ahora o usar el modo demo pre-cargado?** 😊


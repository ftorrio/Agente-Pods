# 🔔 Sistema de Notificaciones y Alertas

Guía completa para configurar alertas automáticas de PODs problemáticos.

---

## 🎯 ¿Qué Hace el Sistema de Notificaciones?

Te **alerta automáticamente** cuando:
- 🔴 **URGENTE:** POD con anotación negativa (reclamación)
- ⚠️ **Advertencia:** POD sin acuse de recibo
- ❌ **Error:** POD incompleto o cortado
- 📊 **Resumen:** Procesamiento completado
- ⚡ **Límite:** Demasiados PODs con el mismo problema

---

## 📋 TIPOS DE ALERTAS

### **1. Alerta de Reclamación** 🔴 URGENTE
```
Cuándo: POD tiene anotación negativa
Ejemplo: "Material dañado", "Incompleto"

Mensaje:
  🔴 URGENTE - POD con Reclamación Detectada
  
  POD: QB14620_1023014620.jpg
  Anotación: "Material dañado - favor recoger"
  Sentimiento: NEGATIVO
  
  ACCIÓN REQUERIDA: Revisar inmediatamente
```

---

### **2. Alerta Sin Acuse** ⚠️ ADVERTENCIA
```
Cuándo: POD sin firma, sello ni anotaciones

Mensaje:
  ⚠️ Advertencia - POD Sin Acuse de Recibo
  
  POD: QC8422_1024008422.jpg
  Sin evidencia de recepción
  
  ACCIÓN: Solicitar POD con firma del cliente
```

---

###  **3. Alerta Umbral Superado** 🔴 CRÍTICO
```
Cuándo: Más de 10 PODs sin acuse en un lote

Mensaje:
  🔴 URGENTE - Alerta: 15 PODs Sin Acuse
  
  Se detectaron 15 PODs sin acuse de recibo.
  Esto supera el umbral de 10.
  
  ACCIÓN: Revisar proceso de recepción
```

---

### **4. Resumen de Procesamiento** 📊 INFO
```
Cuándo: Finaliza el procesamiento

Mensaje:
  📊 Resumen - Procesamiento Completado - 50 PODs
  
  Total: 50 PODs
  ✅ Válidos: 35 (70%)
  ❌ Defectos: 15 (30%)
  
  Sin Acuse: 5
  Poco Legible: 8
  Incorrecto: 2
  Reclamaciones: 1
```

---

## ⚙️ CONFIGURACIÓN

### **Archivo:** `config/notifications.json`

```json
{
  "enabled": true,
  "email": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "validador@tuempresa.com",
    "sender_password": "tu-contraseña-app",
    "recipients": [
      "supervisor@tuempresa.com",
      "gerente@tuempresa.com"
    ]
  },
  "alerts": {
    "negative_annotations": true,
    "sin_acuse_threshold": 10,
    "poco_legible_threshold": 20,
    "incorrecto_threshold": 15,
    "processing_complete": true
  }
}
```

---

## 📧 CONFIGURAR EMAIL

### **Paso 1: Usar Gmail** (Recomendado)

1. **Activa verificación en 2 pasos:**
   - Ve a: https://myaccount.google.com/security
   - Activa verificación en 2 pasos

2. **Crea contraseña de aplicación:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona: "Correo" y "Otro"
   - Nombre: "Sistema PODs"
   - **Copia la contraseña** generada (16 caracteres)

3. **Configura en** `notifications.json`:
```json
"email": {
  "enabled": true,
  "sender_email": "tu-email@gmail.com",
  "sender_password": "xxxx xxxx xxxx xxxx",
  "recipients": ["destino@email.com"]
}
```

---

### **Paso 2: Usar Outlook/Office365**

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp-mail.outlook.com",
  "smtp_port": 587,
  "sender_email": "tu-email@outlook.com",
  "sender_password": "tu-contraseña"
}
```

---

### **Paso 3: Servidor SMTP Personalizado**

```json
"email": {
  "enabled": true,
  "smtp_server": "mail.tuempresa.com",
  "smtp_port": 587,
  "sender_email": "pods@tuempresa.com",
  "sender_password": "contraseña"
}
```

---

## 🎛️ AJUSTAR UMBRALES

### **Umbrales de Alerta:**

```json
"alerts": {
  "sin_acuse_threshold": 10,    ← Si hay 10+ sin acuse → Alerta
  "poco_legible_threshold": 20, ← Si hay 20+ poco legibles → Alerta
  "incorrecto_threshold": 15    ← Si hay 15+ incorrectos → Alerta
}
```

**Recomendaciones:**
- **Pocos PODs diarios (10-50):** Umbrales bajos (5, 10, 8)
- **Muchos PODs diarios (100+):** Umbrales altos (20, 30, 25)

---

## 🔔 CANALES DE NOTIFICACIÓN

### **Actualmente Implementados:**
✅ **Log en consola** (siempre activo)  
✅ **Archivo JSON** (`resultados/alertas.json`)  
✅ **Email** (configurable)  
✅ **Dashboard web** (próximamente)  

### **Futuros (fáciles de agregar):**
- Slack
- Microsoft Teams
- WhatsApp Business
- Telegram
- SMS
- Push notifications

---

## 💡 EJEMPLOS DE USO

### **Caso 1: Supervisor de Calidad**
```json
"recipients": ["supervisor.calidad@empresa.com"],
"alerts": {
  "negative_annotations": true,
  "sin_acuse_threshold": 5
}
```
**Resultado:** Solo recibe alertas críticas (reclamaciones, muchos sin acuse)

---

### **Caso 2: Equipo Completo**
```json
"recipients": [
  "gerente@empresa.com",
  "supervisor@empresa.com",
  "validador@empresa.com"
],
"processing_complete": true
```
**Resultado:** Todo el equipo recibe resumen diario

---

### **Caso 3: Solo Críticos**
```json
"alerts": {
  "negative_annotations": true,
  "sin_acuse_threshold": 999,
  "processing_complete": false
}
```
**Resultado:** Solo alertas de reclamaciones (lo más urgente)

---

## 📊 DASHBOARD DE ALERTAS

En la interfaz web verás:

```
╔════════════════════════════════════╗
║ 🔔 ALERTAS ACTIVAS                 ║
╠════════════════════════════════════╣
║ 🔴 URGENTE (2)                     ║
║  - QB14620: Reclamación            ║
║  - QB15089: Reclamación            ║
║                                    ║
║ ⚠️ ADVERTENCIA (5)                 ║
║  - QC8422: Sin acuse               ║
║  - QC8423: Sin acuse               ║
║  ... 3 más                         ║
║                                    ║
║ [Ver Todas] [Limpiar]             ║
╚════════════════════════════════════╝
```

---

## 🚀 ACTIVAR NOTIFICACIONES

### **Paso 1: Editar configuración**
```
Abre: config/notifications.json
Cambia: "enabled": true
```

### **Paso 2: Configurar email (opcional)**
```
Sigue instrucciones de arriba
O déjalo en false para solo logs
```

### **Paso 3: Reiniciar aplicación**
```
run_web.bat
```

### **Paso 4: ¡Listo!**
Procesa PODs y recibe alertas automáticamente

---

## ✅ BENEFICIOS

✅ **Respuesta rápida** a reclamaciones  
✅ **Prevención** de problemas mayores  
✅ **Visibilidad** de tendencias  
✅ **Automatización** total  
✅ **Sin intervención** manual  
✅ **Historial** de alertas  

---

## 📝 REGISTRO DE ALERTAS

Todas las alertas se guardan en:
```
resultados/alertas.json
resultados/reportes/alertas_FECHA.txt
```

Puedes revisarlas en cualquier momento.

---

**¡Sistema de Notificaciones Implementado!** 🔔✨

**Para activar:** Edita `config/notifications.json` y pon `"enabled": true`



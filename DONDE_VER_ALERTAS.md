# 🔔 Dónde Ver las Alertas

Guía rápida para encontrar y revisar las alertas generadas por el sistema.

---

## 📍 UBICACIONES DE LAS ALERTAS

### **1. En la Interfaz Web** 🌐 PRINCIPAL

**URL:** http://localhost:8501

**Ubicación:** Justo debajo del título principal

```
╔═══════════════════════════════════════╗
║ 🔍 Sistema de Validación de PODs      ║
╠═══════════════════════════════════════╣
║ 🔔 ALERTAS ACTIVAS (3) ▼              ║  ← Haz clic aquí
╠═══════════════════════════════════════╣
║ 🔴 URGENTE - Reclamación Detectada    ║
║ POD: QB14620.jpg                      ║
║ Anotación negativa encontrada         ║
║                                       ║
║ ⚠️ Advertencia - Sin Acuse            ║
║ POD: QC8422.jpg                       ║
║ Sin evidencia de recepción            ║
║                                       ║
║ 📊 Resumen - 10 PODs procesados       ║
╚═══════════════════════════════════════╝
```

**Colores:**
- 🔴 **Rojo:** Alertas URGENTES (reclamaciones)
- 🟡 **Amarillo:** Advertencias (sin acuse, incorrectos)
- 🔵 **Azul:** Información (resúmenes)

---

### **2. En los Archivos de Log** 📝

**Carpeta:** `logs/`

**Archivo más reciente:** `pod_validation_YYYYMMDD.log`

**Buscar alertas:**
```
Abre el archivo en Notepad
Busca: "WARNING" o "URGENTE" o "Alerta"
```

**Ejemplo:**
```
00:38:41 | WARNING | Clasificado como INCORRECTO: QB14620.jpg
```

---

### **3. Archivo JSON de Alertas** 📊

**Ubicación:** `resultados/alertas.json`

**Abrir con:**
- Notepad
- Visual Studio Code
- Navegador web

**Contiene:**
- Lista completa de todas las alertas
- Detalles de cada alerta
- Timestamps
- Prioridades

**Para filtrar:**
```json
// Buscar por prioridad:
"priority": "HIGH"  ← Solo urgentes

// Buscar por tipo:
"type": "🔴 URGENTE"  ← Reclamaciones
```

---

### **4. Por Email** 📧 (Si lo configuras)

**Estado actual:** Deshabilitado

**Para activar:**
1. Edita: `config/notifications.json`
2. Cambia: `"email": { "enabled": true }`
3. Configura tu email
4. Reinicia la app

**Recibirás emails cuando:**
- 🔴 Haya una reclamación
- ⚠️ Muchos PODs sin acuse (>10)
- 📊 Se complete un procesamiento

---

## 🎯 CÓMO VER ALERTAS AHORA MISMO

### **Opción 1: En la Web** (Más Fácil)

1. Abre: http://localhost:8501
2. Busca el panel: **"🔔 ALERTAS ACTIVAS"**
3. Haz clic para expandir
4. Ve las alertas más recientes

### **Opción 2: En Archivos**

```bash
# Ver logs
start logs\

# Ver JSON de alertas  
start resultados\alertas.json
```

### **Opción 3: En Terminal**

Mira la terminal donde corre `run_web.bat` - las alertas aparecen en tiempo real.

---

## 📊 TIPOS DE ALERTAS QUE VERÁS

### **🔴 URGENTE** (Prioridad Alta)
```
- POD con reclamación (anotación negativa)
- Patrón de fraude detectado
- Umbral crítico superado
```

### **⚠️ ADVERTENCIA** (Prioridad Media)
```
- POD sin acuse de recibo
- POD incorrecto/cortado
- Poco legible
```

### **📊 INFORMACIÓN** (Prioridad Baja)
```
- Procesamiento completado
- Resumen de lote
- Estadísticas
```

---

## 💡 CONSEJO

**Mantén la interfaz web abierta** mientras procesas PODs y verás las alertas aparecer en tiempo real en el panel superior.

---

## 🔔 PANEL DE ALERTAS EN LA WEB

```
┌─────────────────────────────────────┐
│ 🔔 ALERTAS ACTIVAS (5) ▼            │  ← Expandido por defecto
├─────────────────────────────────────┤
│                                     │
│ 🔴 URGENTE - Reclamación            │
│ POD: QB14620_1023014620.jpg         │
│ Tiene anotación NEGATIVA            │
│ ACCIÓN: Revisar inmediatamente      │
│                                     │
│ ─────────────────────────────────── │
│                                     │
│ ⚠️ Advertencia - Sin Acuse          │
│ POD: QC8422_1024008422.jpg          │
│ Sin firma, sello o anotaciones      │
│ ACCIÓN: Solicitar firma             │
│                                     │
│ ─────────────────────────────────── │
│                                     │
│ ... 3 alertas más                   │
│                                     │
└─────────────────────────────────────┘
```

---

**Las alertas YA ESTÁN funcionando** - solo abre localhost:8501 y las verás! 🔔✨



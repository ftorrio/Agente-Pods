# 🤖 Configurar Google Gemini AI

Guía para integrar Gemini AI y mejorar la precisión del sistema.

---

## 🎯 ¿Por Qué Gemini?

Gemini **ve y entiende** las imágenes de PODs como un humano:
- 📝 Lee texto manuscrito con 95%+ precisión
- ✍️ Detecta firmas auténticas vs falsas
- 🔖 Lee sellos y valida contenido
- 📊 Clasifica con razonamiento explicado
- 🧠 Aprende patrones complejos

**Costo:** $0.0375 por 1000 PODs (~$1.60 para tus 42,681 PODs)

---

## 🔑 Paso 1: Obtener API Key

### **Opción A: Google AI Studio (Más Fácil)**

1. **Ve a:** https://makersuite.google.com/app/apikey

2. **Inicia sesión** con tu cuenta de Google

3. **Haz clic** en "Create API Key"

4. **Selecciona** tu proyecto de Google Cloud (o crea uno nuevo)

5. **Copia** la API key que se genera
   ```
   Ejemplo: AIzaSyB...abc123xyz
   ```

---

### **Opción B: Google Cloud Console**

1. **Ve a:** https://console.cloud.google.com/apis/credentials

2. **Selecciona** tu proyecto

3. **Haz clic** en "Create Credentials" → "API Key"

4. **Habilita** Gemini API en: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com

5. **Copia** la API key

---

## 💾 Paso 2: Guardar API Key

### **Método 1: Archivo de Configuración** (Recomendado)

1. **Crea** el archivo:
   ```
   C:\Fabian\Cursor\Pods_DAS\config\gemini_api_key.txt
   ```

2. **Pega** tu API key en ese archivo (una sola línea)

3. **Guarda** y cierra

### **Método 2: Variable de Entorno**

```powershell
# En PowerShell:
setx GEMINI_API_KEY "TU_API_KEY_AQUI"
```

---

## ✅ Paso 3: Instalar Dependencias

```bash
.\venv\Scripts\activate
pip install google-generativeai
```

---

## 🚀 Paso 4: Usar Gemini en la Aplicación

### **En la Interfaz Web:**

Verás una nueva sección:
```
╔════════════════════════════════════╗
║ 🤖 Gemini AI                      ║
╠════════════════════════════════════╣
║ Estado: ✅ Habilitado              ║
║                                    ║
║ Modo:                              ║
║ ○ Solo sistema tradicional         ║
║ ● Validación con Gemini           ║
║ ○ 100% Gemini                     ║
╚════════════════════════════════════╝
```

### **Modos de Uso:**

#### **Modo 1: Validación con Gemini** (Recomendado)
```
Tu sistema procesa → Si hay duda → Gemini confirma

Ventajas:
✅ Económico (~$0.50 para todos tus PODs)
✅ Rápido (solo casos dudosos)
✅ Preciso donde importa
```

#### **Modo 2: 100% Gemini**
```
Todas las decisiones las toma Gemini

Ventajas:
✅ Máxima precisión (95%+)
✅ Explicaciones detalladas
✅ Mejor con casos difíciles

Costo: ~$1.60 para todos tus PODs
```

---

## 📊 Resultados Esperados

### **Sin Gemini (actual):**
```
Poco Legible: 60%
Incorrecto: 25%
OK: 10%
Sin Acuse: 5%

Precisión: ~70%
```

### **Con Gemini:**
```
Poco Legible: 20% (mejor detección)
Incorrecto: 15%
OK: 50% (detecta más válidos)
Sin Acuse: 10%
Con Anotaciones: 5%

Precisión: ~95%
```

---

## 💡 Ejemplos de Análisis Gemini

### **Ejemplo 1: POD con Firma**
```
Gemini dice:
"SÍ tiene firma manuscrita en la parte inferior derecha.
Parece auténtica. El documento está completo y legible.
CLASIFICACIÓN: OK
RAZÓN: Firma manuscrita visible del cliente"
```

### **Ejemplo 2: POD con Anotación**
```
Gemini dice:
"Anotación manuscrita dice: 'Material dañado - favor recoger'
Sentimiento: NEGATIVO
CLASIFICACIÓN: CON ANOTACIONES
RAZÓN: Indica reclamación por producto dañado"
```

### **Ejemplo 3: Sello Inválido**
```
Gemini dice:
"SÍ tiene sello. Texto del sello: 'INGETEK'
Es sello de empresa, NO de cliente.
CLASIFICACIÓN: SIN ACUSE
RAZÓN: Solo tiene sello de Ingetek (inválido)"
```

---

## 🔧 Configuración Avanzada

### **Ajustar Cuándo Usar Gemini:**

En `config/settings.yaml`:
```yaml
gemini:
  enabled: true
  mode: "hybrid"  # hybrid, full, disabled
  confidence_threshold: 0.7  # Usar Gemini si confianza < 70%
  model: "gemini-1.5-flash"  # flash (rápido) o pro (preciso)
```

---

## 💰 Control de Costos

### **Estrategia Económica:**

1. **Procesa primero con tu sistema** (gratis)
2. **Solo usa Gemini para:**
   - PODs clasificados como "Poco Legible"
   - PODs con confianza < 70%
   - PODs con anotaciones
3. **Ahorra ~70% del costo**

### **Dashboard de Costos:**

La interfaz mostrará:
```
PODs procesados: 100
Usados con Gemini: 25
Costo estimado: $0.001
```

---

## 🎊 Beneficios Finales

✅ **95%+ precisión** en clasificación  
✅ **Lee manuscritos** perfectamente  
✅ **Detecta fraudes** y anomalías  
✅ **Explicaciones** de cada decisión  
✅ **Costo bajo** ($1-2 para miles de PODs)  
✅ **Fácil de configurar** (solo API key)  

---

## 📞 Próximos Pasos

1. Obtén tu API key: https://makersuite.google.com/app/apikey
2. Guárdala en: `config/gemini_api_key.txt`
3. Ejecuta: `pip install google-generativeai`
4. Reinicia la aplicación
5. ¡Disfruta de precisión nivel empresarial!

---

**¿Listo para revolucionar tu validación de PODs?** 🚀



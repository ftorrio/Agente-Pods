# 🔎 Búsqueda Rápida de PODs en la Nube

## 🎯 ¿QUÉ ES?

Una herramienta para **buscar y evaluar PODs específicos** directamente desde Google Cloud Storage sin necesidad de listar por fechas.

---

## ✨ CARACTERÍSTICAS

### **1. Búsqueda Simple**
```
Buscar: QC8261
Resultado: Encuentra todos los PODs que contengan "QC8261"
```

### **2. Búsqueda Múltiple**
```
Buscar: QC8261, QM2015, QP7957
Resultado: Encuentra PODs que coincidan con cualquiera de estos términos
```

### **3. Búsqueda por Números**
```
Buscar: 1024008261
Resultado: Encuentra PODs con ese número de factura/pedido
```

### **4. Procesamiento Automático**
```
✅ Procesar automáticamente
Resultado: Busca, descarga y evalúa los PODs inmediatamente
```

---

## 📍 UBICACIÓN

### **En la Aplicación Web:**
```
Sidebar → Google Cloud Storage → 🔎 Búsqueda Rápida
```

### **Pantalla:**
```
┌─────────────────────────────────┐
│ ☁️ Google Cloud Storage         │
│ ✅ Credenciales encontradas     │
│                                 │
│ 🔎 Búsqueda Rápida              │
│ Buscar POD(s): [____________]   │
│ [🔍 Buscar] [▶️ Auto-procesar] │
└─────────────────────────────────┘
```

---

## 🚀 CÓMO USAR

### **Caso 1: Buscar UN POD Específico**

**Escenario:** Te preguntan por el POD QC8261

**Pasos:**
1. Ve a la app: https://agentepods.streamlit.app
2. Sidebar → Google Cloud Storage
3. En "Buscar POD(s)" escribe: `QC8261`
4. Haz clic en **🔍 Buscar**
5. Verás los resultados:
   ```
   ✅ Encontrados 1 POD(s)
   📋 PODs encontrados:
       1. QC8261_1024008261.jpg
   ```
6. Haz clic en **▶️ Procesar PODs** (abajo)
7. Espera el resultado

---

### **Caso 2: Buscar VARIOS PODs**

**Escenario:** Te preguntan por 3 PODs: QC8261, QM2015, QP7957

**Pasos:**
1. En "Buscar POD(s)" escribe: `QC8261, QM2015, QP7957`
2. Haz clic en **🔍 Buscar**
3. Verás:
   ```
   ✅ Encontrados 3 POD(s)
   📋 PODs encontrados:
       1. QC8261_1024008261.jpg
       2. QM2015_1033002015.jpg
       3. QP7957_1036007957.jpg
   ```
4. Haz clic en **▶️ Procesar PODs**
5. Verás el dashboard con los 3 PODs evaluados

---

### **Caso 3: Búsqueda con Procesamiento Automático**

**Escenario:** Necesitas resultados INMEDIATOS

**Pasos:**
1. Escribe el POD: `QC8261`
2. ✅ **Marca "▶️ Procesar automáticamente"**
3. Haz clic en **🔍 Buscar**
4. **Automáticamente:**
   - Busca el POD
   - Lo descarga
   - Lo evalúa
   - Muestra resultados
5. Sin necesidad de hacer más clics

---

### **Caso 4: Búsqueda por Número de Factura**

**Escenario:** Te preguntan por la factura 1024008261

**Pasos:**
1. Escribe: `1024008261`
2. Haz clic en **🔍 Buscar**
3. Encontrará: `QC8261_1024008261.jpg`
4. Procesa normalmente

---

## 💡 EJEMPLOS DE BÚSQUEDA

### **Búsquedas Válidas:**
```
✅ QC8261                     # Por código de POD
✅ 1024008261                 # Por número
✅ QC8261, QM2015             # Múltiples PODs
✅ QC82                       # Coincidencia parcial
✅ _103                       # Por patrón en el nombre
```

### **Sugerencias:**
```
💡 Si no sabes el nombre completo, usa parte del código
💡 Separa múltiples búsquedas con coma
💡 No distingue mayúsculas/minúsculas
💡 Busca en el nombre completo del archivo
```

---

## 📊 RESULTADOS

### **Si ENCUENTRA PODs:**
```
✅ Encontrados 3 POD(s) que coinciden
📋 PODs encontrados (expandible):
    1. QC8261_1024008261.jpg
    2. QM2015_1033002015.jpg
    3. QP7957_1036007957.jpg

✅ PODs listos para procesar
```

### **Si NO ENCUENTRA:**
```
❌ No se encontraron PODs con: QC9999
💡 Buscando en carpeta: pod/IES161108I36/
💡 Verifica el nombre o intenta con menos caracteres

📁 La carpeta contiene 42,681 archivos en total
Ver ejemplos de nombres en la carpeta (expandible)
```

---

## ⚙️ CONFIGURACIÓN

### **Carpeta de Búsqueda:**
```
Por defecto: IES161108I36
Puedes cambiarla en: "📁 Carpeta/Prefijo"
```

### **Límite de Resultados:**
```
Máximo: 20 PODs por búsqueda
Si encuentra más: Se procesan los primeros 20
```

---

## 🎯 VENTAJAS vs LISTAR POR FECHA

| Aspecto | Listar por Fecha | Búsqueda Rápida |
|---------|------------------|-----------------|
| **Velocidad** | ⏳ Lento (miles) | ⚡ Rápido |
| **Precisión** | 📅 Por rango | 🎯 Exacto |
| **Uso típico** | Múltiples PODs | PODs específicos |
| **Resultado** | Lista grande | Solo lo buscado |
| **Cuando usar** | Reportes diarios | Consultas puntuales |

---

## 📝 CASOS DE USO REALES

### **1. Cliente llama preguntando por SU POD:**
```
Cliente: "¿Cómo está mi POD QC8261?"
Tú:
   1. Buscas: QC8261
   2. Procesas
   3. Respondes en 30 segundos
```

### **2. Auditoría de facturas específicas:**
```
Auditor: "Necesito ver PODs: 1024008261, 1033002015, 1036007957"
Tú:
   1. Buscas: 1024008261, 1033002015, 1036007957
   2. Procesas los 3
   3. Generas reporte
```

### **3. Verificación de PODs problemáticos:**
```
Sistema alertó: "POD QM2015 con reclamación"
Tú:
   1. Buscas: QM2015
   2. ✅ Procesar automáticamente
   3. Ves imagen y detalles
   4. Tomas acción
```

---

## 🔧 TROUBLESHOOTING

### **No encuentra nada:**
```
1. Verifica que la carpeta sea correcta (IES161108I36)
2. Verifica ortografía del código
3. Intenta con menos caracteres (QC82 en lugar de QC8261)
4. Revisa los ejemplos mostrados en el expander
```

### **Encuentra demasiados:**
```
1. Sé más específico (QC8261 en lugar de QC)
2. El sistema procesará solo los primeros 20
3. Puedes buscar menos a la vez
```

### **No se descarga:**
```
1. Verifica credenciales (debe decir ✅ Credenciales encontradas)
2. Verifica conexión a internet
3. Intenta de nuevo
```

---

## 🌐 DISPONIBLE EN:

### **Streamlit Cloud:**
```
https://agentepods.streamlit.app
```
Disponible en 1-2 minutos después del update.

### **Local:**
```bash
streamlit run src/web_app.py
```
Disponible inmediatamente.

---

## 📊 FLUJO COMPLETO

```
┌─────────────────────────────────────┐
│ 1️⃣ Usuario ingresa código(s)        │
│    "QC8261, QM2015"                 │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 2️⃣ Sistema busca en Google Cloud   │
│    Búsqueda en 42,681 archivos      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 3️⃣ Filtra coincidencias             │
│    Encuentra: 2 PODs                │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 4️⃣ Muestra resultados               │
│    Lista expandible de PODs         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 5️⃣ Usuario hace clic "Procesar"    │
│    O automático si está activado    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 6️⃣ Descarga y Evalúa PODs          │
│    Análisis completo con IA         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 7️⃣ Dashboard con Resultados        │
│    Métricas, alertas, imágenes      │
└─────────────────────────────────────┘
```

---

## ✅ CHECKLIST DE USO

- [ ] Estás en Google Cloud Storage (no archivos locales)
- [ ] Ves "✅ Credenciales encontradas"
- [ ] Conoces el código/número del POD
- [ ] Ingresas el código en "Buscar POD(s)"
- [ ] Separas múltiples códigos con coma
- [ ] Haces clic en 🔍 Buscar
- [ ] Ves los PODs encontrados
- [ ] Haces clic en ▶️ Procesar PODs
- [ ] Esperas resultados (30-60 seg)
- [ ] Revisas dashboard y alertas

---

**🎉 AHORA PUEDES BUSCAR Y EVALUAR PODs ESPECÍFICOS EN SEGUNDOS! 🎉**

**Actualización disponible en Streamlit Cloud en 1-2 minutos.**


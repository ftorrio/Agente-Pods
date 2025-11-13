# 📄 Sistema de Facturas con PODs

## 🎯 Descripción

Página web que consulta facturas desde BigQuery y proporciona acceso directo a los documentos POD almacenados en Google Cloud Storage.

---

## 🚀 Cómo Ejecutar

### **Opción 1: Local**
```bash
run_facturas.bat
```

**URL:** http://localhost:8502

### **Opción 2: Desde menú principal**
```bash
run_web.bat
```
Luego seleccionar "Facturas con PODs" en el menú

---

## 📋 Funcionalidades

### **1. Consulta de Facturas**
- Facturas directas
- Facturas de estimación/remisión
- Filtros por fecha, cliente, proyecto
- Datos desde BigQuery

### **2. Links a PODs**
- Cada factura con link directo a su POD
- PODs almacenados en Google Cloud Storage
- Click para ver/descargar documento

### **3. Métricas**
- Total de facturas
- Importe total
- Kilos totales
- % de facturas con POD

### **4. Exportación**
- Descargar resultados en CSV/Excel
- Incluye todos los campos
- Con URLs de PODs

---

## 🔗 Estructura de URLs

**Base:** `https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/`

**Ejemplo:**
```
NombreEnUbicacion: QC8261_1024008261.jpg
URL completa: https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/QC8261_1024008261.jpg
```

---

## 📊 Campos Mostrados

- Fecha de factura
- Número de factura
- Cliente
- Proyecto
- Tipo (Directa/Estimación)
- Importe
- Kilos
- Estatus (Timbrada/Cancelada/etc)
- **Link al POD** ⭐

---

## ⚙️ Configuración

### **Credenciales de BigQuery:**

**Local:**
- Archivo: `config/credentials.json`

**Streamlit Cloud:**
- Settings → Secrets → `gcp_service_account`

---

## 🎯 Casos de Uso

### **1. Auditoría de Facturas**
```
1. Consultar facturas del mes
2. Filtrar por cliente específico
3. Revisar que todas tengan POD
4. Click en PODs para verificar documentos
```

### **2. Validación de Entregas**
```
1. Buscar factura específica
2. Abrir POD asociado
3. Verificar firma y datos
4. Confirmar entrega
```

### **3. Reportes Ejecutivos**
```
1. Consultar rango de fechas
2. Ver métricas agregadas
3. Descargar CSV para análisis
4. Compartir con gerencia
```

---

## 🔧 Requisitos

- Python 3.10+
- Credenciales de Google Cloud
- Acceso a BigQuery
- Acceso a Google Cloud Storage

---

## 📚 Archivos

```
src/facturas_pods.py     → Aplicación principal
run_facturas.bat         → Script de ejecución
FACTURAS_CON_PODS.md     → Esta documentación
```

---

**🎉 Acceso directo a PODs desde facturas 🎉**


# 🎨 Agregar Logo de Ingetek

## ✅ YA ESTÁ CONFIGURADO

El sistema ya está preparado para mostrar el logo de Ingetek en la **parte superior izquierda** de la aplicación.

---

## 📁 PASO 1: Coloca tu logo

**Copia el archivo del logo aquí:**
```
assets/logo_ingetek.png
```

**Requisitos del archivo:**
- **Nombre:** `logo_ingetek.png` (o `.jpg`)
- **Tamaño recomendado:** 200 x 60 píxeles (ancho x alto)
- **Formato:** PNG con fondo transparente (mejor) o JPG
- **Peso:** Menor a 500 KB

---

## 🌐 PASO 2: Sube a GitHub

```bash
git add assets/logo_ingetek.png
git commit -m "Agregar logo de Ingetek"
git push
```

**Automáticamente:**
- Se verá en tu PC (local)
- Se verá en Streamlit Cloud
- Aparecerá en https://agentepods.streamlit.app

---

## 👁️ CÓMO SE VE:

### **Si TIENES el logo:**
```
┌─────────────────────────────────────┐
│ [🏢 LOGO INGETEK]                   │
│                                     │
│ 🔍 Sistema de Validación de PODs    │
└─────────────────────────────────────┘
```

### **Si NO TIENES el logo (temporal):**
```
┌─────────────────────────────────────┐
│ INGETEK                             │
│ Proof of Delivery System            │
│                                     │
│ 🔍 Sistema de Validación de PODs    │
└─────────────────────────────────────┘
```

---

## 🔗 Características

- ✅ Logo se muestra en la parte superior izquierda
- ✅ Es un enlace a www.ingetek.com (al hacer clic)
- ✅ Se adapta a tema claro/oscuro
- ✅ Funciona local y en la nube

---

## 📍 ¿DÓNDE CONSEGUIR EL LOGO?

1. **Tu departamento de marketing**
2. **Sitio web:** www.ingetek.com
3. **Diseñador gráfico de Ingetek**

---

## 🚀 PARA VER LOS CAMBIOS:

### **Local (tu PC):**
```bash
streamlit run src/web_app.py
```

### **Streamlit Cloud:**
Espera 1-2 minutos después de hacer `git push`

---

## ❓ SI TIENES PROBLEMAS:

1. **Verifica el nombre:** Debe ser exactamente `logo_ingetek.png`
2. **Verifica la carpeta:** Debe estar en `assets/`
3. **Verifica el formato:** PNG o JPG
4. **Reinicia Streamlit:** Ctrl+C y volver a ejecutar

---

## 📧 NECESITAS EL LOGO?

Si no tienes el archivo del logo:
1. Contacta al área de marketing de Ingetek
2. O envíame el logo y lo optimizo para la aplicación

---

Por ahora, se mostrará **"INGETEK"** como texto hasta que agregues el logo oficial. 😊


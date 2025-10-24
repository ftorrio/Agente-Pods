# 🚀 Deploy en Streamlit Cloud

Guía para desplegar el Sistema de Validación de PODs en Streamlit Cloud.

---

## 📋 PASOS PARA DEPLOY:

### **1. Crear Repositorio en GitHub**

1. Ve a: https://github.com/new
2. Nombre: `pods-validation-system`
3. Descripción: `Sistema de validación de PODs con IA`
4. Público o Privado (tu eliges)
5. **NO inicializar** con README (ya tienes uno)
6. Crear repositorio

---

### **2. Conectar y Subir**

En tu terminal (aquí mismo):

```bash
git remote add origin https://github.com/TU_USUARIO/pods-validation-system.git
git branch -M main
git push -u origin main
```

Reemplaza `TU_USUARIO` con tu usuario de GitHub.

---

### **3. Deploy en Streamlit Cloud**

1. Ve a: https://share.streamlit.io/
2. Haz clic en "New app"
3. Conecta tu cuenta de GitHub
4. Selecciona:
   - **Repository:** `pods-validation-system`
   - **Branch:** `main`
   - **Main file:** `src/web_app.py`
5. **Advanced settings** → Agregar secretos:

```
GEMINI_API_KEY = "tu-api-key-aqui"
```

6. Haz clic en "Deploy!"

---

### **4. Configurar Secretos**

En Streamlit Cloud, agrega estos secretos:

```toml
# En secrets.toml de Streamlit Cloud:

[google_cloud]
credentials = '''
{
  "type": "service_account",
  "project_id": "...",
  ...
}
'''

[gemini]
api_key = "AIzaSy..."
```

---

## ⚠️ IMPORTANTE:

### **Archivos que NO se suben (por seguridad):**
- ❌ `config/credentials.json` (Google Cloud)
- ❌ `config/gemini_api_key.txt` (Gemini)
- ❌ `database/pods.db` (base de datos local)

**Estos se configuran como SECRETOS en Streamlit Cloud**

---

## 🌐 DESPUÉS DEL DEPLOY:

Tu app estará disponible en:
```
https://tu-usuario-pods-validation.streamlit.app
```

**Accesible desde:**
- ✅ Cualquier navegador
- ✅ Cualquier dispositivo
- ✅ Cualquier ubicación
- ✅ Sin necesitar tu PC encendida

---

## 📊 VENTAJAS DEL DEPLOY:

✅ **Acceso 24/7** desde cualquier lugar  
✅ **No requiere tu PC** encendida  
✅ **Múltiples usuarios** simultáneos  
✅ **Actualizaciones** automáticas con git push  
✅ **GRATIS** para proyectos públicos  
✅ **Escalable** automáticamente  

---

## 🔧 ACTUALIZAR LA APP:

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

**Streamlit Cloud** se actualiza automáticamente ✨

---

## 💾 BASE DE DATOS EN LA NUBE:

**Opción A: SQLite en el repositorio** (Básico)
- Funciona pero se reinicia con cada deploy
- Para pruebas está bien

**Opción B: Google Cloud SQL** (Producción)
- Base de datos permanente en la nube
- Configurar en secrets

**Opción C: Supabase** (Gratis y fácil)
- Base de datos PostgreSQL gratis
- Fácil integración

---

## 🎯 URL FINAL:

Después del deploy, comparte:
```
https://pods-validation.streamlit.app
```

Y cualquiera con el link puede validar PODs! 🎉

---

**¡Tu sistema disponible para todo el mundo!** 🌍✨


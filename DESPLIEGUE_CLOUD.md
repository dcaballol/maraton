# 🚀 GUÍA PASO A PASO - DESPLIEGUE EN STREAMLIT CLOUD

## ⏱️ Tiempo Total: 10-15 minutos

---

## 📋 ANTES DE EMPEZAR

### ✅ Requisitos:
- [ ] Cuenta de email (Gmail recomendado)
- [ ] Computadora con internet
- [ ] Carpeta `marathon_app` descargada

### 🎯 Resultado Final:
- URL permanente tipo: `https://marathon-tracker-XXXXX.streamlit.app`
- Accesible desde iPhone, iPad, Mac, PC
- 100% GRATIS, sin tarjeta de crédito

---

## 🪜 PASO 1: CREAR CUENTA EN GITHUB (5 minutos)

### Si ya tienes cuenta de GitHub → Saltar al PASO 2

### Si NO tienes cuenta:

**1.1** Ve a: https://github.com

**1.2** Click en **"Sign up"** (esquina superior derecha)

**1.3** Completa el formulario:
```
Email: tu_email@gmail.com
Password: (mínimo 15 caracteres, incluir números)
Username: elige un nombre (ejemplo: maria-runner)
```

**1.4** Verifica tu email:
- GitHub te enviará un código
- Revisa tu bandeja de entrada
- Ingresa el código de 6 dígitos

**1.5** Completa la encuesta (opcional - puedes hacer click en Skip)

**1.6** ¡Listo! Ya tienes cuenta de GitHub ✅

---

## 📤 PASO 2: SUBIR LA APP A GITHUB (5 minutos)

### Opción A: Desde la Interfaz Web (MÁS FÁCIL - RECOMENDADO)

**2.1** Inicia sesión en GitHub: https://github.com/login

**2.2** Click en el botón **"+"** (esquina superior derecha)

**2.3** Selecciona **"New repository"**

**2.4** Completa el formulario:
```
Repository name: marathon-tracker
Description: Aplicación de entrenamiento para maratón
Public/Private: Selecciona "Public" ⭐
```

**IMPORTANTE:** NO marcar ninguna opción de "Initialize this repository with..."

**2.5** Click en **"Create repository"**

**2.6** En la página que aparece, busca la sección:
**"…or create a new repository on the command line"**

Verás algo como:
```bash
echo "# marathon-tracker" >> README.md
git init
git add README.md
...
```

**IGNORA ESTO POR AHORA** - Vamos a usar el método visual

**2.7** Click en **"uploading an existing file"** (enlace azul en el texto)

**2.8** Se abrirá una página de carga de archivos

**2.9** PREPARAR TUS ARCHIVOS:

En tu computadora, abre la carpeta `marathon_app` y asegúrate de tener:
```
marathon_app/
├── app.py ✅
├── database.py ✅
├── requirements.txt ✅
├── README.md ✅
├── PROTOCOLO_MAESTRO_COMPLETO.md ✅
├── DESPLIEGUE_CLOUD.md ✅
├── pages/
│   ├── 1_🧮_Calculadoras.py ✅
│   ├── 2_📊_Métricas_Corporales.py ✅
│   └── 3_💾_Respaldo_de_Datos.py ✅
└── (otros archivos opcionales)
```

**2.10** **ARRASTRA Y SUELTA**:
- Selecciona TODOS los archivos de la carpeta `marathon_app`
- Arrástralos a la página de GitHub donde dice:
  **"Drag files here to add them to your repository"**

**IMPORTANTE:** Puedes arrastrar archivos y carpetas juntos

**2.11** Espera a que se suban todos los archivos (verás una barra de progreso)

**2.12** En el campo de texto abajo, escribe:
```
Initial commit - Marathon Training App
```

**2.13** Click en **"Commit changes"** (botón verde)

**2.14** ¡LISTO! Tus archivos están en GitHub ✅

Deberías ver algo como:
```
marathon-tracker
├── app.py
├── database.py
├── requirements.txt
├── pages/
...
```

---

### Opción B: Desde Terminal (AVANZADO)

**Solo si sabes usar git:**

```bash
cd marathon_app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/marathon-tracker.git
git push -u origin main
```

---

## ☁️ PASO 3: DESPLEGAR EN STREAMLIT CLOUD (3 minutos)

**3.1** Ve a: https://share.streamlit.io

**3.2** Click en **"Sign in"**

**3.3** Selecciona **"Continue with GitHub"**

**3.4** Se abrirá una ventana de GitHub:
- Si ya iniciaste sesión en GitHub → Automáticamente te conectará
- Si no → Inicia sesión con tu usuario y contraseña de GitHub

**3.5** GitHub pedirá autorización para Streamlit:
- Click en **"Authorize streamlit"** (botón verde)
- Puede pedir tu contraseña de GitHub nuevamente

**3.6** Te redirigirá a Streamlit Cloud

**3.7** Click en **"New app"** (botón naranja/morado)

**3.8** Completa el formulario:

```
Repository: TU_USUARIO/marathon-tracker
Branch: main
Main file path: app.py
```

**IMPORTANTE:** 
- En "Repository" deberías ver tu repositorio en la lista desplegable
- Si no aparece, click en "Paste GitHub URL" y pega:
  `https://github.com/TU_USUARIO/marathon-tracker`

**3.9** (Opcional) Puedes cambiar el nombre de la app:
```
App URL (optional): marathon-tracker
```

Esto creará: `https://marathon-tracker-XXXXX.streamlit.app`

**3.10** Click en **"Deploy!"** (botón morado)

**3.11** ESPERA 2-3 MINUTOS

Verás una pantalla que dice:
```
🎈 Your app is deploying...
```

Y luego mostrará logs como:
```
[12:34:56] Installing requirements...
[12:35:10] Starting app...
[12:35:30] App is running!
```

**3.12** ¡LISTO! Tu app está en vivo ✅

Aparecerá tu URL permanente:
```
https://TU_USUARIO-marathon-tracker-app-XXXXX.streamlit.app
```

**GUARDA ESTA URL** - Es tu aplicación para siempre

---

## 📱 PASO 4: AGREGAR A IPHONE (2 minutos)

**4.1** Abre Safari en tu iPhone

**4.2** Ve a tu URL de Streamlit

**4.3** Toca el botón **"Compartir"** (cuadrado con flecha)

**4.4** Scroll hacia abajo → **"Agregar a pantalla de inicio"**

**4.5** Cambia el nombre a: **"Marathon Tracker"**

**4.6** Toca **"Agregar"**

**4.7** ¡Ahora tienes un ícono en tu pantalla! 🎉

---

## ✅ VERIFICACIÓN

### Tu app debe mostrar:

```
🏃‍♀️ MARATÓN TRAINING TRACKER
📅 Objetivo: 42.195 km en 5:30 hrs - 26 Abril 2026

🌙 Fase Hormonal de la Semana
🔴 Menstruación D1-5 + Inicio Folicular
...

📊 Navegación
Semana: 1

🌙 Ciclo Menstrual
Día del Ciclo: 1/28
```

Si ves esto → **¡ÉXITO!** ✅

---

## 🔧 ACTUALIZAR LA APP (Futuro)

Cuando quieras cambiar algo:

**Opción 1: Desde GitHub Web**
1. Ve a tu repositorio en GitHub
2. Click en el archivo que quieres editar
3. Click en el ícono de lápiz (Edit)
4. Haz tus cambios
5. Click en "Commit changes"
6. **Automáticamente** Streamlit actualiza la app en 1-2 minutos

**Opción 2: Desde Terminal**
```bash
git add .
git commit -m "Actualización"
git push
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### ❌ "App not loading" o error 500

**Solución:**
1. Ve a https://share.streamlit.io
2. Click en tu app
3. Click en "⋮" (tres puntos)
4. Click en "Reboot app"
5. Espera 1 minuto

### ❌ "ModuleNotFoundError: No module named 'X'"

**Causa:** Falta una dependencia en `requirements.txt`

**Solución:**
1. Ve a tu repositorio en GitHub
2. Abre `requirements.txt`
3. Click en editar (lápiz)
4. Asegúrate de tener:
```
streamlit==1.54.0
plotly==6.5.2
pandas==2.3.3
numpy==2.4.2
```
5. Commit changes
6. Espera 2 minutos que se actualice

### ❌ "Database error" o "No such table"

**Solución:**
La base de datos se crea automáticamente la primera vez.
1. Refresca la página (F5)
2. Espera 30 segundos
3. Debería funcionar

### ❌ No aparece mi repositorio en Streamlit

**Solución:**
1. Asegúrate de que el repo es "Public" en GitHub
2. En Streamlit, click en "Paste GitHub URL"
3. Pega: `https://github.com/TU_USUARIO/marathon-tracker`

### ❌ La app se ve mal o sin estilos

**Solución:**
1. Refresca la página (Cmd+R en Mac, Ctrl+R en Windows)
2. Limpia caché del navegador
3. Prueba en modo incógnito

---

## 💡 TIPS PRO

### 1. Hacer la app privada (opcional)

En Streamlit Cloud:
1. Ve a Settings de tu app
2. "Access" → Selecciona "Restricted"
3. Agrega emails permitidos
4. Solo personas con esos emails pueden acceder

### 2. Cambiar URL personalizada

En Streamlit Cloud:
1. Settings → "General"
2. Cambia "App URL"
3. Guarda

### 3. Ver logs en tiempo real

En Streamlit Cloud:
1. Click en tu app
2. Click en "Manage app"
3. Verás logs en vivo

### 4. Notificaciones de errores

Streamlit te enviará email si la app crashea

---

## 📊 LÍMITES PLAN GRATUITO

| Recurso | Límite |
|---------|--------|
| Apps desplegadas | 1 app (suficiente) |
| Visitantes | Ilimitado ✅ |
| Almacenamiento | 1 GB ✅ |
| Uptime | 99.9% ✅ |
| CPU/RAM | Compartido (suficiente para esta app) |

**¿Necesitas más?** Puedes actualizar a plan pago ($20/mes) pero NO es necesario para esta app.

---

## 🎓 RECURSOS ADICIONALES

### Videos tutoriales:
- YouTube: "How to deploy Streamlit app"
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud

### Documentación oficial:
- https://docs.streamlit.io/streamlit-community-cloud/get-started

### Soporte:
- Foro: https://discuss.streamlit.io
- Discord: https://discord.gg/streamlit

---

## ✅ CHECKLIST FINAL

- [ ] Cuenta de GitHub creada
- [ ] Repositorio `marathon-tracker` creado
- [ ] Archivos subidos a GitHub
- [ ] App desplegada en Streamlit Cloud
- [ ] URL guardada
- [ ] App agregada a iPhone
- [ ] App funciona correctamente
- [ ] Primer entrenamiento registrado

---

## 🎉 ¡FELICIDADES!

Tu app está en vivo y accesible desde cualquier dispositivo.

**Tu URL:** `https://TU_USUARIO-marathon-tracker-XXXXX.streamlit.app`

**Próximos pasos:**
1. Abre la app desde tu iPhone
2. Registra tu primer entrenamiento
3. Comienza tu preparación para el maratón

---

## 📧 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa la sección "Solución de Problemas" arriba
2. Verifica que seguiste todos los pasos
3. Contacta al soporte de Streamlit

---

**¡ÉXITO EN TU DESPLIEGUE!** 🚀

Ahora tienes tu propia app profesional de entrenamiento accesible 24/7 desde cualquier lugar del mundo.

**¡A ENTRENAR!** 🏃‍♀️💪


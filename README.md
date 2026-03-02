# 🏃‍♀️ Marathon Training Tracker

Aplicación web completa para seguimiento de entrenamiento de maratón con integración de ciclo menstrual y protocolo específico para prevención de lesiones de rodilla.

![Python](https://img.shields.io/badge/python-3.12-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.54.0-red)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Características Principales

### 📅 Plan de Entrenamiento de 8 Semanas
- **Objetivo:** Completar 42.195 km en 5:30 hrs (26 Abril 2026)
- **Método Galloway:** Ratio 4:1 (4 min carrera / 1 min caminata)
- **Volumen Total:** 362 km + 16 sesiones de fuerza
- **Estructura:** Domingo = Rodaje largo, Martes/Jueves = Fuerza

### 🔴 Integración Ciclo Menstrual
- Calendario proyectado de 2 ciclos completos
- Ajustes automáticos de carga por fase hormonal
- Indicadores visuales de fase actual
- **Ventanas óptimas:** Aprovechar fase folicular (días 6-14)
- **Prevención:** Descarga obligatoria en lútea tardía (días 22-28)

### 🦵 Protocolo Rodilla Izquierda
- Modificaciones específicas para dolor patelar anterior
- Ejercicios priorizados (Hip Thrust, VMO, Copenhagen Plank)
- Protocolos pre/post entrenamiento obligatorios
- Monitoreo diario de dolor e inflamación

### 💪 Fuerza Adaptada
- Progresión conservadora basada en fase hormonal
- Hip Thrust como ejercicio #1 (protección rodilla)
- Potencia condicional semanas 5-6 (solo si dolor = 0)
- Tapering inteligente semanas 7-8

### 📊 Dashboard Interactivo
- Vista semanal con plan vs realizado
- Gráficos de progreso (KM acumulados, ritmo)
- Indicador de fase menstrual en tiempo real
- Registro rápido de entrenamientos

### 🧮 Calculadoras Integradas
- Ritmo y Tiempo
- Zonas FC (Método Karvonen)
- Nutrición y Macros
- Método Galloway

### 💾 Sistema de Respaldo Dual
- Exportación CSV/JSON
- Importación de datos
- Preparado para Google Sheets (v2.0)

## 🚀 Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/marathon-tracker.git
cd marathon-tracker

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run app.py
```

## ☁️ Despliegue en Streamlit Cloud

Ver guía completa: [DESPLIEGUE_CLOUD.md](DESPLIEGUE_CLOUD.md)

## 📚 Documentación

- **PROTOCOLO_MAESTRO_COMPLETO.md** - Plan completo integrado
- **DESPLIEGUE_CLOUD.md** - Guía de despliegue
- **PLAN_VISUAL_REESTRUCTURADO.html** - Visualización

## 📝 Licencia

MIT License

---

**Objetivo:** 42.195 km en 5:30 hrs | 26 Abril 2026

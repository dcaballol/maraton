import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import database as db

# Exercise video links - UPDATED AND VERIFIED
EXERCISE_VIDEOS = {
    "hip thrust": "https://youtu.be/xDmFkJxPzeM",
    "terminal knee extension": "https://youtu.be/ciKjoG03WaQ",
    "vmo": "https://youtu.be/ciKjoG03WaQ",
    "split squat": "https://youtu.be/2C-uNgKwPLE",
    "sentadilla búlgara": "https://youtu.be/2C-uNgKwPLE",
    "peso muerto rumano": "https://youtu.be/SHsUIZiNdeY",
    "puente glúteo": "https://youtu.be/OUgsJ8-Vi0E",
    "puente": "https://youtu.be/OUgsJ8-Vi0E",
    "plancha": "https://youtu.be/ASdvN_XEl_c",
    "rkc plancha": "https://youtu.be/ASdvN_XEl_c",
    "clamshells": "https://youtu.be/5LaHGgY3b3Q",
    "clamshell": "https://youtu.be/5LaHGgY3b3Q",
    "monster walks": "https://youtu.be/KgdAqQbS4KA",
    "monster walk": "https://youtu.be/KgdAqQbS4KA",
    "fire hydrants": "https://youtu.be/SFICa-nJTEA",
    "fire hydrant": "https://youtu.be/SFICa-nJTEA",
    "step-up": "https://youtu.be/dQqApCGd5Ss",
    "step up": "https://youtu.be/dQqApCGd5Ss",
    "copenhagen plank": "https://youtu.be/hSvG7hDkguY",
    "copenhagen": "https://youtu.be/hSvG7hDkguY",
    "vmo dips": "https://youtu.be/0rZIbC_u3sE",
    "wall sit": "https://youtu.be/0rZIbC_u3sE",
    "dead bug": "https://youtu.be/g_BYB0R-4Ws",
    "bird dog": "https://youtu.be/wiFNA3sqjCA",
    "sentadilla": "https://youtu.be/gcNh17Ckjgg",
    "squat": "https://youtu.be/gcNh17Ckjgg",
    "sentadilla back": "https://youtu.be/gcNh17Ckjgg",
    "sentadilla goblet": "https://youtu.be/MeIiIdhvXT4",
    "nordic": "https://youtu.be/J8ua0gG1PkU",
    "nordic hamstring": "https://youtu.be/J8ua0gG1PkU",
    "nordic curl": "https://youtu.be/J8ua0gG1PkU",
    "pallof": "https://youtu.be/AH_QZLm_0-s",
    "pallof press": "https://youtu.be/AH_QZLm_0-s",
    "foam roller": "https://youtu.be/IqVF0hT4p7Y",
    "foam rolling": "https://youtu.be/IqVF0hT4p7Y",
    "elevación talones": "https://youtu.be/gwLzBJYoWlI",
    "elevación": "https://youtu.be/gwLzBJYoWlI",
    "estocadas": "https://youtu.be/QOVaHwm-Q6U",
    "estocada": "https://youtu.be/QOVaHwm-Q6U",
    "lunge": "https://youtu.be/QOVaHwm-Q6U",
    "side-lying": "https://youtu.be/iPho4VXRHGk",
    "hip abduction": "https://youtu.be/iPho4VXRHGk",
    "pistol squat": "https://youtu.be/vq5-vdgJc0I",
    "pistol": "https://youtu.be/vq5-vdgJc0I",
    "suitcase carry": "https://youtu.be/VguuwOSW3YI",
    "carry": "https://youtu.be/VguuwOSW3YI"
}

def extract_exercises_from_description(description):
    """Extract exercise names from the workout description"""
    exercises = []
    sections = description.split("|")
    
    for section in sections:
        section = section.strip()
        # Look for numbered exercises (1), 2), etc.)
        if section and section[0].isdigit() and ")" in section:
            parts = section.split(")", 1)
            if len(parts) > 1:
                exercise_detail = parts[1].strip()
                # Extract just the exercise name (before the first space or number)
                exercise_name = exercise_detail.split()[0:3]  # First 3 words usually contain the exercise name
                exercise_name = " ".join(exercise_name)
                # Remove special characters and get clean name
                clean_name = exercise_name.split("(")[0].split(" tempo")[0].split(" 4x")[0].split(" 3x")[0].strip()
                exercises.append(clean_name)
    
    return exercises

def format_workout_description(description):
    """Format workout description with better structure and video links"""
    
    # Split by pipe
    sections = description.split("|")
    
    formatted_html = '<div style="line-height: 1.8;">'
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Section headers (PREVIO, Calent, etc.)
        if any(section.upper().startswith(prefix) for prefix in ["PREVIO:", "CALENT:", "CORRECTIVO:", "ENFRIAMIENTO:", "ENFR:", "POST:"]):
            header, content = section.split(":", 1) if ":" in section else (section, "")
            formatted_html += f'<div style="margin-top: 15px;"><strong style="color: #1f4788;">🔹 {header.strip()}</strong><br>{content.strip()}</div>'
        
        # Exercise lines (start with number)
        elif section and section[0].isdigit() and ")" in section:
            # Extract exercise number and details
            parts = section.split(")", 1)
            exercise_num = parts[0].strip()
            exercise_detail = parts[1].strip() if len(parts) > 1 else ""
            
            # Find video link
            video_html = ""
            for exercise_name, video_url in EXERCISE_VIDEOS.items():
                if exercise_name in exercise_detail.lower():
                    video_html = f' <a href="{video_url}" target="_blank" style="color: #ff4b4b; text-decoration: none;">📺 Video</a>'
                    break
            
            formatted_html += f'<div style="margin: 10px 0; padding-left: 10px; border-left: 3px solid #e0e0e0;"><strong>{exercise_num})</strong> {exercise_detail}{video_html}</div>'
        
        # Regular content
        else:
            formatted_html += f'<div style="margin: 8px 0;">{section}</div>'
    
    formatted_html += '</div>'
    
    return formatted_html

# Page config
st.set_page_config(
    page_title="Maratón Training Tracker",
    page_icon="🏃‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f4788;
    }
    .week-badge {
        background-color: #2e5c8a;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
    }
    .intensity-high {
        color: #c00000;
        font-weight: bold;
    }
    .intensity-moderate {
        color: #ffc000;
        font-weight: bold;
    }
    .intensity-low {
        color: #00b050;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
db.init_db()
db.populate_training_plan()

# Title
st.markdown('<div class="main-header">🏃‍♀️ MARATÓN TRAINING TRACKER</div>', unsafe_allow_html=True)
st.markdown("### 📅 Objetivo: 42.195 km en 5:30 hrs - 26 Abril 2026")

# Sidebar - Week selector
st.sidebar.title("📊 Navegación")
current_week = st.sidebar.selectbox(
    "Seleccionar Semana",
    options=list(range(1, 9)),
    index=0,
    format_func=lambda x: f"Semana {x}"
)

# Get current date and calculate which week we're in
today = datetime.now()
start_date = datetime(2026, 3, 1)
days_elapsed = (today - start_date).days
calculated_week = min(max(1, (days_elapsed // 7) + 1), 8)

if calculated_week != current_week:
    st.sidebar.info(f"📍 Estamos en la **Semana {calculated_week}**")

# Quick stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Resumen General")

# Get all completed workouts
all_completed = db.get_completed_workouts()
total_km = all_completed['distance_km'].sum() if len(all_completed) > 0 else 0
total_workouts = len(all_completed)

st.sidebar.metric("Total KM Corridos", f"{total_km:.1f} km")
st.sidebar.metric("Entrenamientos Completados", total_workouts)

# Days to race
race_date = datetime(2026, 4, 26)
days_to_race = (race_date - today).days
st.sidebar.metric("Días para el Maratón", days_to_race)

# Main content
tab1, tab2, tab3 = st.tabs(["📋 Plan Semanal", "📊 Progreso", "📅 Vista Mensual"])

with tab1:
    # Get weekly summary
    summary = db.get_weekly_summary(current_week)
    planned_df = summary['planned']
    completed_df = summary['completed']
    
    # Week header with menstrual cycle info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Semana", f"{current_week}/8")
    
    with col2:
        st.metric("KM Planificados", f"{summary['planned_km']:.1f} km")
    
    with col3:
        st.metric("KM Completados", f"{summary['completed_km']:.1f} km")
    
    with col4:
        completion = summary['completion_rate']
        st.metric("% Completado", f"{completion:.0f}%")
    
    st.markdown("---")
    
    # Menstrual cycle phase indicator
    menstrual_info = {
        1: ("🔴 Menstruación D1-5 + Inicio Folicular", "Energía baja, entrenamientos SUAVES, pesos -20%, hierro + magnesio"),
        2: ("💚 FASE FOLICULAR ÓPTIMA D8-14", "⭐ VENTANA DE CONSTRUCCIÓN - Máxima energía, fuerza, velocidad - APROVECHAR"),
        3: ("🟡 Fase Lútea Temprana D15-21", "Rendimiento estable, priorizar VOLUMEN sobre intensidad, mantener cargas"),
        4: ("🟠 FASE LÚTEA TARDÍA D22-28", "⚠️ PRECAUCIÓN - Mayor riesgo lesiones, laxitud ligamentos, DESCARGA obligatoria, foam rolling 3x/día"),
        5: ("🔴 Nueva Menstruación D1-5 + Pico", "Semana PICO pero durante menstruación - Ritmo controlado, hierro extra, gel adicional"),
        6: ("💚 FASE FOLICULAR ÓPTIMA D8-14", "⭐ ÚLTIMA VENTANA DE CALIDAD - Aprovechar para cargas máximas y velocidad"),
        7: ("🟡 Lútea Temprana D15-21 + Tapering", "Tapering -40% compatible con fase, mantener calidad en bajo volumen"),
        8: ("🟠 Lútea Tardía D22-28 + Tapering Final", "Retención líquidos +1-2kg es NORMAL (agua), dormir 9h, no restricción calórica")
    }
    
    phase, phase_desc = menstrual_info.get(current_week, ("", ""))
    
    if phase:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h3 style='margin: 0 0 10px 0;'>🌙 Fase Hormonal de la Semana</h3>
            <h2 style='margin: 0 0 10px 0;'>{phase}</h2>
            <p style='margin: 0; font-size: 1.1em;'>{phase_desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add cycle day calculator
    start_date_cycle = datetime(2026, 3, 1)  # Domingo 1 Marzo = Día 1
    days_elapsed = (today - start_date_cycle).days
    cycle_day = ((days_elapsed % 28) + 1) if days_elapsed >= 0 else "N/A"
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌙 Ciclo Menstrual")
    if isinstance(cycle_day, int):
        st.sidebar.metric("Día del Ciclo", f"{cycle_day}/28")
        
        # Phase indicator
        if cycle_day <= 5:
            st.sidebar.error("🔴 Menstruación")
            st.sidebar.caption("Energía baja - Suave")
        elif cycle_day <= 14:
            st.sidebar.success("💚 Folicular - ÓPTIMA")
            st.sidebar.caption("Aprovechar para construcción")
        elif cycle_day <= 21:
            st.sidebar.warning("🟡 Lútea Temprana")
            st.sidebar.caption("Volumen > Intensidad")
        else:
            st.sidebar.error("🟠 Lútea Tardía - PRECAUCIÓN")
            st.sidebar.caption("Descarga - Riesgo lesiones ↑")
    
    st.markdown("### 📅 Plan de la Semana")
    
    # Display each day
    for idx, row in planned_df.iterrows():
        date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
        day_name = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][date_obj.weekday()]
        
        # Check if completed
        is_completed = len(completed_df[completed_df['date'] == row['date']]) > 0
        
        # Create expander for each day
        with st.expander(
            f"{'✅' if is_completed else '⬜'} {day_name} {date_obj.strftime('%d/%m')} - **{row['workout_type']}** ({row['distance_km']} km, {row['duration_min']} min)",
            expanded=not is_completed
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Format and display description
                formatted_desc = format_workout_description(row['description'])
                st.markdown("**📝 Descripción:**")
                st.markdown(formatted_desc, unsafe_allow_html=True)
                
                if row['target_pace']:
                    st.markdown(f"**⏱️ Ritmo objetivo:** {row['target_pace']}")
                
                # Intensity badge
                intensity = row['intensity']
                if 'Alta' in intensity:
                    st.markdown(f'<p class="intensity-high">🔥 Intensidad: {intensity}</p>', unsafe_allow_html=True)
                elif 'Moderada' in intensity:
                    st.markdown(f'<p class="intensity-moderate">⚡ Intensidad: {intensity}</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="intensity-low">✓ Intensidad: {intensity}</p>', unsafe_allow_html=True)
            
            with col2:
                if is_completed:
                    completed_workout = completed_df[completed_df['date'] == row['date']].iloc[0]
                    st.success("✅ Completado")
                    st.metric("Distancia real", f"{completed_workout['distance_km']:.2f} km")
                    st.metric("Tiempo real", f"{completed_workout['duration_min']} min")
                    if completed_workout['avg_pace']:
                        st.metric("Ritmo promedio", completed_workout['avg_pace'])
                else:
                    if st.button("Marcar como completado", key=f"complete_{row['date']}"):
                        st.session_state[f'add_workout_{row["date"]}'] = True
                        st.rerun()
            
            # Quick add workout form - DIFFERENT FORMS BY TYPE
            if st.session_state.get(f'add_workout_{row["date"]}', False):
                st.markdown("---")
                
                workout_type = row['workout_type'].lower()
                
                # FORM 1: RUNNING/CARDIO
                if any(word in workout_type for word in ['rodaje', 'carrera', 'intervalos', 'tempo', 'fartlek', 'ritmo']):
                    st.markdown("**🏃‍♀️ Registrar Carrera:**")
                    
                    with st.form(key=f"workout_form_{row['date']}"):
                        c1, c2, c3 = st.columns(3)
                        
                        with c1:
                            actual_km = st.number_input("KM realizados", value=float(row['distance_km']), min_value=0.0, step=0.1)
                        with c2:
                            actual_min = st.number_input("Minutos", value=int(row['duration_min']), min_value=0, step=1)
                        with c3:
                            if actual_km > 0 and actual_min > 0:
                                pace_min = actual_min / actual_km
                                pace_sec = (pace_min % 1) * 60
                                default_pace = f"{int(pace_min)}:{int(pace_sec):02d}"
                            else:
                                default_pace = ""
                            avg_pace = st.text_input("Ritmo (min/km)", value=default_pace)
                        
                        c4, c5, c6 = st.columns(3)
                        with c4:
                            avg_hr = st.number_input("FC promedio (opcional)", value=0, min_value=0, max_value=220)
                        with c5:
                            max_hr = st.number_input("FC máxima (opcional)", value=0, min_value=0, max_value=220)
                        with c6:
                            feeling = st.slider("Sensación (1-10)", 1, 10, 5, help="1=Muy mal, 10=Excelente")
                        
                        notes = st.text_area("Notas", placeholder="Ej: Ratio 4:1, gel KM 10, dolor rodilla 2/10...")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            if st.form_submit_button("💾 Guardar", type="primary"):
                                db.add_workout(
                                    date=row['date'],
                                    workout_type=row['workout_type'],
                                    distance_km=actual_km,
                                    duration_min=actual_min,
                                    avg_pace=avg_pace,
                                    avg_hr=avg_hr if avg_hr > 0 else None,
                                    max_hr=max_hr if max_hr > 0 else None,
                                    feeling=feeling,
                                    notes=notes
                                )
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.success("✅ Carrera guardada!")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.rerun()
                
                # FORM 2: STRENGTH
                elif 'fuerza' in workout_type:
                    st.markdown("**💪 Registrar Fuerza:**")
                    
                    # Extract exercises from this day's plan
                    day_exercises = extract_exercises_from_description(row['description'])
                    
                    with st.form(key=f"workout_form_{row['date']}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            actual_min = st.number_input("Duración (min)", value=int(row['duration_min']), min_value=0, step=5)
                        with c2:
                            feeling = st.slider("Sensación (1-10)", 1, 10, 5, help="1=Muy pesado, 10=Excelente")
                        
                        # Show exercises from TODAY's plan
                        if day_exercises:
                            st.markdown(f"**Ejercicios del plan de hoy ({len(day_exercises)}):**")
                            
                            completed_exercises = []
                            
                            # Display checkboxes for actual exercises in groups of 2
                            for i in range(0, len(day_exercises), 2):
                                cols = st.columns(2)
                                for j, col in enumerate(cols):
                                    if i + j < len(day_exercises):
                                        exercise = day_exercises[i + j]
                                        with col:
                                            if st.checkbox(f"✅ {exercise}", value=True, key=f"ex_{i+j}"):
                                                completed_exercises.append(exercise)
                        
                        # Hip Thrust weight tracking (if in plan)
                        hip_kg = None
                        if any("hip thrust" in ex.lower() for ex in day_exercises):
                            hip_kg = st.number_input("💪 Peso Hip Thrust (kg)", value=25.0, step=0.5, min_value=0.0)
                        
                        st.markdown("**🦵 Rodilla:**")
                        c5, c6 = st.columns(2)
                        with c5:
                            knee_pain = st.slider("Dolor rodilla (0-10)", 0, 10, 0)
                        with c6:
                            foam_roll = st.checkbox("✅ Foam rolling IT band", value=True)
                        
                        notes = st.text_area("Notas", placeholder="Técnica, próxima carga, ajustes necesarios...")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            if st.form_submit_button("💾 Guardar", type="primary"):
                                # Build detailed notes
                                detail = f"Completados: {', '.join(completed_exercises)}. "
                                if hip_kg:
                                    detail += f"Hip: {hip_kg}kg. "
                                detail += f"Dolor: {knee_pain}/10. "
                                if foam_roll:
                                    detail += "Foam ✅. "
                                else:
                                    detail += "⚠️ Sin foam roll. "
                                detail += notes
                                
                                db.add_workout(
                                    date=row['date'],
                                    workout_type=row['workout_type'],
                                    distance_km=0,
                                    duration_min=actual_min,
                                    avg_pace=None,
                                    avg_hr=None,
                                    max_hr=None,
                                    feeling=feeling,
                                    notes=detail
                                )
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.success("✅ Fuerza guardada!")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.rerun()
                
                # FORM 3: REST/RECOVERY
                else:
                    st.markdown("**😴 Registrar Recuperación:**")
                    
                    with st.form(key=f"workout_form_{row['date']}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            actual_min = st.number_input("Actividad (min)", value=0, min_value=0, step=5, help="Yoga, caminata, etc.")
                        with c2:
                            feeling = st.slider("Estado general (1-10)", 1, 10, 7, help="1=Muy cansada, 10=Recuperada")
                        
                        c3, c4, c5 = st.columns(3)
                        with c3:
                            sleep = st.number_input("Sueño (horas)", value=8.0, step=0.5)
                        with c4:
                            knee_pain = st.slider("Dolor rodilla (0-10)", 0, 10, 0)
                        with c5:
                            foam_roll = st.checkbox("✅ Foam rolling")
                        
                        notes = st.text_area("Notas", placeholder="Estado de recuperación...")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            if st.form_submit_button("💾 Guardar", type="primary"):
                                detail = f"Sueño: {sleep}h. Dolor: {knee_pain}/10. "
                                if foam_roll:
                                    detail += "Foam ✅. "
                                detail += notes
                                
                                db.add_workout(
                                    date=row['date'],
                                    workout_type=row['workout_type'],
                                    distance_km=0,
                                    duration_min=actual_min,
                                    avg_pace=None,
                                    avg_hr=None,
                                    max_hr=None,
                                    feeling=feeling,
                                    notes=detail
                                )
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.success("✅ Recuperación guardada!")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state[f'add_workout_{row["date"]}'] = False
                                st.rerun()


with tab2:
    st.markdown("### 📊 Progreso de Entrenamiento")
    
    # Get all plan and completed
    all_plan = db.get_training_plan()
    all_completed = db.get_completed_workouts()
    
    if len(all_completed) > 0:
        # Weekly distance comparison
        st.markdown("#### KM por Semana: Planificado vs Realizado")
        
        weekly_planned = all_plan.groupby('week')['distance_km'].sum().reset_index()
        weekly_planned.columns = ['Semana', 'Planificado']
        
        # Get completed by week
        all_completed['date'] = pd.to_datetime(all_completed['date'])
        all_completed['week'] = ((all_completed['date'] - pd.Timestamp('2026-03-01')).dt.days // 7) + 1
        weekly_completed = all_completed.groupby('week')['distance_km'].sum().reset_index()
        weekly_completed.columns = ['Semana', 'Realizado']
        
        weekly_comparison = pd.merge(weekly_planned, weekly_completed, on='Semana', how='left')
        weekly_comparison['Realizado'] = weekly_comparison['Realizado'].fillna(0)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekly_comparison['Semana'],
            y=weekly_comparison['Planificado'],
            name='Planificado',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=weekly_comparison['Semana'],
            y=weekly_comparison['Realizado'],
            name='Realizado',
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            barmode='group',
            xaxis_title='Semana',
            yaxis_title='Kilómetros',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cumulative distance
        st.markdown("#### Distancia Acumulada")
        
        all_completed_sorted = all_completed.sort_values('date')
        all_completed_sorted['km_acumulado'] = all_completed_sorted['distance_km'].cumsum()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=all_completed_sorted['date'],
            y=all_completed_sorted['km_acumulado'],
            mode='lines+markers',
            name='KM Acumulados',
            line=dict(color='#1f4788', width=3),
            fill='tozeroy'
        ))
        
        fig2.update_layout(
            xaxis_title='Fecha',
            yaxis_title='KM Acumulados',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Pace evolution
        if all_completed['avg_pace'].notna().any():
            st.markdown("#### Evolución de Ritmo (min/km)")
            
            # Convert pace string to float for plotting
            def pace_to_float(pace_str):
                if pd.isna(pace_str) or pace_str == '':
                    return None
                try:
                    parts = pace_str.split(':')
                    return float(parts[0]) + float(parts[1]) / 60
                except:
                    return None
            
            all_completed_sorted['pace_float'] = all_completed_sorted['avg_pace'].apply(pace_to_float)
            pace_data = all_completed_sorted[all_completed_sorted['pace_float'].notna()]
            
            if len(pace_data) > 0:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=pace_data['date'],
                    y=pace_data['pace_float'],
                    mode='lines+markers',
                    name='Ritmo Promedio',
                    line=dict(color='#c65911', width=2),
                    marker=dict(size=8)
                ))
                
                # Add target pace line
                fig3.add_hline(y=7.83, line_dash="dash", line_color="red", 
                              annotation_text="Ritmo objetivo: 7:50/km")
                
                fig3.update_layout(
                    xaxis_title='Fecha',
                    yaxis_title='Ritmo (min/km)',
                    yaxis_autorange='reversed',
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("🏃‍♀️ Aún no hay entrenamientos registrados. ¡Comienza a entrenar!")

with tab3:
    st.markdown("### 📅 Vista Calendario - 8 Semanas")
    
    # Create calendar view
    all_plan = db.get_training_plan()
    all_completed = db.get_completed_workouts()
    
    # Group by week
    for week in range(1, 9):
        week_data = all_plan[all_plan['week'] == week]
        
        if len(week_data) > 0:
            # Week header
            start_date = datetime.strptime(week_data.iloc[0]['date'], '%Y-%m-%d')
            end_date = datetime.strptime(week_data.iloc[-1]['date'], '%Y-%m-%d')
            
            total_km = week_data['distance_km'].sum()
            completed_km = 0
            
            # Check completion
            week_completed = all_completed[
                (all_completed['date'] >= week_data.iloc[0]['date']) &
                (all_completed['date'] <= week_data.iloc[-1]['date'])
            ]
            
            if len(week_completed) > 0:
                completed_km = week_completed['distance_km'].sum()
            
            completion_pct = (completed_km / total_km * 100) if total_km > 0 else 0
            
            with st.expander(
                f"**Semana {week}** ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')}) | "
                f"{total_km:.0f} km planificados | "
                f"{completed_km:.0f} km realizados ({completion_pct:.0f}%)",
                expanded=(week == calculated_week)
            ):
                # Mini calendar
                cols = st.columns(7)
                
                for idx, row in week_data.iterrows():
                    col_idx = row['day_of_week']
                    date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
                    day_name = ['L', 'M', 'X', 'J', 'V', 'S', 'D'][col_idx]
                    
                    is_completed = len(all_completed[all_completed['date'] == row['date']]) > 0
                    
                    with cols[col_idx]:
                        status = "✅" if is_completed else "⬜"
                        st.markdown(f"**{day_name} {date_obj.day}**")
                        st.markdown(f"{status} {row['workout_type']}")
                        st.markdown(f"📏 {row['distance_km']} km")
                        
                        if row['duration_min'] > 0:
                            st.markdown(f"⏱️ {row['duration_min']} min")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    🏃‍♀️ Marathon Training Tracker | Desarrollado para alcanzar 5:30 en 42.195 km
</div>
""", unsafe_allow_html=True)

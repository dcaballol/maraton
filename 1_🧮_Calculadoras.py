import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Calculadoras", page_icon="🧮", layout="wide")

st.title("🧮 Calculadoras de Running")

tab1, tab2, tab3, tab4 = st.tabs([
    "⏱️ Ritmo y Tiempo", 
    "❤️ Zonas FC", 
    "🍽️ Nutrición",
    "📊 Método Galloway"
])

with tab1:
    st.header("⏱️ Calculadora de Ritmo y Tiempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Calcular Ritmo")
        st.markdown("Ingresa distancia y tiempo para obtener tu ritmo")
        
        distance = st.number_input("Distancia (km)", min_value=0.1, value=10.0, step=0.1)
        
        time_col1, time_col2, time_col3 = st.columns(3)
        with time_col1:
            hours = st.number_input("Horas", min_value=0, max_value=10, value=0)
        with time_col2:
            minutes = st.number_input("Minutos", min_value=0, max_value=59, value=50)
        with time_col3:
            seconds = st.number_input("Segundos", min_value=0, max_value=59, value=0)
        
        total_minutes = hours * 60 + minutes + seconds / 60
        
        if total_minutes > 0 and distance > 0:
            pace_per_km = total_minutes / distance
            pace_min = int(pace_per_km)
            pace_sec = int((pace_per_km - pace_min) * 60)
            
            st.success(f"### Tu ritmo: **{pace_min}:{pace_sec:02d} min/km**")
            
            # Show splits for common distances
            st.markdown("#### Tiempos proyectados en otras distancias:")
            distances = [5, 10, 21.0975, 42.195]
            distance_names = ["5K", "10K", "Media Maratón", "Maratón"]
            
            for dist, name in zip(distances, distance_names):
                projected_min = dist * pace_per_km
                proj_hours = int(projected_min // 60)
                proj_minutes = int(projected_min % 60)
                proj_seconds = int((projected_min % 1) * 60)
                
                if proj_hours > 0:
                    st.metric(name, f"{proj_hours}h {proj_minutes:02d}m {proj_seconds:02d}s")
                else:
                    st.metric(name, f"{proj_minutes}m {proj_seconds:02d}s")
    
    with col2:
        st.subheader("Calcular Tiempo")
        st.markdown("Ingresa distancia y ritmo para obtener tiempo estimado")
        
        target_distance = st.number_input("Distancia objetivo (km)", min_value=0.1, value=42.195, step=0.1)
        
        pace_col1, pace_col2 = st.columns(2)
        with pace_col1:
            pace_minutes = st.number_input("Ritmo - Minutos", min_value=3, max_value=15, value=7)
        with pace_col2:
            pace_seconds = st.number_input("Ritmo - Segundos", min_value=0, max_value=59, value=50)
        
        pace_decimal = pace_minutes + pace_seconds / 60
        total_time_min = target_distance * pace_decimal
        
        result_hours = int(total_time_min // 60)
        result_minutes = int(total_time_min % 60)
        result_seconds = int((total_time_min % 1) * 60)
        
        st.success(f"### Tiempo estimado: **{result_hours}h {result_minutes:02d}m {result_seconds:02d}s**")
        
        # Splits table
        st.markdown("#### Splits cada 5K:")
        
        splits_data = []
        for km in range(5, int(target_distance) + 1, 5):
            split_time = km * pace_decimal
            split_hours = int(split_time // 60)
            split_minutes = int(split_time % 60)
            split_seconds = int((split_time % 1) * 60)
            
            if split_hours > 0:
                time_str = f"{split_hours}:{split_minutes:02d}:{split_seconds:02d}"
            else:
                time_str = f"{split_minutes}:{split_seconds:02d}"
            
            splits_data.append({
                "KM": f"{km} km",
                "Tiempo Acumulado": time_str
            })
        
        st.dataframe(pd.DataFrame(splits_data), hide_index=True, use_container_width=True)

with tab2:
    st.header("❤️ Calculadora de Zonas de Frecuencia Cardíaca")
    
    st.markdown("""
    Las zonas de FC te ayudan a entrenar con la intensidad correcta:
    - **Zona 1 (50-60%)**: Recuperación muy suave
    - **Zona 2 (60-70%)**: Resistencia aeróbica - la base del entrenamiento
    - **Zona 3 (70-80%)**: Ritmo de carrera - tempo runs
    - **Zona 4 (80-90%)**: Umbral anaeróbico - intervalos
    - **Zona 5 (90-100%)**: Máxima intensidad - sprints cortos
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Edad (años)", min_value=15, max_value=100, value=30)
        resting_hr = st.number_input("FC en reposo (ppm)", min_value=40, max_value=100, value=60)
    
    with col2:
        # Calculate max HR using Tanaka formula (more accurate than 220-age)
        max_hr_calculated = 208 - (0.7 * age)
        max_hr = st.number_input("FC máxima (ppm)", value=int(max_hr_calculated), min_value=100, max_value=220)
        
        st.info(f"💡 FC máxima calculada: {int(max_hr_calculated)} ppm\n\n(Fórmula Tanaka: 208 - 0.7 × edad)")
    
    # Karvonen method (more accurate)
    hr_reserve = max_hr - resting_hr
    
    st.markdown("### Tus Zonas de Entrenamiento (Método Karvonen)")
    
    zones = [
        ("Zona 1: Recuperación", 0.50, 0.60, "Muy suave, conversación fácil"),
        ("Zona 2: Resistencia Aeróbica", 0.60, 0.70, "Base de entrenamiento, rodajes largos"),
        ("Zona 3: Ritmo de Carrera", 0.70, 0.80, "Tempo runs, ritmo de maratón"),
        ("Zona 4: Umbral Anaeróbico", 0.80, 0.90, "Intervalos, series"),
        ("Zona 5: Máxima", 0.90, 1.00, "Sprints, esfuerzo máximo"),
    ]
    
    zones_data = []
    for zone_name, low_pct, high_pct, description in zones:
        low_hr = int(resting_hr + (hr_reserve * low_pct))
        high_hr = int(resting_hr + (hr_reserve * high_pct))
        
        zones_data.append({
            "Zona": zone_name,
            "Rango FC": f"{low_hr} - {high_hr} ppm",
            "Descripción": description
        })
    
    st.dataframe(pd.DataFrame(zones_data), hide_index=True, use_container_width=True)
    
    st.markdown("""
    ### 📍 Recomendaciones para Maratón:
    - **80% del tiempo en Zona 2**: Construye resistencia aeróbica
    - **15% en Zona 3-4**: Mejora velocidad y umbral
    - **5% en Zona 1**: Recuperación activa
    - **Evita exceso de Zona 4-5**: Riesgo de sobreentrenamiento
    """)

with tab3:
    st.header("🍽️ Calculadora de Nutrición para Running")
    
    st.markdown("### Necesidades Diarias de Macronutrientes")
    
    weight = st.number_input("Peso corporal (kg)", min_value=40.0, max_value=150.0, value=60.0, step=0.5)
    
    training_intensity = st.select_slider(
        "Intensidad de entrenamiento hoy",
        options=["Descanso", "Suave", "Moderado", "Intenso", "Muy intenso"],
        value="Moderado"
    )
    
    # Carbs based on training intensity
    carb_ranges = {
        "Descanso": (3, 4),
        "Suave": (4, 5),
        "Moderado": (5, 7),
        "Intenso": (7, 9),
        "Muy intenso": (9, 12)
    }
    
    carb_low, carb_high = carb_ranges[training_intensity]
    carbs_g = (carb_low + carb_high) / 2 * weight
    
    # Protein constant for endurance athletes
    protein_g = 1.7 * weight
    
    # Fats
    fats_g = 1.0 * weight
    
    # Calories
    carb_cal = carbs_g * 4
    protein_cal = protein_g * 4
    fats_cal = fats_g * 9
    total_cal = carb_cal + protein_cal + fats_cal
    
    st.markdown("### 📊 Tu Plan Nutricional Diario")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Carbohidratos", f"{carbs_g:.0f}g", f"{carb_cal:.0f} kcal")
    
    with col2:
        st.metric("Proteínas", f"{protein_g:.0f}g", f"{protein_cal:.0f} kcal")
    
    with col3:
        st.metric("Grasas", f"{fats_g:.0f}g", f"{fats_cal:.0f} kcal")
    
    with col4:
        st.metric("Calorías Totales", f"{total_cal:.0f} kcal")
    
    # Meal timing
    st.markdown("### ⏰ Timing de Nutrición")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Pre-Entrenamiento (2-3h antes)")
        st.markdown(f"""
        - **Carbohidratos**: {carbs_g * 0.15:.0f}g
        - **Proteínas**: {protein_g * 0.1:.0f}g
        - **Ejemplos**:
          - Avena + plátano + miel
          - Pan tostado + mermelada + yogurt
          - Smoothie con frutas
        """)
    
    with col2:
        st.markdown("#### Post-Entrenamiento (30 min después)")
        st.markdown(f"""
        - **Carbohidratos**: {carbs_g * 0.25:.0f}g
        - **Proteínas**: {protein_g * 0.25:.0f}g
        - **Ratio 3:1** (carbos:proteína)
        - **Ejemplos**:
          - Batido recuperación + plátano
          - Yogurt griego + frutas + granola
          - Arroz + huevos + palta
        """)
    
    st.markdown("### 💧 Hidratación")
    
    base_water = weight * 35  # ml per kg
    st.markdown(f"""
    - **Mínimo diario**: {base_water:.0f} ml ({base_water/1000:.1f} litros)
    - **En días de entrenamiento**: +500-1000 ml
    - **Durante rodajes >60 min**: 150-250 ml cada 15-20 min
    - **Color de orina**: Amarillo claro = bien hidratada
    """)
    
    st.markdown("### 🏃‍♀️ Estrategia para Día de Maratón")
    
    st.markdown(f"""
    #### 3 Días Antes (Carga de Carbohidratos)
    - **Carbohidratos**: {weight * 9:.0f}g/día ({weight * 9 * 4:.0f} kcal)
    - Aumentar pasta, arroz, pan en todas las comidas
    - Reducir fibra y grasas (evitar malestar)
    
    #### Desayuno Pre-Carrera (3h antes)
    - **Carbohidratos**: {weight * 1.5:.0f}g
    - Opciones: Pan blanco + mermelada + plátano, o Avena + miel + plátano
    - 500 ml agua + bebida deportiva
    
    #### Durante la Carrera (cada hora)
    - **Carbohidratos**: 30-60g/hora
    - 3-4 geles energéticos (KM 10, 20, 30, 40)
    - 150-200 ml agua cada 5K
    - Bebida isotónica alternada con agua
    """)

with tab4:
    st.header("📊 Calculadora Método Galloway (Run-Walk-Run)")
    
    st.markdown("""
    El método Run-Walk-Run de Jeff Galloway alterna períodos de carrera con caminata planificada 
    para reducir fatiga muscular, prevenir lesiones y mantener energía hasta el final.
    """)
    
    target_time = st.time_input("Tiempo objetivo de maratón", value=datetime.strptime("05:30:00", "%H:%M:%S").time())
    
    # Convert to minutes
    target_minutes = target_time.hour * 60 + target_time.minute + target_time.second / 60
    
    # Recommended ratios based on target time
    st.markdown("### 🎯 Ratios Recomendados según Tiempo Objetivo")
    
    if target_minutes < 210:  # < 3:30
        recommended_ratio = "30 seg carrera / 30 seg caminar"
        run_min = 0.5
        walk_min = 0.5
    elif target_minutes < 270:  # 3:30 - 4:30
        recommended_ratio = "2 min carrera / 1 min caminar"
        run_min = 2
        walk_min = 1
    elif target_minutes < 330:  # 4:30 - 5:30
        recommended_ratio = "4 min carrera / 1 min caminar"
        run_min = 4
        walk_min = 1
    elif target_minutes < 390:  # 5:30 - 6:30
        recommended_ratio = "5 min carrera / 1 min caminar"
        run_min = 5
        walk_min = 1
    else:
        recommended_ratio = "5 min carrera / 2 min caminar"
        run_min = 5
        walk_min = 2
    
    st.info(f"**Para tu objetivo de {target_time.hour}:{target_time.minute:02d}h, se recomienda: {recommended_ratio}**")
    
    # Custom ratio calculator
    st.markdown("### 🔧 Personalizar Ratio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        custom_run = st.number_input("Minutos corriendo", min_value=0.5, max_value=10.0, value=float(run_min), step=0.5)
    
    with col2:
        custom_walk = st.number_input("Minutos caminando", min_value=0.5, max_value=5.0, value=float(walk_min), step=0.5)
    
    # Calculate impact on finish time
    st.markdown("### 📈 Simulación de Carrera")
    
    running_pace_min = st.number_input("Ritmo durante la carrera (min/km)", min_value=4.0, max_value=10.0, value=7.5, step=0.1)
    walking_pace_min = st.number_input("Ritmo durante la caminata (min/km)", min_value=10.0, max_value=20.0, value=12.0, step=0.1)
    
    # Calculate weighted average pace
    interval_time = custom_run + custom_walk
    run_portion = custom_run / interval_time
    walk_portion = custom_walk / interval_time
    
    effective_pace = (running_pace_min * run_portion) + (walking_pace_min * walk_portion)
    
    # Marathon time
    marathon_time = 42.195 * effective_pace
    finish_hours = int(marathon_time // 60)
    finish_minutes = int(marathon_time % 60)
    finish_seconds = int((marathon_time % 1) * 60)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Ritmo Efectivo", f"{effective_pace:.2f} min/km")
    
    with col2:
        st.metric("Tiempo Final Estimado", f"{finish_hours}:{finish_minutes:02d}:{finish_seconds:02d}")
    
    with col3:
        # Number of walk breaks
        num_breaks = int(marathon_time / interval_time)
        st.metric("Intervalos de Caminata", num_breaks)
    
    # Splits table
    st.markdown("### 📋 Plan de Intervalos por Kilómetro")
    
    split_data = []
    accumulated_time = 0
    
    for km in range(1, 43):
        time_this_km = effective_pace
        accumulated_time += time_this_km
        
        acc_hours = int(accumulated_time // 60)
        acc_minutes = int(accumulated_time % 60)
        acc_seconds = int((accumulated_time % 1) * 60)
        
        # Check if walk break happens in this km
        intervals_completed = int(accumulated_time / interval_time)
        
        split_data.append({
            "KM": km,
            "Tiempo Acum": f"{acc_hours}:{acc_minutes:02d}:{acc_seconds:02d}",
            "Acción": "🏃 Correr" if (km * effective_pace) % interval_time < custom_run else "🚶 Caminar"
        })
    
    # Show first 10 and last 10
    df_splits = pd.DataFrame(split_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Primeros 10K:**")
        st.dataframe(df_splits.head(10), hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("**Últimos 10K:**")
        st.dataframe(df_splits.tail(10), hide_index=True, use_container_width=True)
    
    st.markdown("### ✅ Consejos para el Método Galloway")
    
    st.markdown("""
    1. **Comenzar desde el KM 1** - No esperar a estar cansada
    2. **Usar cronómetro con alertas** - Cada 4-5 minutos según tu ratio
    3. **Practicar en entrenamientos largos** - Desde semana 3 en adelante
    4. **Mantener ritmo durante carrera** - No acelerar entre caminatas
    5. **Caminata activa y rápida** - No detenerse completamente
    6. **Confiar en el método** - Funciona incluso si sientes que puedes más
    """)

# Footer
st.markdown("---")
st.markdown("🧮 **Calculadoras de Running** | Herramientas para optimizar tu entrenamiento")

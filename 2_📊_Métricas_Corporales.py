import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
sys.path.append('..')
import database as db

st.set_page_config(page_title="Métricas Corporales", page_icon="📊", layout="wide")

st.title("📊 Seguimiento de Métricas Corporales")

# Initialize DB
db.init_db()

tab1, tab2, tab3 = st.tabs(["📝 Registrar Métricas", "📈 Visualizar Progreso", "🔴 Ciclo Menstrual"])

with tab1:
    st.header("Registro Diario de Métricas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("daily_metrics"):
            metric_date = st.date_input("Fecha", value=datetime.now())
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                weight = st.number_input("Peso (kg)", min_value=0.0, max_value=200.0, step=0.1, value=60.0)
                resting_hr = st.number_input("FC en reposo (ppm)", min_value=0, max_value=120, value=0)
                sleep_hours = st.number_input("Horas de sueño", min_value=0.0, max_value=15.0, step=0.5, value=8.0)
            
            with col_b:
                energy_level = st.slider("Nivel de energía (1-10)", 1, 10, 5)
                soreness_level = st.slider("Dolor muscular (1-10)", 1, 10, 1)
            
            notes = st.text_area("Notas (estado general, síntomas, etc.)")
            
            if st.form_submit_button("💾 Guardar Métricas", type="primary"):
                db.add_body_metrics(
                    date=metric_date.strftime("%Y-%m-%d"),
                    weight_kg=weight if weight > 0 else None,
                    resting_hr=resting_hr if resting_hr > 0 else None,
                    sleep_hours=sleep_hours,
                    energy_level=energy_level,
                    soreness_level=soreness_level,
                    notes=notes
                )
                st.success("✅ Métricas guardadas correctamente")
                st.rerun()
    
    with col2:
        st.info("""
        **💡 Tips para medición:**
        
        **Peso:**
        - Medir en la mañana, después de ir al baño
        - Antes de desayunar
        - Con poca ropa
        
        **FC en reposo:**
        - Al despertar, aún en cama
        - Usar monitor o app
        - Más bajo = mejor forma física
        
        **Nivel de energía:**
        - 1-3: Muy fatigada
        - 4-6: Normal
        - 7-10: Excelente
        
        **Dolor muscular:**
        - 1-3: Leve o ninguno
        - 4-6: Moderado
        - 7-10: Intenso (considerar descanso)
        """)

with tab2:
    st.header("📈 Evolución de Métricas")
    
    # Get all metrics
    all_metrics = db.get_body_metrics()
    
    if len(all_metrics) > 0:
        all_metrics['date'] = pd.to_datetime(all_metrics['date'])
        all_metrics = all_metrics.sort_values('date')
        
        # Weight evolution
        if all_metrics['weight_kg'].notna().any():
            st.subheader("⚖️ Evolución del Peso")
            
            fig_weight = go.Figure()
            fig_weight.add_trace(go.Scatter(
                x=all_metrics['date'],
                y=all_metrics['weight_kg'],
                mode='lines+markers',
                name='Peso',
                line=dict(color='#1f4788', width=2),
                marker=dict(size=8)
            ))
            
            # Add trend line
            if len(all_metrics) > 3:
                z = np.polyfit(range(len(all_metrics)), all_metrics['weight_kg'].fillna(method='ffill'), 1)
                p = np.poly1d(z)
                fig_weight.add_trace(go.Scatter(
                    x=all_metrics['date'],
                    y=p(range(len(all_metrics))),
                    mode='lines',
                    name='Tendencia',
                    line=dict(color='red', width=2, dash='dash')
                ))
            
            fig_weight.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Peso (kg)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_weight, use_container_width=True)
            
            # Weight stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Peso Actual", f"{all_metrics['weight_kg'].iloc[-1]:.1f} kg")
            
            with col2:
                st.metric("Peso Inicial", f"{all_metrics['weight_kg'].iloc[0]:.1f} kg")
            
            with col3:
                change = all_metrics['weight_kg'].iloc[-1] - all_metrics['weight_kg'].iloc[0]
                st.metric("Cambio Total", f"{change:+.1f} kg")
            
            with col4:
                avg_weight = all_metrics['weight_kg'].mean()
                st.metric("Promedio", f"{avg_weight:.1f} kg")
        
        # Resting HR evolution
        if all_metrics['resting_hr'].notna().any():
            st.subheader("❤️ Frecuencia Cardíaca en Reposo")
            
            hr_data = all_metrics[all_metrics['resting_hr'].notna()]
            
            fig_hr = go.Figure()
            fig_hr.add_trace(go.Scatter(
                x=hr_data['date'],
                y=hr_data['resting_hr'],
                mode='lines+markers',
                name='FC Reposo',
                line=dict(color='#c00000', width=2),
                marker=dict(size=8)
            ))
            
            fig_hr.update_layout(
                xaxis_title='Fecha',
                yaxis_title='FC (ppm)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_hr, use_container_width=True)
            
            st.info("""
            💡 **Interpretación FC en reposo:**
            - Tendencia a la baja = Mejora de forma física
            - Aumento súbito (>10 ppm) = Posible sobreentrenamiento o enfermedad
            - Valores típicos: 50-70 ppm para corredoras entrenadas
            """)
        
        # Sleep, Energy, Soreness
        st.subheader("💤 Sueño, Energía y Recuperación")
        
        fig_wellness = go.Figure()
        
        fig_wellness.add_trace(go.Scatter(
            x=all_metrics['date'],
            y=all_metrics['sleep_hours'],
            name='Horas Sueño',
            line=dict(color='#4472c4')
        ))
        
        fig_wellness.add_trace(go.Scatter(
            x=all_metrics['date'],
            y=all_metrics['energy_level'],
            name='Nivel Energía',
            line=dict(color='#00b050')
        ))
        
        fig_wellness.add_trace(go.Scatter(
            x=all_metrics['date'],
            y=all_metrics['soreness_level'],
            name='Dolor Muscular',
            line=dict(color='#ffc000')
        ))
        
        fig_wellness.update_layout(
            xaxis_title='Fecha',
            yaxis_title='Valor',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_wellness, use_container_width=True)
        
        # Correlations
        st.subheader("🔍 Análisis de Correlaciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sleep vs Energy
            if all_metrics[['sleep_hours', 'energy_level']].notna().all(axis=1).sum() > 3:
                correlation = all_metrics['sleep_hours'].corr(all_metrics['energy_level'])
                st.metric("Correlación Sueño-Energía", f"{correlation:.2f}")
                
                if correlation > 0.5:
                    st.success("✅ Fuerte correlación positiva - Dormir más aumenta tu energía")
                elif correlation > 0.2:
                    st.info("📊 Correlación moderada")
                else:
                    st.warning("⚠️ Baja correlación - Otros factores afectan tu energía")
        
        with col2:
            # Energy vs Soreness
            if all_metrics[['energy_level', 'soreness_level']].notna().all(axis=1).sum() > 3:
                correlation = all_metrics['energy_level'].corr(all_metrics['soreness_level'])
                st.metric("Correlación Energía-Dolor", f"{correlation:.2f}")
                
                if correlation < -0.5:
                    st.success("✅ Fuerte correlación negativa - Menos dolor, más energía")
                elif correlation < -0.2:
                    st.info("📊 Correlación moderada")
                else:
                    st.warning("⚠️ Revisar recuperación post-entreno")
        
        # Recent data table
        st.subheader("📋 Últimos 7 Registros")
        recent = all_metrics.tail(7).sort_values('date', ascending=False)
        recent['date'] = recent['date'].dt.strftime('%Y-%m-%d')
        
        display_cols = ['date', 'weight_kg', 'resting_hr', 'sleep_hours', 'energy_level', 'soreness_level', 'notes']
        st.dataframe(
            recent[display_cols].rename(columns={
                'date': 'Fecha',
                'weight_kg': 'Peso (kg)',
                'resting_hr': 'FC Reposo',
                'sleep_hours': 'Horas Sueño',
                'energy_level': 'Energía',
                'soreness_level': 'Dolor',
                'notes': 'Notas'
            }),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("📝 Aún no hay métricas registradas. ¡Comienza a registrar tus datos diarios!")

with tab3:
    st.header("🔴 Seguimiento del Ciclo Menstrual")
    
    st.markdown("""
    El ciclo menstrual afecta significativamente el rendimiento deportivo. Conocer tu fase 
    te permite ajustar el entrenamiento para maximizar resultados y prevenir lesiones.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Registrar Inicio de Ciclo")
        
        with st.form("menstrual_cycle"):
            cycle_date = st.date_input("Fecha de inicio del período", value=datetime.now())
            cycle_length = st.number_input("Duración del ciclo (días)", min_value=21, max_value=35, value=28)
            cycle_notes = st.text_area("Notas (síntomas, intensidad, etc.)")
            
            if st.form_submit_button("💾 Registrar Ciclo"):
                db.add_menstrual_cycle(
                    start_date=cycle_date.strftime("%Y-%m-%d"),
                    cycle_length=cycle_length,
                    notes=cycle_notes
                )
                st.success("✅ Ciclo registrado correctamente")
                st.rerun()
    
    with col2:
        st.info("""
        **🔴 Fases del Ciclo:**
        
        **Días 1-5: Menstruación**
        - Energía baja
        - Entrenamientos suaves
        
        **Días 6-14: Folicular**
        - 💚 VENTANA ÓPTIMA
        - Alta intensidad y fuerza
        
        **Días 15-21: Lútea Temprana**
        - Rendimiento estable
        - Rodajes largos
        
        **Días 22-28: Lútea Tardía**
        - ⚠️ Riesgo de lesiones
        - Reducir intensidad
        """)
    
    # Display cycle history and predictions
    st.subheader("📅 Historial y Predicciones")
    
    cycles = db.get_menstrual_cycles()
    
    if len(cycles) > 0:
        cycles['cycle_start_date'] = pd.to_datetime(cycles['cycle_start_date'])
        cycles = cycles.sort_values('cycle_start_date', ascending=False)
        
        # Predict next cycles
        last_cycle = cycles.iloc[0]
        last_date = last_cycle['cycle_start_date']
        cycle_len = last_cycle['cycle_length']
        
        st.markdown("### 🔮 Próximos Ciclos Predichos")
        
        predictions = []
        for i in range(1, 4):
            next_date = last_date + timedelta(days=cycle_len * i)
            
            # Calculate phases
            follicular_start = next_date + timedelta(days=5)
            luteal_start = next_date + timedelta(days=14)
            luteal_late = next_date + timedelta(days=21)
            
            predictions.append({
                "Ciclo": f"Ciclo +{i}",
                "Inicio": next_date.strftime("%Y-%m-%d"),
                "Fase Folicular (Alta)": f"{follicular_start.strftime('%d/%m')} - {luteal_start.strftime('%d/%m')}",
                "Fase Lútea Tardía (Cuidado)": f"{luteal_late.strftime('%d/%m')} - {(next_date + timedelta(days=27)).strftime('%d/%m')}"
            })
        
        st.dataframe(pd.DataFrame(predictions), hide_index=True, use_container_width=True)
        
        # Calendar view
        st.markdown("### 📊 Vista de Calendario")
        
        # Create visual calendar for next 8 weeks
        today = datetime.now()
        dates = pd.date_range(start=today, periods=56, freq='D')
        
        calendar_data = []
        for date in dates:
            # Calculate phase
            days_since_last = (date - last_date).days % cycle_len
            
            if days_since_last <= 5:
                phase = "Menstruación"
                color = "#ff0000"
            elif days_since_last <= 14:
                phase = "Folicular (Óptimo)"
                color = "#00b050"
            elif days_since_last <= 21:
                phase = "Lútea Temprana"
                color = "#ffc000"
            else:
                phase = "Lútea Tardía (Precaución)"
                color = "#ff8800"
            
            calendar_data.append({
                "Fecha": date,
                "Día del Ciclo": days_since_last + 1,
                "Fase": phase,
                "Color": color
            })
        
        df_calendar = pd.DataFrame(calendar_data)
        
        # Group by week
        df_calendar['Semana'] = ((df_calendar['Fecha'] - today).dt.days // 7) + 1
        
        for week in range(1, 9):
            week_data = df_calendar[df_calendar['Semana'] == week]
            
            if len(week_data) > 0:
                st.markdown(f"**Semana {week}** ({week_data.iloc[0]['Fecha'].strftime('%d/%m')} - {week_data.iloc[-1]['Fecha'].strftime('%d/%m')})")
                
                cols = st.columns(7)
                for idx, row in week_data.iterrows():
                    col_idx = row['Fecha'].weekday()
                    with cols[col_idx]:
                        st.markdown(
                            f"<div style='background-color:{row['Color']}; padding:5px; border-radius:5px; text-align:center; color:white; font-size:0.8em;'>"
                            f"{row['Fecha'].day}<br>{row['Fase'][:3]}</div>",
                            unsafe_allow_html=True
                        )
        
        # Historical cycles table
        st.markdown("### 📋 Historial de Ciclos")
        
        cycles_display = cycles.copy()
        cycles_display['cycle_start_date'] = cycles_display['cycle_start_date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            cycles_display[['cycle_start_date', 'cycle_length', 'notes']].rename(columns={
                'cycle_start_date': 'Fecha Inicio',
                'cycle_length': 'Duración (días)',
                'notes': 'Notas'
            }),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("🔴 No hay ciclos registrados. Registra tu primer ciclo para comenzar el seguimiento.")

# Add numpy import for trend line
import numpy as np

st.markdown("---")
st.markdown("📊 **Seguimiento de Métricas Corporales** | Conoce tu cuerpo para entrenar mejor")

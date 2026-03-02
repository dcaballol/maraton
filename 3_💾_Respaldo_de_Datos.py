import streamlit as st
import pandas as pd
import database as db
from datetime import datetime
import json

def create_backup_page():
    """Page for data backup and restore"""
    
    st.title("💾 Respaldo de Datos")
    
    st.markdown("""
    Tu información es valiosa. Usa este sistema de respaldo dual para nunca perder tus datos.
    """)
    
    tab1, tab2, tab3 = st.tabs(["📤 Exportar Datos", "📥 Importar Datos", "☁️ Google Sheets"])
    
    with tab1:
        st.header("📤 Exportar Todos los Datos")
        
        st.info("""
        **¿Por qué exportar?**
        - Backup local en tu iPhone/Mac
        - Migrar a otra instancia de la app
        - Análisis externo en Excel/Sheets
        - Seguridad: tus datos siempre contigo
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Exportar Entrenamientos", type="primary"):
                # Get all workouts
                workouts = db.get_completed_workouts()
                
                if len(workouts) > 0:
                    csv = workouts.to_csv(index=False)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    st.download_button(
                        label="⬇️ Descargar entrenamientos.csv",
                        data=csv,
                        file_name=f"entrenamientos_{timestamp}.csv",
                        mime="text/csv"
                    )
                    st.success(f"✅ {len(workouts)} entrenamientos listos para descargar")
                else:
                    st.warning("No hay entrenamientos registrados aún")
        
        with col2:
            if st.button("📈 Exportar Métricas Corporales"):
                metrics = db.get_body_metrics()
                
                if len(metrics) > 0:
                    csv = metrics.to_csv(index=False)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    st.download_button(
                        label="⬇️ Descargar metricas.csv",
                        data=csv,
                        file_name=f"metricas_{timestamp}.csv",
                        mime="text/csv"
                    )
                    st.success(f"✅ {len(metrics)} registros de métricas listos")
                else:
                    st.warning("No hay métricas registradas aún")
        
        st.markdown("---")
        
        if st.button("📦 Exportar TODO (Backup Completo)"):
            # Create comprehensive backup
            backup_data = {
                "export_date": datetime.now().isoformat(),
                "workouts": db.get_completed_workouts().to_dict('records'),
                "metrics": db.get_body_metrics().to_dict('records'),
                "cycles": db.get_menstrual_cycles().to_dict('records'),
                "training_plan": db.get_training_plan().to_dict('records')
            }
            
            json_str = json.dumps(backup_data, indent=2, ensure_ascii=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="⬇️ Descargar backup_completo.json",
                data=json_str,
                file_name=f"marathon_backup_{timestamp}.json",
                mime="application/json"
            )
            
            st.success("✅ Backup completo generado - Incluye todo tu historial")
            st.info("💡 Guarda este archivo en iCloud, Google Drive o Dropbox")
    
    with tab2:
        st.header("📥 Importar Datos")
        
        st.warning("""
        ⚠️ **IMPORTANTE:**
        - Importar sobrescribirá datos existentes con las mismas fechas
        - Haz backup antes de importar
        - Solo importa archivos exportados desde esta app
        """)
        
        import_type = st.selectbox(
            "Tipo de importación",
            ["Entrenamientos (CSV)", "Métricas Corporales (CSV)", "Backup Completo (JSON)"]
        )
        
        uploaded_file = st.file_uploader(
            "Selecciona archivo a importar",
            type=['csv', 'json']
        )
        
        if uploaded_file is not None:
            try:
                if import_type == "Backup Completo (JSON)":
                    # Import full backup
                    backup_data = json.load(uploaded_file)
                    
                    # Import workouts
                    if 'workouts' in backup_data:
                        for workout in backup_data['workouts']:
                            db.add_workout(
                                date=workout['date'],
                                workout_type=workout['workout_type'],
                                distance_km=workout['distance_km'],
                                duration_min=workout['duration_min'],
                                avg_pace=workout.get('avg_pace', ''),
                                avg_hr=workout.get('avg_hr'),
                                max_hr=workout.get('max_hr'),
                                calories=workout.get('calories'),
                                feeling=workout.get('feeling', 5),
                                notes=workout.get('notes', '')
                            )
                        
                        st.success(f"✅ {len(backup_data['workouts'])} entrenamientos importados")
                    
                    # Import metrics
                    if 'metrics' in backup_data:
                        for metric in backup_data['metrics']:
                            db.add_body_metrics(
                                date=metric['date'],
                                weight_kg=metric.get('weight_kg'),
                                resting_hr=metric.get('resting_hr'),
                                sleep_hours=metric.get('sleep_hours'),
                                energy_level=metric.get('energy_level'),
                                soreness_level=metric.get('soreness_level'),
                                notes=metric.get('notes', '')
                            )
                        
                        st.success(f"✅ {len(backup_data['metrics'])} métricas importadas")
                    
                    # Import cycles
                    if 'cycles' in backup_data:
                        for cycle in backup_data['cycles']:
                            db.add_menstrual_cycle(
                                start_date=cycle['cycle_start_date'],
                                cycle_length=cycle.get('cycle_length', 28),
                                notes=cycle.get('notes', '')
                            )
                        
                        st.success(f"✅ {len(backup_data['cycles'])} ciclos importados")
                    
                    st.balloons()
                    st.success("🎉 Importación completa exitosa!")
                    
                else:
                    # Import CSV
                    df = pd.read_csv(uploaded_file)
                    
                    if import_type == "Entrenamientos (CSV)":
                        for _, row in df.iterrows():
                            db.add_workout(
                                date=row['date'],
                                workout_type=row['workout_type'],
                                distance_km=row['distance_km'],
                                duration_min=row['duration_min'],
                                avg_pace=row.get('avg_pace', ''),
                                avg_hr=row.get('avg_hr') if pd.notna(row.get('avg_hr')) else None,
                                max_hr=row.get('max_hr') if pd.notna(row.get('max_hr')) else None,
                                calories=row.get('calories') if pd.notna(row.get('calories')) else None,
                                feeling=row.get('feeling', 5),
                                notes=row.get('notes', '')
                            )
                        
                        st.success(f"✅ {len(df)} entrenamientos importados")
                    
                    elif import_type == "Métricas Corporales (CSV)":
                        for _, row in df.iterrows():
                            db.add_body_metrics(
                                date=row['date'],
                                weight_kg=row.get('weight_kg') if pd.notna(row.get('weight_kg')) else None,
                                resting_hr=row.get('resting_hr') if pd.notna(row.get('resting_hr')) else None,
                                sleep_hours=row.get('sleep_hours') if pd.notna(row.get('sleep_hours')) else None,
                                energy_level=row.get('energy_level') if pd.notna(row.get('energy_level')) else None,
                                soreness_level=row.get('soreness_level') if pd.notna(row.get('soreness_level')) else None,
                                notes=row.get('notes', '')
                            )
                        
                        st.success(f"✅ {len(df)} métricas importadas")
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error al importar: {str(e)}")
                st.info("Verifica que el archivo sea compatible con esta app")
    
    with tab3:
        st.header("☁️ Sincronización con Google Sheets")
        
        st.info("""
        **Próximamente:**
        - Sincronización automática cada vez que registres datos
        - Dashboard en vivo en Google Sheets
        - Acceso desde cualquier dispositivo
        - Backup automático en la nube
        
        **Estado:** En desarrollo - Requiere configuración de API de Google
        """)
        
        st.markdown("""
        ### 🔧 Configuración Manual (Mientras tanto):
        
        1. **Exporta tus datos** usando el botón de arriba
        2. **Abre Google Sheets** en tu navegador
        3. **Importa el CSV**:
           - Archivo → Importar → Subir
           - Selecciona el CSV descargado
        4. **Guarda en Google Drive** para acceso desde cualquier lugar
        
        ### 📊 Ventajas de usar Google Sheets:
        - ✅ Acceso desde iPhone, iPad, Mac, PC
        - ✅ Editar datos directamente
        - ✅ Crear gráficos personalizados
        - ✅ Compartir con entrenador/nutricionista
        - ✅ Historial de versiones automático
        
        ### 🔮 Próxima Versión (v2.0):
        La integración automática con Google Sheets permitirá:
        - Sync bidireccional (app ↔ sheets)
        - Actualización en tiempo real
        - Notificaciones de cambios
        """)
        
        st.markdown("---")
        
        st.markdown("### 📧 ¿Quieres la integración automática?")
        st.info("Déjame un mensaje y priorizaré esta funcionalidad para ti")

# Add to sidebar in main app
def add_backup_reminder():
    """Add backup reminder to sidebar"""
    
    import sqlite3
    import os
    
    # Check if database exists and has data
    if os.path.exists("data/marathon_training.db"):
        conn = sqlite3.connect("data/marathon_training.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM completed_workouts")
        workout_count = cursor.fetchone()[0]
        
        conn.close()
        
        if workout_count > 0:
            days_since_backup = 7  # Placeholder - should track last backup
            
            if days_since_backup >= 7:
                st.sidebar.warning(f"""
                ⚠️ **Recordatorio de Backup**
                
                Tienes {workout_count} entrenamientos registrados.
                
                Última copia: Hace {days_since_backup} días
                
                [Hacer backup ahora →](#backup)
                """)

if __name__ == "__main__":
    create_backup_page()

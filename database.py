import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

DB_PATH = "data/marathon_training.db"

def init_db():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Training plan table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            description TEXT,
            distance_km REAL,
            duration_min INTEGER,
            target_pace TEXT,
            intensity TEXT,
            notes TEXT,
            UNIQUE(date)
        )
    """)
    
    # Completed workouts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            distance_km REAL,
            duration_min INTEGER,
            avg_pace TEXT,
            avg_hr INTEGER,
            max_hr INTEGER,
            calories INTEGER,
            feeling INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, workout_type)
        )
    """)
    
    # Menstrual cycle tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menstrual_cycle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cycle_start_date TEXT NOT NULL,
            cycle_length INTEGER DEFAULT 28,
            notes TEXT
        )
    """)
    
    # Body metrics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS body_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            weight_kg REAL,
            resting_hr INTEGER,
            sleep_hours REAL,
            energy_level INTEGER,
            soreness_level INTEGER,
            notes TEXT,
            UNIQUE(date)
        )
    """)
    
    # Nutrition log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            meal_type TEXT,
            description TEXT,
            carbs_g REAL,
            protein_g REAL,
            fats_g REAL,
            calories INTEGER,
            timing TEXT
        )
    """)
    
    # User settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            weight_kg REAL,
            max_hr INTEGER,
            goal_time TEXT,
            race_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def populate_training_plan():
    """Populate the 8-week training plan"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if plan already exists
    cursor.execute("SELECT COUNT(*) FROM training_plan")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Start date: March 1, 2026
    start_date = datetime(2026, 3, 1)
    
    # 8-week plan structure - DOMINGO = RODAJE LARGO
    plan = [
        # SEMANA 1 (1-7 Marzo) - Menstruación + Adaptación - Comienza DOMINGO 1 MARZO
        {"week": 1, "day": 0, "type": "Rodaje largo", "desc": "12 km FÁCIL - practicar ratio 5:1 (Galloway) | Ritmo conversacional", "km": 12, "min": 95, "pace": "7:55/km", "intensity": "Moderada"},
        {"week": 1, "day": 1, "type": "Descanso", "desc": "Día 2 menstruación - recuperación post rodaje largo", "km": 0, "min": 0, "pace": "", "intensity": "Muy baja"},
        {"week": 1, "day": 2, "type": "Fuerza A", "desc": "SESIÓN A - Glúteo + Rodilla | PREVIO: Activación glúteos 5min (clamshells 2x15/lado, monster walks 2x10pasos, fire hydrants 2x12/lado) | Calent: 5min trote + movilidad cadera | 1) Hip Thrust 4x12 (25kg) tempo 3-1-1 desc 90s PRIORIDAD | 2) Terminal Knee Extension 3x15/lado (banda) - VMO específico | 3) Split Squat Isométrico 3x30s/lado (6kg c/mano) - NO bajar más de 90° rodilla | 4) Peso Muerto Rumano Unilateral 3x10/lado (12kg) tempo 3-1-1 desc 75s - extra tiempo pierna DERECHA | 5) Puente glúteo unilateral 4x12/lado tempo 2-2-1 desc 60s | 6) Plancha frontal 3x40s | Correctivo: Foam roller IT band izq 3min + estiramiento cuádriceps | Enfriamiento: estiramientos estáticos 12min", "km": 0, "min": 55, "pace": "", "intensity": "Moderada"},
        {"week": 1, "day": 3, "type": "Carrera suave", "desc": "Rodaje fácil conversacional 5 km + técnica de carrera (talones a glúteos, rodillas arriba, skipping)", "km": 5, "min": 35, "pace": "7:00/km", "intensity": "Baja"},
        {"week": 1, "day": 4, "type": "Fuerza B", "desc": "SESIÓN B - Estabilidad + VMO | PREVIO: Activación glúteo medio 5min (side plank hip abduction 2x10/lado, lateral band walks 2x15pasos) | Calent: 5min trote + movilidad | 1) Step-up bajo (15cm) 3x12/lado (6kg c/mano) tempo 2-0-1 desc 60s - control rodilla en línea | 2) Copenhagen Plank 3x20s/lado desc 60s | 3) VMO Dips (Wall sit slides) 3x15 tempo 2-0-2 desc 45s | 4) Elevación talones unilateral 3x15/lado (10kg) tempo 2-2-1 desc 45s | 5) Side-lying Hip Abduction 3x15/lado (banda) - glúteo medio | 6) Dead bug 3x12/lado desc 45s | 7) Clamshells 3x15/lado (banda media-pesada) | Correctivo: Liberación TFL con pelota 2min/lado + IT band foam roller 3min lado izq | Enfriamiento: estiramiento profundo flexores cadera y cuádriceps", "km": 0, "min": 55, "pace": "", "intensity": "Moderada"},
        {"week": 1, "day": 5, "type": "Carrera", "desc": "Rodaje ritmo cómodo 6 km | Incluir 4 aceleraciones progresivas (strides) de 80m al final", "km": 6, "min": 42, "pace": "7:00/km", "intensity": "Moderada"},
        {"week": 1, "day": 6, "type": "Recuperación", "desc": "Yoga restaurativo 30min o caminata activa 40min + foam roller grupos musculares principales", "km": 0, "min": 40, "pace": "", "intensity": "Muy baja"},
        
        # SEMANA 2 (8-14 Marzo) - Fase Folicular Óptima - VENTANA DE ALTA INTENSIDAD
        {"week": 2, "day": 0, "type": "Rodaje largo", "desc": "16 km con ratio 5:1 | Primeros 11 km fáciles, últimos 5K a ritmo objetivo 7:40-7:50/km | Simular nutrición: gel KM 10", "km": 16, "min": 120, "pace": "7:30/km", "intensity": "Moderada-Alta"},
        {"week": 2, "day": 1, "type": "Carrera fácil", "desc": "Rodaje recuperación post-largo 6 km MUY suave | Ritmo conversacional", "km": 6, "min": 45, "pace": "7:30/km", "intensity": "Baja"},
        {"week": 2, "day": 2, "type": "Fuerza A", "desc": "SESIÓN A - Fuerza Máxima | Calent: 5min trote + movilidad dinámica | 1) Hip Thrust 4x12 (27kg) tempo 3-0-1 desc 90s | 2) Sentadilla Búlgara 3x10/lado (10kg c/mano) tempo 3-0-1 desc 75s | 3) Sentadilla Back 4x8 (40kg) tempo 3-0-1 desc 2min | 4) Peso Muerto Rumano 3x10 (32kg) tempo 3-1-1 desc 90s | 5) Plancha frontal 3x50s desc 60s | 6) Zancadas alternas 3x8/lado (8kg c/mano) | Enfriamiento: estiramientos + foam roller IT band", "km": 0, "min": 55, "pace": "", "intensity": "Alta"},
        {"week": 2, "day": 3, "type": "Intervalos", "desc": "Calent 2km fácil + movilidad | SERIE: 6x800m a 6:50-7:00/km (rec 2min trote suave) | Enfr 1km fácil | Total ~8km | Hidratación entre series", "km": 8, "min": 50, "pace": "6:15/km", "intensity": "Alta"},
        {"week": 2, "day": 4, "type": "Fuerza B", "desc": "SESIÓN B - Resistencia + Potencia | Calent: 5min trote + activación | 1) Estocadas caminando 3x12/lado (8kg c/mano) tempo 2-0-X desc 60s | 2) Sentadilla Jump 3x8 (solo peso corporal) explosivo desc 90s | 3) Step-up 3x10/lado (12kg c/mano) tempo 2-0-1 desc 60s | 4) Elevación talones 4x20 (17kg) tempo 2-2-1 desc 45s | 5) Dead bug 3x12/lado desc 45s | 6) Plancha lateral con elevación pierna 3x35s/lado | 7) Monster walks 3x10 pasos c/dirección (banda) | Enfriamiento: movilidad cadera", "km": 0, "min": 55, "pace": "", "intensity": "Alta"},
        {"week": 2, "day": 5, "type": "Tempo", "desc": "Calent 2km fácil | TEMPO: 5km a ritmo 7:20-7:30/km (ritmo de media maratón) | Enfr 1km suave | Mantener ritmo constante, respiración controlada", "km": 8, "min": 57, "pace": "7:07/km", "intensity": "Alta"},
        {"week": 2, "day": 6, "type": "Recuperación activa", "desc": "Trote regenerativo 3km MUY suave 10:00/km + estiramientos profundos 15min | Opcional: baño de contraste piernas", "km": 3, "min": 45, "pace": "10:00/km", "intensity": "Muy baja"},
        
        # SEMANA 3 (15-21 Marzo) - Fase Lútea Temprana
        {"week": 3, "day": 0, "type": "Rodaje largo", "desc": "20 km - IMPORTANTE practicar ratio 4:1 (el que usarás en carrera) | Calent 1km, luego 19km con ratio | Simular nutrición: geles KM 10 y 18 | Hidratación cada 5km", "km": 20, "min": 152, "pace": "7:36/km", "intensity": "Moderada-Alta"},
        {"week": 3, "day": 1, "type": "Descanso activo", "desc": "Día libre completo O caminata suave 30min | Priorizar recuperación", "km": 0, "min": 0, "pace": "", "intensity": "Muy baja"},
        {"week": 3, "day": 2, "type": "Fuerza A", "desc": "SESIÓN A - Fuerza Máxima | Calent: 5min trote + movilidad | 1) Hip Thrust 4x12 (30kg) tempo 3-1-1 desc 90s | 2) Sentadilla Back 4x8 (42kg) tempo 3-0-1 desc 2min | 3) Sentadilla Búlgara 3x10/lado (12kg c/mano) tempo 3-0-1 desc 75s | 4) Peso Muerto Rumano 4x8 (35kg) tempo 3-1-1 desc 90s | 5) Core: Plancha RKC 3x40s + Dead bug 3x10/lado + Bird dog 3x10/lado | Enfriamiento: estiramientos isquios y glúteos", "km": 0, "min": 60, "pace": "", "intensity": "Alta"},
        {"week": 3, "day": 3, "type": "Fartlek", "desc": "Calent 2km fácil | FARTLEK 30min: alternar 1min rápido (6:30-6:40/km) con 2min recuperación (8:00/km) x10 ciclos | Enfr 1km | Jugar con el ritmo, sentir la variabilidad", "km": 7, "min": 48, "pace": "6:51/km", "intensity": "Alta"},
        {"week": 3, "day": 4, "type": "Fuerza B", "desc": "SESIÓN B - Estabilidad + Potencia | Calent: 5min trote + activación glúteo medio | 1) Step-up explosivo 3x8/lado (10kg c/mano) explosivo desc 90s | 2) Pistol squat asistida 3x6/lado (TRX o barra) tempo 3-0-1 desc 90s | 3) Nordic hamstring curl 3x5 (asistido) tempo 4-0-1 desc 2min | 4) Estocadas laterales 3x10/lado (8kg c/mano) tempo 2-0-1 desc 60s | 5) Elevación talones unilateral 3x15/lado (12kg) tempo 2-2-1 desc 45s | 6) Plancha lateral star 3x30s/lado | 7) Copenhagen plank 3x20s/lado | Enfriamiento: foam roller completo", "km": 0, "min": 60, "pace": "", "intensity": "Alta"},
        {"week": 3, "day": 5, "type": "Ritmo objetivo", "desc": "Calent 2km | CORE: 10km a ritmo objetivo EXACTO 7:40-7:50/km (ritmo maratón) | Enfr 1km | Concentración mental, respiración rítmica | Este es TU ritmo de carrera", "km": 13, "min": 98, "pace": "7:32/km", "intensity": "Alta"},
        {"week": 3, "day": 6, "type": "Recuperación", "desc": "Yoga flow 40min enfocado en cadera y piernas O Pilates mat | Foam roller IT band, gemelos, cuádriceps 15min", "km": 0, "min": 55, "pace": "", "intensity": "Muy baja"},
        
        # SEMANA 4 (22-28 Marzo) - Fase Lútea Tardía - SEMANA DE DESCARGA (CRÍTICO)
        {"week": 4, "day": 0, "type": "Rodaje largo", "desc": "18 km FÁCIL - ratio 4:1 pero SIN FORZAR | Ritmo muy cómodo 7:45-8:00/km | Objetivo: kilómetros sin fatiga | Disfrutar el rodaje", "km": 18, "min": 140, "pace": "7:47/km", "intensity": "Moderada"},
        {"week": 4, "day": 1, "type": "Carrera suave", "desc": "Rodaje regenerativo 5km MUY fácil | Conversacional total | Observar sensaciones corporales", "km": 5, "min": 38, "pace": "7:36/km", "intensity": "Baja"},
        {"week": 4, "day": 2, "type": "Fuerza LIGERA", "desc": "DESCARGA - Mantenimiento | Calent: 10min movilidad articular | 1) Hip Thrust 3x8 (20kg) tempo 2-0-1 desc 60s | 2) Sentadilla Goblet 3x8 (10kg) tempo 2-0-1 desc 60s | 3) Peso Muerto Rumano 3x8 (25kg) tempo 2-0-1 desc 60s | 4) Estocadas estáticas 3x6/lado (6kg c/mano) tempo 2-0-1 desc 45s | 5) Core suave: plancha 3x30s, bird dog 3x8/lado | Pesos reducidos 40%, enfoque en técnica perfecta | Enfriamiento: estiramientos 15min", "km": 0, "min": 45, "pace": "", "intensity": "Baja"},
        {"week": 4, "day": 3, "type": "Técnica + Carrera", "desc": "Calent 1km | TÉCNICA: 5 series de ejercicios (talones glúteos, rodillas arriba, skipping, carioca, bounds) 40m c/u | Luego 5km ritmo cómodo 7:30/km | Enfr 1km | Enfoque en forma, no velocidad", "km": 7, "min": 50, "pace": "7:08/km", "intensity": "Baja"},
        {"week": 4, "day": 4, "type": "Fuerza LIGERA", "desc": "DESCARGA - Activación | Calent: 10min movilidad | 1) Sentadilla búlgara 3x6/lado (6kg c/mano) tempo 2-0-1 desc 60s | 2) Step-up 3x8/lado (8kg c/mano) tempo 2-0-1 desc 45s | 3) Puente glúteo 3x12 (15kg) tempo 2-1-1 desc 45s | 4) Plancha lateral 3x25s/lado | 5) Clamshells 3x12/lado (banda ligera) | 6) Monster walks 3x8 pasos | Enfriamiento: foam roller + masaje manual", "km": 0, "min": 45, "pace": "", "intensity": "Baja"},
        {"week": 4, "day": 5, "type": "Ritmo controlado", "desc": "Calent 2km fácil | 8km a ritmo objetivo 7:40-7:50/km CONTROLADO | Enfr 1km | Sin presión, mantener ritmo parejo", "km": 11, "min": 83, "pace": "7:32/km", "intensity": "Moderada"},
        {"week": 4, "day": 6, "type": "Movilidad", "desc": "Yoga restaurativo 45min | Énfasis en relajación, flexibilidad | Meditación 10min | Preparar cuerpo para semana pico", "km": 0, "min": 55, "pace": "", "intensity": "Muy baja"},
        
        # SEMANA 5 (29 Mar-4 Abr) - Nueva Menstruación + SEMANA PICO (Mayor volumen)
        {"week": 5, "day": 0, "type": "RODAJE LARGO PICO", "desc": "25 km - SIMULACIÓN DE CARRERA | Ratio 4:1 desde KM 1 | Ritmo 7:35-7:45/km | NUTRITION TEST: Geles KM 10, 18, 23 + hidratación cada 5K | Llevar cinturón porta-geles | Probar ropa de carrera | Mental: dividir en bloques de 5K", "km": 25, "min": 192, "pace": "7:40/km", "intensity": "Alta"},
        {"week": 5, "day": 1, "type": "Recuperación", "desc": "Día 1 menstruación - Trote regenerativo MUY suave 3km 8:20/km O caminar 40min | Priorizar descanso post-pico", "km": 3, "min": 30, "pace": "8:20/km", "intensity": "Muy baja"},
        {"week": 5, "day": 2, "type": "Fuerza A", "desc": "SESIÓN A - Mantenimiento | Calent: 5min trote + movilidad | 1) Hip Thrust 4x10 (28kg) tempo 2-0-1 desc 90s | 2) Sentadilla Back 3x8 (38kg) tempo 3-0-1 desc 90s | 3) Sentadilla búlgara 3x8/lado (10kg c/mano) tempo 2-0-1 desc 75s | 4) Peso muerto rumano 3x10 (32kg) tempo 3-0-1 desc 75s | 5) Core: Plancha 3x45s + Antirotación Pallof 3x10/lado + Dead bug 3x10/lado | No subir pesos, mantener calidad | Enfriamiento: estiramientos", "km": 0, "min": 55, "pace": "", "intensity": "Moderada"},
        {"week": 5, "day": 3, "type": "Carrera fácil", "desc": "Rodaje conversacional 6km sin presión | Escuchar al cuerpo, ritmo natural", "km": 6, "min": 44, "pace": "7:20/km", "intensity": "Baja"},
        {"week": 5, "day": 4, "type": "Fuerza B", "desc": "SESIÓN B - Resistencia | Calent: 5min + activación | 1) Estocadas caminando 3x10/lado (8kg c/mano) tempo 2-0-1 desc 60s | 2) Step-up 3x10/lado (10kg c/mano) tempo 2-0-1 desc 60s | 3) Puente glúteo unilateral 3x12/lado tempo 2-1-1 desc 45s | 4) Elevación talones 4x18 (15kg) tempo 2-1-2 desc 45s | 5) Plancha lateral 3x35s/lado | 6) Clamshells 3x15/lado (banda) | 7) Fire hydrants 3x12/lado | Enfriamiento: foam roller IT band y gemelos", "km": 0, "min": 50, "pace": "", "intensity": "Moderada"},
        {"week": 5, "day": 5, "type": "Tempo run", "desc": "Calent 2km fácil | TEMPO PROGRESIVO: 2km a 7:30/km + 4km a 7:20/km + 2km a 7:10/km | Enfr 2km suave | Total 12km | Progresión controlada, mantener forma", "km": 12, "min": 88, "pace": "7:20/km", "intensity": "Alta"},
        {"week": 5, "day": 6, "type": "Recuperación activa", "desc": "Trote suavísimo 3km 10:00/km + estiramientos profundos 20min | Baño caliente con sales de Epsom | Dormir temprano", "km": 3, "min": 50, "pace": "10:00/km", "intensity": "Muy baja"},
        
        # SEMANA 6 (5-11 Abril) - Fase Folicular - ÚLTIMA SEMANA DE CALIDAD
        {"week": 6, "day": 0, "type": "Rodaje largo", "desc": "22 km - ÚLTIMA DISTANCIA LARGA | Ratio 4:1 | Ritmo 7:40-7:50/km | Geles KM 10 y 18 | Práctica perfecta de hidratación | Terminar fuerte y con energía", "km": 22, "min": 172, "pace": "7:49/km", "intensity": "Moderada-Alta"},
        {"week": 6, "day": 1, "type": "Recuperación", "desc": "Rodaje fácil post-largo 5km ritmo cómodo | Caminar 2min cada 2km si es necesario", "km": 5, "min": 38, "pace": "7:36/km", "intensity": "Baja"},
        {"week": 6, "day": 2, "type": "Fuerza A - ÚLTIMA FUERTE", "desc": "ÚLTIMA SESIÓN DE CARGA | Calent: 5min trote + movilidad completa | 1) Hip Thrust 4x10 (30kg) tempo 3-1-1 desc 90s MÁXIMA CALIDAD | 2) Sentadilla Back 4x6 (44kg) tempo 3-0-1 desc 2min | 3) Sentadilla búlgara 3x8/lado (12kg c/mano) tempo 3-0-1 desc 90s | 4) Peso muerto rumano 4x8 (35kg) tempo 3-1-1 desc 90s | 5) Nordic curl 3x4 (asistido) tempo 4-0-1 | 6) Core avanzado: RKC plank 3x30s + Pallof 3x12/lado + Suitcase carry 3x20m/lado (16kg) | Esta es tu última sesión pesada - dar el 100% | Enfriamiento completo 15min", "km": 0, "min": 65, "pace": "", "intensity": "Alta"},
        {"week": 6, "day": 3, "type": "Intervalos - ÚLTIMA CALIDAD", "desc": "Calent 2km + drills | SERIES: 5x1000m a ritmo 6:50-7:00/km (rec 2:30 trote) | Enfr 2km | Mantener consistencia en todas las series | Respiración controlada", "km": 11, "min": 65, "pace": "6:54/km", "intensity": "Alta"},
        {"week": 6, "day": 4, "type": "Fuerza B", "desc": "SESIÓN FINAL DE CONSTRUCCIÓN | Calent: 5min + activación glúteos | 1) Step-up 3x10/lado (12kg c/mano) tempo 2-0-X desc 75s | 2) Estocadas búlgaras saltadas 3x6/lado (peso corporal) explosivo desc 90s | 3) Peso muerto unilateral 3x8/lado (18kg) tempo 3-0-1 desc 75s | 4) Elevación talones unilateral 3x12/lado (12kg) tempo 2-2-1 desc 60s | 5) Plancha lateral con rotación 3x8/lado | 6) Copenhagen plank 3x25s/lado | 7) Band walks lateral 3x12 pasos c/dirección | Enfriamiento: foam roller completo + masaje", "km": 0, "min": 60, "pace": "", "intensity": "Moderada-Alta"},
        {"week": 6, "day": 5, "type": "Ritmo objetivo", "desc": "Calent 2km | SIMULACIÓN MENTAL: 12km a ritmo EXACTO de carrera 7:40-7:50/km | Enfr 1km | Concentración total, este es TU ritmo | Visualizar el maratón", "km": 15, "min": 116, "pace": "7:44/km", "intensity": "Alta"},
        {"week": 6, "day": 6, "type": "Movilidad", "desc": "Yoga flow 50min completo | Estiramientos pasivos 20min | Foam roller todo el cuerpo | Preparación mental para tapering", "km": 0, "min": 70, "pace": "", "intensity": "Muy baja"},
        
        # SEMANA 7 (12-18 Abril) - TAPERING FASE 1 (Reducción 40%)
        {"week": 7, "day": 0, "type": "Rodaje medio", "desc": "14 km FÁCIL | Ratio 4:1 practicar SIN esfuerzo | Ritmo 7:45-8:00/km | Objetivo: mantener sensación, NO acumular fatiga | Disfrutar", "km": 14, "min": 110, "pace": "7:51/km", "intensity": "Baja"},
        {"week": 7, "day": 1, "type": "Descanso", "desc": "Día libre COMPLETO | Caminar max 20min suave | Masaje profesional recomendado | Hidratación abundante", "km": 0, "min": 0, "pace": "", "intensity": "Muy baja"},
        {"week": 7, "day": 2, "type": "Fuerza SUAVE - Activación", "desc": "TAPERING - Solo activación neuromuscular | Calent: 10min movilidad articular | 1) Hip Thrust 2x8 (20kg) tempo 2-0-1 desc 60s | 2) Sentadilla Goblet 2x8 (10kg) tempo 2-0-1 desc 60s | 3) Estocadas estáticas 2x6/lado (6kg c/mano) tempo 2-0-1 desc 45s | 4) Puente glúteo 2x10 (solo peso) tempo 2-1-1 | 5) Plancha 2x30s | 6) Clamshells 2x12/lado | Pesos LIGEROS, movimiento de calidad | Enfriamiento: estiramientos suaves 15min", "km": 0, "min": 35, "pace": "", "intensity": "Baja"},
        {"week": 7, "day": 3, "type": "Carrera fácil", "desc": "Rodaje conversacional 6km | Sentir las piernas frescas | Sin reloj, por sensaciones", "km": 6, "min": 48, "pace": "8:00/km", "intensity": "Baja"},
        {"week": 7, "day": 4, "type": "Descanso activo", "desc": "Yoga suave 30min O caminata 30min | Foam roller 15min | Visualización positiva de la carrera", "km": 0, "min": 45, "pace": "", "intensity": "Muy baja"},
        {"week": 7, "day": 5, "type": "Calidad corta", "desc": "Calent 2km muy suave | 4x800m a ritmo objetivo 7:40/km (rec 2min caminando) | Enfr 2km muy suave | Total 6km | Mantener sensación de ritmo, NO cansar", "km": 6, "min": 48, "pace": "8:00/km", "intensity": "Moderada"},
        {"week": 7, "day": 6, "type": "Movilidad", "desc": "Estiramientos completos 30min | Meditación 15min | Revisión mental del plan de carrera | Dormir 9 horas", "km": 0, "min": 45, "pace": "", "intensity": "Muy baja"},
        
        # SEMANA 8 (19-25 Abril) - TAPERING FINAL + PUESTA A PUNTO
        {"week": 8, "day": 0, "type": "Shakeout run", "desc": "Trote suavísimo 15 min + 4 strides de 80m progresivos (NO sprints) | Sentir ligereza en las piernas | Sonreír", "km": 3, "min": 25, "pace": "8:20/km", "intensity": "Muy baja"},
        {"week": 8, "day": 1, "type": "Descanso", "desc": "NADA de ejercicio | Caminar casual OK | Hidratación | Comenzar carga de carbohidratos (7g/kg)", "km": 0, "min": 0, "pace": "", "intensity": "Muy baja"},
        {"week": 8, "day": 2, "type": "Activación mínima", "desc": "Solo movilidad articular 15min | Clamshells 2x10/lado | Monster walks 2x8 pasos | Plancha 2x20s | SIN sudor, solo activar | Estiramientos suaves", "km": 0, "min": 25, "pace": "", "intensity": "Muy baja"},
        {"week": 8, "day": 3, "type": "Carrera suave", "desc": "Rodaje fácil 5 km | Ritmo cómodo sin mirar reloj | Sentir las piernas | Último rodaje antes de la batalla", "km": 5, "min": 42, "pace": "8:24/km", "intensity": "Baja"},
        {"week": 8, "day": 4, "type": "Test corto", "desc": "Calent 3km muy fácil | 3x400m a ritmo de carrera 7:40/km (rec 90s caminando) | Enfr 2km muy fácil | Total 6km | Solo para sentir el ritmo objetivo", "km": 6, "min": 50, "pace": "8:20/km", "intensity": "Moderada"},
        {"week": 8, "day": 5, "type": "Descanso", "desc": "DÍA LIBRE | Caminata suave 20min máximo | Hidratación + electrolitos | Continuar carga carbos | Masaje ligero si lo deseas | Dormir temprano", "km": 0, "min": 0, "pace": "", "intensity": "Muy baja"},
        {"week": 8, "day": 6, "type": "PRE-CARRERA", "desc": "DESCANSO TOTAL | Solo movilidad suave 10min | Preparar TODO: número, ropa, geles (4), cinturón, reloj cargado | Cena: pasta + pollo | Revisar plan de carrera | Dormir 9 horas | Mañana es EL DÍA", "km": 0, "min": 10, "pace": "", "intensity": "Muy baja"},
    ]
    
    # Insert plan
    for entry in plan:
        day_offset = (entry["week"] - 1) * 7 + entry["day"]
        workout_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT OR IGNORE INTO training_plan 
            (week, day_of_week, date, workout_type, description, distance_km, 
             duration_min, target_pace, intensity, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["week"], 
            entry["day"], 
            workout_date,
            entry["type"],
            entry["desc"],
            entry["km"],
            entry["min"],
            entry["pace"],
            entry["intensity"],
            ""
        ))
    
    conn.commit()
    conn.close()

def get_training_plan(week=None):
    """Get training plan, optionally filtered by week"""
    conn = sqlite3.connect(DB_PATH)
    if week:
        df = pd.read_sql_query(
            "SELECT * FROM training_plan WHERE week = ? ORDER BY date",
            conn, params=(week,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM training_plan ORDER BY date",
            conn
        )
    conn.close()
    return df

def get_completed_workouts(start_date=None, end_date=None):
    """Get completed workouts"""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM completed_workouts"
    params = []
    
    if start_date and end_date:
        query += " WHERE date BETWEEN ? AND ?"
        params = [start_date, end_date]
    elif start_date:
        query += " WHERE date >= ?"
        params = [start_date]
    
    query += " ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def add_workout(date, workout_type, distance_km, duration_min, avg_pace, 
                avg_hr=None, max_hr=None, calories=None, feeling=5, notes=""):
    """Add a completed workout"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO completed_workouts 
        (date, workout_type, distance_km, duration_min, avg_pace, avg_hr, 
         max_hr, calories, feeling, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, workout_type, distance_km, duration_min, avg_pace, avg_hr, 
          max_hr, calories, feeling, notes))
    
    conn.commit()
    conn.close()

def add_menstrual_cycle(start_date, cycle_length=28, notes=""):
    """Record menstrual cycle start"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO menstrual_cycle (cycle_start_date, cycle_length, notes)
        VALUES (?, ?, ?)
    """, (start_date, cycle_length, notes))
    
    conn.commit()
    conn.close()

def get_menstrual_cycles():
    """Get all menstrual cycle records"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM menstrual_cycle ORDER BY cycle_start_date DESC",
        conn
    )
    conn.close()
    return df

def add_body_metrics(date, weight_kg=None, resting_hr=None, sleep_hours=None, 
                     energy_level=None, soreness_level=None, notes=""):
    """Add body metrics for a date"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO body_metrics 
        (date, weight_kg, resting_hr, sleep_hours, energy_level, soreness_level, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, weight_kg, resting_hr, sleep_hours, energy_level, soreness_level, notes))
    
    conn.commit()
    conn.close()

def get_body_metrics(start_date=None, end_date=None):
    """Get body metrics"""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM body_metrics"
    params = []
    
    if start_date and end_date:
        query += " WHERE date BETWEEN ? AND ?"
        params = [start_date, end_date]
    
    query += " ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_weekly_summary(week):
    """Get weekly training summary"""
    conn = sqlite3.connect(DB_PATH)
    
    # Planned workouts
    planned = pd.read_sql_query(
        "SELECT * FROM training_plan WHERE week = ?",
        conn, params=(week,)
    )
    
    # Completed workouts
    if len(planned) > 0:
        start_date = planned['date'].min()
        end_date = planned['date'].max()
        completed = pd.read_sql_query(
            "SELECT * FROM completed_workouts WHERE date BETWEEN ? AND ?",
            conn, params=(start_date, end_date)
        )
    else:
        completed = pd.DataFrame()
    
    conn.close()
    
    return {
        'planned': planned,
        'completed': completed,
        'planned_km': planned['distance_km'].sum() if len(planned) > 0 else 0,
        'completed_km': completed['distance_km'].sum() if len(completed) > 0 else 0,
        'completion_rate': len(completed) / len(planned) * 100 if len(planned) > 0 else 0
    }

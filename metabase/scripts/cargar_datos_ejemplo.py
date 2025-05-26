#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para cargar datos de ejemplo en PostgreSQL para visualizarlos en Metabase.
Este script genera datos simulados para el proceso ETL y los carga en las tablas correspondientes.
"""

import psycopg2
import random
import datetime
import argparse
import sys
from faker import Faker
import os

# Configurar generador de datos falsos
fake = Faker()

# Parámetros de conexión a PostgreSQL
DB_PARAMS = {
    'dbname': os.environ.get('DB_NAME', 'dataengineering'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432')
}

# Categorías de ejemplo para los datos
CATEGORIES = ['ventas', 'marketing', 'finanzas', 'operaciones', 'rrhh']
SOURCES = ['api', 'csv', 'database', 'web_scraping', 'manual']
METRICS = ['ingresos', 'gastos', 'conversiones', 'usuarios_activos', 'tiempo_sesion', 
          'tasa_rebote', 'tasa_conversion', 'costo_adquisicion', 'retorno_inversion']
DIMENSIONS = ['region', 'producto', 'canal', 'segmento', 'campaña']
DIMENSION_VALUES = {
    'region': ['norte', 'sur', 'este', 'oeste', 'central'],
    'producto': ['software', 'hardware', 'servicios', 'consultoría', 'soporte'],
    'canal': ['directo', 'online', 'distribuidor', 'mayorista', 'minorista'],
    'segmento': ['enterprise', 'pyme', 'consumidor', 'gobierno', 'educación'],
    'campaña': ['email', 'social_media', 'display', 'search', 'evento']
}

def create_tables(conn):
    """Crear las tablas necesarias si no existen"""
    cursor = conn.cursor()
    
    # Tabla para datos crudos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_data (
        id SERIAL PRIMARY KEY,
        source VARCHAR(50) NOT NULL,
        data TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL
    );
    """)
    
    # Tabla para datos procesados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_data (
        id SERIAL PRIMARY KEY,
        raw_id INTEGER REFERENCES raw_data(id),
        processed_value DECIMAL(10,2) NOT NULL,
        category VARCHAR(50) NOT NULL,
        processed_date TIMESTAMP NOT NULL
    );
    """)
    
    # Tabla para datos finales (métricas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS final_data (
        id SERIAL PRIMARY KEY,
        processed_id INTEGER REFERENCES processed_data(id),
        metric_name VARCHAR(50) NOT NULL,
        metric_value DECIMAL(10,2) NOT NULL,
        dimension1 VARCHAR(50) NOT NULL,
        dimension2 VARCHAR(50) NOT NULL,
        report_date TIMESTAMP NOT NULL
    );
    """)
    
    # Tabla para métricas de ETL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etl_metrics (
        id SERIAL PRIMARY KEY,
        process_name VARCHAR(50) NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        records_processed INTEGER NOT NULL,
        success BOOLEAN NOT NULL,
        error_message TEXT,
        execution_date DATE NOT NULL
    );
    """)
    
    conn.commit()
    cursor.close()

def generate_raw_data(conn, num_records):
    """Generar datos crudos aleatorios"""
    cursor = conn.cursor()
    
    for _ in range(num_records):
        source = random.choice(SOURCES)
        data = fake.json()
        timestamp = fake.date_time_between(start_date='-30d', end_date='now')
        
        cursor.execute(
            "INSERT INTO raw_data (source, data, timestamp) VALUES (%s, %s, %s) RETURNING id",
            (source, data, timestamp)
        )
        raw_id = cursor.fetchone()[0]
        
        # Generar procesados inmediatamente
        generate_processed_data(conn, cursor, raw_id, timestamp)
    
    conn.commit()
    cursor.close()

def generate_processed_data(conn, cursor, raw_id, timestamp):
    """Generar datos procesados basados en los datos crudos"""
    processed_value = round(random.uniform(100, 10000), 2)
    category = random.choice(CATEGORIES)
    processed_date = timestamp + datetime.timedelta(minutes=random.randint(5, 60))
    
    cursor.execute(
        "INSERT INTO processed_data (raw_id, processed_value, category, processed_date) VALUES (%s, %s, %s, %s) RETURNING id",
        (raw_id, processed_value, category, processed_date)
    )
    processed_id = cursor.fetchone()[0]
    
    # Generar datos finales inmediatamente
    generate_final_data(conn, cursor, processed_id, processed_date)

def generate_final_data(conn, cursor, processed_id, processed_date):
    """Generar datos finales basados en los datos procesados"""
    for _ in range(random.randint(1, 3)):
        metric_name = random.choice(METRICS)
        metric_value = round(random.uniform(10, 1000), 2)
        
        dimension1 = random.choice(list(DIMENSION_VALUES.keys()))
        dimension2 = random.choice(list(DIMENSION_VALUES.keys()))
        while dimension2 == dimension1:
            dimension2 = random.choice(list(DIMENSION_VALUES.keys()))
            
        dimension1_value = random.choice(DIMENSION_VALUES[dimension1])
        dimension2_value = random.choice(DIMENSION_VALUES[dimension2])
        
        report_date = processed_date + datetime.timedelta(minutes=random.randint(5, 60))
        
        cursor.execute(
            "INSERT INTO final_data (processed_id, metric_name, metric_value, dimension1, dimension2, report_date) VALUES (%s, %s, %s, %s, %s, %s)",
            (processed_id, metric_name, metric_value, dimension1_value, dimension2_value, report_date)
        )

def generate_etl_metrics(conn, num_processes):
    """Generar métricas de ETL simuladas"""
    cursor = conn.cursor()
    
    process_names = ['extract', 'transform', 'load', 'full_etl']
    
    for _ in range(num_processes):
        process_name = random.choice(process_names)
        execution_date = fake.date_between(start_date='-30d', end_date='now')
        
        # Calcular tiempos de ejecución
        start_time = datetime.datetime.combine(
            execution_date, 
            datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
        )
        
        # Duración entre 10 segundos y 15 minutos
        duration = datetime.timedelta(seconds=random.randint(10, 900))
        end_time = start_time + duration
        
        records_processed = random.randint(100, 10000)
        success = random.random() > 0.1  # 90% de éxito
        error_message = None if success else fake.sentence()
        
        cursor.execute(
            "INSERT INTO etl_metrics (process_name, start_time, end_time, records_processed, success, error_message, execution_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (process_name, start_time, end_time, records_processed, success, error_message, execution_date)
        )
    
    conn.commit()
    cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Generar datos de ejemplo para visualizar en Metabase')
    parser.add_argument('--raw', type=int, default=100, help='Número de registros crudos a generar')
    parser.add_argument('--etl', type=int, default=50, help='Número de métricas de ETL a generar')
    parser.add_argument('--reset', action='store_true', help='Eliminar datos existentes antes de insertar')
    
    args = parser.parse_args()
    
    try:
        # Conectar a la base de datos
        print(f"Conectando a PostgreSQL en {DB_PARAMS['host']}:{DB_PARAMS['port']}...")
        conn = psycopg2.connect(**DB_PARAMS)
        
        # Resetear tablas si se especifica
        if args.reset:
            cursor = conn.cursor()
            print("Eliminando datos existentes...")
            cursor.execute("DELETE FROM final_data;")
            cursor.execute("DELETE FROM processed_data;")
            cursor.execute("DELETE FROM raw_data;")
            cursor.execute("DELETE FROM etl_metrics;")
            conn.commit()
            cursor.close()
        
        # Crear tablas
        create_tables(conn)
        
        # Generar datos
        print(f"Generando {args.raw} registros de datos crudos...")
        generate_raw_data(conn, args.raw)
        
        print(f"Generando {args.etl} métricas de ETL...")
        generate_etl_metrics(conn, args.etl)
        
        print("Datos generados correctamente.")
        print("Ahora puedes visualizar estos datos en Metabase en http://localhost:3000")
        
        # Cerrar conexión
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

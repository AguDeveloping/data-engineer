"""
Este archivo contiene ejemplos de cómo usar SQLAlchemy correctamente en notebooks de Jupyter
para insertar datos en PostgreSQL con parámetros.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import create_engine
import os

# Función para convertir tipos NumPy a tipos nativos de Python
def numpy_to_python(obj):
    """Convierte tipos de NumPy a tipos nativos de Python para serialización JSON"""
    if isinstance(obj, (np.integer)):
        return int(obj)
    elif isinstance(obj, (np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    else:
        return obj

# Ejemplo 1: Usando text() de SQLAlchemy con bindparams
def ejemplo_sqlalchemy_text():
    # Configuración de la conexión a la base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/dataengineering')
    engine = create_engine(DATABASE_URL)
    
    # Crear datos de ejemplo
    data = {
        'producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
        'categoria': ['Electrónica', 'Hogar', 'Electrónica', 'Hogar'],
        'region': ['Norte', 'Sur', 'Norte', 'Este'],
        'cantidad': [10, 5, 8, 12],
        'precio_unitario': [100.50, 200.75, 150.25, 75.80],
        'total_venta': [1005.0, 1003.75, 1202.0, 909.60]
    }
    df = pd.DataFrame(data)
    
    # Crear datos simulados de una API
    api_data = {
        'resumen_ventas': {
            'total_ventas': df['total_venta'].sum(),
            'promedio_venta': df['total_venta'].mean(),
            'max_venta': df['total_venta'].max(),
            'min_venta': df['total_venta'].min(),
            'total_productos': df['cantidad'].sum(),
            'fecha_reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'ventas_por_categoria': df.groupby('categoria')['total_venta'].sum().to_dict(),
        'ventas_por_region': df.groupby('region')['total_venta'].sum().to_dict()
    }
    
    # Método 1: Usando text() con la sintaxis de SQLAlchemy (:nombre)
    with engine.connect() as conn:
        # Crear la consulta con text() y usar :nombre para los parámetros
        insert_query = text("INSERT INTO raw_data (timestamp, source, data) VALUES (:timestamp, :source, :data)")
        
        # Ejecutar la consulta con los parámetros
        conn.execute(
            insert_query,
            {
                'timestamp': datetime.now().isoformat(),
                'source': 'api_simulada',
                'data': json.dumps(api_data, default=numpy_to_python)
            }
        )
    
    print("Método 1: Datos insertados correctamente usando text() con :nombre")

# Ejemplo 2: Usando execute() directamente con la sintaxis de psycopg2
def ejemplo_execute_directo():
    # Configuración de la conexión a la base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/dataengineering')
    engine = create_engine(DATABASE_URL)
    
    # Crear datos de ejemplo
    data = {
        'producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
        'categoria': ['Electrónica', 'Hogar', 'Electrónica', 'Hogar'],
        'region': ['Norte', 'Sur', 'Norte', 'Este'],
        'cantidad': [10, 5, 8, 12],
        'precio_unitario': [100.50, 200.75, 150.25, 75.80],
        'total_venta': [1005.0, 1003.75, 1202.0, 909.60]
    }
    df = pd.DataFrame(data)
    
    # Crear datos simulados de una API
    api_data = {
        'resumen_ventas': {
            'total_ventas': df['total_venta'].sum(),
            'promedio_venta': df['total_venta'].mean(),
            'max_venta': df['total_venta'].max(),
            'min_venta': df['total_venta'].min(),
            'total_productos': df['cantidad'].sum(),
            'fecha_reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'ventas_por_categoria': df.groupby('categoria')['total_venta'].sum().to_dict(),
        'ventas_por_region': df.groupby('region')['total_venta'].sum().to_dict()
    }
    
    # Método 2: Usando execute() directamente con la sintaxis de psycopg2
    # IMPORTANTE: Esto solo funciona si no usas text() de SQLAlchemy
    with engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            "INSERT INTO raw_data (timestamp, source, data) VALUES (%(timestamp)s, %(source)s, %(data)s)",
            {
                'timestamp': datetime.now().isoformat(),
                'source': 'api_simulada_directo',
                'data': json.dumps(api_data, default=numpy_to_python)
            }
        )
    
    print("Método 2: Datos insertados correctamente usando execute() directo con %(nombre)s")

if __name__ == "__main__":
    ejemplo_sqlalchemy_text()
    ejemplo_execute_directo()

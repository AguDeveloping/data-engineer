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

# Configuración de la conexión a la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/dataengineering')
engine = create_engine(DATABASE_URL)

# Asumiendo que ya tienes un DataFrame df con datos
# Si no lo tienes, aquí hay un ejemplo para crear uno:
data = {
    'producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D'],
    'categoria': ['Electrónica', 'Hogar', 'Electrónica', 'Hogar'],
    'region': ['Norte', 'Sur', 'Norte', 'Este'],
    'cantidad': [10, 5, 8, 12],
    'precio_unitario': [100.50, 200.75, 150.25, 75.80],
    'total_venta': [1005.0, 1003.75, 1202.0, 909.60]
}
df = pd.DataFrame(data)

# Simular datos de una API
# En un caso real, usaríamos extract_from_api con una URL real

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

# En un caso real, estos datos vendrían de una API
# Pero aquí los insertamos directamente
with engine.connect() as conn:
    # Usar la sintaxis correcta para PostgreSQL con psycopg2
    conn.execute(
        "INSERT INTO raw_data (timestamp, source, data) VALUES (%(timestamp)s, %(source)s, %(data)s)",
        {
            'timestamp': datetime.now().isoformat(),
            'source': 'api_simulada',
            'data': json.dumps(api_data, default=numpy_to_python)  # Usamos la función personalizada para serializar
        }
    )

print("Datos de API simulada insertados en raw_data.")

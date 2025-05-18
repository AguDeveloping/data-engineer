import pandas as pd
import json
import os
from datetime import datetime
from ..utils.database import engine

def extract_from_csv(file_path, source_name):
    """
    Extrae datos desde un archivo CSV y los guarda en la tabla raw_data
    
    Args:
        file_path (str): Ruta al archivo CSV
        source_name (str): Nombre de la fuente de datos
    
    Returns:
        int: Número de registros extraídos
    """
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        
        # Preparar los datos para inserción
        records = []
        for _, row in df.iterrows():
            record = {
                'timestamp': datetime.now().isoformat(),
                'source': source_name,
                'data': json.dumps(row.to_dict())
            }
            records.append(record)
        
        # Insertar en la base de datos
        with engine.connect() as conn:
            result = conn.execute(
                "INSERT INTO raw_data (timestamp, source, data) VALUES (:timestamp, :source, :data)",
                records
            )
        
        return len(records)
    
    except Exception as e:
        print(f"Error al extraer datos: {e}")
        return 0

def extract_from_api(api_url, params=None, source_name="api"):
    """
    Extrae datos desde una API y los guarda en la tabla raw_data
    
    Args:
        api_url (str): URL de la API
        params (dict): Parámetros para la solicitud API
        source_name (str): Nombre de la fuente de datos
    
    Returns:
        int: Número de registros extraídos
    """
    try:
        import requests
        
        # Realizar la solicitud a la API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Verificar si hay errores
        
        # Convertir respuesta a JSON
        data = response.json()
        
        # Preparar registro para la base de datos
        record = {
            'timestamp': datetime.now().isoformat(),
            'source': source_name,
            'data': json.dumps(data)
        }
        
        # Insertar en la base de datos
        with engine.connect() as conn:
            conn.execute(
                "INSERT INTO raw_data (timestamp, source, data) VALUES (:timestamp, :source, :data)",
                record
            )
        
        return 1
    
    except Exception as e:
        print(f"Error al extraer datos de la API: {e}")
        return 0

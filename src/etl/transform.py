import pandas as pd
import json
from sqlalchemy import text
from ..utils.database import engine

def transform_raw_data(raw_data_id=None):
    """
    Transforma los datos crudos y los guarda en la tabla processed_data
    
    Args:
        raw_data_id (int, optional): ID del registro a transformar. Si es None, procesa todos los registros no procesados.
    
    Returns:
        int: Nu00famero de registros transformados
    """
    try:
        # Construir la consulta SQL
        if raw_data_id:
            query = text("""
                SELECT id, data FROM raw_data 
                WHERE id = :raw_data_id AND id NOT IN (SELECT raw_data_id FROM processed_data WHERE raw_data_id IS NOT NULL)
            """)
            params = {"raw_data_id": raw_data_id}
        else:
            query = text("""
                SELECT id, data FROM raw_data 
                WHERE id NOT IN (SELECT raw_data_id FROM processed_data WHERE raw_data_id IS NOT NULL)
            """)
            params = {}
        
        # Ejecutar la consulta
        with engine.connect() as conn:
            results = conn.execute(query, params).fetchall()
            
            if not results:
                print("No hay nuevos datos para transformar")
                return 0
            
            # Transformar cada registro
            processed_records = []
            for row in results:
                raw_id = row[0]
                data = json.loads(row[1])
                
                # Aplicar transformaciones (ejemplo)
                processed_data = clean_and_transform(data)
                
                # Preparar registro para inserciu00f3n
                processed_record = {
                    'raw_data_id': raw_id,
                    'data': json.dumps(processed_data)
                }
                processed_records.append(processed_record)
            
            # Insertar registros procesados
            if processed_records:
                conn.execute(
                    text("INSERT INTO processed_data (raw_data_id, data) VALUES (:raw_data_id, :data)"),
                    processed_records
                )
            
            return len(processed_records)
    
    except Exception as e:
        print(f"Error al transformar datos: {e}")
        return 0

def clean_and_transform(data):
    """
    Aplica limpieza y transformaciones a los datos
    
    Args:
        data (dict): Datos a transformar
    
    Returns:
        dict: Datos transformados
    """
    # Convertir a DataFrame para facilitar las transformaciones
    df = pd.DataFrame([data])
    
    # Ejemplo de transformaciones:
    # 1. Convertir columnas a minu00fasculas
    df.columns = [col.lower() for col in df.columns]
    
    # 2. Rellenar valores nulos
    df = df.fillna(0)
    
    # 3. Eliminar columnas no necesarias (ejemplo)
    columns_to_drop = [col for col in df.columns if col.startswith('temp_')]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    
    # Convertir de nuevo a diccionario
    return df.iloc[0].to_dict()

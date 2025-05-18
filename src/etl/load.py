import json
from sqlalchemy import text
from ..utils.database import engine

def load_to_final_table(processed_data_id=None):
    """
    Carga los datos procesados en la tabla final_data
    
    Args:
        processed_data_id (int, optional): ID del registro procesado a cargar. Si es None, carga todos los registros no cargados.
    
    Returns:
        int: Nu00famero de registros cargados
    """
    try:
        # Construir la consulta SQL
        if processed_data_id:
            query = text("""
                SELECT id, data FROM processed_data 
                WHERE id = :processed_data_id AND id NOT IN (SELECT processed_data_id FROM final_data WHERE processed_data_id IS NOT NULL)
            """)
            params = {"processed_data_id": processed_data_id}
        else:
            query = text("""
                SELECT id, data FROM processed_data 
                WHERE id NOT IN (SELECT processed_data_id FROM final_data WHERE processed_data_id IS NOT NULL)
            """)
            params = {}
        
        # Ejecutar la consulta
        with engine.connect() as conn:
            results = conn.execute(query, params).fetchall()
            
            if not results:
                print("No hay nuevos datos procesados para cargar")
                return 0
            
            # Preparar cada registro para la tabla final
            final_records = []
            for row in results:
                processed_id = row[0]
                data = json.loads(row[1])
                
                # Calcular mu00e9tricas e insights (ejemplo)
                metrics, insights = calculate_metrics_and_insights(data)
                
                # Preparar registro para inserciu00f3n
                final_record = {
                    'processed_data_id': processed_id,
                    'metrics': json.dumps(metrics),
                    'insights': insights
                }
                final_records.append(final_record)
            
            # Insertar registros finales
            if final_records:
                conn.execute(
                    text("INSERT INTO final_data (processed_data_id, metrics, insights) VALUES (:processed_data_id, :metrics, :insights)"),
                    final_records
                )
            
            return len(final_records)
    
    except Exception as e:
        print(f"Error al cargar datos finales: {e}")
        return 0

def calculate_metrics_and_insights(data):
    """
    Calcula mu00e9tricas e insights a partir de los datos procesados
    
    Args:
        data (dict): Datos procesados
    
    Returns:
        tuple: (metrics, insights) donde metrics es un diccionario y insights es un texto
    """
    # Ejemplo de cu00e1lculo de mu00e9tricas
    metrics = {}
    
    # Calcular totales, promedios, etc. segu00fan los datos disponibles
    numeric_values = [val for val in data.values() if isinstance(val, (int, float))]
    if numeric_values:
        metrics['sum'] = sum(numeric_values)
        metrics['avg'] = sum(numeric_values) / len(numeric_values)
        metrics['max'] = max(numeric_values)
        metrics['min'] = min(numeric_values)
    
    # Generar insights basados en las mu00e9tricas (ejemplo simple)
    insights = f"Los datos muestran un valor promedio de {metrics.get('avg', 'N/A')}. "
    
    if 'max' in metrics and 'min' in metrics:
        range_val = metrics['max'] - metrics['min']
        insights += f"El rango de valores es {range_val}, lo que indica "
        
        if range_val > 100:
            insights += "una alta variabilidad en los datos."
        else:
            insights += "una baja variabilidad en los datos."
    
    return metrics, insights

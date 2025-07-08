# Código corregido para insertar datos en la tabla raw_data

# Insertar datos en la tabla raw_data
for _, row in df.iterrows():
    # Convertir el timestamp a string para que sea serializable
    row_dict = row.to_dict()
    
    # Convertir el objeto Timestamp a string si existe
    if 'fecha' in row_dict:
        row_dict['fecha'] = str(row_dict['fecha'])
    
    # Convertir a formato JSON
    data_json = json.dumps(row_dict)
    
    # Preparar la consulta de inserción
    insert_query = text("""
        INSERT INTO raw_data (timestamp, source, data)
        VALUES (%(timestamp)s, %(source)s, %(data)s)
    """)
    
    # Ejecutar la consulta
    connection.execute(insert_query, {
        'timestamp': datetime.datetime.now(),
        'source': 'ejemplo_notebook',
        'data': data_json
    })

print("Datos insertados correctamente en la tabla raw_data.")

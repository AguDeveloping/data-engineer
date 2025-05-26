# Imagen base de Python con Alpine
FROM python:3.9-alpine

WORKDIR /app

# Instalar dependencias necesarias para psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copiar e instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios para scripts
RUN mkdir -p /app/scripts /app/queries
RUN chmod 777 /app/scripts /app/queries

# Script de entrada
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Comando por defecto
CMD ["/app/entrypoint.sh"]

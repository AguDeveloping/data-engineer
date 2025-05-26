#!/bin/sh

# Configurar permisos para scripts Python
if [ -d /app/scripts ]; then
  find /app/scripts -name "*.py" -exec chmod +x {} \;
  echo "Scripts Python configurados correctamente"
fi

# Mostrar las variables de entorno para la conexión a la base de datos
echo "
Configuración de conexión a la base de datos:"
echo "- Host: $DB_HOST"
echo "- Puerto: $DB_PORT"
echo "- Base de datos: $DB_NAME"
echo "- Usuario: $DB_USER"
echo "
El contenedor de scripts Python está listo."
echo "Para ejecutar un script, usa:"
echo "docker exec -it proyecto-ingenieria-datos_python-scripts_1 python /app/scripts/cargar_datos_ejemplo.py --raw 200 --etl 100"
echo "
Manteniendo el contenedor en ejecución..."

# Mantener el contenedor en ejecución
exec tail -f /dev/null

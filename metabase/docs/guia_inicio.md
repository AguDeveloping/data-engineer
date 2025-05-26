# Guía de Inicio con Metabase

Esta guía proporciona instrucciones paso a paso para acceder y configurar Metabase, una plataforma de análisis y visualización de datos de código abierto que se conecta a la base de datos PostgreSQL que está ejecutándose en un contenedor Docker como parte de este proyecto.

## Requisitos previos

- Contenedores Docker en ejecución (incluidos PostgreSQL y Metabase)
- Navegador web moderno
- Conocimientos básicos de SQL (opcional para consultas avanzadas)

## Acceso a Metabase

### 1. Iniciar los contenedores Docker

Si aún no ha iniciado los contenedores, ejecute:

```bash
cd proyecto-ingenieria-datos/docker
docker-compose up -d
```

Esto iniciará tres servicios:
- Jupyter Lab (puerto 8888)
- PostgreSQL (puerto 5432)
- Metabase (puerto 3000)

### 2. Acceder a la interfaz web de Metabase

1. Abra su navegador web
2. Navegue a http://localhost:3000
3. Espere a que Metabase se inicialice (puede tardar unos minutos la primera vez)

## Configuración inicial

### 1. Crear una cuenta de administrador

La primera vez que acceda a Metabase, se le pedirá crear una cuenta de administrador:

1. Introduzca su nombre, correo electrónico y contraseña
2. Haga clic en "Next"

### 2. Conectar a la base de datos PostgreSQL

Metabase ya está preconfigurado para conectarse a PostgreSQL mediante las variables de entorno del archivo docker-compose.yml, pero deberá confirmar la conexión:

1. Seleccione "PostgreSQL" como tipo de base de datos
2. Proporcione la siguiente información:
   - Nombre: `PostgreSQL ETL`
   - Host: `db` (nombre del servicio en docker-compose)
   - Puerto: `5432`
   - Base de datos: `dataengineering`
   - Usuario: `postgres`
   - Contraseña: `postgres`
3. Haga clic en "Next"

### 3. Finalizar la configuración

1. Seleccione si desea compartir datos de uso anónimos con Metabase
2. Complete la configuración y acceda al dashboard principal

## Creación de consultas y dashboards

### Creación de una consulta básica

1. Haga clic en "New" en la barra superior
2. Seleccione "Question"
3. Elija la base de datos PostgreSQL
4. Seleccione una tabla (por ejemplo, `raw_data`, `processed_data` o `final_data`)
5. Utilice el constructor de consultas para filtrar y visualizar datos
6. Guarde la consulta con un nombre descriptivo

### Creación de un dashboard

1. Haga clic en "New" > "Dashboard"
2. Proporcione un nombre para el dashboard
3. Haga clic en "Add a question" para añadir consultas guardadas
4. Organice y redimensione las visualizaciones según sea necesario
5. Guarde el dashboard

## Exploración de datos con SQL

Para consultas más avanzadas:

1. Haga clic en "New" > "SQL Query"
2. Escriba su consulta SQL
3. Ejecute la consulta y ajuste la visualización
4. Guarde la consulta para reutilizarla

## Automatización y programación

### Programación de consultas

1. Abra una consulta guardada
2. Haga clic en el icono de reloj
3. Configure la frecuencia de actualización
4. Opcionalmente, configure notificaciones por correo electrónico

## Consideraciones de rendimiento

- Para consultas complejas, considere crear vistas en PostgreSQL
- Utilice filtros en las consultas para reducir el volumen de datos
- Para grandes conjuntos de datos, considere crear cachés de consultas en Metabase

## Mejores prácticas

1. Organice las consultas en colecciones para facilitar su gestión
2. Utilice etiquetas para categorizar dashboards y consultas
3. Documente el propósito de cada dashboard y consulta
4. Utilice variables de filtro para crear dashboards interactivos

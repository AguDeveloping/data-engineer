# Manual de Usuario - Metabase para Proyecto ETL

Este manual proporciona instrucciones sobre cómo utilizar los informes y dashboards de Metabase incluidos en este proyecto de ingeniería de datos.

## Contenido

1. [Introducciu00f3n](#introducciu00f3n)
2. [Requisitos](#requisitos)
3. [Instalaciu00f3n](#instalaciu00f3n)
4. [Uso de los informes](#uso-de-los-informes)
5. [Personalizaciu00f3n](#personalizaciu00f3n)
6. [Soluciones a problemas comunes](#soluciones-a-problemas-comunes)

## Introducciu00f3n

La integraciu00f3n de Power BI en este proyecto permite visualizar y analizar los datos procesados por el pipeline ETL. Los informes y dashboards predefinidos ofrecen visibilidad sobre el rendimiento del proceso ETL, la calidad de los datos y mu00e9tricas de negocio derivadas de los datos procesados.

## Requisitos

- Navegador web moderno (Chrome, Firefox, Edge, etc.)
- Contenedores Docker del proyecto en ejecución
- Acceso a http://localhost:3000

## Inicialización

1. Clone o descargue este repositorio
2. Asegúrese de que los contenedores Docker estén en ejecución:
   ```bash
   cd proyecto-ingenieria-datos/docker
   docker-compose up -d
   ```
3. Abra su navegador y acceda a Metabase en http://localhost:3000
4. Si es la primera vez, siga el asistente de configuración como se describe en la guía de inicio

## Uso de los dashboards

### Panel de Control General

El panel de control general proporciona una visión general del proceso ETL y los datos procesados:

- **Rendimiento ETL** - Muestra indicadores clave de rendimiento del proceso ETL
- **Calidad de Datos** - Visualiza métricas de calidad y completitud
- **Tendencias Temporales** - Análisis de tendencias a lo largo del tiempo

### Monitoreo ETL

El dashboard de monitoreo ETL ofrece detalles sobre cada fase del proceso:

- **Extracción** - Estadísticas sobre fuentes de datos y tiempos de extracción
- **Transformación** - Detalles de transformaciones aplicadas y anomalías detectadas
- **Carga** - Rendimiento de la carga de datos y análisis de errores

### Métricas Clave

El dashboard de métricas clave se centra en indicadores de negocio:

- KPIs específicos del dominio
- Segmentación por dimensiones relevantes
- Tendencias y análisis comparativo

### Navegación por los dashboards

1. Acceda a Metabase en http://localhost:3000
2. Inicie sesión con sus credenciales
3. En la página principal, encontrará los dashboards disponibles
4. Haga clic en el dashboard que desee visualizar
5. Utilice los filtros interactivos para ajustar la visualización
6. Para compartir o exportar, utilice los botones en la esquina superior derecha

## Personalización

Para personalizar los dashboards existentes:

1. Abra el dashboard que desea modificar
2. Haga clic en el icono de lápiz (Editar Dashboard) en la esquina superior derecha
3. Modifique las visualizaciones o añada nuevas según sus necesidades
4. Haga clic en 'Guardar' para aplicar los cambios

Para crear nuevos dashboards:

1. Haga clic en 'New' > 'Dashboard' en la barra superior
2. Asigne un nombre descriptivo al dashboard
3. Haga clic en 'Add a card' para añadir preguntas (consultas) existentes
4. Para crear nuevas preguntas, utilice 'New' > 'Question'

Para crear consultas SQL personalizadas:

1. Haga clic en 'New' > 'SQL Query'
2. Escriba su consulta SQL utilizando las tablas disponibles
3. Ejecute la consulta y ajuste la visualización
4. Guarde la consulta y añádala a un dashboard existente

## Soluciones a problemas comunes

### Problema de conexión a PostgreSQL

**Síntoma:** Error "Database connection error" o no se muestran las tablas

**Solución:**
- Verifique que los contenedores Docker estén en ejecución
- Compruebe que el servicio de PostgreSQL esté funcionando correctamente: `docker ps`
- Revise los logs del contenedor de la base de datos: `docker logs proyecto-ingenieria-datos_db_1`
- Verifique los parámetros de conexión en Metabase (Admin > Databases)

### Metabase no inicia correctamente

**Síntoma:** La página de Metabase no carga o muestra errores

**Solución:**
- Reinicie el contenedor de Metabase: `docker restart proyecto-ingenieria-datos_metabase_1`
- Revise los logs del contenedor: `docker logs proyecto-ingenieria-datos_metabase_1`
- Asegúrese de que el volumen `metabase_data` esté correctamente configurado

### Datos desactualizados

**Síntoma:** Los dashboards muestran datos obsoletos

**Solución:**
- Haga clic en el ícono de actualización en la esquina superior derecha del dashboard
- Verifique que el proceso ETL se haya ejecutado correctamente
- Configure la actualización automática en las propiedades de la pregunta (consulta)

### Rendimiento lento

**Síntoma:** Las consultas tardan mucho en ejecutarse

**Solución:**
- Optimice las consultas SQL subyacentes
- Cree índices en las tablas PostgreSQL para las columnas frecuentemente consultadas
- Considere habilitar el caché de consultas en Metabase (Admin > Settings > Caching)

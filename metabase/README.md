# Integración de Metabase

Esta carpeta contiene los recursos necesarios para la visualización de datos utilizando Metabase, una herramienta de análisis y visualización de código abierto que se conecta a los datos almacenados en el contenedor PostgreSQL.

## Arquitectura de la solución

```
+-------------------+    +-------------------+    +-------------------+
|   ETL Pipeline    |    |   PostgreSQL DB   |    |     Metabase      |
| (Python/Jupyter)  |--->| (Docker Container)|<---| (Dashboards)      |
+-------------------+    +-------------------+    +-------------------+
          |                       |                        |
          v                       v                        v
    Extracción de           Almacenamiento          Visualización y
    datos y proceso         centralizado            análisis de datos
    de transformación       de datos                para stakeholders
```

## Estructura

```
proyecto-ingenieria-datos/
├── [Estructura existente]
└── metabase/              # Carpeta para Metabase
    ├── templates/        # Ejemplos de consultas y dashboards predefinidos
    ├── queries/          # Consultas SQL reutilizables para visualizaciones
    ├── scripts/          # Scripts para automatización
    |   ├── cargar_datos_ejemplo.py
    |   └── respaldar_metabase.py
    ├── docs/             # Documentación
    |   ├── guia_inicio.md
    |   └── manual_usuario.md
    └── README.md         # Este archivo
```

## Acceso a Metabase

Metabase está disponible en http://localhost:3000 una vez que los contenedores Docker están en funcionamiento. Consulta la guía de inicio en `docs/guia_inicio.md` para obtener instrucciones detalladas sobre la configuración inicial.

## Dashboards predefinidos

Los ejemplos en la carpeta `queries/` proporcionan consultas SQL listas para usar que cubren:

- Dashboard de métricas ETL (dashboard_etl_metricas.sql)
- Métricas por categoría (metricas_por_categoria.sql)
- Tendencias de métricas (tendencias_metricas.sql)

## Automatización y carga de datos

Esta solución incluye dos scripts principales para trabajar con Metabase:

1. **cargar_datos_ejemplo.py**: Genera datos simulados para todas las etapas del proceso ETL y los carga en PostgreSQL. Uso:
   ```
   docker exec -it proyecto-ingenieria-datos_python-scripts_1 python /app/scripts/cargar_datos_ejemplo.py --raw 200 --etl 100
   ```

2. **respaldar_metabase.py**: Exporta dashboards, colecciones y configuraciones de Metabase. Uso:
   ```
   docker exec -it proyecto-ingenieria-datos_python-scripts_1 python /app/scripts/respaldar_metabase.py --username admin@example.com --password 1234
   ```

La arquitectura utiliza dos contenedores Docker separados para una mejor separación de responsabilidades:
- **metabase**: Ejecuta la aplicación Metabase para visualización
- **python-scripts**: Proporciona un entorno Python para ejecutar los scripts de carga y respaldo

# Proyecto de Ingeniería de Datos

Este proyecto implementa una infraestructura completa de ingeniería de datos utilizando Docker, Jupyter Notebooks, PostgreSQL, Python y Metabase. Proporciona un entorno para realizar procesos ETL (Extract, Transform, Load), análisis de datos y visualización mediante dashboards interactivos.

## Estructura del Proyecto

```
proyecto-ingenieria-datos/
├── docker/              # Configuraciones de Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── metabase/        # Configuración de Metabase
├── notebooks/           # Jupyter Notebooks para análisis
│   ├── 01_exploracion_datos.ipynb
│   └── 02_proceso_etl.ipynb
├── src/                # Código fuente
│   ├── etl/           # Módulos para ETL
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   └── utils/         # Utilidades
│       └── database.py
├── data/               # Directorio para datos
│   ├── raw/          # Datos crudos
│   ├── processed/     # Datos procesados
│   └── final/         # Resultados finales
├── sql/                # Scripts SQL
│   ├── schema.sql     # Esquema de la base de datos
│   ├── queries/       # Consultas SQL
│   └── views/         # Vistas SQL
├── metabase/            # Visualización de datos con Metabase
│   ├── templates/     # Plantillas predefinidas
│   ├── queries/       # Consultas SQL para dashboards
│   ├── scripts/       # Scripts de automatización
│   └── docs/          # Documentación de Metabase
├── tests/              # Pruebas unitarias
├── requirements.txt    # Dependencias de Python
└── README.md           # Documentación del proyecto
```

## Requisitos Previos

- Docker y Docker Compose
- Git (opcional, para control de versiones)

## Configuración e Inicio

1. **Clonar o descargar el repositorio**

2. **Iniciar los servicios con Docker Compose**

   ```bash
   cd proyecto-ingenieria-datos/docker
   docker-compose up -d
   ```

3. **Acceder a Jupyter Lab**

   Abra su navegador y vaya a [http://localhost:8888](http://localhost:8888)

## Estructura de la Base de Datos

El proyecto utiliza PostgreSQL con el siguiente esquema:

- **raw_data**: Almacena datos crudos extraídos de diversas fuentes
- **processed_data**: Contiene datos transformados y procesados
- **final_data**: Almacena resultados finales, métricas e insights

## Flujo de Trabajo ETL

1. **Extracción (Extract)**
   - Implementado en `src/etl/extract.py`
   - Soporta extracción desde archivos CSV y APIs

2. **Transformación (Transform)**
   - Implementado en `src/etl/transform.py`
   - Realiza limpieza, normalización y transformación de datos

3. **Carga (Load)**
   - Implementado en `src/etl/load.py`
   - Genera métricas, insights y carga datos finales

## Ejemplos

El proyecto incluye dos notebooks de ejemplo:

1. **01_exploracion_datos.ipynb**: Muestra cómo conectarse a la base de datos y realizar análisis exploratorio

2. **02_proceso_etl.ipynb**: Implementa un proceso ETL completo con datos de ejemplo

## Visualización con Metabase

### Arquitectura de visualización

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

El proyecto integra Metabase, una herramienta de visualización de código abierto, que permite crear dashboards interactivos a partir de los datos procesados.

### Acceso a Metabase

1. **Iniciar los servicios con Docker Compose** (si aún no lo ha hecho)
   ```bash
   cd proyecto-ingenieria-datos/docker
   docker-compose up -d
   ```

2. **Acceder a la interfaz web de Metabase**
   - Abra su navegador y vaya a [http://localhost:3000](http://localhost:3000)
   - Siga las instrucciones de configuración inicial

### Funcionalidades principales

- **Dashboards predefinidos**: Consultas SQL listas para usar en la carpeta `metabase/queries/`
- **Carga de datos de ejemplo**: Script Python para generar datos simulados
- **Respaldo de configuración**: Herramientas para exportar dashboards y consultas

Para más detalles, consulte la documentación en `metabase/docs/`.

## Personalización

Puede personalizar este proyecto según sus necesidades:

- Modificar el esquema de la base de datos en `sql/schema.sql`
- Agregar nuevas fuentes de datos en `src/etl/extract.py`
- Implementar transformaciones adicionales en `src/etl/transform.py`
- Crear nuevos notebooks para análisis específicos

## Contribución

Si desea contribuir a este proyecto, por favor:

1. Haga un fork del repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios y haga commit (`git commit -am 'Agregar nueva funcionalidad'`)
4. Envíe los cambios a su fork (`git push origin feature/nueva-funcionalidad`)
5. Cree un Pull Request

## Licencia

Este proyecto está disponible bajo la licencia MIT.

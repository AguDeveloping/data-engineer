-- Dashboard de mu00e9tricas ETL
-- Esta consulta muestra el rendimiento del proceso ETL a lo largo del tiempo

SELECT 
    process_name AS "Proceso",
    execution_date AS "Fecha de ejecuciu00f3n",
    COUNT(*) AS "Nu00famero de ejecuciones",
    AVG(EXTRACT(EPOCH FROM (end_time - start_time))) AS "Tiempo promedio (segundos)",
    SUM(records_processed) AS "Total registros procesados",
    SUM(CASE WHEN success = true THEN 1 ELSE 0 END) AS "Ejecuciones exitosas",
    SUM(CASE WHEN success = false THEN 1 ELSE 0 END) AS "Ejecuciones fallidas",
    ROUND(100.0 * SUM(CASE WHEN success = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS "Tasa de u00e9xito (%)"
FROM 
    etl_metrics
GROUP BY 
    process_name, execution_date
ORDER BY 
    execution_date DESC, process_name;

-- Tendencias de mu00e9tricas por dimensiu00f3n
-- Esta consulta permite visualizar la evoluciu00f3n de las mu00e9tricas a lo largo del tiempo

SELECT 
    fd.metric_name AS "Mu00e9trica",
    fd.dimension1 AS "Dimensiu00f3n 1",
    fd.dimension2 AS "Dimensiu00f3n 2",
    DATE_TRUNC('day', fd.report_date) AS "Du00eda",
    SUM(fd.metric_value) AS "Valor total",
    AVG(fd.metric_value) AS "Valor promedio",
    COUNT(*) AS "Cantidad de registros"
FROM 
    final_data fd
GROUP BY 
    fd.metric_name, fd.dimension1, fd.dimension2, DATE_TRUNC('day', fd.report_date)
ORDER BY 
    "Du00eda" DESC, "Valor total" DESC;

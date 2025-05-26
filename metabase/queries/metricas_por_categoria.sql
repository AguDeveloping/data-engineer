-- Mu00e9tricas por categoru00eda
-- Esta consulta permite visualizar el rendimiento de diferentes categoru00edas

SELECT 
    pd.category AS "Categoru00eda",
    COUNT(pd.id) AS "Total registros",
    SUM(pd.processed_value) AS "Valor total procesado",
    AVG(pd.processed_value) AS "Valor promedio",
    MIN(pd.processed_value) AS "Valor mu00ednimo",
    MAX(pd.processed_value) AS "Valor mu00e1ximo",
    DATE_TRUNC('day', pd.processed_date) AS "Du00eda"
FROM 
    processed_data pd
GROUP BY 
    pd.category, DATE_TRUNC('day', pd.processed_date)
ORDER BY 
    "Du00eda" DESC, "Valor total procesado" DESC;

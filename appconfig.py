QUERY_PAGAMENTO = """with valores as (
	SELECT 
    dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    SUM(dp.valorparcela) AS eletronico,
    NULL AS manual,
    1 AS tipo_ordem
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 7
GROUP BY dp.fornecedor, dp.empresa
UNION ALL
SELECT 
    dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    NULL AS eletronico,
    SUM(dp.valorparcela) AS manual,
    2 AS tipo_ordem
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 1
GROUP BY dp.fornecedor, dp.empresa
ORDER BY tipo_ordem, "G.E.F." asc, eletronico asc, manual asc
)
select fornecedor, "G.E.F.", eletronico, manual  from valores"""

QUERY_DATA_VENCIMENTO = """SELECT TO_CHAR(MAX(dp.datavcto), 'DD/MM/YYYY') AS data_maxima
FROM financeiro.detalhamento_pagamento dp"""

QUERY_GROUP_GEF = """with valores as (
	SELECT 
    dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    SUM(dp.valorparcela) AS eletronico,
    NULL AS manual,
    1 AS tipo_ordem
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 7
GROUP BY dp.fornecedor, dp.empresa
UNION ALL
SELECT 
    dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    NULL AS eletronico,
    SUM(dp.valorparcela) AS manual,
    2 AS tipo_ordem
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 1
GROUP BY dp.fornecedor, dp.empresa
ORDER BY tipo_ordem, "G.E.F." asc, eletronico asc, manual asc
)
select "G.E.F.", sum(eletronico) as eletronico, sum(manual) as manual from valores
group by 1"""

QUERY_GROUP_EMPENHO = """with valores as (
	SELECT 
    --dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    SUM(dp.valorparcela) AS eletronico,
    NULL AS manual,
    1 AS tipo_ordem,
    empenho
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 7
GROUP BY dp.empenho, dp.empresa
UNION ALL
SELECT 
    --dp.fornecedor,
    REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
    NULL AS eletronico,
    SUM(dp.valorparcela) AS manual,
    2 AS tipo_ordem,
    empenho
FROM financeiro.detalhamento_pagamento dp
WHERE dp.datavcto = CURRENT_DATE
  AND dp.cod_tipopagamento = 1
GROUP BY dp.empenho, dp.empresa
ORDER BY tipo_ordem, "G.E.F." asc, eletronico asc, manual asc
)
select empenho, "G.E.F.", sum(eletronico) as eletronico, sum(manual) as manual from valores
group by 1, 2
order by 2, 3 desc, 4 desc"""
 
APP_NAME = 'REPORT_TWILIO'

QUERY_PAGAMENTO = """select dp.fornecedor,
REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
sum(case 
	when dp.cod_tipopagamento = 1 then dp.valorparcela 
end) as manual,
sum(case 
	when dp.cod_tipopagamento = 7 then dp.valorparcela
end) as eletronico
from financeiro.detalhamento_pagamento dp
where dp.datavcto = current_date
group by dp.fornecedor, dp.empresa
order by dp.empresa"""

QUERY_DATA_VENCIMENTO = """SELECT TO_CHAR(MAX(dp.datavcto), 'DD/MM/YYYY') AS data_maxima
FROM financeiro.detalhamento_pagamento dp"""
 
APP_NAME = 'REPORT_TWILIO'

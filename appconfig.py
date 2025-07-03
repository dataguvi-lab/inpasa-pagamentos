QUERY_PAGAMENTO = """select dp.fornecedor,
REGEXP_REPLACE(dp.empresa, '^.*INPASA[ ]*', '') AS "G.E.F.",
case 
	when dp.cod_tipopagamento = 1 then dp.valorparcela 
end as manual,
case 
	when dp.cod_tipopagamento = 7 then dp.valorparcela
end as eletronico
from financeiro.detalhamento_pagamento dp
where dp.datavcto = current_date
order by dp.empresa"""
 
APP_NAME = 'REPORT_TWILIO'

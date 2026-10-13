/* Cria visão de dia da semana com maior venda */

create view vendas_semana as
SELECT to_char(to_date("Date", 'MM/DD/YYYY'), 'Day') as "Dia",count (*) FROM raw group by "Dia" order by 2 desc


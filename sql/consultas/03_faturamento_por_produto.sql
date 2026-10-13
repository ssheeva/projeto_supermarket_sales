/* Cria a visão de faturamento por linha de produto*/

create view faturamento_por_produto as 
select "Product line", sum ("Sales") from raw group by "Product line" order by 2 desc

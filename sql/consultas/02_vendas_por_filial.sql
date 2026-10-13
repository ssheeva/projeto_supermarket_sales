/* Cria a visão de vendas por filial */
create view vendas_por_filial as
select "Branch", count(*) from raw group by "Branch" order by 2 desc

/* Cria a visão de relatório de vendas por filial */
create view vendas_por_filial as select "Branch", sum ("Sales") from raw group by "Branch" order by 2 desc
/* Cria a visão de relatório de faturamento por filial */
create view faturamento_por_filial as select "Branch", sum ("Sales") from raw group by "Branch" order by 2 desc
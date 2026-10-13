/* Cria visão de avalição média por produto */

create view avaliacao_media_produto as
select "Product line", AVG ("Rating") from raw group by "Product line" order by 2 desc

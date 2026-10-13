/* Cria visão de forma de pagamento mais utilizada */

create view forma_pagamento as
select "Payment", count(*) from raw group by "Payment" order by 2 desc  
select 
    substring(cast( date_trunc('year',dt) as varchar),1,4) dt
from aemo.inventories
group by 1
order by 1
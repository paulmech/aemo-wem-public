select url,max(dt) dt
from inventories
group by url

with iterations as (
    select
        count(distinct _created_at) cacount,
        max(_created_at) max_dt,
        min(_created_at) min_dt
    from aemo.inventories
),

dancing as (
    select
        fileurl,
        count(distinct _created_at) iterations,
        max(dt) dt
    from aemo.inventories
    where not is_directory
    group by fileurl
)

select fileurl,dt
from dancing
where iterations = (select cacount from iterations)
and dt > ((select max_dt from iterations) - interval '1' day)
order by dt desc


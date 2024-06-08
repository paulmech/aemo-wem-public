with latest as (
    select max(_created_at) _created_at from aemo.inventories
),
recentfiles as (
    select
        dt,
        fileurl
        from aemo.inventories
        join latest using("_created_at")
        where not is_directory
)
SELECT 
    REVERSE(split_part(reverse(fileurl),'.',1)) ext,
    count(*) counted
     from recentfiles
     group by 1
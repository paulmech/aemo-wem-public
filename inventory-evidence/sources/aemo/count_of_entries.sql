with latest as (
    select max(_created_at) _created_at from aemo.inventories
),
recentfiles as (
    select
        dt,
        fileurl,
        REVERSE(split_part(reverse(fileurl),'.',1)) ext,
        filesize,
        is_directory,
        url
        from aemo.inventories
        join latest using("_created_at")
)
SELECT *
FROM recentfiles
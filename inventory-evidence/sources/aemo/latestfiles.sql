with latest as (
    select max(_created_at) _created_at from aemo.inventories
),
recentfiles as (
    select
        dt,
        url,
        fileurl,
        REVERSE(split_part(reverse(fileurl),'.',1)) ext,
        filesize,
        _created_at
        from aemo.inventories
        join latest using("_created_at")
        where not is_directory
)

select * from recentfiles
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
select
    date_trunc('day',dt) dt,
    count(*) number_of_files
    from recentfiles
    group by 1

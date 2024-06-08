with latest as (
    select max(_created_at) _created_at from aemo.inventories
),
recentfiles as (
    select
        dt,
        fileurl,
        REVERSE(split_part(reverse(fileurl),'.',1)) ext,
        filesize
        from aemo.inventories
        join latest using("_created_at")
        where not is_directory
)
select
    substring(cast(date_trunc('month',dt) as varchar),1,7) dt,
    ext,
    arbitrary(cast(date_trunc('month',dt) as varchar)) dt_original,
    count(*) number_of_files,
    round(sum(filesize) / 1048576) filesize_mb
    from recentfiles
    group by 1,2

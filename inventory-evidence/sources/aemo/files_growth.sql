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
SELECT
  date_trunc('hour', dt) dt
, (sum(filesize) / 1048576) file_mb
, count(*) new_files
FROM
  recentfiles
WHERE ((dt > (current_timestamp - INTERVAL  '14' DAY)) AND (NOT is_directory))
GROUP BY 1
ORDER BY 1 DESC
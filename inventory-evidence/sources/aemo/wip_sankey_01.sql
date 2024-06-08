with latest as (
    select max(_created_at) _created_at from aemo.inventories
),
recentfiles as (
    select
        dt,
        url,
        fileurl,
        REVERSE(split_part(reverse(fileurl),'.',1)) ext,
        filesize
        from aemo.inventories
        join latest using("_created_at")
        where not is_directory
),
unique_paths as (
select
  regexp_extract(url,'.+?.com.au/public/(.+?)/$',1) food,
  filesize
  from recentfiles
),
fuller as (
  select food,count(*) files, sum(filesize) total_size
  from unique_paths
  group by 1
),
  parts as (
select
  food,
  string_split(food,'/') parts,
files,
total_size
from fuller
  )
select 
  parts[1] part_one,
  case when len(parts) <= 1 then null else 
  	parts[1] || ' / ' || parts[2]
  end part_two,
  case when len(parts) <= 2 then null else
    parts[1] || ' / ' || parts[2] || ' / ' || parts[3]
  end part_three,
  case when len(parts) <= 3 then null else
    parts[1] || ' / ' || parts[2] || ' / ' || parts[3] || ' / ' || parts[4]
  end part_four,
files,
round(total_size / (1024*1024),1) total_size
from parts

WITH
  dataz AS (
   SELECT
     dt
   , fileurl
   , _created_at
   FROM
     inventories
   WHERE (NOT is_directory)
) 
, under5 AS (
   SELECT
     dt
   , _created_at
   , date_diff('minute', dt, _created_at) trailing_minutes
   , fileurl
   FROM
     dataz
   WHERE (date_diff('minute', dt, _created_at) < 5)
   ORDER BY 3 ASC
) 
SELECT
  fileurl
, count(*) count
FROM
  under5
GROUP BY 1
ORDER BY 2 DESC

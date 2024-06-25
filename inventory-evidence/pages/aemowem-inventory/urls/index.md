---
title: Information by path
sidebar_position: 3
---

## Paths

```sql livedirs
with dirs as (
    select url,
    count(*) file_count,
    max(dt) latest_dt
    from latestfiles
    group by 1)

select
    REPLACE(url,'https://data.wa.aemo.com.au/public/','') shorturl,
    file_count,
    latest_dt,
    '/aemowem-inventory/urls/' || REPLACE(REPLACE(url,'https://data.wa.aemo.com.au/public/',''),'/','|') template_url
from dirs
order by latest_dt desc
```

<DataTable  search=true  rows=20 data={livedirs} sort="url" link=template_url>
<Column id="shorturl" />
<Column id=file_count/>
<Column id=latest_dt/>
</DataTable>

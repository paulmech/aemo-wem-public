---
title: AEMO WEM Data Path - Detailed Information
---

<style type="text/css">
a.bigger > p {
    font-size: 1.2rem;
    font-weight: bold;
    color: #03d !important;
    text-shadow: rgba(160,160,90,0.2) 0.1em 0.1em 0.1em;
    margin-left: 0.6rem;
}
</style>

Click on the link below to visit the specified AEMO WEM Data directory:
<a class="bigger" target="_blank" href="https://data.wa.aemo.com.au/public/{params.url.replaceAll('|','/')}">

↗️ { params.url.replaceAll('|','/')}

</a>

## Current files in the directory

Some links may be out of date, especially for frequently updating JSON files, archived nightly.

```sql median_change
with dates as (
    SELECT
     dt,
     lag(dt) over (order by dt rows between current row and 1 following) lagging
      from latestfiles where ends_with(url,REPLACE('${params.url}','|','/'))
      order by dt
),
diffs as (
    select abs(date_diff('minutes',dt,lagging)) diff_minutes from dates order by 1
),
quantiles as (
    select approx_quantile(diff_minutes,0.5) median_mins from diffs where diff_minutes > 0
)

select
CASE
WHEN median_mins < 150 THEN
median_mins || ' mins'
WHEN median_mins < (24 * 60) THEN
ROUND(median_mins/60,1) || ' hours'
WHEN median_mins < (60 * 24 * 365) THEN
ROUND(median_mins/(24*60),1) || ' days'
ELSE
ROUND(median_mins/(24*60*365),2) || ' years'
END val
from quantiles

```

```sql latestchange
SELECT
    ABS(DATE_DIFF('days',MAX(dt),ARBITRARY(_created_at))) val
FROM latestfiles
WHERE ends_with(url,REPLACE('${params.url}','|','/'))
```

<Grid cols="2">

<BigValue data={latestchange} value=val title="Days Since Update" downIsGood=true
    comparison=val comparisonTitle=" Days Old" neutralMin=8 neutralMax=45/>

<BigValue data={median_change} value=val title="Median Change Period"/>

</Grid>

```sql urlfiles

SELECT

dt,
fileurl,
replace(fileurl,'https://data.wa.aemo.com.au/public/','') shorturl,
ext,
filesize
 from latestfiles
where ends_with(url,REPLACE('${params.url}','|','/'))
order by 1 desc

```

<DataTable rows=15 data={urlfiles} link=fileurl>
    <Column id=dt/>
    <Column id=shorturl/>
    <Column id=ext/>
    <Column id=filesize/>
</DataTable>

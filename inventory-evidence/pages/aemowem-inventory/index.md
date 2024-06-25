---
title: Inventory Overview
description: |
    A brief analysis of the files and folders publicly available on https://data.wa.aemo.com.au/public/ -
    The public datasets for the Wholesale Electricity Market of Western Australia's South West Interconnected System (SWIS)
og:
    image: /og/hunter-harritt-Ype9sdOPdYc-unsplash.jpg
    description: |
        A brief analysis of the files and folders publicly available on https://data.wa.aemo.com.au/public/ -
        The public datasets for the Wholesale Electricity Market of Western Australia's South West Interconnected System (SWIS).
        OpenGraph image courtesy of @hharritt on Unsplash
sidebar_position: 1
---

This page visualises metadata about the data files stored at [https://data.wa.aemo.com.au/public/](https://data.wa.aemo.com.au/public/)

Data is gathered every 6 hours, though no listed data files are downloaded in the process.

## Number of files modified by day

The following gives an indication of last time of update for all files found;
you can filter the starting year using the dropdown box below.

```sql years_active
select dt from years_active
```

<Dropdown
    data={years_active}
    name=years_active_since
    value=dt
    title="Show files beginning from the selected year"
    order="dt desc"
/>

<LineChart data={filesbyday} >

<ReferenceLine x=2023-10-01 label="SCED Go-Live Date" hideValue="true"/>
</LineChart>

```sql filesbyday
SELECT * from files_updated_by_day
where YEAR(dt) >= ${inputs.years_active_since.value}
order by dt
```

## Most Common File Types

Looking at file extensions simply by type alone can be misleading. In the following
bar chart, CSV file types appear dominant; in reality, a small number of services regularly
update (and seldom archive) CSV files.

<BarChart data={files_by_type}
  xAxisTitle="File extension"
  yAxisTitle="Number of files"
/>

```sql files_by_type
select * from files_by_type
where counted > 2
order by ext
```

However, if we review the file sizes in aggregate, it becomes clear the majority
of file size is attributable to `zip` files.

Typically, AEMO archives 1 day
of JSON files for selected data models, each day.

<Heatmap data={files_by_day_by_ext} x=dt y=ext 
title="File types and cumulative size (Mb) by Month"
valueFmt='#,### "Mb"'
value=filesize_mb />

```sql files_by_day_by_ext
select dt,ext,number_of_files,filesize_mb from files_updated_by_day_ext
where ext in ('csv','json','zip','yaml','xml')
and dt_original >=(current_date - interval 8 month )
order by dt
```

## How many files and directories are there?

See how many directories and files are being updated in the pre-canned periods

<Dropdown name="activity_period" 
  title="Precedent Period">
<DropdownOption valueLabel="1 week" value="0007"/>
<DropdownOption valueLabel="1 months" value="0030"/>
<DropdownOption valueLabel="3 months" value="0090"/>
<DropdownOption valueLabel="6 months" value="0187"/>
<DropdownOption valueLabel="12 months" value="0365"/>
<DropdownOption valueLabel="All time" value="9999"/>
</Dropdown>
<LineBreak/>

<BigValue data={entrycounts} value=number_of_directories title="Total Directories"/>
<BigValue data={entrycounts} value=number_of_files title="Total Files"/>
<BigValue data={entrycounts} value=filesize_total_gb title="Total Size (Gb)"/>

```sql entrycounts
select
  count(*) filter(is_directory) number_of_directories,
  count(*) filter(not is_directory) number_of_files,
  sum(filesize) / (1024*1024*1024) filesize_total_gb
  from count_of_entries
```

<BigValue data={activedirs} value=active_directories 
  title="Directories Active in Period"/>
<BigValue data={activedirs} value=active_files title="Files Active in Period" fmt="#,###"/>

```sql activedirs
select
  count(*) filter(is_directory and dt > (current_date - interval '${inputs.activity_period.value}' days)) active_directories,
  count(*) filter( (not is_directory) and dt > (current_date - interval '${inputs.activity_period.value}' days)) active_files
from count_of_entries
```

## Which files are updated repeatedly?

It is useful to know which files are updating most regularly. This is calculated by
identifying files that:

-   Are listed in every inventory run
-   Have been updated within a threshold of the inventory run commencement time

This manages to avoid including files that are recently updated on an inventory run but
are later archived into a daily zip file.

```sql regularly_updating
select
  REPLACE(fileurl,'https://data.wa.aemo.com.au/public','') "Filename",
  fileurl
from consistently_updating_files
order by dt desc
```

<DataTable data={regularly_updating}
rowNumbers=true
rowShading=true  
 search=true
rows=20
searchWholeString=true>
<Column id="fileurl" linkLabel="Filename" contentType="link" openInNewTab=true/>
</DataTable>

Click on any of the table entries above to download the listed file.

## File Growth

The following Bubble Chart shows the periods of high file size drops.

The most recent time periods (to the right of the graph) will always show large
bubbles because of the temporary presence (typically 24 hrs) of very large JSON files
per dispatch interval.

<BubbleChart data={file_growth} x=dt y=new_files size=file_mb
  xFmt='yyyy-mm-dd HH:MM' sizeFmt='#,### "Mb"'
  shape=emptyCircle/>

```sql file_growth
select dt,
file_mb,new_files
 from files_growth order by 1
```

## File Size Distribution

To get an idea of where file volume is hierarchically, a Sankey Diagram is useful to
descend between paths with a visual indicator as to their aggregate size volume.

Below you can see that the recent WEM Dispatch Engine covers a large proportion of the
overall data.

<SankeyDiagram
  data={sankey1}
  sourceCol=source_col
  targetCol=target_col
  valueCol=total_size
  chartAreaHeight=1500
  valueFmt='#,### "Mb"'
  title="Distribution of files by size"
  />

```sql sankey1
select
part_one source_col,
part_two target_col,
sum(files) files,
sum(total_size) total_size
 from wip_sankey_01
 where part_two is not null
 group by 1,2

 UNION ALL

select
part_two source_col,
part_three target_col,
sum(files) files,
sum(total_size) total_size
 from wip_sankey_01
 where part_three is not null
 group by 1,2

UNION ALL

select
part_three source_col,
part_four target_col,
sum(files) files,
sum(total_size) total_size
 from wip_sankey_01
 where part_four is not null
 group by 1,2

order by source_col,target_col
```

## File Count Distribution

Let's repeat the same process but for number of files, instead of storage volume

<SankeyDiagram
data={sankey1}
sourceCol=source_col
targetCol=target_col
valueCol=files
chartAreaHeight=1500
title="Distribution of files by count"
/>

> This space intentionally left blank

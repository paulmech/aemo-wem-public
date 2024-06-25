---
title: Complete Data File Inventory
og:
    title: Searchable Inventory of AEMO WEM Data Files
    description: |
        An easy to use search and filter for all AEMO WEM Data Files. Filter by
        file size, extension, age, directory (url) and keyword to find available files.
        Single click download, direct from AEMO WEM data site. OpenGraph image courtesy of 
        @brett_jordan on Unsplash
    image: /og/brett-jordan-7vxlppVfh8M-unsplash.jpg
sidebar_position: 2
---

```sql distincturl
select
url,
 replace(url,'https://data.wa.aemo.com.au/public','') curtailed
from latestfiles
group by 1
order by 1
```

On this page you can review most of the available files, and filter using key properties.

```sql exts
select
        REVERSE(split_part(reverse(fileurl),'.',1)) ext
from latestfiles

group by 1 having (count(*) > 2)
order by 1
```

## Filters

<Grid cols="2">
<Dropdown
    data={distincturl}
    name=urlbase
    value=url
    label=curtailed
    title="List of file locations">
<DropdownOption default=false value='' valueLabel='All Directories'/>
</Dropdown>

<ButtonGroup name="agegroup" title="Maximum File Age">
    <ButtonGroupItem value="0" valueLabel="All ages"/>
    <ButtonGroupItem value="003" valueLabel="3 days"/>
    <ButtonGroupItem value="010" valueLabel="10 days"/>
    <ButtonGroupItem default=true value="030" valueLabel="1 month"/>
    <ButtonGroupItem value="090" valueLabel="3 months"/>
</ButtonGroup>

</Grid>

<Grid cols="2">
<ButtonGroup name="sizegroup" title="File size Groups">
<ButtonGroupItem value="" valueLabel="All sizes" default=true/>
<ButtonGroupItem value=",50" valueLabel="0 - 50Mb"/>
<ButtonGroupItem value="50,250" valueLabel="50Mb - 250Mb"/>
<ButtonGroupItem value="250," valueLabel="250Mb +"/>
</ButtonGroup>

<ButtonGroup name="extgroup" title="File extension" data={exts} value="ext">
<ButtonGroupItem default=true value="" valueLabel="All extensions"/>
</ButtonGroup>
</Grid>

```sql fullinventory
WITH basics AS (
    select
        fileurl,
        dt,
        REVERSE(split_part(reverse(fileurl),'.',1)) ext,
        CASE
            WHEN filesize < (50 * 1024 * 1024) THEN ',50'
            ELSE
                CASE
                    WHEN filesize >= (50 * 1024 * 1024) and filesize < (250 * 1024 * 1024) THEN '50,250'
                    ELSE '250,'
                END
        END filenotation,
        filesize,
        _created_at
    from latestfiles
    where ('' = '${inputs.urlbase.value}' OR url='${inputs.urlbase.value}')
    AND ('0' = '${inputs.agegroup}' OR dt > _created_at - INTERVAL '${inputs.agegroup}' DAYS)
)
SELECT
 fileurl,
 REPLACE(fileurl,'https://data.wa.aemo.com.au/public','') shortUrl,
 filesize/1024/1024 "filesize",
 cast(age(dt) as varchar) "age"
 FROM basics
  WHERE
    ('${inputs.sizegroup}' = '' OR filenotation = '${inputs.sizegroup}')
    AND
    ('${inputs.extgroup}' = '' OR ext = '${inputs.extgroup}')


```

<DataTable showNoResults=true search=true searchWholeString=true data={fullinventory} rows=15>
    <Column id=fileurl contentType=link linkLabel=shortUrl openInNewTab=true wrap=true/>
    <Column id="filesize" wrap=true fmt='0.0 "Mb"'/>
    <Column id="age" wrap=true/>
</DataTable>

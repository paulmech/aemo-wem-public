# AEMO WEM Data Website - Catalogue Scraper

The role of this tool is to collect information about files that are hosted on the AEMO's WEM data website.

This information can be used to understand the rate of change of data and where to start investigating key data models.

## Technology

-   Program code is written in Python (3)
-   [Pants Build System](https://www.pantsbuild.org/) is used for dependency management, testing and packaging

## As a Lambda Function

Pants build integration is used to package code and dependencies into a lambda ZIP package that can be uploaded with Terraform

When the lambda function runs, it also gzip compresses and persists the data to a S3 bucket, using the execution date (yyyy-mm-dd) and `aws_request_id` as prefix folders

## Run Locally

```sh
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ python src/python/function.py

URL expected

    AEMO WEM Data Utility
    (Also known Aemo Wemdu, pronounced Mace Windu)

    Usage:

    aemo-wem <url> <command> <options>

    URL:
        currently should be https://data.wa.aemo.com.au/public/
        it is required to generate fully qualified URLs

    COMMANDS:
        list-files


    OPTIONS:
        --max-days-old <int>  - only consider files newer than <int> days old
        --min-days-old <int>  - only consider files older than <int> days old
        --no-recurse          - do not recurse into child directories
        --max-depth    <int>  - do not descend further than <int> directories
        --start-url    <str>  - custom URL to begin from
        --no-empty-dirs       - don't return directories that didn't have any files at their relative depth
```

## Results

```sh
(.venv) $ python src/python/function.py https://data.wa.aemo.com.au/public/ list-files --no-recurse
```

```json
{"dt": "2024-06-07T22:23:46", "url": "https://data.wa.aemo.com.au/public/", "depth": 1, "fileCount": 1, "is_directory": true, "_created_at": "2024-06-07T22:23:46"}
{"dt": "2021-04-07T15:59:00", "url": "https://data.wa.aemo.com.au/public/20140301/", "fileCount": 0, "is_directory": true, "_created_at": "2024-06-07T22:23:46"}
{"dt": "2014-04-14T14:08:00", "url": "https://data.wa.aemo.com.au/public/", "depth": 1, "fileName": "web.config", "fileUrl": "https://data.wa.aemo.com.au/public/web.config", "fileSize": 349, "is_directory": false, "_created_at": "2024-06-07T22:23:46"}
...
{"dt": "2021-04-07T16:01:00", "url": "https://data.wa.aemo.com.au/public/xdomain/", "fileCount": 0, "is_directory": true, "_created_at": "2024-06-07T22:23:46"}
```

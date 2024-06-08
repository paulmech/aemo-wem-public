# AEMO WEM Data File Inventory

This repository contains the code for a solution that:

-   Scans the [AEMO Wholesale Electricity Market](https://data.wa.aemo.com.au/public/) data portal for files and their properties
-   Creates a database and visualisation to tell stories about those files
-   Uses schedules to orchestrates pipelines and build runs that regenerate data visualisations every 6 hours.

The aim is actually about exploring technologies rather than any significant insight. The repository is organised as follows:

-   [/inventory-evidence/](./inventory-evidence/) contains the visualisation solution built using [Evidence.dev](https://evidence.dev)
-   [/inventory-scraper/](./inventory-scraper/) contains the Python web scraper that scans the directory listings, emits JSON catalogues and saves them to S3
-   [/terraform/](./terraform/) contains the infrastructure as code (IAC) that delivers the infrastructure to orchestrate and run pipelines that scrape data and create DuckDB databases
-   [/.github/](./.github/) contains the CICD workflows that run in Github Actions. These deploy IAC to AWS, and deploy the Evidence website to S3 where it is served by CloudFront

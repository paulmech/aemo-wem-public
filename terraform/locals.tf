data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
locals {
  permission_boundary_arn          = "arn:aws:iam::${local.account_id}:policy/aemowem-permission-boundary"
  region                           = data.aws_region.current.name
  account_id                       = data.aws_caller_identity.current.account_id
  aemowem_inventory_prefix_duckdb  = "${local.aemowem_inventory_prefix_base}/duckdb"
  lambda_local_file                = "../inventory-scraper/dist/aemo-inventory.zip"
  aemowem_inventory_prefix_base    = "website_inventory"
  aemowem_inventory_prefix_jsonl   = "${local.aemowem_inventory_prefix_base}/jsonl"
  aemowem_inventory_prefix_scripts = "${local.aemowem_inventory_prefix_base}/scripts"
  migration_script_location_key    = "${local.aemowem_inventory_prefix_scripts}/migration.sql"
  duckdb_database_name             = "aemo.duckdb"
}